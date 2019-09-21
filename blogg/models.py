from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

# Create your models here.
class UserInfo(AbstractUser):
    """
    用户信息表
    """
    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.png", verbose_name="头像")
    create_time = models.DateTimeField(auto_now_add=True)

    blog = models.OneToOneField(to="Blog", to_field="nid", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Blog(models.Model):
    """
    博客信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)  # 个人博客标题
    site = models.CharField(max_length=32, unique=True)  # 个人博客后缀
    theme = models.CharField(max_length=32)  # 博客主题

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客站点'
        verbose_name_plural = verbose_name


class Category(models.Model):
    """
    博客文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    blog = models.ForeignKey(to='Blog', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    标签
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    blog = models.ForeignKey(to_field='nid', to='Blog', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
    文章
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20,unique=True)
    desc = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)

    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    see_count = models.IntegerField(default=0)

    category = models.ForeignKey(to='Category', null=True, to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=('article', 'tag')
    )


    def __str__(self):
        return self.title


    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    """
    文章详情表
    """
    nid = models.AutoField(primary_key=True)
    content = RichTextField()
    article = models.OneToOneField(to='Article', to_field='nid', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章详情'
        verbose_name_plural = verbose_name


class Article2Tag(models.Model):
    """
    文章和tag多对多表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to_field='nid', to='Article', on_delete=models.CASCADE)
    tag = models.ForeignKey(to='Tag', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return '<Article2Tag>:{}-{}'.format(self.article,self.tag)
    class Meta:
        unique_together = (('article', 'tag'),)
        verbose_name = '文章--标签'
        verbose_name_plural = verbose_name


class ArticleUpDown(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo',  null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article', null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = (('article', 'user'),)
        verbose_name = '文章点赞'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True,blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering=('create_date',)
        verbose_name = '评论'
        verbose_name_plural = verbose_name
