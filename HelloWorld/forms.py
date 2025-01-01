from django import forms
from django.forms import ModelForm
from django.forms.formsets import formset_factory

from HelloWorld.models import StudentInfo


class StudentForm(ModelForm):
    class Meta:
        model = StudentInfo
        # fields = "__all__"
        fields = [ "name","age"]
        widgets = {
            'name':forms.TextInput(attrs={'id':'name','class':'inputClass'}),
            'age':forms.NumberInput(attrs={'id':'age'})
        }

        labels = {
            'name':'姓名',
            'age':'年齡'
        }
