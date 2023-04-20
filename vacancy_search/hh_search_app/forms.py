from django import forms


class HistoryForm(forms.Form):
    period = forms.IntegerField(label='Период поиска')