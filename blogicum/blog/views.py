from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
from django.utils import timezone


def index(request):
    now = timezone.now()
    sorted_posts = Post.objects.filter(
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    context = {
        'post_list': sorted_posts
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    now = timezone.now()
    post = get_object_or_404(
        Post,
        pk=pk,
        is_published=True,
        pub_date__lte=now,
        category__is_published=True
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, slug):
    now = timezone.now()
    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = category.post_set.filter(
        is_published=True,
        pub_date__lte=now,
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': posts
    }
    template_name = 'blog/category.html'
    return render(request, template_name, context)
