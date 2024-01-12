from . import BASE_DIR

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/sao_paulo'

# Caso não queira traduzir o meu projeto marco isso como False e não preciso criar a variável LOCALE_PATHS
# Remover também no Middleware a parte de tradução
# Tradução feita conforme o idioma do navegador da pessoa
# Comando
# python manage.py makemessages -l "pt_BR" -i 'venv'

# Quando eu fizer alguma alteração de tradução no meu template (usar {% translate 'algo...' %} tenho que jogar o
# comando abaixo python manage.py compilemessages -l "pt_BR" -i 'venv' Instalar o gnu gettext
USE_I18N = True

LOCALE_PATHS = [
    BASE_DIR / 'locale'
]

USE_TZ = True
