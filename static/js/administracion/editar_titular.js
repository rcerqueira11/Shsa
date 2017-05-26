
$('#modal-verificacion').on('shown.bs.modal', function (e) {
    titulo = 'CONFIRMACIÓN'
	subtitulo = 'Edición Titular de Vehículo'
	mensaje = '¿Esta seguro que desea cambiar la información de este Titular?'
	fill_modal_verificacion(titulo,subtitulo,mensaje)
})



$(document).on("click",".confirmar_verificacion", function(){	
	$("#modal-verificacion").modal("hide");
 	submit_form_editar_titular()
	
});

$('#modal-exito').on('shown.bs.modal', function (e) {
	href_aceptar = $('#id_href_modal_aceptar').attr('href')
    titulo = 'EDICIÓN TITULARES'
	subtitulo = 'Edición Titular de Vehículo'
	mensaje = 'Edición Titular de Vehículo realizada exitosamente.'
	$("#modal-exito-href").attr("href", href_aceptar)
	fill_modal_exito(titulo,subtitulo,mensaje)
	
})



function submit_form_editar_titular(){

	$(document).ajaxStop($.unblockUI);
	$.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	var dataForm = $("#form_editar_titular").serializeArray();
	url = $('#form_editar_titular').attr('action')
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
					show_modal_errores_personalizado(results['mensaje'])
				}
	        },
	        error: function(results){
	        	$('#modal-error').modal('show')
	            console.log("ERROR");
	        }
	    });
}















