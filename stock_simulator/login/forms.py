from django import forms
from members.models import Customer  # 修改导入路径

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'identity', 'account', 'password', 'ctfc']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        customer = super(RegisterForm, self).save(commit=False)
        customer.password = self.cleaned_data['password']  
        if commit:
            customer.save()
        return customer
class LoginForm(forms.Form):
    account = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
class InventoryForm(forms.Form):
    snum = forms.CharField(label='Snum', max_length=20)
    amount = forms.IntegerField(label='Amount')
    price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)
class SellForm(forms.Form):
    snum = forms.IntegerField(label='Stock Number')
    amount = forms.IntegerField(label='Amount')
    price = forms.DecimalField(label='Price')