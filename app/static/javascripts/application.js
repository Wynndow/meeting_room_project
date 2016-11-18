$( document ).ready(function(){

  var place = $( '.hour:nth-child(7)' ).offset().top
  $('body').scrollTop(place);

  $('.Free, .Busy').hover(
    function() {
      $('#header-status').text($( this ).find( 'div:first' ).text());
      $('#header-time').text($( this ).find( 'div:last' ).text())
    }, function() {
      $('#header-status').text('---');
      $('#header-time').text('---');
    }
  )

})
