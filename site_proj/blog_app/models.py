from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse #? pozwala utworzyc url na podstawie nazwy


#! Dodaje wlasnego menegera jak Class.< objects >.all()
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

#! model poatu
class Post(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length = 150)
    slug = models.SlugField(max_length = 250, unique_for_date='publish') #? unikalny slug po datie
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')
    #! self manager in shell
    objects = models.Manager()  # Domyslny meneger
    published = PublishedManager()  # Wlasny manager

    class Meta:
        ordering = ('-publish',)
        # db_table = 'self_name' #? dodaje mozliwosc zmieniac nazwe tabeli
        # default_manager_name =  #? ???

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_app:post_detail',  #? reverse pozwala na utworzenie adresu URL na podstawie nazwy i parametru z views.py 
                        args=[self.publish.year, 
                                self.publish.strftime('%m'),
                                self.publish.strftime('%d'),
                                self.slug])



