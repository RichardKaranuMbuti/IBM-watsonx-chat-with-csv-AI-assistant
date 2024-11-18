from pydantic import BaseModel
from typing import List, Optional

class FileBase(BaseModel):
    description: str

class FileCreate(FileBase):
    pass

class File(FileBase):
    id: int
    filename: str

    class Config:
        orm_mode = True

# Request model for query processing
class QueryRequest(BaseModel):
    query: str
    ids: Optional[List[int]] = None
