from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from .tasks import send_payment_email, send_collect_email



class Collect(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    occasion = models.CharField(max_length=100)
    description = models.TextField()
    planned_amount = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='collect_covers/', null=True, blank=True)
    end_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def collected_amount(self):
        return self.payments.aggregate(total_amount=models.Sum('payment_amount'))['total_amount'] or 0
    
    def contributors_count(self):
        return self.payments.values('user').distinct().count()

    def donations(self):
        return self.payments.all()

    def __str__(self) -> str:
        return f'Сбор: {self.title}. Автор: {self.author}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        send_collect_email.delay(self.author.email, self.title)
        

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_amount = models.PositiveIntegerField()
    date_time_payment = models.DateTimeField(auto_now_add=True)
    collect = models.ForeignKey(Collect, related_name='payments', on_delete=models.CASCADE)

    def __str__(self):
        return f'Платёж для сбора: {self.collect.title}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        send_payment_email.delay(self.user.email, self.collect.title, self.payment_amount)
    
