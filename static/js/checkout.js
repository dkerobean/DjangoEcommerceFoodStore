var productQuantity = document.querySelectorAll('.item-quantity');
var productPrice = document.querySelectorAll('.item-total');
var productTotal = document.getElementById("item-total");

var total = 0; 

for (var i = 0; i < productQuantity.length; i++) {
   total += parseFloat(productQuantity[i].textContent) * parseFloat(productPrice[i].textContent.slice(1));
}

productTotal.textContent = "$" + total.toFixed(2); 