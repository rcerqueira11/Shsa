
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
	         if (results['results'] == "success"){
	                  // $(document).ajaxStop($.unblockUI);
	                  $("#modal-exito").modal('show');               
	              }
			if(results['results']=="error"){

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
$("#id_cedula_titular").on('focusout',function(){
	cedula = this.value

	if (cedula != ""){
	// $(document).ajaxStop($.unblockUI);
	// $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	$.ajax({
	        type: 'GET' ,
	        url: '/rcs/verificar_cedula_titular_existe' , // <= Providing the URL
	        data: jQuery.param({'cedula':cedula}) , // <= Providing the form data, serialized above
	        success: function(results){
		        if(results.results == 'success'){
					$("#id_nombre_titular").val(results.nombre)
					$("#id_apellido_titular").val(results.apellido)
					$("#id_telefono_titular").val(results.telefono)
					$("#id_nombre_titular").prop('readonly', true);
					$("#id_apellido_titular").prop('readonly', true);
					$("#id_telefono_titular").prop('readonly', true);
	                
	            }else{
	            	$("#id_nombre_titular").prop('readonly', false);
					$("#id_apellido_titular").prop('readonly', false);
					$("#id_telefono_titular").prop('readonly', false);	
					$("#id_nombre_titular").val('')
					$("#id_apellido_titular").val('')
					$("#id_telefono_titular").val('')
	            }
	            
	        },
	        error: function(results){
	            console.log("ERROR");
	        }
	    });
	}

})
// function verificar_trajo_cedula(cedula){

$("#id_cedula_trajo_vehiculo").on('focusout',function(){
	cedula = this.value
	// $(document).ajaxStop($.unblockUI);
	// $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	if (cedula != ""){

	$.ajax({
	        type: 'GET' ,
	        url: '/rcs/verificar_cedula_trajo_existe' , // <= Providing the URL
	        data: jQuery.param({'cedula':cedula}) , // <= Providing the form data, serialized above
	        success: function(results){
		        if(results.results == 'success'){
					$("#id_nombre_trajo").val(results.nombre)
					$("#id_apellido_trajo").val(results.apellido)
					$("#id_parentesco_trajo").val(results.parentesco)
					$("#id_nombre_trajo").prop('readonly', true);
					$("#id_apellido_trajo").prop('readonly', true);
					$("#id_parentesco_trajo").prop('readonly', true);
	                
	            }else{
	            	$("#id_nombre_trajo").prop('readonly', false);
					$("#id_apellido_trajo").prop('readonly', false);
					$("#id_parentesco_trajo").prop('readonly', false);	
					$("#id_nombre_trajo").val('')
					$("#id_apellido_trajo").val('')
					$("#id_parentesco_trajo").val('')
	            }
	            
	        },
	        error: function(results){
	            console.log("ERROR");
	        }
	    });
	}
})

$("#id_placa").on('focusout',function(){
	placa = this.value
	// $(document).ajaxStop($.unblockUI);
	// $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	if (placa != ""){
	$.ajax({
	        type: 'GET' ,
	        url: '/rcs/verificar_placa_carro_existe' , // <= Providing the URL
	        data: jQuery.param({'placa':placa}) , // <= Providing the form data, serialized above
	        success: function(results){
		        if(results.results == 'success'){
					$("#id_nombre_titular").val(results.nombre)
					$("#id_apellido_titular").val(results.apellido)
					$("#id_telefono_titular").val(results.telefono)
					$("#id_cedula_titular").val(results.cedula)
					$("#id_cedula_titular").prop('readonly', true);
					$("#id_nombre_titular").prop('readonly', true);
					$("#id_apellido_titular").prop('readonly', true);
					$("#id_telefono_titular").prop('readonly', true);
	                
	            }else{
	    //         	$("#id_nombre_titular").prop('readonly', false);
					// $("#id_apellido_titular").prop('readonly', false);
					// $("#id_telefono_titular").prop('readonly', false);	
					// $("#id_cedula_titular").prop('readonly', false);
					validar_cedula_onfocus_placa()
					// $("#id_nombre_titular").val('')
					// $("#id_apellido_titular").val('')
					// $("#id_telefono_titular").val('')
					// $("#id_cedula_titular").val('')
	            }
	            
	        },
	        error: function(results){
	            console.log("ERROR");
	        }
	    });
	}

})



function validar_cedula_onfocus_placa(){
	cedula = $("#id_cedula_trajo_vehiculo").val()
	$("#id_cedula_titular").prop('readonly', false);
	// $(document).ajaxStop($.unblockUI);
	// $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	if (cedula != ""){

	$.ajax({
	        type: 'GET' ,
	        url: '/rcs/verificar_cedula_trajo_existe' , // <= Providing the URL
	        data: jQuery.param({'cedula':cedula}) , // <= Providing the form data, serialized above
	        success: function(results){
		        if(results.results == 'success'){
					$("#id_nombre_trajo").val(results.nombre)
					$("#id_apellido_trajo").val(results.apellido)
					$("#id_parentesco_trajo").val(results.parentesco)
					$("#id_nombre_trajo").prop('readonly', true);
					$("#id_apellido_trajo").prop('readonly', true);
					$("#id_parentesco_trajo").prop('readonly', true);
	                
	            }else{
	            	$("#id_nombre_trajo").prop('readonly', false);
					$("#id_apellido_trajo").prop('readonly', false);
					$("#id_parentesco_trajo").prop('readonly', false);	
					$("#id_nombre_trajo").val('')
					$("#id_apellido_trajo").val('')
					$("#id_parentesco_trajo").val('')
	            }
	            
	        },
	        error: function(results){
	            console.log("ERROR");
	        }
	    });
	}
}