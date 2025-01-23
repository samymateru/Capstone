from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Role(BaseModel):
    name: str
    description: str
    category: str
    write: bool
    read: bool
    edit: bool
    assign: bool
    approve: bool
    delete: bool

class NewRole(BaseModel):
    name: str
    description: str
    category: str
    write: bool
    read: bool
    edit: bool
    assign: bool
    approve: bool
    delete: bool
    created_at: datetime = datetime.now()



class DeleteRoles(BaseModel):
    role_id: int

class UpdateRole(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


