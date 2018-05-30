$(window).load(function(){

  var place = $( '.hour:nth-child(5)' ).offset().top
  $(window).scrollTop(place);

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
