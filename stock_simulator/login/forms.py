from django import forms
from members.models import Customer  # 修改导入路径

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'identity', 'account', 'ctfc', 'password']
        labels = {
            'name': '姓名',
            'identity': '身分字號',
            'account': '帳號',
            'ctfc': '股票憑證',
            'password': '密碼',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': '請輸入您的姓名',
                    'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
                }
            ),
            'identity': forms.TextInput(
                attrs={
                    'placeholder': '請輸入您的身分字號',
                    'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
                }
            ),
            'account': forms.TextInput(
                attrs={
                    'placeholder': '請輸入您的帳號',
                    'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'placeholder': '請輸入您的密碼',
                    'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
                }
            ),
            'ctfc': forms.TextInput(
                attrs={
                    'placeholder': '請輸入您的股票憑證',
                    'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
                }
            )
        }

    def save(self, commit=True):
        customer = super(RegisterForm, self).save(commit=False)
        customer.password = self.cleaned_data['password']
        if commit:
            customer.save()
        return customer

class LoginForm(forms.Form):
    account = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '請輸入帳號',
                'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '請輸入密碼',
                'style': 'height: 30px; width: 250px; border-radius: 5px; border-width: 1px; text-align: center; font-size: 16px;'
            }
        )
    )

class InventoryForm(forms.Form):
    snum = forms.CharField(label='Snum', max_length=20)
    amount = forms.IntegerField(label='Amount')
    price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)

class SellForm(forms.Form):
    snum = forms.IntegerField(label='Stock Number')
    amount = forms.IntegerField(label='Amount')
    price = forms.DecimalField(label='Price')