
$('#modal-verificacion').on('shown.bs.modal', function (e) {
    titulo = 'CONFIRMACIÓN'
	subtitulo = 'Edición Usuario'
	mensaje = '¿Esta seguro que desea cambiar la información de este Usuario?'
	fill_modal_verificacion(titulo,subtitulo,mensaje)
})



$(document).on("click",".confirmar_verificacion", function(){	
	$("#modal-verificacion").modal("hide");
 	submit_form_editar_usuario()
	
});

$('#modal-exito').on('shown.bs.modal', function (e) {
	href_aceptar = $('#id_href_modal_aceptar').attr('href')
    titulo = 'EDICIÓN USUARIO'
	subtitulo = 'Edición Usuario'
	mensaje = 'Edición del Usuario del sistema realizada exitosamente.'
	$("#modal-exito-href").attr("href", href_aceptar)
	fill_modal_exito(titulo,subtitulo,mensaje)
	
})



function submit_form_editar_usuario(){

	$(document).ajaxStop($.unblockUI);
	$.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	var dataForm = $("#form_editar_usuario").serializeArray();
	url = $('#form_editar_usuario').attr('action')
	$.ajax({
	        type: 'POST' ,
	        url: url , // <= Providing the URL
	        data: dataForm , // <= Providing the form data, serialized above
	        success: function(results){
	          
				if (results['results'] == "success"){
					$("#modal-exito").modal('show');               
				}
				if (results['results'] == "data_igual"){
					show_modal_errores_personalizado(results['mensaje'])           
				}
				if(results['errors']){
					$('.error').empty();
			        $.each(results['errors'], function(key, value){
			          $('#' + key + '_error').html(value);
			        });
					// show_modal_errores_personalizado(results['mensaje'])
				}
	        },
	        error: function(results){
	        	$('#modal-error').modal('show')
	            console.log("ERROR");
	        }
	    });
}



$("#id_correo_electronico").attr('onblur',"confirmEmail2();");
$("#id_correo_electronico").attr("autocomplete","off");


function confirmEmail() {
    var email = document.getElementById("id_correo_electronico").value;
    var confemail = document.getElementById("id_correo2").value;
    valido = false


    if(!jQuery.isEmptyObject($('#id_correo2').val())){

        if(email != confemail) {

            document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
            document.getElementById("id_correo2").style.borderColor = "#E34234";
            //id_correo2.focus();
            $("#email2_error").html('<p class="small_error_letter"> El correo de confirmación no es igual al correo principal <i class="fa fa-times-circle-o fa-lg"></i> </p>');
            // alert('El correo de confirmacion no es igual al correo principal');


        }else{

            if(confemail.length!=0){
                if(!validarEmail(email)){
                    document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                    document.getElementById("id_correo2").style.borderColor = "#E34234";
                    //id_correo2.focus();
                    $("#email2_error").html('<p class="small_error_letter"> El correo debe ser válido <i class="fa fa-times-circle-o fa-lg"></i> </p>');
                    // alert('El correo de confirmacion no es igual al correo principal');
                }else{
                        // console.log("SOY JURIDICO EN confirmEmail<<");
                        document.getElementById("id_correo_electronico").style.borderColor = "#14D100";
                        document.getElementById("id_correo2").style.borderColor = "#14D100";
                        $("#email2_error").empty();
                        $("#correo_electronico_error").empty();
                        $("#email2_error").html('<i class="fa fa-check-circle-o fa-lg" style="color:#14D100"></i>');
                        valido = true
                    
                }
            }
        }
    }
    else {
    	if(!es_vacio('id_correo_electronico')){

	        document.getElementById("id_correo2").style.borderColor = "#E34234";
	        if (jQuery.isEmptyObject($('#id_correo2').val())){
	            $("#email2_error").html('<p class="small_error_letter"> Este campo no puede estar vacio <i class="fa fa-times-circle-o fa-lg"></i> </p>');
	            
	        } else{
	            if(!validarEmail(confemail)){
	                $("#email2_error").html('<p class="small_error_letter"> El correo del usuario debe ser válido<i class="fa fa-times-circle-o fa-lg"></i> </p>');
	            } 
	        }
	        $("#email2_error").html('<p class="small_error_letter"> Este campo no puede estar vacio <i class="fa fa-times-circle-o fa-lg"></i> </p>');
    	} else {

        	valido = true
    	}
    }
    return valido
}

function confirmEmail2() {
    var email = document.getElementById("id_correo_electronico").value;
    var confemail = document.getElementById("id_correo2").value;

    // verificar si el correo ya esta siendo usado por otro usuario 
    valido = false

    if(!jQuery.isEmptyObject($('#id_correo_electronico').val())){
    
        if(email == confemail) {
            if(confemail.length!=0){
                if(validarEmail(email)){
                        
                   // console.log("SOY JURIDICO EN confirmEmail2");
                    document.getElementById("id_correo_electronico").style.borderColor = "#14D100";
                    document.getElementById("id_correo2").style.borderColor = "#14D100";
                    $("#email2_error").html('<i class="fa fa-check-circle-o fa-lg" style="color:#14D100"></i>');
                    valido = true
                

                }else{

                    document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                    document.getElementById("id_correo2").style.borderColor = "#E34234";
                    //id_correo2.focus();
                    $("#email2_error").html('<p class="small_error_letter"> El correo debe ser valido <i class="fa fa-times-circle-o fa-lg"></i> </p>');

                }
            }else{

                if(!validarEmail(email)){

                    document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                    document.getElementById("id_correo2").style.borderColor = "#E34234";

                    $("#correo_electronico_error").html('<p class="small_error_letter"> El correo debe ser válido <i class="fa fa-times-circle-o fa-lg"></i> </p>');
                }
            }

        } else {
            if(confemail.length!=0){
                document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
                document.getElementById("id_correo2").style.borderColor = "#E34234";
                // id_correo2.focus();
               $("#email2_error").html('<p class="small_error_letter"> El correo de confirmación no es igual al correo principal  <i class="fa fa-times-circle-o fa-lg"></i> </p>');

            }
        }

        if(!validarEmail(email)){
            document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
            // document.getElementById("id_correo2").style.borderColor = "#E34234";

            $("#correo_electronico_error").html('<p class="small_error_letter"> El correo debe ser válido <i class="fa fa-times-circle-o fa-lg"></i> </p>');
        }

    } else {
    	block_correo2()
        document.getElementById("id_correo_electronico").style.borderColor = "";

      	$("#email2_error").html('');

        // document.getElementById("id_correo2").style.borderColor = "#E34234";
        // if (jQuery.isEmptyObject($('#id_correo_electronico').val())){
        //     $("#correo_electronico_error").html('<p class="small_error_letter"> Este campo no puede estar vacio <i class="fa fa-times-circle-o fa-lg"></i> </p>');
            
        // } else{
        //     if(!validarEmail(email)){
        //         $("#correo_electronico_error").html('<p class="small_error_letter"> El correo del usuario debe ser válido<i class="fa fa-times-circle-o fa-lg"></i> </p>');
        //     } 
        // }
        valido = true
        // document.getElementById("id_correo_electronico").style.borderColor = "#E34234";
        // $("#correo_electronico_error").html('<p class="small_error_letter"> Este asdasdcampo no puede estar vacio <i class="fa fa-times-circle-o fa-lg"></i> </p>');

    }
    return valido
}












