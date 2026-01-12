from django.shortcuts import render, get_object_or_404
from .models import Topic, Category


def category_list(request):
    categories = Category.objects.all().order_by('order', 'name')
    context = {
        'categories': categories,
    }
    return render(request, 'topics/category_list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    topics = category.topics.all()
    context = {
        'category': category,
        'topics': topics,
    }
    return render(request, 'topics/category_detail.html', context)


def topic_detail(request, category_slug, slug):
    category = get_object_or_404(Category, slug=category_slug)
    topic = get_object_or_404(Topic, slug=slug, category=category)
    recent_topics = Topic.objects.filter(category=category).exclude(id=topic.id)[:5]
    
    context = {
        'category': category,
        'topic': topic,
        'recent_topics': recent_topics,
    }
    return render(request, 'topics/topic_detail.html', context)
