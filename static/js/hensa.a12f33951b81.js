$(function() {
  // Handler for .ready() called.
  $('.carousel.carousel-slider').carousel({fullWidth: false});
  $('.modal').modal();
  $('.slider').slider();
      // Detect touch screen and enable scrollbar if necessary
    function is_touch_device() {
      try {
        document.createEvent("TouchEvent");
        return true;
      } catch (e) {
        return false;
      }
    }
    if (is_touch_device()) {
      $('#nav-mobile').css({ overflow: 'auto'});
    }
});
document.addEventListener("DOMContentLoaded", function(){
  $('.preloader-background').delay(1000).fadeOut('fast');
  
  $('.preloader-wrapper')
    .delay(1000)
    .fadeOut('fast');
});