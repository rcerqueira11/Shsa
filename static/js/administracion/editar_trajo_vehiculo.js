
$('#modal-verificacion').on('shown.bs.modal', function (e) {
    titulo = 'CONFIRMACIÓN'
	subtitulo = 'Edición persona Trajo el Vehículo'
	mensaje = '¿Esta seguro que desea cambiar la información de la persona que trajo el vehículo?'
	fill_modal_verificacion(titulo,subtitulo,mensaje)
})



$(document).on("click",".confirmar_verificacion", function(){	
	$("#modal-verificacion").modal("hide");
 	submit_form_editar_trajo_vehiculo()
	
});

$('#modal-exito').on('shown.bs.modal', function (e) {
    titulo = 'EDICIÓN PERSONA TRAJO EL VEHÍCULO'
	subtitulo = 'Edición persona Trajo el Vehículo'
	mensaje = 'Edición de quien trajo el vehículo realizada exitosamente.'
	fill_modal_exito(titulo,subtitulo,mensaje)
	
})



function submit_form_editar_trajo_vehiculo(){

	$(document).ajaxStop($.unblockUI);
	$.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	var dataForm = $("#form_editar_trajo_vehiculo").serializeArray();
	url = $('#form_editar_trajo_vehiculo').attr('action')
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



// function verificar_titular_cedula(cedula){
// $("#id_cedula_titular").on('focusout',function(){
// 	cedula = this.value

// 	if (cedula != ""){
// 	// $(document).ajaxStop($.unblockUI);
// 	// $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
// 	$.ajax({
// 	        type: 'GET' ,
// 	        url: '/rcs/verificar_cedula_titular_existe' , // <= Providing the URL
// 	        data: jQuery.param({'cedula':cedula}) , // <= Providing the form data, serialized above
// 	        success: function(results){
// 		        if(results.results == 'success'){
// 					$("#id_nombre_titular").val(results.nombre)
// 					$("#id_apellido_titular").val(results.apellido)
// 					$("#id_telefono_titular").val(results.telefono)
// 					$("#id_nombre_titular").prop('readonly', true);
// 					$("#id_apellido_titular").prop('readonly', true);
// 					$("#id_telefono_titular").prop('readonly', true);
	                
// 	            }else{
// 	            	$("#id_nombre_titular").prop('readonly', false);
// 					$("#id_apellido_titular").prop('readonly', false);
// 					$("#id_telefono_titular").prop('readonly', false);	
// 					$("#id_nombre_titular").val('')
// 					$("#id_apellido_titular").val('')
// 					$("#id_telefono_titular").val('')
// 	            }
	            
// 	        },
// 	        error: function(results){
// 	            console.log("ERROR");
// 	        }
// 	    });
// 	}

// })













