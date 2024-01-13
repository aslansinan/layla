/**
 * Created by MACPRO on 17.08.2016.
 */
django.jQuery(function($) {
    $('#password').click(function(e) {
        e.preventDefault();
        var url=window.location.href;
        var newUrl=url.replace('change','password');
        window.location.href = newUrl;
    });
});