$('#modal-verificacion').on('shown.bs.modal', function (e) {
    titulo = 'CONFIRMACIÓN'
	subtitulo = 'Finalizar inspección'
	mensaje = '¿Esta seguro que desea terminar la inspección?'
	fill_modal_verificacion(titulo,subtitulo,mensaje)
})



$(document).on("click",".confirmar_verificacion", function(){	
	$("#modal-verificacion").modal("hide");
 	submit_form_completar_solicitud()
	
});

$('#modal-exito').on('shown.bs.modal', function (e) {
    titulo = 'INSPECCIÓN'
	subtitulo = 'Finalizar inspección'
	mensaje = 'Inspección realizada exitosamente.'
	fill_modal_exito(titulo,subtitulo,mensaje)
	
})



function submit_form_completar_solicitud(){


	// $(document).ajaxStop($.unblockUI);
	// $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	var data = $("#form_completar_solicitud").serializeArray();
	url= $("#form_completar_solicitud").attr('action')
	$.ajax({
	        type: 'POST' ,
	        url: url, // <= Providing the URL
	        data: data , // <= Providing the form data, serialized above
	        success: function(results){
	         if(results.results == 'success'){
	
	                $("#modal-verificacion").modal('hide');
	                $("#modal-exito").modal('show');
	            }
	            if(results.Result == 'error'){
	                if(results.codigo_error == "SESSION_EXPIRE")
	                        $('#expireModal').modal('show');
	                else{
	                    console.log('error');
	                    
	                }
	            }
	        },
	        error: function(results){
	            console.log("ERROR");
	        }
	    });
	


}