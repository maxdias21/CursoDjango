from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Decorador que recebe o tipo de signal
# Usei o post_save, ou seja, quando a pessoa salvar algo ele envia um sinal
# sender = model de ‘User’
# Modificar "apps.py"
@receiver(post_save, sender=User)
def send_email(sender, instance, created, *args, **kwargs):
    # Sender = mostra a classe do ‘user’
    # instance = mostra o seu usuário, instância
    # created = se criou mostra true, se editou mostra false
    if created:
        ...
        # enviar um email
