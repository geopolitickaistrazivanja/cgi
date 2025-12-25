def cart(request):
    """Context processor for shopping cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    from .models import Product, ProductDimension, ProductPattern
    for product_id, cart_data in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            if product.is_in_stock:
                # Handle both old format (just quantity) and new format (dict)
                if isinstance(cart_data, dict):
                    quantity = cart_data.get('quantity', 0)
                    dimension_id = cart_data.get('dimension_id')
                    pattern_id = cart_data.get('pattern_id')
                else:
                    quantity = cart_data
                    dimension_id = None
                    pattern_id = None
                
                if quantity > 0:
                    dimension = None
                    pattern = None
                    if dimension_id:
                        try:
                            dimension = ProductDimension.objects.get(id=dimension_id, product=product)
                        except ProductDimension.DoesNotExist:
                            pass
                    if pattern_id:
                        try:
                            pattern = ProductPattern.objects.get(id=pattern_id, product=product)
                        except ProductPattern.DoesNotExist:
                            pass
                    
                    # Calculate total only if price exists
                    item_total = None
                    if product.current_price is not None:
                        item_total = float(product.current_price) * quantity
                        total += item_total
                    
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'dimension': dimension,
                        'pattern': pattern,
                        'total': item_total,
                    })
        except (Product.DoesNotExist, ValueError):
            continue
    
    return {
        'cart_items': cart_items,
        'cart_total': total,
        'cart_count': sum(item.get('quantity', item) if isinstance(item, dict) else item for item in cart.values()),
    }

