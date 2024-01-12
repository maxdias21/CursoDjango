from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
import string
from random import SystemRandom


# Create your models here.

# Vou fazer um many to many, lá em baixo comentado tem o ContentType
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters +
                    string.digits,
                    k=5
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Desativei ContentType para testar ManyToMany
'''class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Aqui começa os campos da relação genérica

    # Representa o model que queremos encaixar aqui
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # Representa o id da linha do model descrito acima
    object_id = models.PositiveIntegerField()

    # Um campo que representa a relação gerérica que conhece os campos acima (content_type e object_id_
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters +
                    string.digits,
                    k=5
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
'''
