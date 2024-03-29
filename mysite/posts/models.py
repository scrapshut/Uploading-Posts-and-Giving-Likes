from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
from django.db.models import CharField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(models.Model):
    objects=models.Manager()
    published = PublishedManager()
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=100,default='')
    slug = models.SlugField(max_length=120,default='')
    author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.id,self.slug])


@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug=slugify(kwargs['instance'].title)
    kwargs['instance'].slug=slug

