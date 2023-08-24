const productPrice = document.querySelectorAll(".cart-price");
var productQuantity = document.querySelectorAll(".cart-quantity");
var subTotals = document.querySelectorAll(".cart-subtotal");
var total = 0;
var totalPrice = document.getElementById("total-price");
var subtotal = document.getElementById('sub-total');

for (var i = 0; i < productQuantity.length; i++) {

    const quantity = parseInt(productQuantity[i].textContent);
    const price = parseFloat(productPrice[i].textContent.slice(1));

    const subtotalValue = price * quantity;
    subTotals[i].textContent = `$${subtotalValue.toFixed(2)}`;

    total += subtotalValue;
    totalPrice.textContent = "$" + total;
    subtotal.textContent = "$" + total;
    
}


const inputQuantity = document.querySelectorAll(".input-quantity"); 

function updateCart(q) {
    for (var i = 0; i < productQuantity.length; i++) {

    productQuantity.textContent = "$" + q
    const quantity = parseInt(productQuantity[i].textContent);
    const price = parseFloat(productPrice[i].textContent.slice(1));

    const subtotalValue = price * quantity;
    subTotals[i].textContent = `$${subtotalValue.toFixed(2)}`;

    total += subtotalValue;
    totalPrice.textContent = "$" + total;
    subtotal.textContent = "$" + total;
    
    }
}







