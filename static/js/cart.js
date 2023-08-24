const productPrice = document.querySelectorAll(".cart-price");
const productQuantity = document.querySelectorAll(".cart-quantity");
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




// changeQuantity = document.querySelectorAll(".change-quantity");

// changeQuantity.forEach(quant => {
//     console.log(quant.textContent);
// });







