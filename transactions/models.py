from django.db import models
from acounts.models import UserAccount
from django.contrib.auth.models import User
from Book.models import BOOK

class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return f'{self.amount} deposited to {self.account.user.username}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BOOK, on_delete=models.CASCADE)
    rating = models.IntegerField()  # You can adjust this as needed
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.book.Title}'