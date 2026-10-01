from pydantic import BaseModel
import datetime 

# class EntryRequest(BaseModel):
#     plates_image : str

class EntryResponse(BaseModel):
    id: int
    plate_number : str
    entry_time : datetime.datetime

    class Config:
        from_attributes: True