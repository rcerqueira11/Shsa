// Email y contraseña comparacion bilateral
$("#id_correo_electronico").attr('onblur',"confirmEmail2();");

//Contraseña minimo 8 digitos y que contenga una Mayuscula
$("#id_password").attr('pattern','(?=.*[A-Z]).{8,}')
$("#id_password").attr('onkeypress','return beta(event)');
$("#id_password").attr('onblur',"confirmPasswordRecuperar2();");

$("#id_password_confirm").attr('onblur',"confirmPasswordRecuperar()");
$("#id_password_confirm").attr('pattern','(?=.*[A-Z]).{8,}');
$("#id_password_confirm").attr('onkeypress','return beta(event)');
$("#id_password_confirm").attr('onselectstart','return false');
$("#id_password_confirm").attr('onpaste','return false');
$("#id_password_confirm").attr('onCopy','return false');
$("#id_password_confirm").attr('onCut','return false');
$("#id_password_confirm").attr('onDrag','return false');
$("#id_password_confirm").attr('onDrop','return false');


$('.ci-mask').inputmask('[9]{8}', {placeholder: ''});
$('.anho').inputmask('[9]{4}', {placeholder: ''});
$('.numeros').inputmask('[9]{20}', {placeholder: ''});

$('.chosen-select').chosen();

function validarEmail( email ) {
    expr = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9])+$/;
    if ( expr.test(email)){
        return 1;
    }else{
        return 0;
    }
}

//Evitar espacion en el password
function beta(e) {
     var k;
     document.all ? k = e.keyCode : k = e.which;
     return (k!=32);
}

var letras_mayusculas="ABCDEFGHIJKLMNÑOPQRSTUVWXYZ";

function tiene_mayusculas(texto){
   for(i=0; i<texto.length; i++){
      if (letras_mayusculas.indexOf(texto.charAt(i),0)!=-1){
         return 1;
      }
   }
   return 0;
}

function validarPassword(clave){
  if (tiene_mayusculas(clave) && (clave.length>=8)){
    return true
  }
 return false
}



function capfirst(val){

    val = val.charAt(0).toUpperCase() + val.substr(1).toLowerCase();
    return val;
}

function isEmpty( el ){
      return !$.trim(el.html())
  }


function es_vacio(id){
    return jQuery.isEmptyObject($("#"+id).val())
}

function show_modal_errores(){
  $("#modal-aviso-msj").html("Hay errores en el formulario de registro, favor verificar información suministrada.")
  $("#modal-aviso").modal('show')
}

function show_modal_errores_personalizado(mensaje){
  $("#modal-aviso-msj").html(mensaje)
  $("#modal-aviso").modal('show')
}

function confirmPasswordRecuperar() {
        var pass1 = document.getElementById("id_password").value;
        var pass2 = document.getElementById("id_password_confirm").value;

        if (pass1 != pass2) {
            document.getElementById("id_password").style.borderColor = "#E34234";
            document.getElementById("id_password_confirm").style.borderColor = "#E34234";
            $("#id-error-confirm-pass-recover").html('<p class="small_error_letter"> Las contraseñas no son iguales! <i class="fa fa-times-circle-o fa-lg"></i> </p>');


        } else {

            if (pass1.length<8) {
                document.getElementById("id_password").style.borderColor = "#E34234";
                document.getElementById("id_password_confirm").style.borderColor = "#E34234";
                $("#id-error-confirm-pass-recover").html('<p class="small_error_letter"> Las contraseñas deben tener al menos 8 caracteres! <i class="fa fa-times-circle-o fa-lg"></i> </p>');
            }else{

                if(!tiene_mayusculas(pass1)){

                    document.getElementById("id_password").style.borderColor = "#E34234";
                    document.getElementById("id_password_confirm").style.borderColor = "#E34234";
                    $("#id-error-confirm-pass-recover").html('<p class="small_error_letter"> Las contraseñas deben tener al menos una letra mayúscula! <i class="fa fa-times-circle-o fa-lg"></i> </p>');

                }else{

                    document.getElementById("id_password").style.borderColor = "#14D100";
                    document.getElementById("id_password_confirm").style.borderColor = "#14D100";
                    $("#id-error-confirm-pass-recover").empty();
                    $("#id-error-confirm-pass-recover").html('<i class="fa fa-check-circle-o fa-lg" style="color:#14D100"></i>');
                }

            }

        }
};


function confirmPasswordRecuperar2() {
        var pass1 = document.getElementById("id_password").value;
        var pass2 = document.getElementById("id_password_confirm").value;

        if (pass1 == pass2) {
            if(pass2.length>=8){
                if(tiene_mayusculas(pass2)){
                    document.getElementById("id_password").style.borderColor = "#14D100";
                    document.getElementById("id_password_confirm").style.borderColor = "#14D100";
                    $("#id-error-confirm-pass-recover").empty();
                    $("#id-error-confirm-pass-recover").html('<i class="fa fa-check-circle-o fa-lg" style="color:#14D100"></i>');

                }else{
                    document.getElementById("id_password").style.borderColor = "#E34234";
                    document.getElementById("id_password_confirm").style.borderColor = "#E34234";
                    $("#id-error-confirm-pass-recover").html('<p class="small_error_letter"> Las contraseñas deben tener al menos una letra mayúscula! <i class="fa fa-times-circle-o fa-lg"></i> </p>');
                }
            }else{
                document.getElementById("id_password").style.borderColor = "#E34234";
                document.getElementById("id_password_confirm").style.borderColor = "#E34234";
                $("#id-error-confirm-pass-recover").html('<p class="small_error_letter"> Las contraseñas deben tener al menos 8 caracteres! <i class="fa fa-times-circle-o fa-lg"></i> </p>');
            }
        } else {

            if(pass2.length!=0){
                document.getElementById("id_password").style.borderColor = "#E34234";
                document.getElementById("id_password_confirm").style.borderColor = "#E34234";
                $("#id-error-confirm-pass-recover").html('<p class="small_error_letter"> Las contraseñas no son iguales! <i class="fa fa-times-circle-o fa-lg"></i> </p>');

            }

            if(pass1.length!=0){
                $("#id-error-password").html('');
            }

        }
};


function show_modal_exito(titulo,subtitulo,mensaje){
  $("#modal-exito-titulo").html(titulo)
  $("#modal-exito-subtitulo").html(subtitulo)
  $("#modal-exito-msj").html(mensaje)
  $("#modal-exito").modal('show')
};

function show_modal_verificacion(titulo,subtitulo,mensaje){
  $("#modal-verificacion-titulo").html(titulo)
  $("#modal-verificacion-subtitulo").html(subtitulo)
  $("#modal-verificacion-msj").html(mensaje)
  $("#modal-verificacion").modal('show')
};

function fill_modal_exito(titulo,subtitulo,mensaje){
  $("#modal-exito-titulo").html(titulo)
  $("#modal-exito-subtitulo").html(subtitulo)
  $("#modal-exito-msj").html(mensaje)
};

function fill_modal_verificacion(titulo,subtitulo,mensaje){
  $("#modal-verificacion-titulo").html(titulo)
  $("#modal-verificacion-subtitulo").html(subtitulo)
  $("#modal-verificacion-msj").html(mensaje)
};