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
                    'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
                }
            ),
            'identity': forms.TextInput(
                attrs={
                    'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
                }
            ),
            'account': forms.TextInput(
                attrs={
                    'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
                }
            ),
            'ctfc': forms.TextInput(
                attrs={
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
                'style': 'text-align: center; height: 30px; width: 250px; border-radius: 5px; border-width: 1px; font-size: 16px;'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'style': 'height: 30px; width: 250px; border-radius: 5px; border-width: 1px; text-align: center; font-size: 16px;'
            }
        )
    )

class InventoryForm(forms.Form):
    snum = forms.CharField(
        label='股票代號',
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'style': 'height: 30px; width: 250px; border-radius: 5px; border-width: 1px; text-align: center; font-size: 16px;'
            }
        )
    )
    amount = forms.IntegerField(
        label='買進股數',
        widget=forms.TextInput(
            attrs={
                'style': 'height: 30px; width: 250px; border-radius: 5px; border-width: 1px; text-align: center; font-size: 16px;'
            }
        )
    )
    price = forms.DecimalField(
        label='買進價格',
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(
            attrs={
                'style': 'height: 30px; width: 250px; border-radius: 5px; border-width: 1px; text-align: center; font-size: 16px;'
            }
        )
    )

class SellForm(forms.Form):
    snum = forms.CharField(label='Stock Number')
    amount = forms.IntegerField(label='Amount')
    price = forms.DecimalField(label='Price')