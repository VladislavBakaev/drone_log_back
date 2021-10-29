from django.db import models

# Create your models here.

class YDLogFile(models.Model):
    upload = models.FileField(upload_to="logs/")
    flight_data = models.DateField()
    description = models.TextField()
    mission = models.ForeignKey('YDMission', on_delete=models.CASCADE)
    at_create = models.DateTimeField()

    def delete(self, using=None, keep_parents=False):
        self.upload.storage.delete(self.upload.name)
        super().delete()

    class Meta:
        db_table = 'yd_drone_logs_file'


class YDMission(models.Model):
    mission_name = models.CharField(max_length=120)
    user_info = models.CharField(max_length=120)
    description = models.TextField()
    flight_mission_file = models.FileField(upload_to="flight_missions/")
    at_create = models.DateTimeField()

    def delete(self, using=None, keep_parents=False):
        self.flight_mission_file.storage.delete(self.flight_mission_file.name)
        super().delete()

    class Meta:
        db_table = 'yd_drone_missions'
        unique_together = ('user_info' , 'mission_name')