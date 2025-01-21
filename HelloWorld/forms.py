from django import forms
import os

from django import forms
from django.forms import ModelForm, Form, widgets
from django.forms.formsets import formset_factory

from .utils import get_current_language, get_translated_text
from HelloWorld import utils
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
            'name':'名前',
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
            'bookName':'書籍名',
            'price':'書籍価格',
            'publishDate':'出版日',
            'bookType':'書籍カテゴリ',
        }

        help_texts = {
            'bookName' : '書籍名を入力してください'
        }

class BookInfoForm(Form):
    bookName = forms.CharField(
        max_length=20,
        label="書籍名",
        required=True,
        widget=widgets.TextInput(attrs={'placeholder':'名前を入力して',"class":"inputClass"})
    )
    price = forms.FloatField(label="書籍価格")
    publishDate = forms.DateField(label="出版日")
    bookTypeList = BookTypeInfo.objects.values()
    # 書籍カテゴリをドロップダウン形式で表示し、選択肢のidは書籍カテゴリId、それに対する選択肢のテキストは書籍カテゴリ名
    choices =[(v['id'], v['bookTypeName']) for v, v in  enumerate(bookTypeList)]
    bookType_id = forms.ChoiceField(choices=choices , label="カテゴリ")

class ImageConversionForm(forms.ModelForm):
    """  ユーザーがフォルダと変換形式を選択するためのフォーム  """
    class Meta:
        model = ImageConversion
        fields = ["source_folder", "target_folder", "output_format"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lang = get_current_language()


        self.fields["source_folder"].label = get_translated_text(lang, "source_folder_label")
        self.fields["source_folder"].widget.attrs.update(
            {
                "class": "form-control",
                "style": "width: 100%; max-width: 400px;"
            }
        )

        self.fields["target_folder"].label = get_translated_text(lang, "target_folder_label")
        self.fields["target_folder"].widget.attrs.update(
            {
                "placeholder": get_translated_text(lang, "default_target_folder"),
                "class": "form-control",
                "style": "width: 100%; max-width: 400px;"
            }
        )

        self.fields["output_format"].label = get_translated_text(lang, "output_format_label")

    # lang = utils.get_current_language()
    # print("ImageConversionForm", lang)



    # source_folder = forms.CharField(
    #     label= utils.get_translated_text(lang, "source_folder_label"),
    #     widget=forms.TextInput(attrs={"class": "form-control"}),
    # )
    # target_folder = forms.CharField(
    #     label=utils.get_translated_text(lang, "target_folder_label"),
    #     required=False,
    #     widget=forms.TextInput(attrs={"class": "form-control", "placeholder": utils.get_translated_text(lang, "default_target_folder")}),
    # )
    # output_format = forms.ChoiceField(
    #     label=utils.get_translated_text(lang, "output_format_label"),
    #     choices=ImageConversion._meta.get_field("output_format").choices,
    #     widget=forms.Select(attrs={"class": "form-control"}),
    # )

def get_folder_choices(path):
    try:
        return [(os.path.join(path, folder), folder) for folder in os.listdir(path) if
                os.path.isdir(os.path.join(path, folder))]
    except FileNotFoundError:
        return []


