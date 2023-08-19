const btnAddPhone = document.getElementById('btn-add-phone');

btnAddPhone.addEventListener('click', (e) => {
    const containerInputPhone = document.querySelector('.phone-proveedor'); // mover la definición aquí

    const input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('name', `telefono`);
    input.setAttribute('maxlength', '255');
    input.setAttribute('required', '');
    input.setAttribute('id', `id_telefono`);
    input.setAttribute('class', `new-input`);
    
    containerInputPhone.appendChild(input);

});