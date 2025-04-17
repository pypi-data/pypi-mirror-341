"""
CreateModel operation for Tortoise ORM migrations.
"""

from typing import Dict, TYPE_CHECKING

from tortoise.fields import Field, IntField
from tortoise.fields.relational import RelationalField

from tortoise_pathway.operations.operation import Operation
from tortoise_pathway.operations.utils import default_to_sql, field_to_migration

if TYPE_CHECKING:
    from tortoise_pathway.state import State


class CreateModel(Operation):
    """Create a new model."""

    def __init__(
        self,
        model: str,
        fields: Dict[str, Field],
    ):
        super().__init__(model)
        self.fields = fields

    def forward_sql(self, state: "State", dialect: str = "sqlite") -> str:
        """Generate SQL for creating the table."""
        return self._generate_sql_from_fields(state, dialect)

    def backward_sql(self, state: "State", dialect: str = "sqlite") -> str:
        """Generate SQL for dropping the table."""
        return f"DROP TABLE {self.get_table_name(state)}"

    def _generate_sql_from_fields(self, state: "State", dialect: str = "sqlite") -> str:
        """
        Generate SQL to create a table from the fields dictionary.

        Args:
            state: State object that contains schema information.
            dialect: SQL dialect to use (default: "sqlite").

        Returns:
            SQL string for table creation.
        """
        columns = []
        constraints = []

        # Process each field
        for field_name, field in self.fields.items():
            field_type = field.__class__.__name__

            # Skip if this is a reverse relation
            if field_type == "BackwardFKRelation":
                continue

            # Handle ForeignKey fields
            if isinstance(field, RelationalField):
                # For ForeignKeyField, use the actual db column name (typically field_name + "_id")
                db_field_name = getattr(field, "model_field_name", field_name)
                source_field = getattr(field, "source_field", None)
                if source_field:
                    db_column = source_field
                else:
                    # Default to tortoise convention: field_name + "_id"
                    db_column = f"{db_field_name}_id"

                # Add foreign key constraint if related table is known
                _ = getattr(field, "model_name", None)
                related_table = getattr(field, "related_table", None)

                if related_table:
                    constraints.append(f"FOREIGN KEY ({db_column}) REFERENCES {related_table} (id)")

                # TODO: foreign keys might have a different type
                sql_type = IntField().get_for_dialect(dialect, "SQL_TYPE")
            else:
                # Use source_field if provided, otherwise use the field name
                source_field = getattr(field, "source_field", None)
                db_column = source_field if source_field is not None else field_name

                sql_type = field.get_for_dialect(dialect, "SQL_TYPE")

            nullable = getattr(field, "null", False)
            unique = getattr(field, "unique", False)
            pk = getattr(field, "pk", False)
            default = getattr(field, "default", None)

            # Handle special cases for primary keys
            if pk:
                if dialect == "sqlite" and field_type == "IntField":
                    # For SQLite, INTEGER PRIMARY KEY AUTOINCREMENT must use exactly "INTEGER" type
                    sql_type = "INTEGER"
                elif pk and field_type == "IntField" and dialect == "postgres":
                    sql_type = "SERIAL"

            # Build column definition
            column_def = f"{db_column} {sql_type}"

            if pk:
                if dialect == "sqlite":
                    column_def += " PRIMARY KEY"
                    if field_type == "IntField":
                        column_def += " AUTOINCREMENT"
                else:
                    column_def += " PRIMARY KEY"
                    if field_type == "IntField" and dialect == "postgres":
                        # For PostgreSQL, we'd use SERIAL instead
                        column_def = f"{db_column} {sql_type} PRIMARY KEY"

            if not nullable and not pk:
                column_def += " NOT NULL"

            if unique and not pk:
                column_def += " UNIQUE"

            if default is not None and not callable(default):
                default_val = default_to_sql(default, dialect)

                column_def += f" DEFAULT {default_val}"

            columns.append(column_def)

        # Build the CREATE TABLE statement
        sql = f'CREATE TABLE "{self.get_table_name(state)}" (\n'
        sql += ",\n".join(["    " + col for col in columns])

        if constraints:
            sql += ",\n" + ",\n".join(["    " + constraint for constraint in constraints])

        sql += "\n);"

        return sql

    def to_migration(self) -> str:
        """Generate Python code to create a model in a migration."""
        lines = []
        lines.append("CreateModel(")
        lines.append(f'    model="{self.model}",')

        # Include fields
        lines.append("    fields={")
        for field_name, field_obj in self.fields.items():
            # Skip reverse relations
            if field_obj.__class__.__name__ == "BackwardFKRelation":
                continue

            # Use field_to_migration to generate the field representation
            lines.append(f'        "{field_name}": {field_to_migration(field_obj)},')
        lines.append("    },")

        lines.append(")")
        return "\n".join(lines)
