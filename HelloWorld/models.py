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