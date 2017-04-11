$("#id_username").focus();
$("#id_username").attr("autocomplete","off");
$("#id_correo2").prop('readonly',true)

function no_vacio_error(id){
    $("#"+id).html('<p class="small_error_letter"> Este campo no puede estar vacio <i class="fa fa-times-circle-o fa-lg"></i> </p>');
}

function es_vacio(id){
    return jQuery.isEmptyObject($("#"+id).val())
}

function show_modal_errores(){
  $("#modal-aviso-msj").html("Hay errores en el formulario de registro, favor verificar información suministrada.")
  $("#modal-aviso").modal('show')
}

function block_correo2(){
    $("#id_correo2").prop('readonly',true)
    $("#id_correo2").val("")
    document.getElementById("id_correo2").style.borderColor = "";
    $("#id-error-confirm-email").html('');
}
// funciones retornan true si el valor del campo esta disponible en caso contrario false
function consulta_nombre_usuario(usuario){
    if(usuario.length){
        $.ajax({
                type: 'GET' ,
                url: '/registro/verificar_nombre_usuario' , // <= Providing the URL
                data:{
                    'username': usuario,
                },
                success: function(results){
                    if(results.Result=='ocupado'){
                        $("#id-error-username").html('<p class="small_error_letter"> El nombre de usuario ya se encuentra registrado. Por favor intente con otro Nombre de Usuario <i class="fa fa-times-circle-o fa-lg"></i> </p>');
                        return false
                    }
                    if (results.Result=='libre'){
                        $("#id-error-username").html('<i class="fa fa-check-circle-o fa-lg" style="color:#14D100"></i>');
                        return true
                    }
                    
                },
                error: function(results){
                    console.log("ERROR");
                }
            });
        

    }else{
        $("#id-error-username").html('<p class="small_error_letter"> El nombre de usuario debe ser válido<i class="fa fa-times-circle-o fa-lg"></i> </p>');
    }
}

function consulta_correo_usuario(correo){

    if(correo.length){
        $.ajax({
                type: 'GET' ,
                url: '/registro/verificar_correo_usuario' , // <= Providing the URL
                data:{
                    'email': correo,
                },
                success: function(results){
                    console.log(results);
                    
                    if(results.Result=='ocupado'){
                        $("#id-error-correo").html('<p class="small_error_letter"> El correo de usuario ya se encuentra registrado. Por favor intente con otro correo <i class="fa fa-times-circle-o fa-lg"></i> </p>');
                        block_correo2()
                        
                    }
                    if (results.Result=='libre'){
                        if(jQuery.isEmptyObject($('#id_correo2').val())){
                            if(!validarEmail(correo)){
                                 $("#id-error-correo").html('<p class="small_error_letter"> El correo del usuario debe ser válido<i class="fa fa-times-circle-o fa-lg"></i> </p>');
                                 // console.log("adasd");
                                 
                            } else {
                                document.getElementById("id_correo_electronico").style.borderColor = "";
                                $("#id-error-correo").html('');
                                
                            }
                            // $("#id-error-correo").html('<i class="fa fa-check-circle-o fa-lg" style="color:#14D100"></i>');
                        }
                        $("#id_correo2").prop('readonly',false)
                       
                    }
                    
                },
                error: function(results){
                    console.log("ERROR");
                }
            });
        

    }else{
        document.getElementById("id_correo_electronico").style.borderColor = "#E34234";

        if (jQuery.isEmptyObject($('#id_correo_electronico').val())){
            $("#id-error-correo").html('<p class="small_error_letter"> Este campo no puede estar vacio <i class="fa fa-times-circle-o fa-lg"></i> </p>');
            block_correo2()
        } else{
            if(!validarEmail(correo)){
                $("#id-error-correo").html('<p class="small_error_letter"> El correo del usuario debe ser válido<i class="fa fa-times-circle-o fa-lg"></i> </p>');
            } 
        }
    }

}

