from django.db import models


class SpeedRecord(models.Model):
    speed = models.FloatField()
    time = models.DateTimeField()
    lane_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Speed: {self.speed}, Time: {self.time}, Lane Number: {self.lane_number}, Created At: {self.created_at}"
