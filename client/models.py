from django.db import models
from account.models import Client, Freelancer
import datetime


# Create your models here.
class AvailableProjects(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='available_orders')
    amount = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    task=models.CharField(max_length=200, default='videographer')
    description=models.TextField(null=True,blank=True)
    deadline=models.DateField()
    start_date=models.DateField(default=datetime.date.today)
    role=models.CharField(max_length=50, default='videographer')
    applicants=models.JSONField(default=[],null=True,blank=True)
    location=models.CharField(max_length=50, default='remote')

class Application(models.Model):
    project = models.ForeignKey(AvailableProjects, on_delete=models.CASCADE)
    crew = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(default=datetime.datetime.now)
    is_accepted = models.BooleanField(default=False)