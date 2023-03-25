let form = document.querySelector("#search-form");
let input = document.querySelector("#search-input");
let spinner = document.querySelector(".spinner");

form.addEventListener('submit', (e)=>{
    if (input.value == ''){
        e.preventDefault(); // don't submit if input is empty
    }
    else {
        e.target.classList.add('is-hidden');
        spinner.classList.remove('is-hidden');
    }
});
