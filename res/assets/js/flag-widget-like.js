define(['pytsite-http-api', 'pytsite-lang', 'assetman'], function (httpApi, lang, assetman) {
    return function (widget) {
        widget.em.find('a').click(function (e) {
            e.preventDefault();

            var em = widget.em;

            if (widget.em.hasClass('flagged') && !confirm(lang.t('flag@dislike_confirmation')))
                return;

            httpApi.patch('flag/like/' + em.data('model') + '/' + em.data('uid')).done(function (data) {
                if (data['status']) {
                    em.addClass('flagged');
                    em.find('a').attr('title', lang.t('flag@dislike'));
                }
                else {
                    em.removeClass('flagged');
                    em.find('a').attr('title', lang.t('flag@like'));
                }

                em.find('.count').text(data['count']);
            });
        });

        assetman.loadCSS('plugins.flag@css/flag-widget-like.css');
    }
});
