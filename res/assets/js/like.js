$(window).on('pytsite.widget.init:plugins.flag._widget.Like', function (e, widget) {
    widget.em.find('a').click(function (e) {
        e.preventDefault();

        var em = widget.em;

        if (widget.em.hasClass('flagged') && !confirm(t('flag@dislike_confirmation')))
            return;

        pytsite.httpApi.patch('flag/like/' + em.data('model') + '/' + em.data('uid')).done(function (data) {
            if (data['status']) {
                em.addClass('flagged');
                em.find('a').attr('title', t('flag@dislike'));
            }
            else {
                em.removeClass('flagged');
                em.find('a').attr('title', t('flag@like'));
            }

            em.find('.count').text(data['count']);
        });
    });
});
