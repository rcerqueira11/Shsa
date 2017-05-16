
var url_elim_sol 
$(document).on("click",".eliminar_boton", function(){   
	url_elim_sol = $(this).attr('data-ref')
});


$(document).on('show.bs.modal','#modal-verificacion-eliminar', function () {
	// console.log("$(this).attr('data-ref'):",url_elim_sol);
    titulo = 'CONFIRMACIÓN'
    subtitulo = 'Cancelar Solcitud'
    mensaje = '¿Esta seguro que desea cancela esta solicitud?'
    fill_modal_verificacion_eliminar(titulo,subtitulo,mensaje)
})



$(document).on("click",".confirmar_eliminacion", function(){   
    $("#modal-verificacion-eliminar").modal("hide");
    cancelar_solictud(url_elim_sol)
    
});

function cancelar_solictud(url){
	$(document).ajaxStop($.unblockUI);
    $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	$.ajax({
            type: 'GET' ,
            url: url , // <= Providing the URL
            // data: dataForm , // <= Providing the form data, serialized above
            success: function(results){
             if(results.results == 'success'){
                    titulo = 'SOLICITUDES'
                    subtitulo = 'Cancelar Solicitud'
                    mensaje = 'La solicitud fue cancelada exitosamente.' 

                   fill_modal_exito_eliminar(titulo,subtitulo,mensaje)
                   $("#filter_form_id").submit();
	                $("#modal-exito-eliminar").modal('show');
                }
               
            },
            error: function(results){
                $('#modal-error').modal('show')
                console.log("ERROR");
            }
        });
	
}