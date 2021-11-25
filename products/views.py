from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from products.models import Products

def index(request):
    products = Products.objects.all()
    format_price(products)
    format_product_name(products)

    data = {
        'products' : products
    }
    return render(request, 'index.html', data)

def product_id(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    format_price(product)
    data = {
        'product' : product
    }

    return render(request, "products/product-page.html", data)

def create_product(request):
    if request.method == 'POST':
        product_owner = get_object_or_404(User, pk=request.user.id)
        name = request.POST['product_name']
        description = request.POST['description']
        price = request.POST['price']
        product_resume = request.POST['product_resume']
        comment1 = request.POST['comment1']
        comment2 = request.POST['comment2']
        product_information = request.POST['product_information']
        reasons_to_buy = get_reasons_to_buy(request)
        if reasons_to_buy == '':
            return render(request, 'products/create-product.html')
        photo = request.FILES['photo']
        print(reasons_to_buy)
        product = Products.objects.create(
            product_owner = product_owner,
            name = name,
            description = description,
            price = price,
            product_resume = product_resume,
            comment1 = comment1,
            comment2 = comment2,
            product_informations = product_information,
            reasons_to_buy = reasons_to_buy,
            photo = photo
        )
        product.save()
        return redirect('index')

    return render(request, 'products/create-product.html')

def get_reasons_to_buy(request):
    """Armazena numa string todos os motivos para comprar o produto"""
    i = 1
    all_reasons = ''

    try:
        while request.POST['reasons_to_buy'+str(i)] != '':
            reasons = request.POST['reasons_to_buy'+str(i)]
            all_reasons += "\n" + reasons      
                     
            i += 1 
    except:
        return all_reasons

def format_price(products):
    """Muda o ponto do número decimal para vírgula para ficar nos padrões brasileiros"""
    if type(products) is Products:
        products = [products]

    for product in products:
        product.price = str(product.price).replace(".", ",")

def format_product_name(products):
    """Não permite que o nome do produto ultrapasse 32 caracteres"""
    if type(products) is Products:
        products = [products]

    for product in products:
        if len(product.name) > 30:
            caracters_to_remove = len(product.name) - 30
            product.name = product.name[:-caracters_to_remove]
            product.name = product.name + "..." 