function consulta_cedula_usuario(cedula){
    if(cedula.length){
        $.ajax({
                type: 'GET' ,
                url: '/registro/verificar_cedula_usuario' , // <= Providing the URL
                data:{
                    'cedula': cedula,
                },
                success: function(results){
                    if(results.Result=='ocupado'){
                        $("#id-error-cedula").html('<p class="small_error_letter"> La cedula ya se encuentra registrada. Por favor verificarla. <i class="fa fa-times-circle-o fa-lg"></i> </p>');
                        return false
                    }
                    if (results.Result=='libre'){
                        $("#id-error-cedula").html('<i class="fa fa-check-circle-o fa-lg" style="color:#14D100"></i>');
                        return true
                    }
                    
                },
                error: function(results){
                    console.log("ERROR");
                }
            });
        

    }else{
        $("#id-error-cedula").html('<p class="small_error_letter"> El campo de cedula no puede quedar vacio.<i class="fa fa-times-circle-o fa-lg"></i> </p>');
    }
}


$('#id_username').focusout(function(){
    usuario = $('#id_username').val()
    if (usuario){
        consulta_nombre_usuario(usuario)
        
    }else{
        $("#id-error-username").html('<p class="small_error_letter"> El nombre de usuario debe ser válido<i class="fa fa-times-circle-o"></i> </p>');
    }
})

$('#id_cedula').focusout(function(){
    cedula = $('#id_cedula').val()
    if (cedula){
        consulta_cedula_usuario(cedula)
        
    }else{
        $("#id-error-cedula").html('<p class="small_error_letter"> El campo de correo no puede quedar vácio<i class="fa fa-times-circle-o"></i> </p>');
    }
})


$("#id_correo_electronico").attr('onblur',"confirmEmail2();");
$("#id_correo_electronico").attr("autocomplete","off");


function confirmEmail() {
    var email = document.getElementById("id_correo_electronico").value;
    var confemail = document.getElementById("id_correo2").value;
    consulta_correo_usuario(email)
    valido = false


    if(!jQuery.isEmptyObject($('#id_correo2').val())){

        if(email != confemail) {

            document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
            document.getElementById("id_correo2").style.borderColor = "#E34234";
            //id_correo2.focus();
            $("#id-error-confirm-email").html('<p class="small_error_letter"> El correo de confirmación no es igual al correo principal <i class="fa fa-times-circle-o fa-lg"></i> </p>');
            // alert('El correo de confirmacion no es igual al correo principal');


        }else{

            if(confemail.length!=0){
                if(!validarEmail(email)){
                    document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                    document.getElementById("id_correo2").style.borderColor = "#E34234";
                    //id_correo2.focus();
                    $("#id-error-confirm-email").html('<p class="small_error_letter"> El correo debe ser válido <i class="fa fa-times-circle-o fa-lg"></i> </p>');
                    // alert('El correo de confirmacion no es igual al correo principal');
                }else{
                        // console.log("SOY JURIDICO EN confirmEmail<<");
                        document.getElementById("id_correo_electronico").style.borderColor = "#14D100";
                        document.getElementById("id_correo2").style.borderColor = "#14D100";
                        $("#id-error-confirm-email").empty();
                        $("#id-error-correo").empty();
                        $("#id-error-confirm-email").html('<i class="fa fa-check-circle-o fa-lg" style="color:#14D100"></i>');
                        valido = true
                    
                }
            }
        }
    }
    else {
        document.getElementById("id_correo2").style.borderColor = "#E34234";
        if (jQuery.isEmptyObject($('#id_correo2').val())){
            $("#id-error-confirm-email").html('<p class="small_error_letter"> Este campo no puede estar vacio <i class="fa fa-times-circle-o fa-lg"></i> </p>');
            
        } else{
            if(!validarEmail(confemail)){
                $("#id-error-confirm-email").html('<p class="small_error_letter"> El correo del usuario debe ser válido<i class="fa fa-times-circle-o fa-lg"></i> </p>');
            } 
        }
        // $("#id-error-confirm-email").html('<p class="small_error_letter"> Este campo no puede estar vacio <i class="fa fa-times-circle-o fa-lg"></i> </p>');

    }
    return valido
}

