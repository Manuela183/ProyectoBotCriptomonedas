$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});

function verify_password() {
    /*pw1 = document.formulario_registro.password1.value
    pw2 = document.formulario_registro.password2.value

    if (pw1 == pw2)
       alert("Las dos claves son iguales...\nRealizaríamos las acciones del caso positivo")
    else
       alert("Las dos claves son distintas...\nRealizaríamos las acciones del caso negativo")*/

    let pw1 = document.getElementById('password1')
    let pw2 = document.getElementById('password2')
    let button = document.getElementById("submit");
    if (pw1.value == pw2.value) {
        pw2.style.border = "1px solid"
        pw2.style.borderColor = 'green'
        pw1.style.borderColor = 'green'
        button.disabled = false;
    } else {
        pw2.style.border = "1px solid"
        pw2.style.borderColor = 'red'
        pw1.style.borderColor = 'red'
        button.disabled = true;
    }
}

