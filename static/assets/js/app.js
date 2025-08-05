var THEMEIM = THEMEIM || {};

(function($) {

  /*!----------------------------------------------
  # This beautiful code written with heart
  # by Sonia Shurmi
  # In Dhaka, BD at the WD IT Solution workstation.
  ---------------------------------------------*/

  // USE STRICT
  "use strict";

  THEMEIM.initialize = {

    init: function() {
      THEMEIM.initialize.general();
      THEMEIM.initialize.mobileMenu();
      THEMEIM.initialize.sectionBackground();
      THEMEIM.initialize.countUp();
      THEMEIM.initialize.countDown();
      THEMEIM.initialize.svg();
      THEMEIM.initialize.owlslider();
      THEMEIM.initialize.slickcarousel();
      THEMEIM.initialize.gmap();
    },

    /*=========================================*/
    /*=           General function         =*/
    /*=========================================*/
    general: function() {
      //page active
      $('.main_menu li a').each(function() {
        if ($(this).attr('href') == location.href.split("/").slice(-1)) {
          $(this).addClass('current_page_item');
        }
      });

      //popup video
      $('.pop-up').magnificPopup({
        type: 'iframe',
        removalDelay: 300
      });

      var $grid = $('.grid').isotope({
        itemSelector: '.grid-item',
        stagger: 30,
      });
      //product detail tablet select
      $('.ingredient_slider_detail .product_quantity li').on('click', function() {
        $('.ingredient_slider_detail .product_quantity li').removeClass('border');
        $(this).addClass('border');
      });

      //quickview popup
      $('.trigger').on('click', function(e) {
        e.preventDefault();
        var mask = '<div class="mask-overlay2">';

        $('.quickview-wrapper').toggleClass('open');
        $(mask).hide().appendTo('body').fadeIn('fast');
        $('.mask-overlay2, .close-qv').on('click', function() {
          $('.quickview-wrapper').removeClass('open');
          $('.mask-overlay2').remove();
        });
      });


      // rangeslider
      $('input[type="range"]').rangeslider({
        polyfill: false
      })

      //key ingredient select code
      var $content = $('.ingredients_key_single_feature');

      function showContent(type) {
        $content.filter('.' + type).show().addClass('active').siblings().removeClass('active');
      }

      $('.ingredients_key_featurs_menu').on('click', '.key_feature_btn', function(e) {
        showContent(e.currentTarget.hash.slice(1));
        e.preventDefault();
        $('.ingredients_key_featurs_menu li a.active').removeClass('active');
        $(this).addClass('active');
      });
      showContent('a');

      //faq page collapsing
      $(".faq_custom_single_post_link").click(function(e) {
        if ($(this).prev().hasClass("faq_custom_single_post_more_text")) {
          $(this).parent(".faq_custom_single_post_container").toggleClass("show-more");
        }
        e.preventDefault();
      });

      //contact input label
      $('.map_two_area_input').on('click', function() {
        $(this).focus().addClass('active').siblings().removeClass('active');
      });

      //cart item increase decrease
      $(".qtyminus").on("click", function() {
        var input = $(this).siblings(".cart__quantity-selector"),
          qty = parseInt(input.val(), 10);
        if (qty > 1) {
          input.val(qty - 1)
        }
      });

      $(".qtyplus").on("click", function() {
        var input = $(this).siblings(".cart__quantity-selector"),
          qty = parseInt(input.val(), 10);
        input.val(qty + 1)
      });

      //back to top
      var backtotop = $(".backtotop");
      $(backtotop).on('click', function() {
        $('html, body').animate({
          scrollTop: 0
        }, 800);
        return false;
      });

      $(window).on('scroll', function() {
        var topPos = $(this).scrollTop();
        if (topPos > 150) {
          $(backtotop).css("opacity", "1");

        } else {
          $(backtotop).css("opacity", "0");
        }
      });

      //map hover
      $(".map_click_me").on('click', function() {
        $(".map_hovarable").toggleClass("slideup");
      });

      //tab with changing icon
      $('.how_it_work_tab_menu').on('click', 'a', function(index) {
        var $this = $(this),
          activedIcon = $($this.attr('data-icon'));
        $('.icon_menu .icon_menu_item').removeClass("active");
        activedIcon.addClass("active");
      });


      //click event for review
      $(".write_scroll_review").on('click', function() {
        var $this = $(this),
          tabNav = $(".product_review_tab .nav li a"),
          tabContent = $(".tab-content .tab-pane"),
          moveTo = $this.attr("data-moveto"),
          href = $(moveTo).attr("href");

        tabNav.removeClass("active show");
        tabContent.removeClass("active show");
        $(moveTo).addClass("active show");
        $(href).addClass("active show");
      });


      //  Twitter Feed
      var config4 = {
        "profile": {
          "screenName": 'imthemedesigner'
        },
        "domId": 'twitter_feed',
        "maxTweets": 2,
        "enableLinks": true,
        "showUser": true,
        "showTime": false,
        "showRetweet": false
      };

      $('#twitter_feed').each(function() {
        twitterFetcher.fetch(config4);
      });

      /* Video Play With Poster */
      $('.youtube-wrapper').on('click', function(event) {
        event.preventDefault();
        var fr = $(this).find('iframe');
        var fadr = $(this).find('iframe').attr('src');
        var fuadr = fadr + '?autoplay=1';

        $(this).toggleClass('reveal');
        fr.attr('src', fuadr);
        console.log(fadr);
      });

      // headroom
      $('#header').each(function() {
        var header = document.querySelector("#header");
        var headroom = new Headroom(header, {
          tolerance: {
            down: 10,
            up: 5
          },
          offset: 126
        });
        headroom.init();
      });

      //aos animation
      if ($(window).width() > 767) {
        AOS.init({
          duration: 1200,
          once: true
        });
      }

      $('.toolbar_right ul li.search').on('click', function() {
        $('.search_detail_two').toggleClass('active');
        $('.search_detail_two_close').on('click', function() {
          $('.search_detail_two').removeClass('active');
        });
      });
    },

    /*=========================================*/
    /*=           Section Background          =*/
    /*=========================================*/
    sectionBackground: function() {
      // Section Background Image
      $('[data-bg-image]').each(function() {
        var img = $(this).data('bg-image');
        $(this).css({
          backgroundImage: 'url(' + img + ')',
        });
      });

      //Parallax Background
      $('[data-parallax="image"]').each(function() {
        var actualHeight = $(this).position().top;
        var speed = $(this).data('parallax-speed');
        var reSize = actualHeight - $(window).scrollTop();
        var makeParallax = -(reSize / 3);
        var posValue = makeParallax + "px";

        $(this).css({
          backgroundPosition: '50% ' + posValue,
        });
      });
    },

    /*==================================*/
    /*=           Mobile Menu          =*/
    /*==================================*/
    mobileMenu: function() {
      var Accordion = function(el, multiple) {
        this.el = el || {};

        this.multiple = multiple || false;

        var dropdownlink = this.el.find('.dropdownlink');
        dropdownlink.on('click', {
            el: this.el,
            multiple: this.multiple
          },
          this.dropdown);
      };

      Accordion.prototype.dropdown = function(e) {
        e.preventDefault();
        var $el = e.data.el,
          $this = $(this),
          $next = $this.next();
        $next.slideToggle();
        $this.parent().toggleClass('open');

        if (!e.data.multiple) {
          //show only one menu at the same time
          $el.find('.submenuItems').not($next).slideUp().parent().removeClass('open');
        }
      }

      var accordion = new Accordion($('.accordion-menu'), false);

      $('.toggle-inner').on('click', function(e) {
        e.preventDefault();
        var mask = '<div class="mask-overlay">';

        $('body').toggleClass('active');
        $(mask).hide().appendTo('body').fadeIn('fast');
        $('.mask-overlay, .close-menu').on('click', function() {
          $('body').removeClass('active');
          $('.mask-overlay').remove();
        });
      });
    },

    /*==============================*/
    /*=           Countup          =*/
    /*==============================*/
    countUp: function() {
      $('.count_up').waypoint(function(direction) {
        if (direction == 'down') {
          $('.counter').each(function() {
            var $this = $(this);
            var countTo = $this.attr('data-count');
            $({
              countNum: $this.text()
            }).animate({
                countNum: countTo
              },

              {
                duration: 10000,
                easing: 'linear',
                step: function() {
                  $this.text(Math.floor(this.countNum));
                },
                complete: function() {
                  $this.text(this.countNum);
                }
              });
          });
        } else {
          $('.count_up').addClass('swingI');
        }
      }, {
        offset: '100%'
      });

      var $banner_static_left_anim = $('.banner_static_left');
      $banner_static_left_anim.waypoint(function(direction) {
        if (direction == 'down') {
          // $banner_static_left_anim.css("margin-left", "0");
        } else {
          $banner_static_left_anim.addClass('swingI');
        }
      }, {
        offset: '100%'
      });
    },
    /*=================================*/
    /*=           Count Down          =*/
    /*=================================*/
    countDown: function() {
      $('#count_down').countdown('2019/08/25', function(event) {
        $(this).html(event.strftime('<p><span>%D</span> days</p>'));
      });

      $('#count_down_two').countdown('2020/08/19', function(event) {
        $(this).html(event.strftime('<p><span>%D</span> Years</p> <p><span>%H</span> days</p> <p><span>%M</span> days</p>  <p><span>%S</span> days</p>'));
      });
    },

    /*=========================================*/
    /*=           SVG function         =*/
    /*=========================================*/
    svg: function() {
      // Convert Image to SVG
      $('img.svg').each(function() {
        var $img = $(this),
          imgID = $img.attr('id'),
          imgClass = $img.attr('class'),
          imgURL = $img.attr('src');

        $.get(imgURL, function(data) {
          // Get the SVG tag, ignore the rest
          var $svg = $(data).find('svg');

          // Add replaced image's ID to the new SVG
          if (typeof imgID !== 'undefined') {
            $svg = $svg.attr('id', imgID);
          }
          // Add replaced image's classes to the new SVG
          if (typeof imgClass !== 'undefined') {
            $svg = $svg.attr('class', imgClass);
          }

          // Remove any invalid XML tags as per http://validator.w3.org
          $svg = $svg.removeAttr('xmlns:a');

          // Replace image with new SVG
          $img.replaceWith($svg);
        }, 'xml');
      });
    },

    /*=========================================*/
    /*=           owlslider function         =*/
    /*=========================================*/
    owlslider: function() {
      //Screenshot slider
      $('.carousel').carousel();

      //owl carousel slider banner two
      $('.banner_slider').owlCarousel({
        loop: true,
        items: 1,
        autoplay: false,
        dots: true,
        smartSpeed: 600,
        nav: true,
        navText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"],
        responsive: {
          320: {
            autoplay: false
          },

          576: {
            autoplay: false
          }
        }
      });

      $(".banner_slider").on('translate.owl.carousel', function() {
        $('.banner_right_cell').removeClass('fadeInRight animated').hide();
      });

      $(".banner_slider").on('translated.owl.carousel', function() {
        $('.banner_right_cell').addClass('fadeInRight animated').show();
      });

      $(".banner_slider").on('translate.owl.carousel', function() {
        $('.banner_left_cell h1').removeClass('fadeInDown animated').hide();
      });

      $(".banner_slider").on('translated.owl.carousel', function() {
        $('.banner_left_cell h1').addClass('fadeInDown animated').show();
      });

      $(".banner_slider").on('translated.owl.carousel', function() {
        $('.banner_left_cell p').addClass('fadeInDown animated').show();
      });

      $(".banner_slider").on('translate.owl.carousel', function() {
        $('.banner_left_cell p').removeClass('fadeInDown animated').hide();
      });

      $(".banner_slider").on('translated.owl.carousel', function() {
        $('.banner_left_cell .slr_btn_wrapper').addClass('fadeInUp animated').show();
      });

      $(".banner_slider").on('translate.owl.carousel', function() {
        $('.banner_left_cell .slr_btn_wrapper').removeClass('fadeInUp animated').hide();
      });


      $(".banner_slider").on('translate.owl.carousel', function() {
        $('.banner_left_cell h2').removeClass('fadeInDown animated').hide();
      });

      $(".banner_slider").on('translated.owl.carousel', function() {
        $('.banner_left_cell h2').addClass('fadeInDown animated').show();
      });

      $(".banner_slider").on('translate.owl.carousel', function() {
        $('.banner_left_cell h4').removeClass('fadeInDown animated').hide();
      });

      $(".banner_slider").on('translated.owl.carousel', function() {
        $('.banner_left_cell h4').addClass('fadeInDown animated').show();
      });

      $(".banner_slider").on('translate.owl.carousel', function() {
        $('.banner_left_cell .btn_wrapper').removeClass('fadeInUp animated').hide();
      });

      $(".banner_slider").on('translated.owl.carousel', function() {
        $('.banner_left_cell .btn_wrapper').addClass('fadeInUp animated').show();
      });

      $(".banner_slider").on('translate.owl.carousel', function() {
        $('.bnr_title_img').removeClass('fadeInDown animated').hide();
      });

      $(".banner_slider").on('translated.owl.carousel', function() {
        $('.bnr_title_img').addClass('fadeInDown animated').show();
      });

      //Product owl Carousel
      $('.product-carousel').owlCarousel({
        loop: true,
        nav: false,
        items: 1,
        autoplay: false,
        dots: true,
        smartSpeed: 900,
        navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
      });

      //Product owl Carousel
      $('.home5_recent_slider').owlCarousel({
        loop: true,
        items: 4,
        autoplay: false,
        dots: false,
        smartSpeed: 900,
        nav: true,
        navText: ["<i class='material-icons'>arrow_back</i>", "<i class='material-icons'>arrow_forward</i>"],
        margin: 30,
        responsive: {
          320: {
            items: 1
          },

          767: {
            items: 2
          },

          992: {
            items: 3
          },

          1500: {
            items: 4
          }
        }
      });

      //Tetimonial owl Carousel
      $('.testimonial-carousel').owlCarousel({
        loop: true,
        nav: false,
        items: 1,
        autoplay: true,
        dots: true,
        smartSpeed: 900,
        navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"]
      });

      //blog owl carousel
      $('.blog_carousel').owlCarousel({
        loop: true,
        nav: false,
        items: 3,
        autoplay: false,
        dots: false,
        margin: 30,
        responsive: {
          320: {
            items: 1
          },
          768: {
            items: 2
          },
          992: {
            items: 3
          }
        }

      });

      //product two owl carousel
      $('.product_two_slider').owlCarousel({
        items: 4,
        margin: 30,
        autoplay: true,
        loop: true,
        smartSpeed: 1500,
        autoplayTimeout: 5500,
        autoplayHoverPause: true,
        nav: true,
        navText: ["<i class='fas fa-chevron-circle-left'></i>", "<i class='fas fa-chevron-circle-right'></i>"],
        responsive: {
          300: {
            items: 1
          },

          576: {
            items: 2
          },

          768: {
            items: 3
          },
          1200: {
            items: 4
          }
        }
      });

      //product detail owl carousel
      $('.product_detail_slider').owlCarousel({
        items: 1,
        nav: true,
        dots: false
      });

      //product detail owl carousel
      $('.blog_hm_five_slider').owlCarousel({
        items: 2,
        nav: true,
        margin: 30,
        dots: false,
        navText: ["<i class='fas fa-angle-left'></i>", "<i class='fas fa-angle-right'></i>"],
        responsive: {
          300: {
            items: 1,
            margin: 0
          },

          768: {
            items: 2,
            margin: 30,
          }
        }

      });

      //related product owl carousel
      $('.related_product_slider').owlCarousel({
        items: 5,
        nav: true,
        margin: 30,
        navText: ["<i class='fas fa-chevron-circle-left'></i>", "<i class='fas fa-chevron-circle-right'></i>"],
        autoplay: true,
        loop: true,
        slideTransition: 'linear',
        autoplayTimeout: 5500,
        smartSpeed: 1500,
        autoplayHoverPause: true,
        responsive: {

          300: {
            items: 1
          },
          480: {
            items: 2
          },
          576: {
            items: 2
          },
          768: {
            items: 3
          },
          992: {
            items: 4
          },
          1200: {
            items: 4
          },
          1500: {
            items: 5
          }
        }
      });

      $(".supplement_page_right_slider").owlCarousel({
        items: 1,
        navText: ["<i class='material-icons'>arrow_back</i>", "<i class='material-icons'>arrow_forward</i>"],
        nav: true
      });

      $(".supplement_hot_selling_slider").owlCarousel({
        items: 2,
        margin: 30,
        navText: ["<i class='material-icons'>arrow_back</i>", "<i class='material-icons'>arrow_forward</i>"],
        nav: true,
        dots: false,
        responsive: {
          300: {
            items: 1
          },

          768: {
            items: 2
          }
        }
      });
    },

    /*=========================================*/
    /*=           slickcarousel function         =*/
    /*=========================================*/
    slickcarousel: function() {
      //Ingredient page slick slider
      $(".gredient_tab").slick({
        dots: false,
        vertical: true,
        slidesToShow: 5,
        slidesToScroll: 1,
        asNavFor: '.slick_slider_two',
        focusOnSelect: true,
        responsive: [

          {
            breakpoint: 992,
            settings: {
              vertical: false,
              asNavFor: false
            }
          }
        ]
      });

      $(".slick_slider_two").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.gredient_tab',
        responsive: [

          {
            breakpoint: 992,
            settings: {
              arrows: true
            }
          }

        ]
      });

      //Ingredient page slick slider two
      $(".ingredient_slider_one").slick({
        dots: false,
        vertical: true,
        slidesToShow: 4,
        slidesToScroll: 1,
        asNavFor: '.ingredient_slider_two',
        focusOnSelect: true,
        responsive: [

          {
            breakpoint: 992,
            settings: {
              asNavFor: false,
              slidesToShow: 3
            }
          },
          {
            breakpoint: 400,
            settings: {
              slidesToShow: 2,
            }
          }

        ]
      });

      $(".ingredient_slider_two").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.ingredient_slider_one',
        responsive: [

          {
            breakpoint: 992,
            settings: {
              arrows: false
            }
          }
        ]
      });

      $(".megamenu-product-slider").slick({
        slidesToShow: 2,
        arrows: false,
        slidesToScroll: 1,
        dots: false,
        infinite: true,
        autoplay: true,
        speed: 500,
        draggable: true
      });

      $('.supplement_we_say_content_for').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.supplement_we_say_content_nav'
      });

      $('.supplement_we_say_content_nav').slick({
        slidesToShow: 2,
        slidesToScroll: 1,
        asNavFor: '.supplement_we_say_content_for',
        dots: true,
        centerMode: true,
        focusOnSelect: true,
        vertical: true
      });

      if ($(window).width() > 767) {
        $('.supplement_we_say_content_nav').on('wheel', (function(e) {
          e.preventDefault();

          if (e.originalEvent.deltaY < 0) {
            $(this).slick('slickNext');
          } else {
            $(this).slick('slickPrev');
          }
        }));
      }
    },

    /*=========================================*/
    /*=           gmap function         =*/
    /*=========================================*/
    gmap: function() {
      //gmap3
      $('.map').each(function() {
        var $this = $(this),
          key = $this.data('key'),
          lat = $this.data('lat'),
          lng = $this.data('lng'),
          mrkr = $this.data('mrkr');

        $this.gmap3({
            center: [lat, lng],
            zoom: 8,
            mapTypeId: "shadeOfGrey",
            mapTypeControlOptions: {
              mapTypeIds: [google.maps.MapTypeId.ROADMAP, "shadeOfGrey"]
            }
          })
          .marker(function(map) {
            return {
              position: map.getCenter(),
              icon: "media/images/home6/map-marker.png"
            };
          })
          .styledmaptype(
            "shadeOfGrey", [{
                "featureType": "water",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#e9e9e9"
                  },
                  {
                    "lightness": 17
                  }
                ]
              },
              {
                "featureType": "landscape",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#f5f5f5"
                  },
                  {
                    "lightness": 20
                  }
                ]
              },
              {
                "featureType": "road.highway",
                "elementType": "geometry.fill",
                "stylers": [{
                    "color": "#ffffff"
                  },
                  {
                    "lightness": 17
                  }
                ]
              },
              {
                "featureType": "road.highway",
                "elementType": "geometry.stroke",
                "stylers": [{
                    "color": "#ffffff"
                  },
                  {
                    "lightness": 29
                  },
                  {
                    "weight": 0.2
                  }
                ]
              },
              {
                "featureType": "road.arterial",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#ffffff"
                  },
                  {
                    "lightness": 18
                  }
                ]
              },
              {
                "featureType": "road.local",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#ffffff"
                  },
                  {
                    "lightness": 16
                  }
                ]
              },
              {
                "featureType": "poi",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#f5f5f5"
                  },
                  {
                    "lightness": 21
                  }
                ]
              },
              {
                "featureType": "poi.park",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#dedede"
                  },
                  {
                    "lightness": 21
                  }
                ]
              },
              {
                "elementType": "labels.text.stroke",
                "stylers": [{
                    "visibility": "on"
                  },
                  {
                    "color": "#ffffff"
                  },
                  {
                    "lightness": 16
                  }
                ]
              },
              {
                "elementType": "labels.text.fill",
                "stylers": [{
                    "saturation": 36
                  },
                  {
                    "color": "#333333"
                  },
                  {
                    "lightness": 40
                  }
                ]
              },
              {
                "elementType": "labels.icon",
                "stylers": [{
                  "visibility": "off"
                }]
              },
              {
                "featureType": "transit",
                "elementType": "geometry",
                "stylers": [{
                    "color": "#f2f2f2"
                  },
                  {
                    "lightness": 19
                  }
                ]
              },
              {
                "featureType": "administrative",
                "elementType": "geometry.fill",
                "stylers": [{
                    "color": "#fefefe"
                  },
                  {
                    "lightness": 20
                  }
                ]
              },
              {
                "featureType": "administrative",
                "elementType": "geometry.stroke",
                "stylers": [{
                    "color": "#fefefe"
                  },
                  {
                    "lightness": 17
                  },
                  {
                    "weight": 1.2
                  }
                ]
              }
            ], {
              name: "Shades of Grey"
            }
          );
      });
    },
  };

  THEMEIM.documentOnReady = {
    init: function() {
      THEMEIM.initialize.init();
    },
  };

  THEMEIM.documentOnLoad = {
    init: function() {
      // $("#loader-wrapper").delay(3000).fadeOut("slow");
      if ($(window).width() > 991) {
        if ($('#loading-subscribe1').modal('show')) {
          var $cookies = $('.megamenu-cookies').addClass('seen'),
            $cookiesRemove = $cookies.children('.remove, .agree');
          $cookiesRemove.on('click', function() {
            $('.megamenu-cookies').removeClass('seen');
          });
        };
        $('#loading-subscribe2').modal('show');
      }
    },
  };

  THEMEIM.documentOnResize = {
    init: function() {},
  };

  THEMEIM.documentOnScroll = {
    init: function() {
      THEMEIM.initialize.sectionBackground();

      if ($(this).scrollTop() > 150) {
        $('header').addClass("hide-topbar")
      } else {
        $('header').removeClass("hide-topbar")
      }
    },
  };

  // Initialize Functions
  $(document).ready(THEMEIM.documentOnReady.init);
  $(window).on('load', THEMEIM.documentOnLoad.init);
  $(window).on('resize', THEMEIM.documentOnResize.init);
  $(window).on('scroll', THEMEIM.documentOnScroll.init);

})(jQuery);