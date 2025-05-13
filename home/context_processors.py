from utils.redis_utils import redis_manager



def daily_visits(request):
    visits = redis_manager.get_daily_visits()
    return {'today_visits': visits}