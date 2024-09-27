from django.db import models


class GraphLog(models.Model):
    value = models.PositiveIntegerField()
    day = models.CharField(max_length=5)
    date_created = models.DateField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.day} {self.value}"