
$('#modal-verificacion').on('shown.bs.modal', function (e) {
    titulo = 'CONFIRMACIÓN'
	subtitulo = 'Creación de solicitud de inspección'
	mensaje = '¿Esta seguro que desea crear esta solicitud de inspección?'
	fill_modal_verificacion(titulo,subtitulo,mensaje)
})



$(document).on("click",".confirmar_verificacion", function(){	
	$("#modal-verificacion").modal("hide");
 	submit_form_crear_solicitud()
	
});

$('#modal-exito').on('shown.bs.modal', function (e) {
    titulo = 'SOLICITUD DE INSPECCIÓN'
	subtitulo = 'Creación de solicitud de inspección'
	mensaje = 'Solicitud de inspección creada exitosamente.'
	fill_modal_exito(titulo,subtitulo,mensaje)
	
})


$( document ).ready(function() {
	if ($('input[name=radio_titular]:checked', '#form_crear_ticket').val() == undefined){
		$("#radio_si").prop('checked',true)
	}
    valor_radio = $('input[name=radio_titular]:checked', '#form_crear_ticket').val()
    if (valor_radio == "false"){
    	$("#id_trajo_form").show('slide')
    }else{
    	$("#id_trajo_form").hide()

    }
});



$('#form_crear_ticket input[name=radio_titular]').on('change', function() {
   valor_radio = $('input[name=radio_titular]:checked', '#form_crear_ticket').val()
    if (valor_radio == "false"){
    	$("#id_trajo_form").show('slide')
    }else{
    	$("#id_trajo_form").hide('slide')

    }
});



function submit_form_crear_solicitud(){

	$(document).ajaxStop($.unblockUI);
	$.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	var dataForm = $("#form_crear_ticket").serializeArray();
	url = $('#form_crear_ticket').attr('action')
	$.ajax({
	        type: 'POST' ,
	        url: url , // <= Providing the URL
	        data: dataForm , // <= Providing the form data, serialized above
	        success: function(results){
	                
	         // if(results.result == 'success'){
	
	         //    }
	         //    if(results.result == 'error'){
	         //        if(results.codigo_error == "SESSION_EXPIRE")
	         //                $('#expireModal').modal('show');
	         //        else{
	         //            console.log('error');
	                    
	         //        }
	         //    }
	         if (results['errors'] == undefined){
                      // $(document).ajaxStop($.unblockUI);
                      $("#modal-exito").modal('show');               
                  }
                  if(results['errors'] != undefined){
                      for (key in results['errors']){
						  console.log(key)
						  console.log(results['errors'][key])
						  $('#'+key+"_error").html(results['errors'][key])
						}
                  }
	        },
	        error: function(results){
	        	$('#modal-error').modal('show')
	            console.log("ERROR");
	        }
	    });
}