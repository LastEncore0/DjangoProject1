import os
from PIL import Image
from django.db import models

from HelloWorld import utils


# Create your models here.
class StudentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    age = models.IntegerField()

    class Meta:
        db_table = 't_student'

class BookTypeInfo(models.Model):
    id = models.AutoField(primary_key=True)
    bookTypeName = models.CharField(max_length=20)

    class Meta:
        db_table = 't_booktype'
        verbose_name="書籍類別"

    def __str__(self):
        return self.bookTypeName

class BookInfo(models.Model):
    id = models.AutoField(primary_key=True)
    bookName = models.CharField(max_length=20,verbose_name='書名')
    publishDate = models.DateField(verbose_name='発売日')
    price = models.FloatField(verbose_name='値段')
    bookType = models.ForeignKey(BookTypeInfo, on_delete=models.Prefetch,verbose_name='類別')

    class Meta:
        db_table = 't_book'
        verbose_name = "書籍情報"


class AccountInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=20)
    account = models.FloatField()

    class Meta:
        db_table = 't_account'
        verbose_name = "ユーザー情報"


class ImageConversion(models.Model):

    source_folder = models.CharField(max_length=500, verbose_name="オリジナルファイル")
    target_folder = models.CharField(max_length=500, blank=True, verbose_name="目標ファイル")
    output_format = models.CharField(
        max_length=10,
        choices=[
            ("tga", "TGA"),
            ("png", "PNG"),
            ("bmp", "BMP"),
            ("gif", "GIF"),
            ("tiff", "TIFF"),
        ],
        default="tga",
        verbose_name="フォマード"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def convert_images(self):
        source_folder = self.source_folder
        target_folder = self.target_folder or source_folder
        os.makedirs(target_folder, exist_ok=True)

        format_mapping = {
            "jpg": "JPEG",
            "png": "PNG",
            "bmp": "BMP",
            "gif": "GIF",
            "tiff": "TIFF",
            "tga": "TGA",
        }

        supported_formats =  (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")
        logs = [] # メッセージを保存するため
        lang = utils.get_current_language()

        for filename in os.listdir(source_folder):
            if filename.lower().endswith(supported_formats):
                input_path = os.path.join(source_folder, filename)
                output_filename = os.path.splitext(filename)[0] + f".{self.output_format}"
                output_path = os.path.join(target_folder, output_filename)

                if os.path.exists(output_path):
                    skip_message = utils.get_translated_text(lang, "skipped")
                    logs.append(f"{skip_message} {output_path} ")
                    continue

                with Image.open(input_path) as img:
                    img.save(output_path, format=self.output_format.upper())
                    success_message = utils.get_translated_text(lang, "conversion_success")
                    logs.append(f"{success_message} {output_path}")

        complete_message = utils.get_translated_text(lang, "batch_conversion_complete")
        logs.append(f"{complete_message} {target_folder}")
        return logs

    class Meta:
        db_table = 't_convert_images'
        verbose_name = "convert_images"

    def __str__(self):
        return f"{self.source_folder} -> {self.output_format}"