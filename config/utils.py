from config.models import Setting
from akun.models import Users, Premium
from kelas.models import Langganan
from datetime import datetime, date

def is_date_in_range(request):
    if not request.user.is_authenticated:
        return False
    premium = Premium.objects.filter(user=request.user)
    if not premium.exists():
        return False
    return premium.premium_start <= datetime.now() <= premium.premium_end
    
def beforeRequest(request):
    if request.user.is_authenticated:
        user = Users.objects.filter(user=request.user.id)
        if not user.exists():
            Users.objects.create(user=request.user)

def config(request):

    beforeRequest(request)
    url = request.resolver_match

    context = {}
    context['config']   = Setting.objects.get()
    context['me']       = Users.objects.get(user=request.user) if request.user.is_authenticated else ''
    context['premium']  = is_date_in_range(request) if request.user.is_authenticated else False
    context['url'] = url.url_name if len(url.app_names) == 0 else url.app_names[0]
    context['langganan'] = Langganan.objects.all()
    return context