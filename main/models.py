from django.db import models

# 🔹 Category for organizing menu items (e.g., Drinks, Meals)
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"  # Fixes "Categorys" in admin

    def __str__(self):
        return self.name


# 🔹 Each menu item belongs to a category
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


# 🔹 Orders placed by customers with scheduling support
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    scheduled_time = models.DateTimeField()
    items = models.ManyToManyField(MenuItem)

    def __str__(self):
        return f"{self.customer_name} - {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
