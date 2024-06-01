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
