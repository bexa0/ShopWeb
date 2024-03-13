from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView

from shop.models import Category, Product


def category_list(request):
    category_list = Category.objects.all()
    context = {"category_list": category_list}
    return render(request, 'shop/category_list.html', context)


# def category_detail(request, pk):
#     detail = Category.objects.filter(pk=pk)
#

class Category_detail(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        products = Product.objects.filter(category=self.object)
        context['products'] = products
        return context


def add_to_cart(request, product_id):
    if not request.session.get('cart'):
        request.session['cart'] = []
    cart = request.session['cart']
    items = [i['product'] for i in cart]
    if product_id in items:
        for i in cart:
            if i['product'] == product_id:
                i['quantity'] += 1
                break
    else:
        cart_item = {
            "product": product_id,
            "quantity": 1
        }
        cart.append(cart_item)

    request.session.modified = True
    product = Product.objects.get(pk=product_id)
    category_id = product.category.pk
    print(cart)
    return redirect('category_detail', category_id)


# def add_to_cart(request, product_id: int) -> None:
#     if "order" not in request.session or not request.session["order"]:
#         request.session["order"] = []
#
#     order_exists = False
#     for item in request.session["order"]:
#         if item["product_id"] == product_id:
#             item["quantity"] += 1
#             order_exists = True
#             print(f"Item {product_id} updated")
#             break
#
#     if not order_exists:
#         request.session["order"].append({"product_id": product_id, "quantity": 1})
#         print(f"Item {product_id} created")
#
#     request.session.modified = True
#
#     print(request.session["order"])
#     # reverse_url = reverse(
#     #     "products", args=(Product.objects.get(id=product_id).category.id,)
#     # )
#     # return redirect(reverse_url)
#     return HttpResponse(f'add to cart {request.session["order"]}')

def cart(request):
    my_cart = request.session.get('cart')
    my_cart_context = []
    for item in my_cart:  # {'product': 1, 'quantity': 8}
        my_cart_item = {}
        my_cart_item['product'] = Product.objects.get(pk=item['product'])
        my_cart_item['quantity'] = item['quantity']
        my_cart_item['total'] = float(my_cart_item['product'].price * my_cart_item['quantity'])
        my_cart_context.append(my_cart_item)

    context = {'cart_items': my_cart_context}
    return render(request, 'shop/cart.html', context)
