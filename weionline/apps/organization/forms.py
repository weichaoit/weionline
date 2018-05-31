# _*_ coding: utf-8 _*_
import re
from django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']

        mobile_pattern = '^1\d{10}$'
        p = re.compile(mobile_pattern)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法!',code='mobile_invalid')

