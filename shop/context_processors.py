def cart(request):
    """Context processor for shopping cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    from .models import Product
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            if product.is_in_stock:
                item_total = float(product.current_price) * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total,
                })
                total += item_total
        except Product.DoesNotExist:
            continue
    
    return {
        'cart_items': cart_items,
        'cart_total': total,
        'cart_count': sum(cart.values()),
    }

