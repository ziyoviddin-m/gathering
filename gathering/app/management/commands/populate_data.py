from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from app.models import Collect, Payment

class Command(BaseCommand):
    help = 'Populates the database with mock data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        users = []
        for _ in range(50):
            user, created = User.objects.get_or_create(
                username=fake.user_name(),
                defaults={
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': fake.email(),
                    'password': 'password'
                }
            )
            if created:
                user.set_password('password')
                user.save()
            users.append(user)

        for _ in range(20):
            author = fake.random_element(users)
            collect, created = Collect.objects.get_or_create(
                author=author,
                title=fake.sentence(),
                occasion=fake.word(),
                description=fake.paragraph(),
                planned_amount=fake.random_number(digits=5),
                end_datetime=fake.future_datetime(),
            )

            for _ in range(fake.random_int(min=1, max=5)):
                user = fake.random_element(users)
                payment_amount = fake.random_number(digits=4)
                Payment.objects.get_or_create(
                    user=user,
                    payment_amount=payment_amount,
                    collect=collect,
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))