from django.db import models
from django.utils import timezone

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    scheduled_time = models.DateTimeField(default=timezone.now)
    items = models.ManyToManyField(MenuItem)

    def __str__(self):
        return f"{self.customer_name} - {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"

