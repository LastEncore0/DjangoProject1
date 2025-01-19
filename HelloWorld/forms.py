from django import forms
from django.forms import ModelForm, Form, widgets
from django.forms.formsets import formset_factory

from HelloWorld.models import StudentInfo, BookTypeInfo, BookInfo, ImageConversion


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

class ImageConversionForm(forms.ModelForm):
    """  用户选择文件夹 & 转换格式的表单 """
    class Meta:
        model = ImageConversion
        fields = ["source_folder", "target_folder", "output_format"]

    source_folder = forms.CharField(
        label="源文件夹",
        path="C:/",  #  起始路径，可以修改为特定目录
        allow_folders=True,
        allow_files=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "source-folder",
            "placeholder": "手动输入或点击选择文件夹",
        }),
    )
    target_folder = forms.CharField(
        label="目标文件夹（可选）",
        path=" C:/",  # 也可以设置为 "/home" 或 "C:/Users"
        allow_folders=True,
        allow_files=False,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "target-folder",
            "placeholder": "默认保存到源文件夹",
        }),
    )
    output_format = forms.ChoiceField(
        label="转换格式",
        choices=ImageConversion._meta.get_field("output_format").choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )