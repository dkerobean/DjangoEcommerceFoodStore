from .models import Cart


def cart_items(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = cart.cartitem_set.all()
        return {'cart_items': cart_items}
    return {'cart_items': []}