function confirmEmail2() {
    var email = document.getElementById("id_correo_electronico").value;
    var confemail = document.getElementById("id_correo2").value;

    // verificar si el correo ya esta siendo usado por otro usuario 
    consulta_correo_usuario(email)
    valido = false

    if(!jQuery.isEmptyObject($('#id_correo_electronico').val())){
    
        if(email == confemail) {
            if(confemail.length!=0){
                if(validarEmail(email)){
                        
                   // console.log("SOY JURIDICO EN confirmEmail2");
                    document.getElementById("id_correo_electronico").style.borderColor = "#14D100";
                    document.getElementById("id_correo2").style.borderColor = "#14D100";
                    $("#id-error-confirm-email").html('<i class="fa fa-check-circle-o fa-lg" style="color:#14D100"></i>');
                    valido = true
                

                }else{

                    document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                    document.getElementById("id_correo2").style.borderColor = "#E34234";
                    //id_correo2.focus();
                    $("#id-error-confirm-email").html('<p class="small_error_letter"> El correo debe ser valido <i class="fa fa-times-circle-o fa-lg"></i> </p>');

                }
            }else{

                if(!validarEmail(email)){

                    document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                    document.getElementById("id_correo2").style.borderColor = "#E34234";

                    $("#id-error-correo").html('<p class="small_error_letter"> El correo debe ser válido <i class="fa fa-times-circle-o fa-lg"></i> </p>');
                }
            }

        } else {
            if(confemail.length!=0){
                document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                document.getElementById("id_correo2").style.borderColor = "#E34234";
                // id_correo2.focus();
               $("#id-error-confirm-email").html('<p class="small_error_letter"> El correo de confirmación no es igual al correo principal  <i class="fa fa-times-circle-o fa-lg"></i> </p>');

            }
        }

        if(!validarEmail(email)){
            document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
            // document.getElementById("id_correo2").style.borderColor = "#E34234";

            $("#id-error-correo").html('<p class="small_error_letter"> El correo debe ser válido <i class="fa fa-times-circle-o fa-lg"></i> </p>');
        }

    } else {
        document.getElementById("id_correo2").style.borderColor = "#E34234";
        if (jQuery.isEmptyObject($('#id_correo_electronico').val())){
            $("#id-error-correo").html('<p class="small_error_letter"> Este campo no puede estar vacio <i class="fa fa-times-circle-o fa-lg"></i> </p>');
            
        } else{
            if(!validarEmail(email)){
                $("#id-error-correo").html('<p class="small_error_letter"> El correo del usuario debe ser válido<i class="fa fa-times-circle-o fa-lg"></i> </p>');
            } 
        }
        // document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
        // $("#id-error-correo").html('<p class="small_error_letter"> Este asdasdcampo no puede estar vacio <i class="fa fa-times-circle-o fa-lg"></i> </p>');

    }
    return valido
}

function validar_campos(){

    // if inspector{
        validar_campos_vacios_inspector()
    // }
}


