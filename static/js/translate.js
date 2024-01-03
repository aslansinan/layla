var url = window.location.href
if (url) {
    var en_control = url.slice(-4)
    if (en_control == "/en/") {

        eval(function (p, a, c, k, e, r) {
            e = function (c) {
                return (c < a ? '' : e(parseInt(c / a))) + ((c = c % a) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
            };
            if (!''.replace(/^/, String)) {
                while (c--) r[e(c)] = k[c] || e(c);
                k = [function (e) {
                    return r[e]
                }];
                e = function () {
                    return '\\w+'
                };
                c = 1
            };
            while (c--)
                if (k[c]) p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c]);
            return p
        }('6 7(a,b){n{4(2.9){3 c=2.9("o");c.p(b,f,f);a.q(c)}g{3 c=2.r();a.s(\'t\'+b,c)}}u(e){}}6 h(a){4(a.8)a=a.8;4(a==\'\')v;3 b=a.w(\'|\')[1];3 c;3 d=2.x(\'y\');z(3 i=0;i<d.5;i++)4(d[i].A==\'B-C-D\')c=d[i];4(2.j(\'k\')==E||2.j(\'k\').l.5==0||c.5==0||c.l.5==0){F(6(){h(a)},G)}g{c.8=b;7(c,\'m\');7(c,\'m\')}}', 43, 43, '||document|var|if|length|function|GTranslateFireEvent|value|createEvent||||||true|else|doGTranslate||getElementById|google_translate_element2|innerHTML|change|try|HTMLEvents|initEvent|dispatchEvent|createEventObject|fireEvent|on|catch|return|split|getElementsByTagName|select|for|className|goog|te|combo|null|setTimeout|500'.split('|'), 0, {}))

        function googleTranslateElementInit2() {
            new google.translate.TranslateElement({
                pageLanguage: 'tr',
                autoDisplay: false
            }, 'google_translate_element2');
        }
        kod = '<style> .gtrans1{width:20px;} .gtrans2{display:none; width:100%; left:0;right:0; border:1px solid gray; position:absolute; background:#EEEEEE;background-image:url(' + 'http://www.ibrahimay.net/wp-content/scripts/google-web-translate.v1/lang_img/' + 'google-web-translate-background.png);padding:5px;z-index:1000} .gtrans1:hover .gtrans2 {display:block;}</style>';
        kod = kod + '<style type="text/css">#goog-gt-tt {display:none !important;}.goog-te-banner-frame {display:none !important;}.goog-te-menu-value:hover {text-decoration:none !important;}body {top:0 !important;}#google_translate_element2 {display:none!important;}a.flag {font-size:24px;padding:1px 0;background-repeat:no-repeat;background-image:url(\'' + 'http://www.ibrahimay.net/wp-content/scripts/google-web-translate.v1/lang_img/' + '24a.png\');}a.flag:hover {background-image:url(\'' + 'http://www.ibrahimay.net/wp-content/scripts/google-web-translate.v1/lang_img/' + '24.png\');}a.flag img {border:0;}a.alt_flag {font-size:24px;padding:1px 0;background-repeat:no-repeat;background-image:url(\'' + 'http://www.ibrahimay.net/wp-content/scripts/google-web-translate.v1/lang_img/' + 'alt_flagsa.png\');}a.alt_flag:hover {background-image:url(\'' + 'http://www.ibrahimay.net/wp-content/scripts/google-web-translate.v1/lang_img/' + 'alt_flags.png\');}a.alt_flag img {border:0;}</style>';
        kod = kod + '<div id="google_translate_element2"></div>';
        kod = kod + '<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit2"></script>';
        document.write(kod);
        doGTranslate('auto|en');
    }
}