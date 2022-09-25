from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  
from .models import Work

class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')  

class WorkForm(forms.ModelForm):
    price = forms.IntegerField(min_value=1000,max_value=50000)
    def clean(self):
        price = self.cleaned_data['price']
        time =  self.cleaned_data['time']
        if time < 3 and price > 30000:
            raise forms.ValidationError('حداکثر قیمت کار‌های با زمان ۳ روز ۳۰۰۰۰ تومان می باشد')
    class Meta:
        model = Work
        fields = ('work_title', 'price', 'time', 'info')
        widgets = {
            'work_title' : forms.Textarea(attrs={'cols': 80, 'rows': 1}),
            'info' : forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }
