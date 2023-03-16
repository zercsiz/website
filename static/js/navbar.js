
const navFl = document.querySelector('.navbar')
const winHref = window.location.href

if (winHref === 'http://127.0.0.1:8000') {
    window.addEventListener('scroll', () => {
    if (window.scrollY >= 56) {
            navFl.classList.add('navbar-scrolled');
    } else if (window.scrollY < 56) {
            navFl.classList.remove('navbar-scrolled')
    }
    })
} else {
    navFl.classList.add('navbar-scrolled')
}
