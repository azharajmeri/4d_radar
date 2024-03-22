from django.db import models


class SpeedRecord(models.Model):
    frame_number = models.CharField(max_length=255)
    speed = models.FloatField()
    time = models.DateTimeField()
    lane_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Speed: {self.speed}, Time: {self.time}, Lane Number: {self.lane_number}, Created At: {self.created_at}"


class Display(models.Model):
    ip = models.CharField(max_length=20, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    lane_number = models.IntegerField()
    camera_ip = models.CharField(max_length=20, null=True, blank=True)
    camera_user = models.CharField(max_length=20, null=True, blank=True)
    camera_pass = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.ip}:{self.port} - Lane Number: {self.lane_number}"


class SpeedLimit(models.Model):
    limit = models.IntegerField()


class Radar(models.Model):
    ip = models.CharField(max_length=20, null=True, blank=True)
    host_ip = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.ip}:{self.host_ip}"


class TriggerPoint(models.Model):
    display = models.IntegerField()
    camera = models.IntegerField()

    def __str__(self):
        return f"{self.display}:{self.camera}"


class ConfiguredConnection(models.Model):
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.status}"
