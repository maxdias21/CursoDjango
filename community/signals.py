from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from community.models import Community
import os


def delete_cover(instance):
    try:
        os.remove(instance.image.path)
    except (ValueError, FileNotFoundError):
        pass


# Decorador que recebe o tipo de signal
# Usei o pre_delete, ou seja, antes de deletar ele faz algo (deletar a imagem pra não ficar salva no servidor)
# sender = model de 'Community'
# Modificar "apps.py"
@receiver(pre_delete, sender=Community)
def community_cover_delete(sender, instance, *args, **kwargs):
    # Sender = mostra a classe do ‘user’
    # instance = mostra a instância
    old_instance = Community.objects.filter(pk=instance.pk).first()
    delete_cover(old_instance)


@receiver(pre_save, sender=Community)
def community_cover_update(sender, instance, *args, **kwargs):
    # Sender = mostra a classe do ‘Community’
    # instance = mostra a instância
    old_instance = Community.objects.filter(pk=instance.pk).first()
    is_new_cover = old_instance.image != instance.image

    if is_new_cover:
        delete_cover(old_instance)
