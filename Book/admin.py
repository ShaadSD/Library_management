from django.contrib import admin

# Register your models here.
from .models import BOOK
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug' : ('category',)}
    list_display=['category','slug']
    def __str__(self):
        return self.category
admin.site.register(BOOK,BookAdmin)