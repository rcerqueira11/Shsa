
var inactivar_id 

// modales INACTIVAR
$(document).on("click",".inactivar_boton", function(){   
	inactivar_id = $(this).attr('data-ref')
	
});


$(document).on('show.bs.modal','#modal-verificacion-inactivar', function () {
    titulo = 'CONFIRMACIÓN'
    subtitulo = 'Desactivar Usuario'
    mensaje = '¿Esta seguro que desea desactivar este usuario?'
    fill_modal_verificacion_inactivar(titulo,subtitulo,mensaje)
})



$(document).on("click",".confirmar_inactivacion", function(){   
    $("#modal-verificacion-inactivar").modal("hide");
    inactivar_usuario(inactivar_id)
    
});

// modales INACTIVAR
// modales ACTIVAR

$(document).on("click",".activar_boton", function(){   
	inactivar_id = $(this).attr('data-ref')
	
});


$(document).on('show.bs.modal','#modal-verificacion-activar', function () {
    titulo = 'CONFIRMACIÓN'
    subtitulo = 'Activar Usuario'
    mensaje = '¿Esta seguro que desea activar este usuario?'
    fill_modal_verificacion_activar(titulo,subtitulo,mensaje)
})



$(document).on("click",".confirmar_activacion", function(){   
    $("#modal-verificacion-activar").modal("hide");
    inactivar_usuario(inactivar_id)
    
});
// modales ACTIVAR

function inactivar_usuario(url){
	// $(document).ajaxStop($.unblockUI);
    // $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
    dataForm = $("#id_csrf").serializeArray();
    dataForm.push({name:'usuario_id', value:inactivar_id});
	$.ajax({
            type: 'POST' ,
            url: '/administracion/inactivar_usuario/' , // <= Providing the URL
            data: dataForm , // <= Providing the form data, serialized above
            success: function(results){
             if(results.results == 'success'){
				titulo = 'USUARIOS'

             	if (results.tipo == "ACT"){

                    subtitulo = 'Usuario Activado'
                    mensaje = 'El usuario ha sido activado exitosamente.' 
                    fill_modal_exito_activar(titulo,subtitulo,mensaje)
                    $("#modal-exito-activar").modal('show');
                } 
                if(results.tipo == "INACT"){

                    subtitulo = 'Usuario Inactivado'
                    mensaje = 'El usuario ha sido inacitvado exitosamente.' 
                    fill_modal_exito_inactivar(titulo,subtitulo,mensaje)
                    $("#modal-exito-inactivar").modal('show');
                }

				$("#filter_form_id").submit();
                }
            else{
            	show_modal_errores_personalizado(results.mensaje)
            }
               
            },
            error: function(results){
                show_modal_errores_personalizado("Ocurrio un error favor intentarlo mas tarde.")
                console.log("ERROR");
            }
        });
	
}