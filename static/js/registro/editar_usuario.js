$("#id_correo2").prop('readonly',true)

function block_correo2(){
    $("#id_correo2").prop('readonly',true)
    $("#id_correo2").val("")
    document.getElementById("id_correo2").style.borderColor = "";
    $("#id-error-confirm-email").html('');
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

    correo = $('#id_correo_electronico').val()
    conf_correo = $('#id_correo2').val()
    password = $('#id_password').val()
    conf_password = $('#id_password_confirm').val()
    validar_email1 = confirmEmail2()
    validar_email2 = confirmEmail()
    validar_password = validarPassword(password)
    console.log("validar_email1");
    console.log(validar_email1);
    
    console.log("validar_email2");
    console.log(validar_email2);
    
    correos_iguales = correo == conf_correo ? true : false;

    passwords_iguales = password == conf_password ? true : false;

	correo_vacio = es_vacio('id_correo_electronico')

	password_vacio = es_vacio('id_password')


    if(correos_iguales || passwords_iguales) {

    	correo_vacio = es_vacio('id_correo_electronico')
    	
		password_vacio = es_vacio('id_password')

		if(!password_vacio || !correo_vacio){    	


		} else {
			

		}
    }
    // 
// 
    if( ){
        console.log("Hay errores!");
        // $('#id_submit_registro').html('<center><p class="small_error_letter"> Hay errores en el formulario de registro, favor verificar información suministrada. <i class="fa fa-times-circle-o fa-lg"></i> </p></center>')
        show_modal_errores()


        if
        if(es_vacio("id_password")){
            no_vacio_error("id-error-password")
        }

        if(es_vacio("id_password_confirm")){
            no_vacio_error("id-error-confirm-pass-recover")
        }

        






    } else {
        if(validar_email1 && validar_email2 && validar_password){
            console.log("a guardar");
            guardar_usuario()
            
        }
        else {
            // $('#id_submit_registro').html('<center><p class="small_error_letter"> Hay errores en el formulario de registro, favor verificar información suministrada. <i class="fa fa-times-circle-o fa-lg"></i> </p></center>')
            show_modal_errores()
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


    if () {} else {}

    if(correos_iguales || passwords_iguales) {

		correo_vacio = es_vacio('id_correo_electronico')
    	
		password_vacio = es_vacio('id_password')

		if(!password_vacio || !correo_vacio){

	        $(document).ajaxStop($.unblockUI);
	        $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	        var theData = $("#id_form_editar_usuario").serializeArray();

	        $.ajax({
	                type: 'POST' ,
	                url: 'registro/editar_cuenta' , // <= Providing the URL
	                data: theData , // <= Providing the form data, serialized above
	                success: function(results){
	                 if(results.Result == 'success'){
	                        titulo = ' EDICIÓN DE USUARIO'
	                        subtitulo = 'Edición de usuario realizado exitosamente'
	                        mensaje = results.mensaje
	                        show_modal_exito(titulo,subtitulo,mensaje)
	        
	                    }
	                    if(results.Result == 'error'){
	                        show_modal_errores()
	                    }
	                },
	                error: function(results){
	                    console.log("ERROR");
	                    show_modal_errores()
	                }
	            });


		}
		else{
        	show_modal_errores()
        	console.log("No hay nada que guardar");
        	
			
		}	        


    }else {
        // $('#id_submit_registro').html('<center><p class="small_error_letter"> Hay errores en el formulario de registro, favor verificar información suministrada. <i class="fa fa-times-circle-o fa-lg"></i> </p></center>')
        show_modal_errores()
    }

    

}