function validar_campos_vacios_inspector(){

    correo = $('#id_correo_electronico').val()
    conf_correo = $('#id_correo2').val()
    password = $('#id_password').val()
    conf_password = $('#id_password_confirm').val()
    usuario = $('#id_username').val()
    cedula = $('#id_cedula').val()
    nombre = $('#id_nombre').val()
    apellido = $('#id_apellido').val()
    validar_email1 = confirmEmail2()
    validar_email2 = confirmEmail()
    validar_password = validarPassword(password)
    console.log("validar_email1");
    console.log(validar_email1);
    
    console.log("validar_email2");
    console.log(validar_email2);
    

    // 
// 
    if( (correo == "") || (conf_correo == "") || (password == "") || (conf_password == "") || (usuario == "") || (cedula == "") || (nombre == "") || (apellido == "")){
        console.log("Hay errores!");
        $('#id_submit_registro').html('<center><p class="small_error_letter"> Hay errores en el formulario de registro, favor verificar información suministrada. <i class="fa fa-times-circle-o fa-lg"></i> </p></center>')

        if(jQuery.isEmptyObject($('#id_nombre').val())){
            no_vacio_error("id-error-nombre")
        }

        if(jQuery.isEmptyObject($('#id_apellido').val())){
            no_vacio_error("id-error-apellido")
        }


        if(es_vacio("id_password")){
            no_vacio_error("id-error-password")
        }

        if(es_vacio("id_password_confirm")){
            no_vacio_error("id-error-confirm-pass-recover")
        }







    } else {
        if(validar_email1 && validar_email2 && validar_password){
            console.log("a guardar");
            
        }
        else {
            $('#id_submit_registro').html('<center><p class="small_error_letter"> Hay errores en el formulario de registro, favor verificar información suministrada. <i class="fa fa-times-circle-o fa-lg"></i> </p></center>')
        }
        // console.log("Yay!");
        
    }




}

function guardar_usuario(){

    correo = $('#id_correo_electronico').val()
    conf_correo = $('#id_correo2').val()
    password = $('#id_password').val()
    conf_password = $('#id_password_confirm').val()

    correos_iguales = correo == conf_correo ? true : false;
    passwords_iguales = password == conf_password ? true : false;

    if(correos_iguales && passwords_iguales) {


    }else {
        $('#id_submit_registro').html('<center><p class="small_error_letter"> Hay errores en el formulario de registro, favor verificar información suministrada. <i class="fa fa-times-circle-o fa-lg"></i> </p></center>')
    }

    

}






