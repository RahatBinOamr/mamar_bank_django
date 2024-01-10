from django.db import models
from account.models import UserBankAccount
# Create your models here.

TRANSACTION_TYPE=(
  ('withdraw','withdraw'),
  ('deposit','deposit'),
  ('loan','loan'),
  ('loan paid','loan paid'),
)

class Transaction(models.Model):
  account = models.ForeignKey(UserBankAccount, related_name='transactions',on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=20, decimal_places=2)
  balance_after_transaction = models.DecimalField(max_digits=20, decimal_places=2)
  transaction_type = models.CharField(max_length=300, choices=TRANSACTION_TYPE)
  timestamp = models.DateTimeField(auto_now_add=True)
  loan_approved = models.BooleanField(default=False)

  class Meta:
    ordering = ['timestamp']


