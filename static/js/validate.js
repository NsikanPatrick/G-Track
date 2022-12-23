// JS function should only validate the fields one at a time then you re-attach this 
// file again to the main login page

const form = document.getElementById('form');
const uname = document.getElementById('uname');
const lname = document.getElementById('lname');
const email = document.getElementById('email');
const password = document.getElementById('password');


form.addEventListener("submit", (e) => {
    e.preventDefault();
    checkInputs();  
});

function checkInputs() {
    // Get the form input values so you can use them to write the conditions
    const unameValue = uname.value.trim();
    // const lnameValue = lname.value.trim();
    // const emailValue = email.value.trim();
    const passwordValue = password.value.trim();

    if(unameValue === ''){
        // The input field is accepted as an argument so we can use it to show the error
        // or success states and also a message that will be displayed on the small tag
        setErrorFor(uname, 'First name field must not be empty');
    }else{
        // No message will be displayed so we only need the input field as an argument
        setSuccessFor(uname);
    }

    // if(lnameValue === ''){
    //     setErrorFor(lname, 'Last name field must not be empty');
    // }else{
    //     setSuccessFor(lname);
    // }

    // if(emailValue == ''){
    //     setErrorFor(email, 'Email field must not be empty');
    
    // }else if(!isValidEmail(emailValue)){
    //     setErrorFor(email, 'Pls input a valid email');
    // }else{
    //     setSuccessFor(email);
    // }

    if(passwordValue === ''  || passwordValue.length < 8){
        setErrorFor(password, 'Password field must not be empty or less than 8 characters');
    }else{
        setSuccessFor(password);
    }
}

function setErrorFor(input, message){
    const formGroup = input.parentElement;
    const small = formGroup.querySelector('small');

    small.innerText = message;
    formGroup.classList.add('error');
    // formGroup.className = 'form-group error';
}

function setSuccessFor(input){
    const formGroup = input.parentElement;
    formGroup.classList.add('success');
    // formGroup.classList.remove('error');
}

function isValidEmail(testEmail){
    return emailPattern.test(testEmail)
}


const emailPattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

const simplePattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/