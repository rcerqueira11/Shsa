

function recuperar_cuenta(){

	$(document).ajaxStop($.unblockUI);
	$.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
	dataForm = $("#id_post_recuperar_cuenta").serializeArray();
	$.ajax({
	        type: 'POST' ,
	        url: 'registro/recuperar_cuenta' , // <= Providing the URL
	        data: dataForm , // <= Providing the form data, serialized above
	        success: function(results){
	         if(results.Result == 'success'){
					
						
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