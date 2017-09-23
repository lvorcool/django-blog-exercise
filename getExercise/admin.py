from django.contrib import admin
from getExercise.models import People, Article, Comment, UserProfile, Ticket

# Register your models here. admin后台显示的数据结构
admin.site.register(People)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Ticket)