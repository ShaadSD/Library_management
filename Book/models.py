from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
# Create your models here.
class BOOK(models.Model):
    Title=models.CharField(max_length=100, default='Title')
    Description=models.TextField(max_length=100)
    photo=models.ImageField(upload_to='boook',default='path/to/default/image.jpg')
    Borrowing_Price=models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    category=models.CharField(max_length=100,default='category')
    user=models.ForeignKey(User,related_name='books',on_delete=models.CASCADE)
    slug=models.SlugField(max_length=100,unique=True,null=True,blank=True)
    def __str__(self):
        return self.Title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Title)
        super().save(*args, **kwargs)

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BOOK, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    borrow_date = models.DateTimeField(auto_now_add=True) 