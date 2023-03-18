
const navFl = document.querySelector('.navbar')

if(window.location.pathname==='/') {
    window.addEventListener('scroll',
    () => {
        if (window.scrollY >= 56) {
            navFl.classList.add('navbar-scrolled');
        } else if (window.scrollY < 56) {
            navFl.classList.remove('navbar-scrolled');
        }
    });
} else {
     navFl.classList.add('navbar-scrolled');
}

