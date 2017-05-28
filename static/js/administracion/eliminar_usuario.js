
var url_elim_sol 
$(document).on("click",".eliminar_boton", function(){   
	url_elim_sol = $(this).attr('data-ref')
	console.log("url_elim_sol:",url_elim_sol);
	
});


$(document).on('show.bs.modal','#modal-verificacion-eliminar', function () {
    titulo = 'CONFIRMACIÓN'
    subtitulo = 'Eliminar Usuario'
    mensaje = '¿Esta seguro que desea eliminar este usuario?'
    fill_modal_verificacion_eliminar(titulo,subtitulo,mensaje)
})



$(document).on("click",".confirmar_eliminacion", function(){   
    $("#modal-verificacion-eliminar").modal("hide");
    eliminar_usuario(url_elim_sol)
    
});

function eliminar_usuario(url){
	// $(document).ajaxStop($.unblockUI);
    // $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
    dataForm = $("#id_csrf").serializeArray();
    dataForm.push({name:'usuario_id', value:url_elim_sol});
	$.ajax({
            type: 'POST' ,
            url: '/administracion/eliminar_usuario/' , // <= Providing the URL
            data: dataForm , // <= Providing the form data, serialized above
            success: function(results){
             if(results.results == 'success'){
				titulo = 'USUARIOS'
				subtitulo = 'Usuario Eliminado'
				mensaje = 'El usuario ha sido eliminado exitosamente.' 

				fill_modal_exito_eliminar(titulo,subtitulo,mensaje)
				$("#filter_form_id").submit();
				$("#modal-exito-eliminar").modal('show');
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