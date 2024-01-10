from django import forms
from .models import Transaction



class TransactionForm(forms.ModelForm):
  class Meta:
    model = Transaction
    fields =['amount', 'transaction_type', ]


    def __init__(self,*args, **kwargs) :
      self.account = kwargs.pop('accounts')
      super().__init__(*args, **kwargs)
      self.fields['transaction_type'].disabled = True
      self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self,commit=True):
      self.instance.accounts= self.instance.accounts
      self.instance.balance_after_transaction=self.accounts.balance
      return super().save()
    


class DepositorForm(TransactionForm):
    def clean_amount(self):
      min_deposit_amount=100
      amount = self.cleaned_data.get('amount')
      if amount <min_deposit_amount:
        raise forms.ValidationError(f'you need to must be deposited amount at least{min_deposit_amount}')
      return amount
    


class WithdrawForm(TransactionForm):
  def clean_amount(self):
    accounts = self.accounts
    min_withdraw_amount = 500
    max_withdraw_amount = 20000
    balance = accounts.balance
    amount = self.cleaned_data.get('amount') 

    if(amount < min_withdraw_amount):
      raise forms.ValidationError(f'you can withdraw at least{min_withdraw_amount} amount')
    if(amount > max_withdraw_amount):
      raise forms.ValidationError(f'you can withdraw maximum{max_withdraw_amount}amount')
    if amount > balance:
      raise forms.ValidationError(f'you can not withdraw more than{amount} because your have only {balance} amount')
    return amount
  

class LoanRequestForm(TransactionForm):
  def clean_amount(self):
    amount = self.cleaned_data.get('amount')
    return amount