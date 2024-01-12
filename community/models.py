from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify
from django.utils.translation import gettext_lazy


# Create your models here.

class Community(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=gettext_lazy('Author'))
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name=gettext_lazy('Title'))
    description = models.TextField(max_length=250, blank=False, null=False, verbose_name=gettext_lazy('Description'))
    content = models.CharField(verbose_name=gettext_lazy('Content'), max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    image = models.ImageField(upload_to='community/covers/%Y/%m/%d', null=False, blank=False,
                              verbose_name=gettext_lazy('Image'))
    is_published = models.BooleanField(default=False, verbose_name=gettext_lazy('Published'))
    slug = models.SlugField(unique=True, blank=False, null=False, max_length=255)
    qty_read = models.IntegerField(default=0)

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        time = datetime.now()
        time_slug = time.strftime('%d %m %Y %I %M %S')
        self.slug = slugify(f'{self.title}-{time_slug}')

        return super().full_clean()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = gettext_lazy('Community')
        verbose_name = gettext_lazy('Community')
