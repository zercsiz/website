const sideNL1 = document.querySelector('.sidebar-nav-link1')
const sideNL2 = document.querySelector('.sidebar-nav-link2')
const sideNL3 = document.querySelector('.sidebar-nav-link3')

if(window.location.pathname==='/accounts/details/') {
    sideNL1.classList.add('nav-link-active');
    sideNL2.classList.add('nav-link-deactive');
    sideNL3.classList.add('nav-link-deactive');

}
if (window.location.pathname==='/courses/time_checkbox') {
    sideNL2.classList.add('nav-link-active');
    sideNL1.classList.add('nav-link-deactive');
    sideNL3.classList.add('nav-link-deactive');
}
if (window.location.pathname==='/accounts/edit/') {
    sideNL3.classList.add('nav-link-active');
    sideNL2.classList.add('nav-link-deactive');
    sideNL1.classList.add('nav-link-deactive');
}
