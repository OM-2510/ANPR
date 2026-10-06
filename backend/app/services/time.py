import datetime 

IST_OFFSET = datetime.timedelta(hours=5, minutes=30)

def start_of_today(offset: datetime.timedelta = IST_OFFSET) -> datetime.datetime:
    now_utc = datetime.datetime.utcnow()
    now_local = now_utc + offset
    start_of_today = now_local.replace(hour=0, minute=0, microsecond=0)
    return start_of_today