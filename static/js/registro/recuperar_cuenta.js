

function recuperar_cuenta(){

	$(document).ajaxStop($.unblockUI);
	$.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	dataForm = $("#id_post_recuperar_cuenta").serializeArray();
	$.ajax({
	        type: 'POST' ,
	        url: '/registro/restaurar_cuenta' , // <= Providing the URL
	        data: dataForm , // <= Providing the form data, serialized above
	        success: function(results){
	         if(results.Result == 'success'){
	         	titulo = 'RECUPERAR CONTRASEÑA'
                subtitulo = 'Recuperación de contraseña realizada exitosamente'
                mensaje = "La información de usuario y contraseña fue enviada a su correo."
                show_modal_exito(titulo,subtitulo,mensaje)
					

	            }
	        else {
	            if(results.Result == 'error'){
                	console.log("results.mensaje");
                	console.log(results.mensaje);
	                if(results.ERROR_CODE == "NO_MAIL_SEND")
	                    show_modal_errores_personalizado(results.mensaje)
	                    
	                }

	                if(results.ERROR_CODE == "DATOS_INVALIDOS"){
	                   	show_modal_errores_personalizado(results.mensaje)
	                    
	                }
	            }
	        },
	        error: function(results){
	            console.log("ERROR");
	        }
	    });
	

}