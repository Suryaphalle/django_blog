console.log('signup.js loaded');


let form = document.querySelector("#signupform");
let $password1 = document.querySelector("#id_password1");
let $email_id = document.querySelector("#id_email");
let $password2 = document.querySelector("#id_password2");


form.addEventListener("focus",function(event){
    $email_id.onblur = function(e){
        if (!this.value.includes('@')){
            this.classList.add('invalid-feedback');
            let error_message = this.parentElement.children.errorMessage;
            error_message.textContent = 'Please enter a correct email.';
        }
    };

    $email_id.onfocus = function(e){
        if (!this.value.includes('@')){
            this.classList.add('invalid-feedback');
            let error_message = this.parentElement.children.errorMessage;
            error_message.textContent = '';
        }
    };

    $password2.onblur = function(e){
        if (this.value !== $password1.value){
            this.classList.add('invalid-feedback');
            let error_message = this.parentElement.children.errorMessage;
            error_message.textContent = 'Password didn\'t match';
        }
    };
}, true);
