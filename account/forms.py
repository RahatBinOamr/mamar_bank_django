from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserBankAccount, UserAddress


class UserRegistrationForm(UserCreationForm):
    street_address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=255)
    account_type = forms.ChoiceField(choices=(
        ('Savings', 'Savings'),
        ('Current', 'Current')
    ))
  
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=(
        ('Male', 'Male'),
        ('Female', 'Female')
    ))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'street_address', 'city',
                  'postal_code', 'country', 'account_type', 'date_of_birth', 'gender']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            account_type = self.cleaned_data.get('account_type')
            date_of_birth = self.cleaned_data.get('date_of_birth')
            gender = self.cleaned_data.get('gender')

            UserAddress.objects.create(
                user=user,
                street_address=street_address,
                city=city,
                postal_code=postal_code,
                country=country,
            )
            UserBankAccount.objects.create(
                user=user,
                account_type=account_type,
                account_no=100000 + user.id,
                date_of_birth=date_of_birth,
                gender=gender,
            )

        return user
    


class UserUpdateForm(forms.ModelForm):
    street_address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=255)
    account_type = forms.ChoiceField(choices=(
        ('Savings', 'Savings'),
        ('Current', 'Current')
    ))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=(
        ('Male', 'Male'),
        ('Female', 'Female')
    ))

    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'email']

        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance:
                try:
                    user_accounts = self.instance.accounts
                    user_address = self.instance.address
                except UserBankAccount.DoesNotExist:
                    user_accounts = None
                    user_address = None
                if user_accounts:
                    self.fields['account_type'].initial = user_accounts.account_type
                    self.fields['account_no'].initial = user_accounts.account_no
                    self.fields['date_of_birth'].initial = user_accounts.date_of_birth
                    self.fields['gender'].initial = user_accounts.gender
                    
                    self.fields['street_address'].initial = user_address.street_address
                    self.fields['city'].initial = user_address.city
                    self.fields['postal_code'].initial = user_address.postal_code
                    self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_account ,created= UserBankAccount.objects.get_or_create(user=user)
            user_address ,created= UserAddress.objects.get_or_create(user=user)


            user_address.street_address = self.cleaned_data.get('street_address')
            user_address.city = self.cleaned_data.get('city')
            user_address.postal_code = self.cleaned_data.get('postal_code')
            user_address.country = self.cleaned_data.get('country')
            user_address.save()


            user_account.account_type = self.cleaned_data.get('account_type')
            user_account.date_of_birth = self.cleaned_data.get('date_of_birth')
            user_account.gender = self.cleaned_data.get('gender')
            user_account.save()

        return user
