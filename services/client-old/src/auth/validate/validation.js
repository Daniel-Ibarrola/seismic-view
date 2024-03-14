

export const validatePassword = (password) => {
    if (!password) {
        return 'Requerido';
    }

    let passwordError = "";
    if (password.length < 8 || password.length > 20){
        passwordError += 'Entre 8 y 20 caractéres. ';
    }
    if (!/[A-Z]+/.test(password)) {
        passwordError += 'Al menos una letra mayúscula. ';
    }
    if (!/[a-z]+/.test(password)) {
        passwordError += 'Al menos una letra minúscula. ';
    }
    if (/\s+/.test(password)) {
        passwordError += 'No debe contener espacios. ';
    }
    if (!/\W+/.test(password)) {
        passwordError += 'Al menos un carácter especial. ';
    }
    return passwordError;
};


export const validateEmail = (email) => {
    let emailError = "";
    if (!email) {
        emailError = 'Requerido';
    } else if (
        !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(email)
    ) {
        emailError = 'Correo inválido';
    }
    return emailError;
};

export const formPasswordValidation = (values) => {
    const errors = {}
    const passwordErrors = validatePassword(values.password);
    if (passwordErrors){
        errors.password = passwordErrors;
    }
    return errors;
};


export const formEmailAndPasswordValidation = (values) => {
    const errors = {}
    const emailErrors = validateEmail(values.email);
    if (emailErrors){
        errors.email = emailErrors;
    }
    const passwordErrors = validatePassword(values.password);
    if (passwordErrors){
        errors.password = passwordErrors;
    }
    return errors;
};
