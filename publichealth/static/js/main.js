$(document).load(function() {

	$('.carousel-inner.slick').slick({
		autoplay: true,
		autoplaySpeed: '10000',
		dots: true,
		infinite: true,
		speed: 1000,
		fade: true,
		cssEase: 'linear',
		prevArrow: '<span class="arrow left glyphicon glyphicon-chevron-left" aria-hidden="true">Previous</span>',
		nextArrow: '<span class="arrow right glyphicon glyphicon-chevron-right" aria-hidden="true">Next</span>',
	});

});
