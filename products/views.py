from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from products.models import Products

def index(request):
    """Leva para a landing-page do site"""
    products = Products.objects.all()
    format_price(products)
    format_product_name(products)

    data = {
        'products' : products
    }
    return render(request, 'index.html', data)

def product_page(request, product_id):
    """Direciona para a página do produto escolhido"""
    product = get_object_or_404(Products, pk=product_id)
    formatted_reasons_to_buy = product.reasons_to_buy.split(",")
    format_price(product)
    data = {
        'product' : product,
        'formatted_reasons': formatted_reasons_to_buy
    }

    return render(request, "products/product-page.html", data)

def create_product(request):
    """Cria um anúncio de produto"""
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

def edit_product(request, product_id):
    """Direciona para a página que irá editar as informações do produtos, passando o produto específico para edição"""
    product = get_object_or_404(Products, pk=product_id)
    product_to_edit = {'product':product}
    return render(request, 'products/edit-product.html', product_to_edit)

def update_product(request):
    """Atualiza as informações do produto"""
    if request.method == 'POST':
        product_id = request.POST['product_id']
        prod = Products.objects.get(pk=product_id)
        prod.name = request.POST['product_name']
        prod.description = request.POST['description']
        prod.price = request.POST['price']
        prod.product_resume = request.POST['product_resume']
        prod.comment1 = request.POST['comment1']
        prod.comment2 = request.POST['comment2']
        prod.product_information = request.POST['product_information']
        if get_reasons_to_buy(request) != '':
            prod.reasons_to_buy = get_reasons_to_buy(request)
        if 'photo' in request.FILES:
            prod.photo = request.FILES['photo']
        prod.save()
        return redirect('product-page/' + str(product_id))

def get_reasons_to_buy(request):
    """Armazena numa string todos os motivos para comprar o produto"""
    i = 1
    all_reasons = ''

    try:
        while request.POST['reasons_to_buy'+str(i)] != '':
            reasons = request.POST['reasons_to_buy'+str(i)]
            all_reasons += reasons + ","      
                     
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