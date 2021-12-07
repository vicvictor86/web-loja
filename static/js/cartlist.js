function AddQuantityInput(price_product, product_id) {
    //Adiciona de forma dinâmica o local para modificar a quantidade de produtos desejados
    h = product_id;
    var form = document.getElementById("price_form" + h);
    var label = document.createElement("LABEL");
    var div = document.createElement("div");

    var unit_for_buying = document.createElement("b");
    var input_price = document.createElement("INPUT");
    var input_quantity = document.createElement("INPUT");

    label.setAttribute("for", "file");
    unit_for_buying.innerText = "Unidades para compra";
    unit_for_buying.setAttribute("style", "margin-right: 8px");

    input_price.setAttribute("type", "text");
    input_price.setAttribute("id", "product_price" + h);
    input_price.setAttribute("name", "product_price" + h);
    input_price.setAttribute("hidden", " ");
    input_price.setAttribute("value", price_product);

    input_quantity.setAttribute("type", "number");
    input_quantity.setAttribute("id", "product_quantity" + h);
    input_quantity.setAttribute("min", "1");
    input_quantity.setAttribute("value", "1");
    input_quantity.setAttribute("class", "form-control");
    input_quantity.setAttribute("name", "product_quantity" + h);
    input_quantity.setAttribute("required", "");
    //input_quantity.setAttribute("onblur", "PriceProduct(" + product_id + ")");

    div.setAttribute("id", "ref" + h);
    div.setAttribute("name", "ref" + h);

    form.appendChild(div);
    label.appendChild(unit_for_buying);

    div.appendChild(label);
    div.appendChild(input_price);
    div.appendChild(input_quantity);
}

function ValueDefaultResult(price_product, product_id) {
    //Chamado no loading da página, tem a função de fazer a primeira atualização dos preços totais dos produtos
    document.getElementById("result" + product_id).innerHTML =
        "R$" + price_product;
}

function PriceProduct(product_id) {
    //Atualiza o valor do produto ao multiplicar-se com a quantidade de produtos que serão comprados
    price_formatted = document.getElementById("product_price" + product_id).value;
    price_formatted = price_formatted.replace(",", ".");

    product_price = parseFloat(price_formatted);
    product_quantity = parseFloat(
        document.getElementById("product_quantity" + product_id).value
    );

    result = product_price * product_quantity;
    if (isNaN(result)) {
        result = product_price;
    }

    document.getElementById("result" + product_id).innerHTML = "R$" + result;
}

var listIds = [];
function AddListId(product_id) {
    //Pega os id dos produtos existentes no carrinho
    listIds.push(product_id);
}

function GetListResults() {
    //Pega os valores individuais de cada produto dependendo de sua quantidade
    var listInput = [];
    var listResults = [];
    listIds.forEach((id) => {
        //O PriceProduct aqui tem a função de atualizar as informações antes de coletá-las
        PriceProduct(id);
        listInput.push(document.getElementById("product_quantity" + id));
        value_result = document.getElementById("result" + id).textContent;
        value_result = value_result.replace(",", ".");
        value_result = value_result.replace("R$", "");
        console.log(value_result);
        value_result = parseFloat(value_result);

        listResults.push(value_result);
    });

    return [listResults, listInput];
}

function VerifyChange() {
    //Muda o valor total, vindo da soma dos valores parciais dos produtos dos carrinhos
    var informations = GetListResults();
    var listResults = informations[0];
    var listInput = informations[1];

    listInput.forEach((input) => {
        input.addEventListener("change", (event) => {
            informations = GetListResults();
            listResults = informations[0];
            listInput = informations[1];
            var totalPrice = 0.0;
            listResults.forEach((result) => {
                totalPrice += result;
            });

            const result = document.getElementById("total_result");
            result.textContent = totalPrice;
        });
    });
}
