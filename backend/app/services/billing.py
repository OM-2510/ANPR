import math
from datetime import datetime

billing_rate = 20

def calculate_fee_and_durtation(entry_time: datetime, exit_time: datetime):
    duration = exit_time - entry_time
    hours = math.ceil(duration.total_seconds() / 3600)
    amount = hours * billing_rate

    return (amount, duration)