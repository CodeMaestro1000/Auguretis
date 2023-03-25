const params = new URL(location.href).searchParams;
const next = params.get('next');

if (next) {
    let formUrl = document.querySelector("#login-form");
    let action = formUrl.getAttribute("action").concat(`?next=${next}`);
    formUrl.setAttribute("action", action);
    console.log(formUrl);    
}
