from pydantic import BaseModel


class DataColumn(BaseModel):
    title: str
    description: str | None = None

class DataSchema(BaseModel):
    id: str
    columns: list[DataColumn]
    source: str

class DataRow(BaseModel):
    hash: str
    bin_iin: str | None = None
    fio: str | None = None
    title: str | None = None
    data: list[str | int | float]
    data_schema: DataSchema
