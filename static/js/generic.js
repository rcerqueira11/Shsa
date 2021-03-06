// Email y contraseña comparacion bilateral
$("#id_correo_electronico").attr('onblur',"confirmEmail2();");
$('.tlf-cel-mask').inputmask('(9999)-999-99-99');
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

$('.ci-mask').inputmask('[9]{8}',{placeholder: ""})
$('.placa-mask').inputmask('[9|a]{8}', {placeholder: ''});
$('.anho').inputmask('[9]{4}', {placeholder: ''});
$('.numeros').inputmask('[9]{20}', {placeholder: ''});
$('.decimals').inputmask('[9]{20}.[9]{1,2}', {placeholder: ''});

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


$(".no-space").on('keypress',function(e){
  if(e.which === 32){
    return false
  }
  
})

function fill_modal_exito_eliminar(titulo,subtitulo,mensaje){
  $("#modal-exito-eliminar-titulo").html(titulo)
  $("#modal-exito-eliminar-subtitulo").html(subtitulo)
  $("#modal-exito-eliminar-msj").html(mensaje)
};

function fill_modal_verificacion_eliminar(titulo,subtitulo,mensaje){
  $("#modal-verificacion-eliminar-titulo").html(titulo)
  $("#modal-verificacion-eliminar-subtitulo").html(subtitulo)
  $("#modal-verificacion-eliminar-msj").html(mensaje)
};



function fill_modal_exito_inactivar(titulo,subtitulo,mensaje){
  $("#modal-exito-inactivar-titulo").html(titulo)
  $("#modal-exito-inactivar-subtitulo").html(subtitulo)
  $("#modal-exito-inactivar-msj").html(mensaje)
};

function fill_modal_verificacion_inactivar(titulo,subtitulo,mensaje){
  $("#modal-verificacion-inactivar-titulo").html(titulo)
  $("#modal-verificacion-inactivar-subtitulo").html(subtitulo)
  $("#modal-verificacion-inactivar-msj").html(mensaje)
};

function fill_modal_exito_activar(titulo,subtitulo,mensaje){
  $("#modal-exito-activar-titulo").html(titulo)
  $("#modal-exito-activar-subtitulo").html(subtitulo)
  $("#modal-exito-activar-msj").html(mensaje)
};

function fill_modal_verificacion_activar(titulo,subtitulo,mensaje){
  $("#modal-verificacion-activar-titulo").html(titulo)
  $("#modal-verificacion-activar-subtitulo").html(subtitulo)
  $("#modal-verificacion-activar-msj").html(mensaje)
};


// $(":radio").on('click', function(){
//   console.log("this:",this);
//   console.log("$(this).prop('checked'):",$(this).prop('checked'));
  
//   // if ($(this).prop('checked')){
//   //   $(this).prop('checked', false);
//   // }else{
//   //   $(this).prop('checked', true);

//   // }
  

// })

$('.tlf-cel-mask').each(function(i, obj) {
    $(obj).on('input', function (event) {
            var str_sample = '(0424)-123-12-12';
            var replace_1 = '(____)-___-__-__';
            var re = /^\(0(?:412|414|416|424|426|415)\)\-[0-9]{3}\-[0-9]{2}\-[0-9]{2}/;
            var new_str = '';
            var primer_str = '';
            var cant_nums = this.value.replace(/[^0-9]/g,"").length;
            if(cant_nums == 1){
                primer_str = this.value.substring(0,2);
                if(primer_str != '(0')
                    this.value = replace_1;
            }
            if(cant_nums == 2){
                primer_str = this.value.substring(0,3);
                new_str = primer_str + str_sample.substring(3,16);
                if( !new_str.match(re) )
                    this.value = this.value.substring(0,2) + replace_1.substring(2,16);
            }
            if(cant_nums == 3){
                primer_str = this.value.substring(0,4);
                new_str = primer_str + str_sample.substring(4,16);
                if( !new_str.match(re) )
                    this.value = this.value.substring(0,3) + replace_1.substring(3,16);
            }
            if(cant_nums == 4){
                primer_str = this.value.substring(0,5);
                new_str = primer_str + str_sample.substring(5,16);
                if( !new_str.match(re) )
                    this.value = this.value.substring(0,4) + replace_1.substring(4,16);
            }
        });

});


$(document).on("click","input[type=radio]",function(e){
   
  if (e.ctrlKey) {
    if($(this).prop('checked')){$(this).prop('checked',false)}
  }    
})