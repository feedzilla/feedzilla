$(function() {
    $('code').each(function() {
        if ($(this).find('br').length) {
            $(this).addClass('block');
        }
    });
});
