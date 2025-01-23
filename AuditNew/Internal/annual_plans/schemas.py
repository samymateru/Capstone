from pydantic import BaseModel
from datetime import datetime
from enum import  Enum
from typing import Optional, List

class AnnualPlansStatus(str, Enum):
    NOT_STARTED = "Not Started"
    PROGRESS = "In progress"
    COMPLETED = "Completed"

class NewAnnualPlan(BaseModel):
    name: str
    year: Optional[str] = datetime.now().year
    status:  AnnualPlansStatus = AnnualPlansStatus.NOT_STARTED
    description: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    created_at: Optional[datetime] = datetime.now()
    # audit_type: str = None


class DeleteAnnualPlan(BaseModel):
    id: int

class UpdateAnnualPlan(BaseModel):
    id: int
    name: Optional[str] = None
    year: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    audit_type: Optional[str] = None
    date: Optional[datetime] = None
    date: Optional[datetime] = None

