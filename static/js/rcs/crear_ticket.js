$('#modal-verificacion').on('shown.bs.modal', function (e) {
    titulo = 'CONFIRMACIÓN'
	subtitulo = 'Creación de solicitud de inspección'
	mensaje = 'Esta seguro de crear esta solicitud de inspección.'
	fill_modal_verificacion(titulo,subtitulo,mensaje)
})



$(document).on("click",".confirmar_verificacion", function(){	
	$("#modal-verificacion").modal("hide");
 	$("#form_crear_ticket").submit();
	
});


$('#modal-exito').on('shown.bs.modal', function (e) {
    titulo = 'SOLICITUD DE INSPECCIÓN'
	subtitulo = 'Creación de solicitud de inspección'
	mensaje = 'Solicitud de inspección creada exitosamente.'
	fill_modal_exito(titulo,subtitulo,mensaje)
	
})