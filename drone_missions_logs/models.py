from django.db import models

class LogFile(models.Model):
    upload = models.FileField(upload_to="logs/")
    flight_data = models.DateTimeField()
    description = models.TextField()
    mission = models.ForeignKey('Mission', on_delete=models.CASCADE, null=True)
    at_create = models.DateTimeField()

    def delete(self, using=None, keep_parents=False):
        self.upload.storage.delete(self.upload.name)
        super().delete()

    class Meta:
        db_table = 'yd_drone_logs_file'


class Mission(models.Model):
    mission_name = models.CharField(max_length=120)
    user_info = models.CharField(max_length=120)
    description = models.TextField()
    flight_mission_file = models.FileField(upload_to="flight_missions/")
    at_create = models.DateTimeField()

    def delete(self, using=None, keep_parents=False):
        self.flight_mission_file.storage.delete(self.flight_mission_file.name)
        super().delete()

    class Meta:
        db_table = 'drone_missions'
        unique_together = ('user_info' , 'mission_name')


class YDMissionPoint(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    targetLat = models.DecimalField(max_digits=15, decimal_places=9)
    targetLon = models.DecimalField(max_digits=15, decimal_places=9)
    targetAlt = models.DecimalField(max_digits=9, decimal_places=4)
    targetRadius = models.DecimalField(max_digits=9, decimal_places=4)
    loiterTime = models.IntegerField()
    maxHorizSpeed = models.DecimalField(max_digits=9, decimal_places=4)
    maxVertSpeed = models.DecimalField(max_digits=9, decimal_places=4)
    poiLat = models.DecimalField(max_digits=15, decimal_places=9)
    poiLon = models.DecimalField(max_digits=15, decimal_places=9)
    poiHeading = models.DecimalField(max_digits=9, decimal_places=4)
    poiAltitude = models.DecimalField(max_digits=9, decimal_places=4)
    flags = models.IntegerField()
    photo = models.IntegerField()
    panoSectorsCount = models.IntegerField()
    panoDeltaAngle = models.DecimalField(max_digits=9, decimal_places=4)
    poiPitch = models.DecimalField(max_digits=9, decimal_places=4)
    poiRoll = models.DecimalField(max_digits=9, decimal_places=4)
    type = models.IntegerField()

    class Meta:
        db_table = 'yd_drone_mission_point'