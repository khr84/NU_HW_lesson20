from django.db import models

# Create your models here.
class Region(models.Model):
    region_name = models.CharField(max_length=250, unique=True)
    region_id = models.IntegerField(default=-1000)


class Skill(models.Model):
    skill_name = models.CharField(max_length=250, unique=True)


class Search_vacancy(models.Model):
    search_str = models.CharField(max_length=100)
    count_vacancy = models.IntegerField(default=0)
    search_date = models.CharField(max_length=25)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    strict_search = models.IntegerField(default=-1)
    skill_id = models.ManyToManyField(Skill)

    class Meta:
        unique_together = ('search_str','region_id','strict_search',)


class Search_salary(models.Model):
    search_id = models.ForeignKey(Search_vacancy, on_delete=models.CASCADE)
    low_value = models.FloatField(null=True)
    high_value= models.FloatField(null=True)
    count_salary = models.IntegerField(default=0)


class Employer(models.Model):
    emp_name = models.CharField(max_length=250, unique=True)
    emp_url = models.CharField(max_length=250)
    emp_id = models.CharField(max_length=25)


class Schedule(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)


class Currency(models.Model):
    code = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=50)


class Vacancy(models.Model):
    search_id = models.ForeignKey(Search_vacancy, on_delete=models.CASCADE)
    vacancy_name = models.CharField(max_length=250)
    vacancy_url = models.CharField(max_length=250)
    salary_from = models.CharField(max_length=50, null=True)
    salary_to = models.CharField(max_length=50, null=True)
    salary_cur = models.ForeignKey(Currency, on_delete=models.CASCADE)
    salary_grace = models.CharField(max_length=5, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('search_id','vacancy_url',)