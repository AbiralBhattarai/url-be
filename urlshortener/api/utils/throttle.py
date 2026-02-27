from django_redis import get_redis_connection
from .services import get_client_ip

RATE_LIMIT = 5  #limit per window
WINDOW = 60  #seconds


def check_rate_limit(request):
    ip = get_client_ip(request)
    key = f"rate_limit:{ip}"
    
    redis = get_redis_connection("default")
    
    #atomic increment
    current_count = redis.incr(key)
    
    #check limit
    if current_count > RATE_LIMIT:
        #set waiting window
        if current_count == RATE_LIMIT + 1:
            redis.expire(key, WINDOW)
        wait_time = redis.ttl(key)
        return False, wait_time
    
    return True, None