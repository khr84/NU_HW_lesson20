from django.contrib import admin
from .models import Region, Skill, Search_vacancy, Search_salary, Employer, Schedule, Currency, Vacancy

# Register your models here.
admin.site.register(Region)
admin.site.register(Skill)
admin.site.register(Search_vacancy)
admin.site.register(Search_salary)
admin.site.register(Employer)
admin.site.register(Schedule)
admin.site.register(Currency)
admin.site.register(Vacancy)