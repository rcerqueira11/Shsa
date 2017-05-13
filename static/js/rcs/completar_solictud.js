var estado_sol = $("#id_estado_solicitud").val()

$('#modal-verificacion').on('shown.bs.modal', function (e) {
    titulo = 'CONFIRMACIÓN'
    if (estado_sol =="PEND_INSP"){
		subtitulo = 'Finalizar inspección'
		mensaje = '¿Esta seguro que desea terminar la inspección?'
    }
    else{
		subtitulo = 'Finalizar Gestión'
		mensaje = '¿Esta seguro que desea terminar de editar la inspección esta no podra volver a ser editada?'
    }
	fill_modal_verificacion(titulo,subtitulo,mensaje)
})

// PEND_GEST
// PEND_INSP

$(document).on("click",".confirmar_verificacion", function(){	
	$("#modal-verificacion").modal("hide");
 	submit_form_completar_solicitud()
	
});

$('#modal-exito').on('shown.bs.modal', function (e) {
    titulo = 'INSPECCIÓN'
	if (estado_sol =="PEND_INSP"){
	subtitulo = 'Inspección Finalizada'
	mensaje = 'Inspección realizada exitosamente.'
	}

	else{
		subtitulo = 'Edición Finalizada'
		mensaje = 'Gestión realizada exitosamente, la solicitud de inspección ha sido cerrada.'
	}
	fill_modal_exito(titulo,subtitulo,mensaje)
	
})



function submit_form_completar_solicitud(){


	$(document).ajaxStop($.unblockUI);
	$.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
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

					url = results.pdf_dir;
					console.log(url);
					link=document.createElement('a');
					link.href=url;
					window.open(link.href);
	            }
	            if(results.results == 'error'){
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