from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Product


def shop(request):
    search_query = request.GET.get('search', '').strip()
    
    products = Product.objects.filter(is_active=True)
    
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(sku__icontains=search_query)
        )
    
    context = {
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'shop/shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
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
    
    # Get selected dimension and pattern
    dimension_id = request.POST.get('dimension_id', '')
    pattern_id = request.POST.get('pattern_id', '')
    
    # Validate dimension if product has dimensions
    if product.dimensions.exists():
        if not dimension_id:
            return JsonResponse({'success': False, 'message': _('Molimo izaberite dimenzije.')})
        try:
            dimension = product.dimensions.get(id=dimension_id)
            # Price is now mandatory - dimension must have a price
            if not dimension.price:
                return JsonResponse({'success': False, 'message': _('Izabrane dimenzije nemaju cenu. Molimo izaberite druge dimenzije.')})
        except:
            return JsonResponse({'success': False, 'message': _('Neispravne dimenzije.')})
    else:
        dimension_id = None
    
    # Validate pattern if product has patterns
    if product.patterns.exists():
        if not pattern_id:
            return JsonResponse({'success': False, 'message': _('Molimo izaberite dezen.')})
        try:
            pattern = product.patterns.get(id=pattern_id)
        except:
            return JsonResponse({'success': False, 'message': _('Neispravan dezen.')})
    else:
        pattern_id = None
    
    if product.stock_type == 'limited' and product.stock_quantity:
        current_quantity = cart.get(str(product_id), {}).get('quantity', 0) if isinstance(cart.get(str(product_id)), dict) else (cart.get(str(product_id), 0) if isinstance(cart.get(str(product_id)), (int, str)) else 0)
        if isinstance(current_quantity, str):
            current_quantity = int(current_quantity)
        if current_quantity + quantity > product.stock_quantity:
            return JsonResponse({
                'success': False,
                'message': _('Nema dovoljno proizvoda na stanju.')
            })
    
    # Store cart item with dimension and pattern
    # Use composite key: product_id_dimension_id_pattern_id to allow multiple variations
    cart_key = f"{product_id}_{dimension_id or 'none'}_{pattern_id or 'none'}"
    
    if cart_key not in cart or not isinstance(cart[cart_key], dict):
        cart[cart_key] = {
            'quantity': 0,
            'dimension_id': dimension_id,
            'pattern_id': pattern_id,
            'product_id': product_id  # Store product_id for reference
        }
    
    cart[cart_key]['quantity'] = cart[cart_key].get('quantity', 0) + quantity
    cart[cart_key]['dimension_id'] = dimension_id
    cart[cart_key]['pattern_id'] = pattern_id
    
    request.session['cart'] = cart
    request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'message': _('Proizvod je dodat u korpu.'),
        'cart_count': len(cart)  # Count number of unique items
    })


@require_http_methods(["POST"])
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    # Get cart_key from POST data if available (for composite keys)
    cart_key = request.POST.get('cart_key', '')
    
    if cart_key and cart_key in cart:
        # Remove specific cart item by composite key
        del cart[cart_key]
    else:
        # Fallback: remove all cart items for this product (handle both old and new key formats)
        keys_to_remove = []
        for key in cart.keys():
            if isinstance(key, str):
                # New format: product_id_dimension_id_pattern_id
                if key.startswith(f"{product_id}_"):
                    keys_to_remove.append(key)
                # Old format: just product_id
                elif key == str(product_id):
                    keys_to_remove.append(key)
            elif key == product_id:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del cart[key]
    
    request.session['cart'] = cart
    request.session.modified = True
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from .context_processors import cart as cart_processor
        cart_context = cart_processor(request)
        return JsonResponse({
            'success': True,
            'cart_count': cart_context['cart_count'],
            'cart_total': float(cart_context['cart_total']) if cart_context['cart_total'] else 0
        })
    
    return redirect('shop:cart')


@require_http_methods(["POST"])
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 0))
    dimension_id = request.POST.get('dimension_id', '')
    pattern_id = request.POST.get('pattern_id', '')
    
    # Use composite key to find the exact cart item
    cart_key = f"{product_id}_{dimension_id or 'none'}_{pattern_id or 'none'}"
    
    if quantity <= 0:
        if cart_key in cart:
            del cart[cart_key]
    else:
        product = get_object_or_404(Product, id=product_id, is_active=True)
        if product.stock_type == 'limited' and product.stock_quantity:
            if quantity > product.stock_quantity:
                messages.error(request, _('Nema dovoljno proizvoda na stanju.'))
                return redirect('shop:cart')
        
        if cart_key not in cart:
            cart[cart_key] = {
                'quantity': 0,
                'dimension_id': dimension_id if dimension_id else None,
                'pattern_id': pattern_id if pattern_id else None,
                'product_id': product_id
            }
        
        cart[cart_key]['quantity'] = quantity
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('shop:cart')


def cart_view(request):
    from .context_processors import cart
    cart_context = cart(request)
    return render(request, 'shop/cart.html', cart_context)


def cart_dropdown(request):
    """Return cart items as JSON for dropdown"""
    from .context_processors import cart
    cart_context = cart(request)
    
    items = []
    for item in cart_context['cart_items']:
        image_url = ''
        if item['product'].thumbnail:
            image_url = item['product'].thumbnail.url
        elif item['product'].images.first():
            image_url = item['product'].images.first().image.url
        
        # Get price from dimension (price is now mandatory) - format with thousands separator
        price_display = "Izaberite opcije"
        if item.get('dimension') and item['dimension'].price:
            price_num = int(float(item['dimension'].price))
            price_display = f"{price_num:,} RSD"
        
        items.append({
            'product_id': item['product'].id,
            'title': item['product'].title,
            'quantity': item['quantity'],
            'price': price_display,
            'image': request.build_absolute_uri(image_url) if image_url else ''
        })
    
    total_num = int(cart_context['cart_total']) if cart_context['cart_total'] else 0
    total_display = f"{total_num:,} RSD"
    
    return JsonResponse({
        'items': items,
        'total': total_display,
        'cart_count': cart_context['cart_count']
    })


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
            image_url = request.build_absolute_uri(p.thumbnail.url)
        elif p.images.first():
            image_url = request.build_absolute_uri(p.images.first().image.url)
        
        # Price is now per dimension, so show "Izaberite opcije"
        results.append({
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'price': 'Izaberite opcije',
            'image': image_url,
        })
    
    return JsonResponse({'products': results})


