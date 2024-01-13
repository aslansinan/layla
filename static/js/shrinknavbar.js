function scrollValue() {
    var navbar = document.getElementById('navbar');
    var logo=document.getElementById('logo-item')
    var scroll = window.scrollY;
    if (scroll < 200) {
        navbar.classList.remove('BgColour');
        logo.classList.remove('logo-item-scroll')
    } else {
        navbar.classList.add('BgColour');
        logo.classList.add('logo-item-scroll')
        document.getElementById("navigation").style.transformStyle = "preserve-3d";
    }
}

    window.addEventListener('scroll', scrollValue);