function processForm(e) {

    $(document).ajaxStop($.unblockUI);

    if (e.preventDefault) e.preventDefault();

    var theData = $("#registro_form").serializeArray();

    // si no son iguales no realizar el ajax pass & email & email2
    var pass1 = document.getElementById("id_password").value;
    var pass2 = document.getElementById("id_password_confirm").value;
    var email = document.getElementById("id_correo_electronico").value;
    var email2 = document.getElementById("id_correo_secundario").value;
    var confemail = document.getElementById("id_correo2").value;
    var rif = document.getElementById("id_rif").value;
    var correoInst= false;

    if((rif[0]=='V')||(rif[0]=='P')||(rif[0]=='E')){
        if(validarEmailGob(email)|| validarEmailGob(email2)){
            correoInst=true;
        }
    }

    if((pass1==pass2)&&(email==confemail)&&(email!=email2)&& !preguntas_vacias() &&(!correoInst)){

        //Comprobando que el correo no sea institucional
        email = email.toLowerCase();
        email2 = email2.toLowerCase();

        var aux1=-1;
        var aux2=-1;
        var aux3=-1;
        var aux4=-1;

        if ((rif[0]=='V')||(rif[0]=='P')||(rif[0]=='E')){
            aux1=email.search(".gob.ve");
            aux2=email2.search(".gob.ve");
            aux3=email.search(".gov.ve");
            aux4=email2.search(".gov.ve");
        }

        // if((aux1==-1)&&(aux2==-1)&&(aux3==-1)&&(aux4==-1)){


            $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });

            $(".form-usuario-error").html('');
            $(".persona-natural-error").html('');

            // console.log('ajax: registro de usuario');

            $.ajax({
                type:     "POST",
                url: "/registro/registro_natural", // <= Providing the URL
                data: theData, // <= Providing the form data, serialized above
                success: function(results){
                        //console.log('entra en ajax');
                        if(results.Result == 'success'){
                            $('#registroModal').modal('show');
                            $(".captcha-has-errors").html('');
                        }else if(results.Result == 'error'){
                            // $(".form-usuario-error").html('Datos invalidos en el formulario.');
                            $('#errorModal').modal('show'); // Texto al final de pagina "Datos invalidos en el formulario" cambiado por este modal
                            if (typeof results.formularios != 'undefined') {
                                if(results.form.length > 0){
                                    form=JSON.parse(results.form)
                                    $("#id-error-confirm-email").html('');
                                    if(form.correo_electronico){
                                        $("#id-error-correo").html(imprimir_error('El correo electronico ya ha sido registrado anteriormente'));
                                        $("#id_correo_electronico").css("border-bottom-color",'red');
                                        $("#id_correo_electronico").css("border-left-color",'red');
                                        $("#id_correo_electronico").css("border-right-color",'red');
                                        $("#id_correo_electronico").css("border-top-color",'red');

                                        $("#id_correo2").css("border-bottom-color",'red');
                                        $("#id_correo2").css("border-left-color",'red');
                                        $("#id_correo2").css("border-right-color",'red');
                                        $("#id_correo2").css("border-top-color",'red');
                                        $("#id-error-confirm-email").html('');
                                    }


                                    $("#id-correo2-error").html('');
                                    if(form.correo_secundario){
                                        $("#id-correo2-error").html(imprimir_error(form.correo_secundario));
                                        $("#id_correo_secundario").css("border-bottom-color",'red');
                                        $("#id_correo_secundario").css("border-left-color",'red');
                                        $("#id_correo_secundario").css("border-right-color",'red');
                                        $("#id_correo_secundario").css("border-top-color",'red');
                                        // $(".correo-secundario-error").htl('');
                                    }
                                }
                            }
                            // console.log('vacia');
                            $("#errores_pregunta").html('');
                            // console.log(results.preguntas);
                            if (results.preguntas) {

                                $("#errores_pregunta").html(imprimir_error("Debe responder todas las preguntas"))

                            }

                            if(typeof results.codigo_error != 'undefined')

                            if(results.codigo_error == '100'){
                                // Muestra error cuando la consulta al seniat retorn algun dato vacio para usuarios naturales
                                $(".persona-natural-error").html('<p style="color: #CE4744">'+results.message+'. <i class="fa fa-times-circle-o fa-lg"></i></p>');
                            }//else if(results.codigo_error == '101'){
                            //     // Validacion del correo electronico institucional (no puede ser institucional)
                            //     $(".correo-primario-error").html('<p>'+results.message+'<i class="fa fa-times-circle-o fa-lg"></i></p>');
                            //     document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                            //     document.getElementById("id_correo2").style.borderColor = "#E34234";
                            //     $("#id-error-confirm-email").html('<p> <i class="fa fa-times-circle-o fa-lg"></i> </p>');
                            // }
                            // TODO CAPTCHA decomentar
                            if(results.Message == 'InvalidCaptcha'){
                                $(".captcha-has-errors").html('<p>Captcha inválido <i class="fa fa-times-circle-o fa-lg"></i></p>');
                            
                                var $form = $('.captcha-refresh').parents('form');
                                var url = location.protocol + "//" + window.location.hostname + ":"
                                          + location.port + "/captcha/refresh/";
                            
                                // Make the AJAX-call
                                $.getJSON(url, {}, function(json) {
                                    $form.find('input[name="captcha_0"]').val(json.key);
                                    $form.find('img.captcha').attr('src', json.image_url);
                                });
                            }
                            //verifica invalid data
                            // if(results.Message == 'InvalidData'){
                            //     var obj = JSON.parse(results.form);
                            //     if(obj.apellido_denominacion_comercial[0] == 'El apellido es obligatorio para el registro en el sistema'){
                            //         $(".apellido_denominacion_comercial_errors").html('<p>Campo requerido <i class="fa fa-times-circle-o fa-lg"></i></p>');
                            //     }
                            // }
                            //verifica invalid data
                            if(results.Message == 'InvalidData'){
                                var obj = JSON.parse(results.form);
                                if( typeof obj.apellido_denominacion_comercial != 'undefined')
                                    if( typeof obj.apellido_denominacion_comercial[0] != 'undefined')
                                        if(obj.apellido_denominacion_comercial[0] == 'El apellido es obligatorio para el registro en el sistema'){
                                            $(".apellido_denominacion_comercial_errors").html('<p>Campo requerido <i class="fa fa-times-circle-o fa-lg"></i></p>');
                                        }
                            }

                            //Verificando correo
                            if (results.Message == 'Correo1Invalido') {

                                $(".correo-primario-error").html('<p>El dominio del correo principal no existe, ingrese un dominio valido. <i class="fa fa-times-circle-o fa-lg"></i></p>');
                                document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                                document.getElementById("id_correo2").style.borderColor = "#E34234";
                                $("#id-error-confirm-email").html('<p> <i class="fa fa-times-circle-o fa-lg"></i> </p>');

                            }
                            if (results.Message == 'AmbosCorreosInvalidos') {

                                $(".correo-primario-error").html('<p>El dominio del correo principal no existe, ingrese un dominio valido. <i class="fa fa-times-circle-o fa-lg"></i></p>');
                                $(".correo-secundario-error").html('<p>El dominio del correo secundario no existe, ingrese un domino valido. <i class="fa fa-times-circle-o fa-lg"></i></p>');

                                $("#id-error-confirm-email").html('<p> <i class="fa fa-times-circle-o fa-lg"></i> </p>');

                                document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                                document.getElementById("id_correo2").style.borderColor = "#E34234";
                                document.getElementById("id_correo_secundario").style.borderColor = "#E34234";

                            }
                            if (results.Message == 'Correo2Invalido') {
                                $(".correo-secundario-error").html('<p>El dominio del correo secundario no existe, ingrese un dominio correo valido. <i class="fa fa-times-circle-o fa-lg"></i></p>');
                                document.getElementById("id_correo_secundario").style.borderColor = "#E34234";
                            }
                            if (results.codigo_error == 'CORREO_INVALIDO'){
                                $(".correo-primario-error").html('<p>El correo es inválido, ingrese uno válido. <i class="fa fa-times-circle-o fa-lg"></i></p>');
                                document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                                document.getElementById("id_correo2").style.borderColor = "#E34234";
                                $("#id-error-confirm-email").html('<p>El correo es inválido, ingrese uno válido. <i class="fa fa-times-circle-o fa-lg"></i> </p>');
                                // console.log('LLEGO AQUI');
                            }
                            //FIN Verificando correo


                        }
                },
                        //}
                    //},
                error: function(results){
                        console.log("ERROR");
                }
            });

        // }else{
        //     console.log('HAY UN CORREO INSTITUCIONAL')
        // }
        //FIN DE NO INSTITUCIONAL

    }else{
        $('#errorModal2').modal('show');
    }
    return false;
}




/***
 * fin
 **/



 //# TODO CAPTCHA decomentar
// $(function() {

//     // if ($('#captcha_engine').attr('value') == true){
//     //     console.log('captcha engine true');
//     // }else{
//     //     console.log('captcha engine false');
//     //     console.log($('#captcha_engine').attr('value'));
//     // }

//     // Add refresh button after field (this can be done in the template as well)
//     $('img.captcha').after(
//             $('<a href="#void" class="fa fa-refresh captcha-refresh" title="Da click para cambiar la imagen"></a><br><br>')
//             );

//     // Click-handler for the refresh-link
//     $('.captcha-refresh').click(function(){
//         var $form = $(this).parents('form');
//         var url = location.protocol + "//" + window.location.hostname + ":"
//                   + location.port + "/captcha/refresh/";

//         // Make the AJAX-call
//         $.getJSON(url, {}, function(json) {
//             $form.find('input[name="captcha_0"]').val(json.key);
//             $form.find('img.captcha').attr('src', json.image_url);
//         });

//         return false;
//     });
// });
/***
 * fin
 **/
