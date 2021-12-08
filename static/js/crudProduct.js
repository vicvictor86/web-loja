var CountProds = 1;
function AddInput() {
    if (CountProds <= 10) {
        h = CountProds;
        var form = document.getElementById("divForm");
        var input = document.createElement("INPUT");
        var div = document.createElement("div");

        input.setAttribute("type", "text");
        input.setAttribute("id", "reasons_to_buy" + h);
        input.setAttribute("name", "reasons_to_buy" + h);
        input.setAttribute("required", "");

        div.setAttribute("id", "ref" + h);
        div.setAttribute("name", "ref" + h);
        div.setAttribute("class", "mb-2 ml-2")

        form.appendChild(div)
        div.appendChild(input);
        CountProds++;
    }
}