from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy


# Create your models here.

class AuthorRegister(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name=gettext_lazy('Username'),
                                    default=None,
                                    related_name='profile')
    age = models.IntegerField(blank=False, null=False, default='', verbose_name=gettext_lazy('Age'), )
    hometown = models.CharField(choices=(
        ('Acre', 'Acre'),
        ('Alagoas', 'Alagoas'),
        ('Amapá', 'Amapá'),
        ('Amazonas', 'Amazonas'),
        ('Bahia', 'Bahia'),
        ('Ceará', 'Ceará'),
        ('Distrito Federal', 'Distrito Federal'),
        ('Espírito Santo', 'Espírito Santo'),
        ('Goiás', 'Goiás'),
        ('Maranhão', 'Maranhão'),
        ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso do Sul', 'Mato Grosso do Sul'),
        ('Minas Gerais', 'Minas Gerais'),
        ('Pará ', 'Pará '),
        ('Paraíba', 'Paraíba'),
        ('Paraná', 'Paraná'),
        ('Pernambuco', 'Pernambuco'),
        ('Piauí', 'Piauí'),
        ('Rio de Janeiro', 'Rio de Janeiro'),
        ('Rio Grande do Norte', 'Rio Grande do Norte'),
        ('Rio Grande do Sul', 'Rio Grande do Sul'),
        ('Rondônia', 'Rondônia'),
        ('Roraima', 'Roraima'),
        ('Santa Catarina', 'Santa Catarina'),
        ('São Paulo', 'São Paulo'),
        ('Sergipe', 'Sergipe'),
        ('Tocantins', 'Tocantins'),
    ), max_length=19, default='', null=False, blank=False, verbose_name=gettext_lazy('Hometown'))
    current_city = models.CharField(choices=(
        ('Acre', 'Acre'),
        ('Alagoas', 'Alagoas'),
        ('Amapá', 'Amapá'),
        ('Amazonas', 'Amazonas'),
        ('Bahia', 'Bahia'),
        ('Ceará', 'Ceará'),
        ('Distrito Federal', 'Distrito Federal'),
        ('Espírito Santo', 'Espírito Santo'),
        ('Goiás', 'Goiás'),
        ('Maranhão', 'Maranhão'),
        ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso do Sul', 'Mato Grosso do Sul'),
        ('Minas Gerais', 'Minas Gerais'),
        ('Pará ', 'Pará '),
        ('Paraíba', 'Paraíba'),
        ('Paraná', 'Paraná'),
        ('Pernambuco', 'Pernambuco'),
        ('Piauí', 'Piauí'),
        ('Rio de Janeiro', 'Rio de Janeiro'),
        ('Rio Grande do Norte', 'Rio Grande do Norte'),
        ('Rio Grande do Sul', 'Rio Grande do Sul'),
        ('Rondônia', 'Rondônia'),
        ('Roraima', 'Roraima'),
        ('Santa Catarina', 'Santa Catarina'),
        ('São Paulo', 'São Paulo'),
        ('Sergipe', 'Sergipe'),
        ('Tocantins', 'Tocantins'),
    ), max_length=19, default='', null=False, blank=False, verbose_name=gettext_lazy('Current City'))
    sex = models.CharField(choices=(('Masculino', 'Masculino'),
                                    ('Feminino', 'Feminino'),
                                    ('Outro', 'Outro')),
                           max_length=10, default='', verbose_name=gettext_lazy('Sex'))
    marital_status = models.CharField(choices=(
        ('Solteiro', 'Solteiro'),
        ('Casado', 'Casado'),
        ('Divorciado', 'Divorciado'),
        ('Viúvo', 'Viúvo')
    ), max_length=15, default='', verbose_name=gettext_lazy('Marital Status'))
    phone_number = models.IntegerField(blank=False, null=False, verbose_name=gettext_lazy('Phone Number'))
    description = models.TextField(blank=False, null=False, default='', verbose_name=gettext_lazy('Description'))
    photo = models.ImageField(upload_to='authors/covers/profile', blank=True,
                              null=True, verbose_name='Foto de perfil')
    profile_status = models.CharField(choices=(('Público', 'Público'),
                                               ('Privado', 'Privado')),
                                      max_length=8, default='', verbose_name=gettext_lazy('Profile Status'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=False, max_length=255)
    is_active = models.BooleanField(default=False, verbose_name=gettext_lazy('Activated'))

    def save(self, *args, **kwargs):
        self.slug = str(self.username)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)

    class Meta():
        verbose_name_plural = gettext_lazy('User Profile')
        verbose_name = gettext_lazy('User Profile')
