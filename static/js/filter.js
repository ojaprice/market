$(document).ready(function() {
    $('.featured__controls ul li').click(function() {
        var filterValue = $(this).attr('data-filter');

        $('.featured__controls ul li').removeClass('active');
        $(this).addClass('active');

        if (filterValue === '*') {
            $('.featured__filter .product-item').show('1000');
        } else {
            $('.featured__filter .product-item').hide('3000');
            $('.featured__filter .product-item').filter(filterValue).show('3000');
        }
    });
});
