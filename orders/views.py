from django.http import JsonResponse
from .models import Order, ProductInBasket, ProductInOrder
from django.shortcuts import render
from .forms import *
from django.contrib.auth.models import User

def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    data = request.POST
    print("дата из views")
    print(data)
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, is_active=True, defaults={"nmb": nmb})
        if not created:
            print("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    # #common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)

def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    form = CheckoutContactForm(request.POST or None)

    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("valid")
            data = request.POST

            name = data.get("name")
            phone = data.get("phone")
            email = data.get("email")
            user, created = User.objects.get_or_create(username=email, defaults={"first_name": name, "last_name": phone})

            order = Order.objects.create(
                user=user,
                customer_name=name,
                customer_email=email,
                customer_phone=phone,
                customer_address="blank", #доделать
                comments="blank",#доделать
                total_price=0, #????
                status_id=1
            )

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    products_in_basket_id = name.split("product_in_basket_")[1] #тут будут появляться id товаров из products_in_basket
                    print(products_in_basket_id)
                    product_in_basket = ProductInBasket.objects.get(id=products_in_basket_id) # по id выбираем элемент из корзины
                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(
                        product=product_in_basket.product,
                        nmb=product_in_basket.nmb,
                        price_per_item=product_in_basket.price_per_item,
                        amount=product_in_basket.amount,#is_active автоматом в True
                        order=order
                    ) #добавляем в заказ

        else:
            print("not_valid")
    return render(request, 'orders/checkout.html', locals())