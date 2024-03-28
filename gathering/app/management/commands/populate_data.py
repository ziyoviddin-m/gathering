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
            user = User.objects.create_user(
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password='password'
            )
            users.append(user)

        for _ in range(5000):
            author = fake.random_element(users)
            collect = Collect.objects.create(
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
                Payment.objects.create(
                    user=user,
                    payment_amount=payment_amount,
                    collect=collect,
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
