from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Product, Category


def shop(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search', '').strip()
    
    products = Product.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        category = None
    
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(sku__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'search_query': search_query,
    }
    return render(request, 'shop/shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Prepare all product images (thumbnail + gallery) for carousel
    product_images = []
    if product.thumbnail:
        product_images.append({
            'url': product.thumbnail.url,
            'alt': product.title,
            'type': 'thumbnail'
        })
    for img in product.images.all():
        product_images.append({
            'url': img.image.url,
            'alt': img.alt_text or product.title,
            'type': 'gallery'
        })
    
    context = {
        'product': product,
        'related_products': related_products,
        'product_images': product_images,
    }
    return render(request, 'shop/product_detail.html', context)


@require_http_methods(["POST"])
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    if not product.is_in_stock:
        return JsonResponse({'success': False, 'message': _('Proizvod nije na stanju.')})
    
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))
    
    if product.stock_type == 'limited' and product.stock_quantity:
        current_quantity = cart.get(str(product_id), 0)
        if current_quantity + quantity > product.stock_quantity:
            return JsonResponse({
                'success': False,
                'message': _('Nema dovoljno proizvoda na stanju.')
            })
    
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    request.session['cart'] = cart
    request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'message': _('Proizvod je dodat u korpu.'),
        'cart_count': sum(cart.values())
    })


@require_http_methods(["POST"])
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')


@require_http_methods(["POST"])
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 0))
    
    if quantity <= 0:
        if str(product_id) in cart:
            del cart[str(product_id)]
    else:
        product = get_object_or_404(Product, id=product_id, is_active=True)
        if product.stock_type == 'limited' and product.stock_quantity:
            if quantity > product.stock_quantity:
                messages.error(request, _('Nema dovoljno proizvoda na stanju.'))
                return redirect('cart')
        cart[str(product_id)] = quantity
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


def cart_view(request):
    return render(request, 'shop/cart.html')


def search_products(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'products': []})
    
    products = Product.objects.filter(
        Q(title__icontains=query) |
        Q(short_description__icontains=query) |
        Q(sku__icontains=query),
        is_active=True
    )[:10]
    
    results = []
    for p in products:
        image_url = ''
        if p.thumbnail:
            image_url = p.thumbnail.url
        elif p.images.first():
            image_url = p.images.first().image.url
        
        results.append({
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'price': str(p.current_price),
            'image': image_url,
        })
    
    return JsonResponse({'products': results})
