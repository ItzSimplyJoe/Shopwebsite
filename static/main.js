$(document).ready(function() {
  $('.add-to-cart-button').click(function() {
      var cartCount = parseInt($('.cart-count').text());
      $('.cart-count').text(cartCount + 1);
      $('#popup').show();
  });
  $('#popup-close-button').click(function() {
      $('#popup').hide();
  });
});

