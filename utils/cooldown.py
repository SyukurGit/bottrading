import time
from utils.db import get_last_analysis, update_last_analysis
from config import COOLDOWN_SECONDS

def is_on_cooldown(user_id: int) -> bool:
    last = get_last_analysis(user_id)
    if last is None:
        return False
    return (time.time() - last) < COOLDOWN_SECONDS

def update_cooldown(user_id: int):
    update_last_analysis(user_id, int(time.time()))
