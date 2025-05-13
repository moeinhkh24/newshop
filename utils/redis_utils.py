import random
import datetime
import redis
from django.conf import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True 
)


class RedisManager:
    
    def generate_otp(self, phone_number: str, expire: int = 120):
        otp_code = str(random.randint(10000, 99999))
        redis_client.setex(f"otp:{phone_number}", expire , otp_code)
        return otp_code
    
    def validate_otp(self, phone_number: str, input_code: str):
        key = f"otp:{phone_number}"
        real_code = redis_client.get(key)
        if real_code and real_code == input_code:
            redis_client.delete(key)
            return True
        return False
    
    
    def has_valid_otp(self, phone_number: str):
        return redis_client.exists(f'otp:{phone_number}') == 1
    
    
    def track_daily_visit(self, session_id):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        key = f'daily_visits:{today}'
        redis_client.pfadd(key, str(session_id))
        redis_client.expire(key, 60 * 60 * 24)
        
    def get_daily_visits(self, date_str=None):
        if not date_str:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        key = f'daily_visits:{date_str}'
        return redis_client.pfcount(key)


redis_manager = RedisManager()