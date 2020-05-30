from django.db import models


# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey('City', related_name='suppliers', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categoties'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ManyToManyField(Category)
    suppliers = models.ForeignKey(Supplier, related_name='products', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} Product {self.product_id} in order {self.order_id}'

class Order(models.Model):
    user_email = models.EmailField()
    products = models.ManyToManyField(Product, through=OrderProducts)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} from {self.user_email}'

class CurrencyRate(models.Model):

    CURRENCIES = (
        ('usd', 'usd'),
        ('eur', 'eur')
    )

    currency = models.CharField(max_length=3, choices=CURRENCIES)
    rate = models.DecimalField(max_digits=10, decimal_places=6, default=1)

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                rate = CurrencyRate.objects.get(currency=self.currency)
                self.pk = rate.pk
            except CurrencyRate.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Rate of {self.currency} is {self.rate}'
