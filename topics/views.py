from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import translation
from .models import Topic, Category


def category_list(request):
    categories = Category.objects.all().order_by('order', 'name')
    context = {
        'categories': categories,
    }
    return render(request, 'topics/category_list.html', context)


def category_detail(request, slug):
    # Look up category by any of the three slugs
    from django.utils import translation
    lang = translation.get_language()
    
    if lang == 'sr-cyrl':
        category = get_object_or_404(
            Category.objects.filter(Q(slug_sr_cyrl=slug) | Q(slug=slug))
        )
    elif lang == 'en':
        category = get_object_or_404(
            Category.objects.filter(Q(slug_en=slug) | Q(slug=slug))
        )
    else:
        category = get_object_or_404(
            Category.objects.filter(Q(slug=slug) | Q(slug_sr_cyrl=slug) | Q(slug_en=slug))
        )
    
    topics = category.topics.all()
    context = {
        'category': category,
        'topics': topics,
    }
    return render(request, 'topics/category_detail.html', context)


def topic_detail(request, category_slug, slug):
    # Look up category by any of the three slugs
    from django.utils import translation
    lang = translation.get_language()
    
    if lang == 'sr-cyrl':
        category = get_object_or_404(
            Category.objects.filter(Q(slug_sr_cyrl=category_slug) | Q(slug=category_slug))
        )
    elif lang == 'en':
        category = get_object_or_404(
            Category.objects.filter(Q(slug_en=category_slug) | Q(slug=category_slug))
        )
    else:
        category = get_object_or_404(
            Category.objects.filter(Q(slug=category_slug) | Q(slug_sr_cyrl=category_slug) | Q(slug_en=category_slug))
        )
    
    # Look up topic by any of the three slugs
    if lang == 'sr-cyrl':
        topic = get_object_or_404(
            Topic.objects.filter(Q(slug_sr_cyrl=slug) | Q(slug=slug), category=category)
        )
    elif lang == 'en':
        topic = get_object_or_404(
            Topic.objects.filter(Q(slug_en=slug) | Q(slug=slug), category=category)
        )
    else:
        topic = get_object_or_404(
            Topic.objects.filter(Q(slug=slug) | Q(slug_sr_cyrl=slug) | Q(slug_en=slug), category=category)
        )
    
    recent_topics = Topic.objects.filter(category=category).exclude(id=topic.id)[:5]
    
    context = {
        'category': category,
        'topic': topic,
        'recent_topics': recent_topics,
    }
    return render(request, 'topics/topic_detail.html', context)
