from django.core.management.base import BaseCommand
import random

from faker import Faker

from catalog.models import Product, Supplier, City, Category


class Command(BaseCommand):

    def generate(self, amount=10):
        fake = Faker()
        categories = Category.objects.values_list('id', flat=True)
        suppliers = list(Supplier.objects.values_list('id', flat=True))
        for i in range(amount):
            product = Product.objects.create(
                name=fake.name(),
                price=random.random()*100,
                description=fake.text(),
                category_id=random.choice(categories),
            )
            product.suppliers.add(
                *random.sample(suppliers, random.randint(1, len(suppliers)))
            )

    def handle(self, *args, **options):
        self.generate()