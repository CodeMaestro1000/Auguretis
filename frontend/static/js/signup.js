window.onload = ()=> {

    let username = document.querySelector("#username");
    let email = document.querySelector("#email");
    let password = document.querySelector("#password");
    let confirmPassword = document.querySelector("#password-confirm");
    let terms = document.querySelector("#t-c");
    let submitBtn = document.querySelector("#signup-submit");
    let form = document.querySelector("#signup-form");


    // flags to ensure all inputs are in order before activating submit button
    let flag1 = true;
    let flag2 = true;
    let flag3 = true;
    let flag4 = true;

    let timer = '';

    submitBtn.disabled = true; // initial state of submit button for form

    username.value = "";

    const verify_email = async(email) => {
        const response = await fetch(`${window.location.origin}/verify-email/${email}`, {
            method: 'GET',
        });
        const data = await response.json();  
        return data['status'];
    }

    const verify_username = async(username) => {
        const response = await fetch(`${window.location.origin}/verify-username/${username}`, {
            method: 'GET',
        });
        const data = await response.json();  
        return data['status'];
    }

    // Helper to update form input
    const update_helper = (element, helper, text, icon, mode)=> {
        helper.textContent = text;
        if (mode == 1){
            element.classList.add("is-success");
            element.classList.remove('is-danger');
            helper.classList.add("is-success");
            helper.classList.remove("is-danger");
        }
        else {
            element.classList.add("is-danger");
            element.classList.remove('is-success');
            helper.classList.add("is-danger");
            helper.classList.remove("is-success");
        } 
        icon.classList.remove("is-hidden");
        helper.classList.remove("is-hidden");
    }

    // helper to reset form-input
    const reset = (element, helper, icon1, icon2) => {
        element.classList.remove("is-success", "is-danger");
        helper.classList.remove("is-success", "is-danger");
        helper.classList.add("is-hidden");
        icon1.classList.add("is-hidden");
        icon2.classList.add("is-hidden");
    }

    // helper for validating email
    const validateEmail = ($email) => {
        var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
        return emailReg.test( $email );
    }

    // helper for validating username when it is pre-populated by the browser
    const validateUsername = (elem)=> {
        let helper = document.querySelector("#username-help");
        let icon_good = document.querySelector("#username-good");
        let icon_bad = document.querySelector("#username-bad");
        
        verify_username(elem.value).then(status => {
            if (status == 200){
                update_helper(elem, helper, "You're good to go", icon_good, 1);
                flag1 = false; // enable submit btn
            }
            else {
                update_helper(elem, helper, "Username already taken", icon_bad, 2);
                flag1 = true; // disable submit btn
            } 
        });
    }

    // helper for ensuring all fields are correct b4 activating button
    const updateSubmitBtnState = ()=>{
        submitBtn.disabled = flag1 || flag2 || flag3 || flag4;
    }

    // IMPORTANT - Validate the username if it is pre-populated by the browser
    if (username.value != ''){
        validateUsername(username);
    }


    /* ============================= EVENT LISTENERS ============================= */

    username.addEventListener('input', async (e)=>{
        let helper = document.querySelector("#username-help");
        let icon_good = document.querySelector("#username-good");
        let icon_bad = document.querySelector("#username-bad");
        reset(e.target, helper, icon_good, icon_bad);
        clearTimeout(timer);
       
        timer = setTimeout(function() {
            if (e.target.value.length < 3){
                update_helper(e.target, helper, "Username cannot be less than 3 characters", icon_bad, 2);
                flag1 = true;
            }
            else {
                verify_username(e.target.value).then(status => {
                    if (status == 200){
                        update_helper(e.target, helper, "You're good to go", icon_good, 1);
                        flag1 = false; // enable submit btn
                    }
                    else {
                        update_helper(e.target, helper, "Username already taken", icon_bad, 2);
                        flag1 = true; // disable submit btn
                    } 
                });
            }
            updateSubmitBtnState();
        }, 1000); // end timeout function
    })

    email.addEventListener('input', async (e)=>{
        let helper = document.querySelector("#email-help");
        let icon_good = document.querySelector("#email-good");
        let icon_bad = document.querySelector("#email-bad");
        reset(e.target, helper, icon_good, icon_bad);
        clearTimeout(timer);
        

        timer = setTimeout(function() {
            if (!validateEmail(e.target.value)){ // if code fails email validation, don't bother checking
                update_helper(e.target, helper, "Invalid email", icon_bad, 2);
                flag2 = true;
            }
            else {
                verify_email(e.target.value).then(status => {
                    if (status == 200){
                        update_helper(e.target, helper, "You're good to go", icon_good, 1);
                        flag2 = false;
                    }
                    else {
                        update_helper(e.target, helper, "User with email already exists", icon_bad, 2);
                        flag2 = true;
                    } 
                });
            }
            updateSubmitBtnState();
        }, 1000); // end timeout function
    })

    password.addEventListener('input', (e) => {
        let helper = document.querySelector("#password-help");
        let icon_good = document.querySelector("#password-good");
        let icon_bad = document.querySelector("#password-bad");

        let confirm_helper = document.querySelector("#confirm-password-help");
        let confirm_icon_good = document.querySelector("#confirm-password-good");
        let confirm_icon_bad = document.querySelector("#confirm-password-bad");

        reset(e.target, helper, icon_good, icon_bad);
        reset(confirmPassword, confirm_helper, confirm_icon_good, confirm_icon_bad);
        clearTimeout(timer);
        
        timer = setTimeout(function() {
            if (e.target.value.length < 6) {
                flag3 = true;
                reset(confirmPassword, confirm_helper, confirm_icon_good, confirm_icon_bad);
                update_helper(e.target, helper, "Password must be more than 5 characters", icon_bad, 2);
            }
            else if ((e.target.value != '') &&(e.target.value === confirmPassword.value)){
                flag3 = false;
                update_helper(e.target, helper, "You're good to go", icon_good, 1);
                update_helper(confirmPassword, confirm_helper, "You're good to go", confirm_icon_good, 1);
            }
            else {
                flag3 = true;
                update_helper(e.target, helper, "Passwords do not match", icon_bad, 2);
                update_helper(confirmPassword, confirm_helper, "Passwords do not match", confirm_icon_bad, 2);
            }
            updateSubmitBtnState();
            
        }, 500); // end timeout function
    });

    confirmPassword.addEventListener('input', (e) => {
        let helper = document.querySelector("#password-help");
        let icon_good = document.querySelector("#password-good");
        let icon_bad = document.querySelector("#password-bad");

        let confirm_helper = document.querySelector("#confirm-password-help");
        let confirm_icon_good = document.querySelector("#confirm-password-good");
        let confirm_icon_bad = document.querySelector("#confirm-password-bad");

        reset(e.target, confirm_helper, confirm_icon_good, confirm_icon_bad);
        reset(password, helper, icon_good, icon_bad);
        clearTimeout(timer);
        
        timer = setTimeout(function() {
            if (password.value.length < 6) {
                flag3 = true;
                reset(e.target, confirm_helper, confirm_icon_good, confirm_icon_bad);
                update_helper(password, helper, "Password must be more than 5 characters", icon_bad, 2);
            }
            else if ((e.target.value != '') && (e.target.value === password.value)){
                flag3 = false;
                update_helper(password, helper, "You're good to go", icon_good, 1);
                update_helper(e.target, confirm_helper, "You're good to go", confirm_icon_good, 1);
            }
            else {
                flag3 = true;
                update_helper(password, helper, "Passwords do not match", icon_bad, 2);
                update_helper(e.target, confirm_helper, "Passwords do not match", confirm_icon_bad, 2);
            }
            updateSubmitBtnState();
            
        }, 500); // end timeout function
    });

    terms.addEventListener('input', (e) => {
        if (e.target.checked == true) {
            flag4 = false;
        } else {
            flag4 = true;
        }
        updateSubmitBtnState();
    });

    submitBtn.addEventListener('click', ()=>{
        if ((flag1 || flag2 || flag3 || flag4) == true){ // if one of the disable flags are true
            // do nothing
        }
        else form.submit();
    });

}