@require_http_methods(["GET", "POST"])
def checkout(request):
    from .context_processors import cart
    from accounts.models import Order, OrderItem
    from django.core.mail import send_mail
    from django.conf import settings
    from .models import ProductDimension, ProductPattern
    
    cart_context = cart(request)
    cart_items = cart_context.get('cart_items', [])
    
    if not cart_items:
        messages.error(request, _('Vaša korpa je prazna.'))
        return redirect('shop:cart')
    
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        
        # Validate required fields
        if not all([email, first_name, last_name, phone, address, city, postal_code]):
            messages.error(request, _('Molimo popunite sva polja.'))
            return render(request, 'shop/checkout.html', cart_context)
        
        # Archive email (if not already archived)
        from core.models import UserEmail
        UserEmail.objects.get_or_create(
            email=email,
            defaults={'source': 'checkout'}
        )
        
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            city=city,
            postal_code=postal_code,
            total_amount=cart_context['cart_total'] if cart_context['cart_total'] else 0
        )
        
        # Create order items with dimensions and patterns
        order_items_html = []
        request_scheme = 'https' if request.is_secure() else 'http'
        request_host = request.get_host()
        
        for item in cart_items:
            dimension = item.get('dimension')
            pattern = item.get('pattern')
            
            # Get price from dimension (price is now mandatory) - format with thousands separator
            item_price = None
            price_display = "Izaberite opcije"
            if dimension and dimension.price:
                item_price = dimension.price
                price_num = int(float(item_price))
                price_display = f"{price_num:,} RSD"
            
            order_item = OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item_price,
                selected_dimension=dimension,
                selected_pattern=pattern
            )
            
            # Build order item HTML for email
            item_html = f"""
            <div style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px;">
                <h3 style="margin-top: 0;">{item['product'].title} x {item['quantity']} - {price_display}</h3>
            """
            if dimension:
                item_html += f'<p><strong>Dimenzije:</strong> {dimension.get_display()}</p>'
            if pattern:
                pattern_image_url = f"{request_scheme}://{request_host}{pattern.image.url}"
                item_html += f'<p><strong>Dezen:</strong></p><img src="{pattern_image_url}" alt="Dezen" style="max-width: 200px; border: 1px solid #ddd; border-radius: 4px; margin-top: 5px;">'
            item_html += "</div>"
            order_items_html.append(item_html)
        
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        # Build HTML email for admin
        admin_email_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>Nova porudžbina #{order.id}</h2>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <h3>Kupac:</h3>
                <p><strong>Ime:</strong> {first_name} {last_name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Telefon:</strong> {phone}</p>
                <p><strong>Adresa:</strong> {address}</p>
                <p><strong>Grad:</strong> {city}</p>
                <p><strong>Poštanski broj:</strong> {postal_code}</p>
            </div>
            
            <h3>Stavke:</h3>
            {''.join(order_items_html)}
            
            <div style="margin-top: 20px; padding: 15px; background-color: #f5f5f5; border-radius: 5px;">
                <h3 style="margin-top: 0;">Ukupan iznos: {order.total_amount} RSD</h3>
            </div>
        </body>
        </html>
        """
        
        admin_email_text = f"""
Nova porudžbina #{order.id}

Kupac:
Ime: {first_name} {last_name}
Email: {email}
Telefon: {phone}
Adresa: {address}
Grad: {city}
Poštanski broj: {postal_code}

Broj porudžbine: #{order.id}
Ukupan iznos: {order.total_amount} RSD
"""
        
        try:
            send_mail(
                subject=f'Nova porudžbina #{order.id}',
                message=admin_email_text,
                html_message=admin_email_html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            pass
        
        # Build HTML email for customer
        customer_email_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>Poštovani/a {first_name} {last_name},</h2>
            
            <p>Hvala vam na porudžbini!</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p><strong>Broj porudžbine:</strong> #{order.id}</p>
            </div>
            
            <h3>Stavke:</h3>
            {''.join(order_items_html)}
            
            <div style="margin-top: 20px; padding: 15px; background-color: #f5f5f5; border-radius: 5px;">
                <h3 style="margin-top: 0;">Ukupan iznos: {order.total_amount} RSD</h3>
            </div>
            
            <p>Kontaktiraćemo vas uskoro u vezi sa isporukom.</p>
            
            <p>Srdačan pozdrav,<br>EhoLux tim</p>
        </body>
        </html>
        """
        
        customer_email_text = f"""
Poštovani/a {first_name} {last_name},

Hvala vam na porudžbini!

Broj porudžbine: #{order.id}
Ukupan iznos: {order.total_amount} RSD

Kontaktiraćemo vas uskoro u vezi sa isporukom.

Srdačan pozdrav,
EhoLux tim
"""
        
        try:
            send_mail(
                subject=f'Potvrda porudžbine #{order.id}',
                message=customer_email_text,
                html_message=customer_email_html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            pass
        
        messages.success(request, _('Porudžbina je uspešno kreirana!'))
        return redirect('accounts:account')
    
    return render(request, 'shop/checkout.html', cart_context)
