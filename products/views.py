from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from products.models import Cart_Products, Products

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
        quantity = request.POST['quantity']
        product_resume = request.POST['product_resume']
        comment1 = request.POST['comment1']
        comment2 = request.POST['comment2']
        product_information = request.POST['product_information']
        reasons_to_buy = get_reasons_to_buy(request)
        if reasons_to_buy == '':
            return render(request, 'products/create-product.html')
        photo = request.FILES['photo']

        product = Products.objects.create(
            product_owner = product_owner,
            name = name,
            description = description,
            price = price,
            quantity= quantity,
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
        prod.quantity = request.POST['quantity']
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

def buy_product(request, product_id, quantity = 1):
    product = get_object_or_404(Products, pk=product_id)
    if request.method == "POST":
        quantity = str(request.POST['product_quantity'+str(product_id)])
    format_price(product)
    data = {
        'product': product,
        'quantity': quantity
    }
    return render(request, 'products/buy-product.html', data)

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

def confirmed_purchase(request, product_id, user_id):
    """Faz a compra do produto, fazendo a transferência entre vendedor e comprador e mudando o dono do produto"""
    product = Products.objects.get(pk=product_id)
    buyer = User.objects.get(pk=user_id)
    seller = User.objects.get(pk=product.product_owner_id)
    if request.method == "POST":
        buy_quantity = int(request.POST['buy_quantity'])

    if product.product_owner_id == user_id:
        messages.error(request, "Você já é dono do produto.")
        return redirect('buy_product', product_id, buy_quantity)
    if buyer.client.fund < product.price:
        messages.error(request, "Você não possui dinheiro suficiente para comprar esse produto.")
        return redirect('buy_product', product_id, buy_quantity)
    if product.sold:
        messages.error(request, "Esse produto já foi vendido.")
        return redirect('buy_product', product_id, buy_quantity)
    if product.quantity < buy_quantity:
        messages.error(request, "Você está tentando comprar uma quantidade maior do que a disponível.")
        return redirect('buy_product', product_id, buy_quantity)

    #transferência
    buyer.client.fund -= product.price
    seller.client.fund += product.price
    product.quantity -= buy_quantity

    #mudança de dono
    product.product_owner_id = user_id
    #Todos os produtos vendidos
    if product.quantity == 0:
        product.sold = True
    
    #Deleta o produto do carrinho de compras
    cart_product = Cart_Products.objects.filter(buyer_id=user_id, product_id=product_id)
    if cart_product:
        cart_product.delete()

    #salva no banco de dados
    buyer.client.save()
    seller.client.save()
    product.save()

    #menssagem de sucesso de compra
    return redirect('index')

def cancel_purchase(request, product_id):
    return redirect('product_page', product_id)

def add_cart(request, product_id, user_id):
    """Adiciona um produto no carrinho do usuário, caso já não exista"""
    if user_id == Products.objects.get(id=product_id).product_owner_id:
        messages.error(request, "O produto que quer adicionar já é seu.")
        return redirect('product_page', product_id)
    if Cart_Products.objects.filter(buyer_id=user_id, product_id=product_id):
        messages.error(request, "O produto já existe no seu carrinho")
        return redirect('product_page', product_id)
    Cart_Products.objects.create(buyer_id=user_id, product_id=product_id)
    return redirect('products_in_cart', user_id)

def products_in_cart(request, user_id):
    """Pega os produtos salvos na lista de carrinhos e busca na tabela de produtos as informações daqueles produtos"""
    products_cart = Cart_Products.objects.filter(buyer_id=user_id)
    
    product_sequence = {}
    products = []
    counter = 0
    for product in products_cart:
        actual_product = Products.objects.get(id=product.product_id)
        format_product_name(actual_product)
        format_price(actual_product)

        products.append(actual_product)
        product_sequence[actual_product.id] = counter
        counter += 1

    data = {
        'products':products,
        'sequence':product_sequence
    }

    return render(request, 'products/cart-list.html', data)

def delete_cart_product(request, user_id, product_id):
    """Deleta um produto do carrinho do usuário"""
    product = Cart_Products.objects.filter(buyer_id=user_id, product_id=product_id)
    product.delete()
    return redirect('products_in_cart', user_id)

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
