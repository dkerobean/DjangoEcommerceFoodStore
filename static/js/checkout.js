
var productQuantity = document.querySelectorAll('.item-quantity');
var productPrice = document.querySelectorAll('.item-total');
var productTotal = document.getElementById("item-total");

var total = 0;

for (var i = 0; i < productQuantity.length; i++) {
   total += parseFloat(productQuantity[i].textContent) * parseFloat(productPrice[i].textContent.slice(1));
}

productTotal.textContent = "$" + total.toFixed(2);


// set order total in checkout
var orderTotal = document.getElementById("order-total1");
orderTotal.value = total.toFixed(2);

var ammount = parseFloat(orderTotal.value) * 100

// generate random reference
function generateFunction(){
   var randomNumber = Math.random().toString().slice(2, 12);
   var reference = 'REF-' + randomNumber;

   return reference
}

var randomReference = generateFunction();


// Process Payment using Paystack API
var paymentForm = document.getElementById('paymentForm');
paymentForm.addEventListener('submit', payWithPaystack, false);
function payWithPaystack() {
  var handler = PaystackPop.setup({
    key: 'pk_test_5d771c071afa4a41656e20bc1780d18fdc05d728',
    email: document.getElementById('email-address').value,
    amount: ammount,
    currency: 'GHS',
    ref: randomReference,
    callback: function(response) {
      var reference = response.reference;
      paymentForm.submit();
    },
    onClose: function() {
      toastr.error('Transaction was not completed, window closed.');
    },
  });
  handler.openIframe();
}

