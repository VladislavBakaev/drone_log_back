from django.db import models

class UserInfo(models.Model):
    system_user_name = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    operation_system = models.CharField(max_length=150)
    ardupilot_version = models.CharField(max_length=150)

    class Meta:
        db_table = "user_info"


class Point(models.Model):
    mission = models.ForeignKey("mission", on_delete=models.CASCADE, null=False)

    param1 = models.DecimalField(max_digits=15, decimal_places=9)
    param2 = models.DecimalField(max_digits=15, decimal_places=9)
    param3 = models.DecimalField(max_digits=15, decimal_places=9)
    param4 = models.DecimalField(max_digits=15, decimal_places=9)
    
    x = models.DecimalField(max_digits=15, decimal_places=9)
    y = models.DecimalField(max_digits=15, decimal_places=9)
    z = models.DecimalField(max_digits=15, decimal_places=9)

    seq = models.IntegerField()
    command = models.IntegerField()
    target_system = models.IntegerField()
    target_component = models.IntegerField()
    
    frame = models.IntegerField()
    current = models.IntegerField()
    autocontinue = models.IntegerField()
    mission_type = models.IntegerField()

    class Meta:
        db_table = "point_info"


class Mission(models.Model):
    mission_name = models.CharField(max_length=150)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=False)
    at_create = models.DateTimeField()

    class Meta:
        db_table = "mission_info"
