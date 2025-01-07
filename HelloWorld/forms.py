from django import forms
from django.forms import ModelForm, Form, widgets
from django.forms.formsets import formset_factory

from HelloWorld.models import StudentInfo, BookTypeInfo, BookInfo


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

class BookInfoModelForm(ModelForm):
    class Meta:
        model = BookInfo
        fields = "__all__"
        # fields = [ "name","age"]
        widgets = {
            'bookName':forms.TextInput(attrs={'id':'bookName','class':'inputClass','placeholder':'請輸入名稱'})
        }

        labels = {
            'bookName':'圖書名稱',
            'price':'圖書價格',
            'publishDate':'出版日期',
            'bookType':'圖書類別',
        }

        help_texts = {
            'bookName' : '請輸入圖書名稱'
        }

class BookInfoForm(Form):
    bookName = forms.CharField(
        max_length=20,
        label="圖書名稱",
        required=True,
        widget=widgets.TextInput(attrs={'placeholder':'請輸入名稱',"class":"inputClass"})
    )
    price = forms.FloatField(label="圖書價格")
    publishDate = forms.DateField(label="出版日期")
    bookTypeList = BookTypeInfo.objects.values()
    # 图书类别以下拉框形式显示，下拉框选项id是图书类别Id，下拉框选项文本是图书类别名称
    choices =[(v['id'], v['bookTypeName']) for v, v in  enumerate(bookTypeList)]
    bookType_id = forms.ChoiceField(choices=choices , label="圖書類別")
