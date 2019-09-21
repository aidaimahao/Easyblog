"""
bbs用到的form类
"""

from django import forms
from django.core.exceptions import ValidationError

# 定义一个注册的form类
class RegForms(forms.Form):
    username = forms.CharField(
        max_length=6,
        label='用户名',
        error_messages={
            'max_length':'用户名最长16位',
            'required':'用户名不能为空',
        },
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password = forms.CharField(
        max_length=18,
        min_length=6,
        label='密码',
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        error_messages={
            'max_length': '密码最长18位',
            'required': '密码不能为空',
            'min_length':'密码不能少于6位',
        },

    )
    repwd = forms.CharField(
        max_length=18,
        min_length=6,
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        error_messages={
            'max_length': '密码最长18位',
            'required': '确认密码不能为空',
            'min_length': '密码不能少于6位',
        }
    )
    email = forms.CharField(
        max_length=18,
        min_length=6,
        label='邮箱',
        widget=forms.EmailInput(attrs={'class':'form-control'}),
        error_messages={
            'invalid': '邮箱格式错误',
            'required': '邮箱不能为空',
        }
    )
    def clean(self):
        password = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('repwd')
        print(password)
        print(repwd)
        if  repwd and  repwd!= password:
            print('fdfsdf')
            self.add_error('repwd',ValidationError('两次密码不一致'))
        else:
            return self.cleaned_data