def cart(request):
    """Context processor for shopping cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    from .models import Product, ProductDimension, ProductPattern
    for cart_key, cart_data in cart.items():
        try:
            # Handle both old format (product_id as key) and new format (composite key)
            if isinstance(cart_data, dict) and 'product_id' in cart_data:
                product_id = cart_data['product_id']
            else:
                # Old format: key is product_id
                try:
                    product_id = int(cart_key.split('_')[0])
                except (ValueError, IndexError):
                    product_id = int(cart_key)
            
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
                    
                    # Calculate total from dimension price (price is now mandatory)
                    item_total = None
                    item_price = None
                    if dimension and dimension.price:
                        item_price = float(dimension.price)
                        item_total = item_price * quantity
                        total += item_total
                    
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'dimension': dimension,
                        'pattern': pattern,
                        'total': item_total,
                        'price': item_price,
                        'cart_key': cart_key,  # Store cart_key for remove functionality
                    })
        except (Product.DoesNotExist, ValueError):
            continue
    
    return {
        'cart_items': cart_items,
        'cart_total': total,
        'cart_count': len(cart),  # Count number of unique items (products with different dimensions/patterns)
    }

