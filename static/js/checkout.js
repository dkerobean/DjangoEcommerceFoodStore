document.addEventListener("DOMContentLoaded", function () {
      // Paystack payment request
   function payWithPaystack() {
      var handler = PaystackPop.setup({
         key: 'pk_test_5d771c071afa4a41656e20bc1780d18fdc05d728', // Replace with your public key
         email: document.getElementById('email-address').value,
         amount: orderTotal.value * 100, // the amount value is multiplied by 100 to convert to the lowest currency unit
         currency: 'USD', // Use GHS for Ghana Cedis or USD for US Dollars
         ref: 'YOUR_REFERENCE', // Replace with a reference you generated
         callback: function (response) {
               // This happens after the payment is completed successfully
               var reference = response.reference;
               alert('Payment complete! Reference: ' + reference);
               // Make an AJAX call to your server with the reference to verify the transaction

               // Now, submit the form programmatically
               paymentForm.submit();
         },
         onClose: function () {
               alert('Transaction was not completed, window closed.');
         },
      });
      handler.openIframe();
   }


   function come(){
      alert('Payment');
   }

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

   console.log("Order total: " + orderTotal.value);
   
});
