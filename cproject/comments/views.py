from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.db import transaction
from django.contrib.auth.models import User

from .models import Post, Comment
from .forms import CommentForm
from .utils import create_comments_tree


def base_view(request):
    comments = Post.objects.first().comments.all()
    result = create_comments_tree(comments)
    comment_form = CommentForm(request.POST or None)
    return render(request, 'base.html', {'comments': result, 'comment_form': comment_form})


def create_comment(request):
    """
    Бизнес-логика для создания комментариев без 'детей', при чем они сами не являются 'детьми'
    """
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.user = request.user
        new_comment.text = comment_form.cleaned_data['text']
        new_comment.content_type = ContentType.objects.get(model='post')
        new_comment.object_id = 1
        new_comment.parent = None
        new_comment.is_child = False
        new_comment.save()
    return HttpResponseRedirect('/post-comments')


@transaction.atomic
def create_child_comment(request):
    """ Функция которая добавляет комментария к другому комментарию """

    user_name = request.POST.get('user')
    current_id = request.Post.get('id')
    text = request.POST.get('text')
    user = User.objects.get(username=user_name)
    content_type = ContentType.objects.get(model='post')
    parent = Comment.objects.get(id=int(current_id))
    is_child = False if not parent else True
    Comment.objects.create(
        user=user, text=text, content_type=content_type, object_id=1,
        parent=parent, is_child=is_child
    )
    comments_ = Post.objects.first().comments.all()
    comments_list = create_comments_tree(comments_)
    return render(request, 'base.html', {'comments': comments_list})