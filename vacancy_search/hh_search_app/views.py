from django.shortcuts import render
from datetime import datetime, timedelta
from .forms import HistoryForm
from .models import Search_vacancy

# Create your views here.
def main_view(request):
    pass
    return render(request, 'hh_search_app/index.html')

def search_view(request):
    pass
    return render(request, 'hh_search_app/search.html')

def result_view(request):
    pass
    return render(request, 'hh_search_app/result.html')

def history_view(request):
    if request.method == 'POST':
        form = HistoryForm(request.POST)
        if form.is_valid():
            period = form.cleaned_data['period']
            hist_period = min(30, int(period))
            now = datetime.now()
            date_end = now + timedelta(days=1)
            date_end = date_end.strftime("%Y.%m.%d")
            date_beg = now - timedelta(days=hist_period)
            date_beg = date_beg.strftime("%Y.%m.%d")
            res_list = Search_vacancy.objects.filter(search_date__gte=date_beg, search_date__lt=date_end)
            return render(request, 'hh_search_app/history.html', context={'vacancy_list': res_list, 'hide':'hidden'})
        else:
            return render(request, 'hh_search_app/history.html', context={'form': form, 'hide_res':'hidden'})
    else:
        form = HistoryForm()
        return render(request, 'hh_search_app/history.html', context={'form':form, 'hide_res':'hidden'})