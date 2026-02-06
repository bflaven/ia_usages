/**
 * Theme Customizer enhancements for a better user experience.
 *
 * Contains handlers to make Theme Customizer preview reload changes asynchronously.
 */

/* global wp:true */

(function ($) {
  // Site Title and Description.
  wp.customize('blogname', function (value) {
    value.bind(function (to) {
      $('.site-title a').text(to);
    });
  });

  wp.customize('blogdescription', function (value) {
    value.bind(function (to) {
      $('.site-description').text(to);
    });
  });

  // Background Color
  wp.customize('background_color', function (value) {
    value.bind(function (to) {
      $('body').css('background-color', to);
    });
  });

  // Header text color.
  wp.customize('header_textcolor', function (value) {
    value.bind(function (to) {
      if (to === 'blank') {
        $('.site-title a, .site-description').css({
          'clip': 'rect(1px, 1px, 1px, 1px)',
          'position': 'absolute'
        });
      } else {
        $('.site-title a, .site-description').css({
          'clip': 'auto',
          'position': 'relative'
        });
        $('.site-title a, .site-description').css({
          'color': to
        });
        $('.site-description').css({
          'opacity': 0.7
        });
      }
    });
  });

  // Read More Label
  wp.customize('allium_read_more_label', function (value) {
    value.bind(function (to) {
      $('.more-link').html(to);
    });
  });

  // Copyright Control
  wp.customize('allium_copyright', function (value) {
    value.bind(function (to) {
      $('.credits-blog').html(to);
    });
  });

  // Credit Control
  wp.customize('allium_credit', function (value) {
    value.bind(function (to) {
      if (to === true) {
        $('.credits-designer').css({
          'clip': 'auto',
          'position': 'relative'
        });
      } else {
        $('.credits-designer').css({
          'clip': 'rect(1px, 1px, 1px, 1px)',
          'position': 'absolute'
        });
      }
    });
  });
})(jQuery);
