

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function getAmount(product_id){
  amount = $(`#${product_id}_amount`).val();
  // alert(amount);
  if(amount < 1)
    return 1
  return amount;
}

function AddToBasket(product_id, basket_id, calculate=false){
  // alert(getAmount(product_id));
  $.ajax({
      type: 'POST',
      async: true,
      url: '/ajax/basket-control/',
      data: {
        'type' : 'add',
        'product_id' : product_id,
        'basket_id' : basket_id,
        'amount' : getAmount(product_id),
        // "X-CSRFToken": csrftoken,
      },
      // data: `type=add&product_id=${product_id}&basket_id=${basket_id}&"X-CSRFToken"=${csrftoken};`,
      success: function(data, status) {
              $(`#add_${product_id}`).hide();
              $(`#delete_${product_id}`).show();
              $(`#${product_id}_amount_div`).hide();

              if(calculate){
                setNewCommonPrice(basket_id);
              }
            // alert('loool');
      },
      // statusCode: {
      //     401: function() {
      //       window.location.pathname = data['login_url'];
      //       alert(401)''
      //     }
      //   },
      error: function(data, status) {
        if(data.status == 401){
                    // console.log(data);
          // $('#login-button').click();
          modalDisplay();
          // window.location.pathname = data.responseJSON['login_url'];

        }
        else if(data.status != 500){
        alert('Error');
        }
        // else{
        //   alert('Error');
          // console.log(data);
        // }
     },
      dataType: 'json',
    });
}

function setNewCommonPrice(basket_id){
  $.ajax({
      type: 'GET',
      async: true,
      url: '/ajax/get-new-common-price',
      data: {
        'basket_id' : basket_id,
      },
      success: function(data) {
            var new_common_price = data['common_price'];
            // alert(new_common_price);
            $('#common_price').val(new_common_price)
      },
      error: function(data, status) {
      alert('Error');
     },
      dataType: 'json',
    });
}

function removeFromBasket(product_id, basket_id, calculate=false){
  $.ajax({
      type: 'POST',
      async: true,
      url: '/ajax/basket-control/',
      data: {
        'type' : 'delete',
        'product_id' : product_id,
        'basket_id' : basket_id,
        // "X-CSRFToken": csrftoken,
      },
      // data: `type=add&product_id=${product_id}&basket_id=${basket_id}&"X-CSRFToken"=${csrftoken};`,
      success: function(data) {
            $(`#delete_${product_id}`).hide();
            $(`#add_${product_id}`).show();
            $(`#${product_id}_amount_div`).show();

            if(calculate){
              setNewCommonPrice(basket_id);
            }
            // alert('loool');
      },
      error: function(data, status) {
      if(data.status != 500){
      alert('Error');
      }
     },
      dataType: 'json',
    });
}

// function deleteOrder(basket_id){
//   $.ajax({
//       type: 'DELETE',
//       async: true,
//       url: '/ajax/basket-control/',
//       data: {
//         'type' : 'delete',
//         'product_id' : product_id,
//         'basket_id' : basket_id,
//         // "X-CSRFToken": csrftoken,
//       },
//       // data: `type=add&product_id=${product_id}&basket_id=${basket_id}&"X-CSRFToken"=${csrftoken};`,
//       success: function(data) {
//             $(`#delete_${product_id}`).hide();
//             $(`#add_${product_id}`).show();
//             $(`#${product_id}_amount_div`).show();
//             // alert('loool');
//       },
//       error: function(data, status) {
//       alert('Error');
//      },
//       dataType: 'json',
//     });
// }
