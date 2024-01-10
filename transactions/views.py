import datetime
from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Sum
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.views import View
from django.views.generic import CreateView,ListView
from .forms import DepositorForm,LoanRequestForm,TransactionForm,WithdrawForm
from .models import Transaction
# Create your views here.



class TransactionCreateMixin(LoginRequiredMixin,CreateView):
  template_name =''
  model = Transaction
  title=''
  success_url= reverse_lazy('')


  def get_form_kwargs(self) :
    kwargs =super().get_form_kwargs()
    kwargs.update({
      'account' : self.request.user.accounts
    })
    return kwargs
  
  def get_context_data(self, **kwargs: Any) :
    context= super().get_context_data(**kwargs)
    context.update({
      'title' : self.title
    })
    return context
  

class DepositMonyView(TransactionCreateMixin):
  from_class = DepositorForm
  title='Deposit'


  def get_initial(self) :
    initial ={'transaction_type':'deposit'}
    return initial
  
  def form_valid(self, form) :
    amount = form.cleaned_data.get('amount')
    account = self.user.accounts
    if not account.initial_deposit_date:
      now = timezone.now()
      account.initial_deposit_date = now
      account.balance += amount
      account.save(
        update_fields=[
          'initial_deposit_date',
          'balance'
        ]
      )
      messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
      return super().form_valid(form)
  

class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money'

    def get_initial(self):
        initial = {'transaction_type': 'withdraw'}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.accounts.balance -= form.cleaned_data.get('amount')
        
        self.request.user.accounts.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account'
        )
        
        return super().form_valid(form)

class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request For Loan'

    def get_initial(self):
        initial = {'transaction_type': 'loan'}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transaction.objects.filter(
            account=self.request.user.accounts,transaction_type='loan',loan_approve=True).count()
        if current_loan_count >= 'loan':
            return HttpResponse("You have cross the loan limits")
        messages.success(
            self.request,
            f'Loan request for {"{:,.2f}".format(float(amount))}$ submitted successfully'
        )
        
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = ''
    model = Transaction
    balance = 0 
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.accounts
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.accounts.balance

        return queryset.distinct() 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.accounts
        })

        return context
    
        
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transaction, id=loan_id)
        print(loan)
        if loan.loan_approve:
            user_account = loan.account
                
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.loan_approved = True
                loan.transaction_type = 'loan paid'
                loan.save()
                return redirect('transactions:loan_list')
            else:
                messages.error(
            self.request,
            f'Loan amount is greater than available balance'
        )

        return redirect('loan_list')


class LoanListView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = ''
    context_object_name = '' 
    
    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transaction.objects.filter(account=user_account,transaction_type=3)
        print(queryset)
        return queryset
  

  
