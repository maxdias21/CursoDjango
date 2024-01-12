from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from news.models import News
import os
from django.conf import settings
from PIL import Image


def resize_image(image, new_width=800):
    image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)

    # Abrir imagem com pillow
    image_pillow = Image.open(image_full_path)

    # Pegar largura, altura da minha imagem original
    original_width, original_height = image_pillow.size

    new_height = round(new_width * original_height / original_width)

    new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
    new_image.save(
        image_full_path,
        optimize=True,
        quality=100,
    )


def delete_cover(instance):
    try:
        os.remove(instance.image.path)
    except (ValueError, FileNotFoundError):
        ...


# Decorador que recebe o tipo de signal
# Usei o pre_delete, ou seja, antes de deletar ele faz algo (deletar a imagem pra não ficar salva no servidor)
# sender = model de 'News'
# Modificar "‘apps’.py"

@receiver(pre_delete, sender=News)
def news_recipe_delete(sender, instance, *args, **kwargs):
    # Sender = mostra a classe do ‘News’
    # instance = mostra a instância
    old_instance = News.objects.filter(pk=instance.pk).first()
    delete_cover(old_instance)


@receiver(pre_save, sender=News)
def news_recipe_update(sender, instance, *args, **kwargs):
    # Sender = mostra a classe do ‘News’
    # instance = mostra a instância
    try:
        old_instance = News.objects.filter(pk=instance.pk).first()

        is_new_cover = old_instance.image != instance.image

        if is_new_cover:
            delete_cover(old_instance)
    except:
        ...


@receiver(post_save, sender=News)
def news_recipe_resize_image(sender, instance, created, *args, **kwargs):
    instance.image = resize_image(instance.image)

