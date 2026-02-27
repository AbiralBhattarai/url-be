import hashlib
from ..models import *
from django.utils import timezone
from datetime import timedelta
def generate_short_url(url:str,length:int=6)->str:
    counter = 0
    while True:
        salt = url+str(counter)
        short = hashlib.sha256(salt.encode()).hexdigest()[:length]

        if not ShortURL.objects.filter(shortened_url = short).exists():
            return short
        counter+=1


def get_client_ip(request):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            return ip.split(",")[0]
        return request.META.get("REMOTE_ADDR")



def get_clicks_for_url(shortened_url, days=7):    
    short_url_obj = ShortURL.objects.get(shortened_url=shortened_url)
    
    start_date = timezone.now() - timedelta(days=days)
    clicks = Click.objects.filter(
        url=short_url_obj,
        clicked_at__gte=start_date
    ).order_by('-clicked_at')
    
    return {
        'url_obj': short_url_obj,
        'clicks': clicks,
        'total_count': clicks.count()
    }