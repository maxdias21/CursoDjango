from django.shortcuts import redirect, reverse
from community.models import Community
from django.contrib import messages
from django.views import View


class DeleteCommunityPost(View):
    def dispatch(self, request, *args, **kwargs):
        if self.kwargs.get('id'):
            return self.post(request)

    def post(self, request):
        # Pegar dados do site + id para apagar o post
        # id está em um input "hidden"
        id = self.kwargs.get('id')

        # Pegar post
        post = Community.objects.filter(id=id, author=request.user).first()

        # Deletar post
        post.delete()

        messages.success(request, 'Post deletado com sucesso!')
        return redirect(reverse('community:my_posts'))
