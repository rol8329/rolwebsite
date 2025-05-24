from django.shortcuts import render, redirect, get_object_or_404

from blog.forms import BasePostForm
from blog.models import BasePost


# Create your views here.
# HTML views (function-based)
def post_list(request):
    posts = BasePost.objects.prefetch_related('postImagePost', 'postVideoPost', 'postAudioPost', 'postFilePost')
    return render(request, 'blog/list_post.html', {'posts': posts})



def post_create(request):
    if request.method == 'POST':
        form = BasePostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('blog:post_list')
    else:
        form = BasePostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def post_update(request, uuid):
    post = get_object_or_404(BasePost, uuid=uuid)
    if request.method == 'POST':
        form = BasePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_list')
    else:
        form = BasePostForm(instance=post)
    return render(request, 'blog/create_post.html', {'form': form})

def post_delete(request, uuid):
    post = get_object_or_404(BasePost, uuid=uuid)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def read_post(request, uuid):
    post = get_object_or_404(BasePost.objects.prefetch_related(
        'postImagePost', 'postVideoPost', 'postAudioPost', 'postFilePost'
    ), uuid=uuid)
    return render(request, 'blog/read_post.html', {'post': post})
