from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class People(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    job = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.name

'''
字段说明
1. null   如果为True，Django将在数据库中将空值存储为NULL。 默认为False
2. blank  如果为True，则该字段被允许为空白。 默认为False

'''
# 文章表
class Article(models.Model):
    # 文章标题
    headline = models.CharField('标题', null=True, blank=True, max_length=500)
    # 文章内容
    content = models.TextField('文章正文', null=True, blank=True)
    # 给文章上传图片
    # img = models.ImageField('图片',upload_to='img', height_field=300, width_field=300, max_length=200, null=True, blank=True)
    img = models.CharField('文章附图', null=True, blank=True, max_length=500)
    # 阅读量
    views = models.IntegerField(default=0)
    # 收藏量
    favs = models.IntegerField(default=0)
    # 创建文章的时间, 默认创建文章的当前时间
    createtime = models.DateTimeField('创建时间', default=timezone.now)
    # 文章标签, 选项有Tech和Life
    TAG_CHOICES = (
        ('知识', 'Tech'),
        ('生活', 'Life'),
    )
    tag = models.CharField(null=True, blank=True, max_length=5, choices=TAG_CHOICES)
    cover = models.FileField(upload_to='cover_image', null=True)

    def __str__(self):
        return self.headline
# 评论表
class Comment(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    avatar = models.CharField(default="http://n.sinaimg.cn/ent/crawl/20170907/K0wM-fykufii0195474.jpg", max_length=1000)
    comment = models.TextField()
    createtime = models.DateTimeField(default=timezone.now)
    # ForeignKey,多对一关系, 需要一个位置参数：与该模型关联的类,to=Article,
    belong_to = models.ForeignKey(to=Article, related_name='under_comments', null=True, blank=True)
    best_comment = models.BooleanField(default=False)
    def __str__(self):
        return self.comment

class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    profile_image = models.FileField(upload_to='profile_image')

class Ticket(models.Model):
    voter = models.ForeignKey(to=UserProfile, related_name='voted_tickets')
    article = models.ForeignKey(to=Article, related_name='tickets')
    VOTE_CHOICES = (
        ('like', 'like'),
        ('dislike','dislike'),
        ('normal','normal')
    )
    choice = models.CharField(choices=VOTE_CHOICES, max_length=10)

    def __str__(self):
        return str(self.id)