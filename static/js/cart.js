// const productPrice = document.querySelectorAll(".cart-price");
// var productQuantity = document.querySelectorAll(".cart-quantity");
// var subTotals = document.querySelectorAll(".cart-subtotal");
// var total = 0;
// var totalPrice = document.getElementById("total-price");
// var subtotal = document.getElementById('sub-total');

// for (var i = 0; i < productQuantity.length; i++) {

//     const quantity = parseInt(productQuantity[i].textContent);
//     const price = parseFloat(productPrice[i].textContent.slice(1));

//     const subtotalValue = price * quantity;
//     subTotals[i].textContent = `$${subtotalValue.toFixed(2)}`;

//     total += subtotalValue;
//     totalPrice.textContent = "$" + total;
//     subtotal.textContent = "$" + total;
    
// }




// function updateCart() {
//     var inputQuantity = document.querySelectorAll(".input-quantity");

//     for (var i = 0; i < productQuantity.length; i++) {

//     const quantity = parseInt(inputQuantity[i].value);
//     const price = parseFloat(productPrice[i].textContent.slice(1));


//     const subtotalValue = price * quantity;
//     subTotals[i].textContent = `$${subtotalValue.toFixed(2)}`;

//     total += subtotalValue;
//     totalPrice.textContent = "$" + total;
//     subtotal.textContent = "$" + total;
    
// }
// }


// Your code here
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

    function updateCart() {
      var inputQuantity = document.querySelectorAll(".input-quantity");

      for (var i = 0; i < productQuantity.length; i++) {

        const quantity = parseInt(inputQuantity[i].value);
        const price = parseFloat(productPrice[i].textContent.slice(1));

        const subtotalValue = price * quantity;
        subTotals[i].textContent = `$${subtotalValue.toFixed(2)}`;

        total += subtotalValue;
        totalPrice.textContent = "$" + total;
        subtotal.textContent = "$" + total;
        
      }
    }

    // Store the total price in local storage
    localStorage.setItem("totalPrice", totalPrice.textContent);

    // Store the input quantities in local storage as an array
    var inputQuantity = document.querySelectorAll(".input-quantity");
    var quantityArray = [];
    for (var i = 0; i < inputQuantity.length; i++) {
      quantityArray.push(inputQuantity[i].value);
    }
    localStorage.setItem("quantityArray", JSON.stringify(quantityArray));

    // Get the total price from local storage
    var storedTotalPrice = localStorage.getItem("totalPrice");
    if (storedTotalPrice) {
      // Update the UI with the stored total price
      totalPrice.textContent = storedTotalPrice;
      subtotal.textContent = storedTotalPrice;
    }

    // Get the input quantities from local storage as an array
    var storedQuantityArray = JSON.parse(localStorage.getItem("quantityArray"));
    if (storedQuantityArray) {
      // Update the UI with the stored input quantities
      var inputQuantity = document.querySelectorAll(".input-quantity");
      for (var i = 0; i < inputQuantity.length; i++) {
        inputQuantity[i].value = storedQuantityArray[i];
        // Update the subtotals and total accordingly
        updateCart();
      }
    }













