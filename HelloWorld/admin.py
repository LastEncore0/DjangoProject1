from django.contrib import admin

from HelloWorld.models import BookTypeInfo, BookInfo

# Register your models here.
admin.site.register(BookTypeInfo)

@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'bookName', 'publishDate', 'price', 'bookType']
    search_fields = ['bookName', 'publishDate']

    #設置只讀字段
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            self.readonly_fields = []
        else:
            self.readonly_fields = ['id']
        return self.readonly_fields

    #網站標題
    admin.site.site_title='後臺管理系統'
    admin.site.index_title='圖書管理模塊'
    admin.site.site_header='Hakuya管理系統'