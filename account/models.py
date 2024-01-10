from django.db import models
from django.contrib.auth.models import User
# Create your models here.

ACCOUNT_TYPE =(
  ('Savings','Savings'),
  ('Current','Current'),
)
GENDER_TYPE=(
  ('Male','Male'),
  ('Female','Female'),
)

class UserBankAccount(models.Model):
  user = models.OneToOneField(User,related_name="accounts",on_delete=models.CASCADE)
  account_type = models.CharField(max_length=255,choices=ACCOUNT_TYPE)
  account_no = models.IntegerField(unique=True)
  date_of_birth = models.DateField(null=True, blank=True)
  gender = models.CharField(max_length=255,choices=GENDER_TYPE)
  initial_deposit_date = models.DateField(auto_now_add=True,null=True, blank=True)
  balance = models.DecimalField(max_digits=50, decimal_places=2,default=0)


  def __str__(self) :
    return str(self.account_no)

class UserAddress(models.Model):
  user = models.OneToOneField(User, related_name="address", on_delete=models.CASCADE)
  street_address = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  postal_code = models.IntegerField()
  country = models.CharField(max_length=255)

  def __str__(self) :
    return self.user.username+ ''+self.user.email