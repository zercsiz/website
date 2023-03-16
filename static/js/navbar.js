
const navFl = document.querySelector('.navbar')

window.addEventListener('scroll', () => {
    if (window.scrollY >= 56) {
        navFl.classList.add('navbar-scrolled');
    } else if (window.scrollY < 56) {
        navFl.classList.remove('navbar-scrolled')
    }
})
