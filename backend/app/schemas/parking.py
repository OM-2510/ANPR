from pydantic import BaseModel
import datetime 

class EntryResponse(BaseModel):
    id: int
    plate_number : str
    entry_time : datetime.datetime

    class Config:
        from_attributes= True

class ExitResponse(BaseModel):
    id:int
    plate_number: str
    exit_time: datetime.datetime
    amount: float
    status: str

    class Config:
        from_attributes= True