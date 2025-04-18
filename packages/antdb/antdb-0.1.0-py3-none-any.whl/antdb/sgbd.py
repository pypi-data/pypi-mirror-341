from typing import Any, Dict, List, Type

from pydantic import BaseModel, Field


class TableModel(BaseModel):
    id: int = Field(default=None)


class Table:
    def __init__(self, name: str, model: Type[BaseModel]):
        self.name = name
        self.model = model
        self.records: List[BaseModel] = []
        self._id_counter = 1

    def _get_next_id(self) -> int:
        current_id = self._id_counter
        self._id_counter += 1
        return current_id

    def insert(self, record: BaseModel) -> None:
        if not isinstance(record, self.model):
            raise ValueError(
                f"Record must be an instance of {self.model.__name__}"
            )

        if hasattr(record, "id") and record.id is None:
            record.id = self._get_next_id()
        self.records.append(record)

    def select_all(self) -> List[BaseModel]:
        return self.records

    def select_where(
        self, field: str, operator: str, value: Any
    ) -> List[BaseModel]:
        ops = {
            "=": lambda x, y: x == y,
            ">": lambda x, y: x > y,
            "<": lambda x, y: x < y,
            ">=": lambda x, y: x >= y,
            "<=": lambda x, y: x <= y,
            "!=": lambda x, y: x != y,
        }
        if operator not in ops:
            raise ValueError(
                f"Invalid operator. Use one of: {', '.join(ops.keys())}"
            )

        return [
            r for r in self.records if ops[operator](getattr(r, field), value)
        ]

    def update_where(
        self, field: str, operator: str, value: Any, new_values: dict
    ) -> int:
        updated_count = 0
        records = self.select_where(field, operator, value)

        for record in records:
            for key, val in new_values.items():
                setattr(record, key, val)
            updated_count += 1
        return updated_count

    def delete_where(self, field: str, operator: str, value: Any) -> int:
        initial_length = len(self.records)
        to_delete = self.select_where(field, operator, value)
        self.records = [r for r in self.records if r not in to_delete]
        return initial_length - len(self.records)


class DataBase:
    def __init__(self, name: str):
        self.name = name
        self.tables: Dict[str, Table] = {}

    def create_table(self, name: str, model: Type[BaseModel]) -> Table:
        if name in self.tables:
            raise ValueError(f"Table '{name}' already exists")
        table = Table(name, model)
        self.tables[name] = table
        return table

    def drop_table(self, name: str) -> None:
        if name not in self.tables:
            raise ValueError(f"Table '{name}' does not exist")
        del self.tables[name]

    def get_table(self, name: str) -> Table:
        if name not in self.tables:
            raise ValueError(f"Table '{name}' does not exist")
        return self.tables[name]

    def list_tables(self) -> List[str]:
        return list(self.tables.keys())
