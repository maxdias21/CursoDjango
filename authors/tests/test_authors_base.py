from authors.models import AuthorRegister


class AuthorMixin():
    def create_author(self, username=None, age=22, hometown='Bahia', current_city='Bahia',
                      sex='Masculino', marital_status='Solteiro', phone_number=11111111111,
                      description='Description Test', photo='None', slug='Slug', profile_status='Público',
                      is_active=True):
        return AuthorRegister.objects.create(username=username, age=age, hometown=hometown, current_city=current_city,
                                             sex=sex, marital_status=marital_status, phone_number=phone_number,
                                             description=description, photo=photo, profile_status=profile_status,
                                             is_active=is_active, slug=slug)
