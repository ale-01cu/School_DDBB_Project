const selectorCategoria = document.querySelector('#id_categoria')
const inputPantalla = document.getElementById('pantalla')
const inputEspacio = document.getElementById('espacio')
const inputMemoria = document.getElementById('memoria')
const inputConsumo = document.getElementById('consumo')

selectorCategoria.addEventListener('change', e => {
    if (selectorCategoria.value === 'componente_pc'){
        inputPantalla.style.display = 'none'
        inputEspacio.style.display = 'none'
        inputMemoria.style.display = 'none'
        inputConsumo.style.display = 'none'

    }else if(selectorCategoria.value === 'equipo_hogar'){
        inputPantalla.style.display = 'none'
        inputEspacio.style.display = 'none'
        inputMemoria.style.display = 'none'
        inputConsumo.style.display = 'block'

    }else{
        inputPantalla.style.display = 'block'
        inputEspacio.style.display = 'block'
        inputMemoria.style.display = 'block'
        inputConsumo.style.display = 'block'
    }
})