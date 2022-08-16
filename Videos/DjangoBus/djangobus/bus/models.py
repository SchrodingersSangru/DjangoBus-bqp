from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Bus(models.Model):
    bus_id = models.IntegerField()
    bus_name = models.CharField(max_length=30)
    bus_start = models.CharField(max_length=30)
    bus_dest = models.CharField(max_length=30)
    bus_route = models.CharField(max_length=50)
    start_time = models.TimeField()
    reaching_time = models.TimeField()
    total_seats = models.IntegerField()
    bus_person = models.ForeignKey("user.user", default = "", on_delete= models.DO_NOTHING)
    
    class Meta:
        db_table = "Bus_details"