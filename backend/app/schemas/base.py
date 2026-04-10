from pydantic import BaseModel

class PaginationInfo(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int

class GenericResponse(BaseModel):
    success: bool
    message: str
