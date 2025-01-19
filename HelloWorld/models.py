import os
from PIL import Image
from django.db import models

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
        verbose_name="圖書類別信息"

    def __str__(self):
        return self.bookTypeName

class BookInfo(models.Model):
    id = models.AutoField(primary_key=True)
    bookName = models.CharField(max_length=20,verbose_name='書名')
    publishDate = models.DateField(verbose_name='出版日期')
    price = models.FloatField(verbose_name='價格')
    bookType = models.ForeignKey(BookTypeInfo, on_delete=models.Prefetch,verbose_name='類別')

    class Meta:
        db_table = 't_book'
        verbose_name = "圖書信息"


class AccountInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=20)
    account = models.FloatField()

    class Meta:
        db_table = 't_account'
        verbose_name = "用戶賬戶信息"


class ImageConversion(models.Model):

    source_folder = models.CharField(max_length=500, verbose_name="源文件夹")  # 用户选择的源文件夹
    target_folder = models.CharField(max_length=500, blank=True, verbose_name="目标文件夹")  # 目标文件夹（可选）
    output_format = models.CharField(
        max_length=10,
        choices=[
            ("tga", "TGA"),
            ("png", "PNG"),
            ("jpg", "JPG"),
            ("bmp", "BMP"),
            ("gif", "GIF"),
            ("tiff", "TIFF"),
        ],
        default="tga",
        verbose_name="转换格式"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def convert_images(self):
        source_folder = self.source_folder
        target_folder = self.target_folder or source_folder  # 默认保存到原文件夹
        os.makedirs(target_folder, exist_ok=True)

        supported_formats = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")

        for filename in os.listdir(source_folder):
            if filename.lower().endswith(supported_formats):
                input_path = os.path.join(source_folder, filename)
                output_filename = os.path.splitext(filename)[0] + f".{self.output_format}"
                output_path = os.path.join(target_folder, output_filename)

                if os.path.exists(output_path):
                    print(f"跳过：{output_path} 已存在")
                    continue

                with Image.open(input_path) as img:
                    img.save(output_path, format=self.output_format.upper())

        print(f"批量转换完成！已保存至: {target_folder}")

    class Meta:
        db_table = 't_convert_images'
        verbose_name = "convert_images"

    def __str__(self):
        return f"{self.source_folder} -> {self.output_format}"