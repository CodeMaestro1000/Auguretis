// JS to toggle navbar with hamburger button and to change button from burger to x

let navBtn = document.querySelector(".navbar-burger")
let navMenu = document.querySelector(".navbar-menu")

navBtn.addEventListener('click', ()=>{
    navBtn.classList.toggle('is-active');
    navMenu.classList.toggle('is-active');
});