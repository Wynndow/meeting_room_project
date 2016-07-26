$( document ).ready(function(){

  $('body').scrollTop(475);

  $('.Free, .Busy').hover(
    function() {
      $('#header-status').text($( this ).find( 'div:first' ).text());
      $('#header-time').text($( this ).find( 'div:last' ).text())
    }, function() {
      $('#header-status').text('');
      $('#header-time').text('');
    }
  )

})
