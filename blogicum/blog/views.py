from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category

POST_PER_PAGE = 5


def index(request):
    sorted_posts = Post.objects.get_published()[:POST_PER_PAGE]
    context = {
        'post_list': sorted_posts
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.get_published(),
        pk=pk,
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = Post.objects.get_published().filter(category=category)

    context = {
        'category': category,
        'post_list': posts
    }
    template_name = 'blog/category.html'
    return render(request, template_name, context)
