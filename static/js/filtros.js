$('#tabla-resultado').hide();

$(document).on('submit', '.filter_form', function(event){

	$(document).ajaxStop($.unblockUI);

	event.preventDefault();
	console.log("this");
	console.log(this);
	
	json = $(this).serializeObject();

	if(!empty_fields(json) || json['admin_site'] == '1'){
		method = $(this).attr('method');
	  	action = $(this).attr('action');

		$.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });

		$.ajax({
			url: action,
			type: method,
			data: json,
			success: function(results){

				//si la busqueda arroja resultados, entonce se procede a procesarlo
				if(results['data']){
					$('#error-filtro').empty();
                    $('#error_fil').empty();
					$('#tabla-resultado').show('fade');

					tbody_filter = $('#tabla-resultado').children('tbody');
					json_list = $.parseJSON(results['data']);
					order_list = results['order'];
					n = order_list.length;
					aux = '';

					//generar contenido de la tabla con los campos obtenidos por el filtro
		   			$.each(json_list, function(index, json){
		   				aux += '<tr>';

		   				for(i = 0; i < n; i++){
		   					key = order_list[i];
		   					value = json[key];

		   					//este 'key' representa el campo con los botones de las opciones de los registros mostrados en la tabla html
		   					if(key == 'options'){
		   						aux += '<td>';
		   						$.each(value, function(i, option){
		   							href = option['href'] ? 'href="'+option['href']+'"' : '';
		   							target = option['target'] ? 'target="'+option['target']+'"' : '';
		   							data_ref = option['data-ref'] ? 'data-ref="'+option['data-ref']+'"' : '';
		   							modal_info = option['target-modal'] ? 'data-toggle="modal" data-target="#'+option['target-modal']+'"' : '';
		   							on_click = option['onclick'] ? 'onclick="'+option['onclick']+'"' : '';
		   							type = option['type'] ? 'type="'+option['type']+'"' : '';

									aux += '<a '+type+' '+href+' '+target+' class="'+option['class']+' '+option['status']+'" '+modal_info+' title="'+option['tooltip']+'" '+data_ref+' '+on_click+'  style=" margin-top: 5px; " >\
												<i class="fa '+option['icon']+'" style="color: white;'+option['style_icon']+'"></i>\
											</a>&nbsp;';
		   						});
		   						aux += '</td>';
		   					}
		   					else{
		   						if(value){
		   							//este campo representa los valores que llevan asociada una etiqueta con color
				   					if(value.indexOf('|') != -1){
				   						tmp = value.split('|');
				   						aux += '<td style="word-wrap:break-word;">';
				   						style="";
					   						for(k= 0; k < tmp.length-2; k++){
					   							if(k==0){
						   							style='style=" padding-bottom: 5px; "';
					   							}else{
						   							style='style=" padding-bottom: 5px;padding-top: 5px; "';
					   							}
					   							aux += '<span class="label label-'+tmp[tmp.length-1]+'" '+style+'>'+tmp[k]+'</span><br>';
					   						}
					   						if(style!="")style='style="padding-top: 5px; "'
				   							aux += '<span class="label label-'+tmp[tmp.length-1]+'" '+style+'>'+tmp[tmp.length-2]+'</span>';
			   							aux += '</td>';
				   					}
				   					else
				   						aux += '<td>'+value+'</td>';
				   				}
				   				//tecnicamente este caso no debería pasar... pero hay campos que por los momentos vienen vacios hay un bug que no se puede mostrar --VACIO-- si no el vacio y ya.
				   				else{
				   					aux += '<td></td>';
				   				}
			   				}

		   				}
					});

					aux += '</tr>';
		   			$(tbody_filter).html(aux);

					//se procede a indexar el resultado en a lo sumo 6 páginas
					$('#indice-busqueda').empty();

					max_page = results['total_pages'];
					if(max_page > 1){
						page = results['page_number'];
						prev_page = page - 1;
						next_page = page + 1;

						if(page > 1){
							$('#indice-busqueda').append('<li><a class="page_index" page-target="1" title="Primera P&aacute;gina" ><i class="fa fa-step-backward"></i></a></li>');
							$('#indice-busqueda').append('<li><a class="page_index" page-target="'+prev_page+'" title="P&aacute;gina Anterior" ><i class="fa fa-caret-left"></i></a></li>');
						}

						offset_prev = page - 3;
						offset_next = page + 3;
						offset_prev = (offset_prev > 1) ? offset_prev : 1;
						offset_next = (offset_next < max_page) ? offset_next : max_page;

						for(i = offset_prev; i <= offset_next; i++){
							status = (i == page) ? 'class="active"' : '';
							$('#indice-busqueda').append('<li '+status+'><a class="page_index" page-target="'+i+'">'+i+'</a></li>');
						}

						if(page < max_page){
							$('#indice-busqueda').append('<li><a class="page_index" page-target="'+next_page+'" title="Siguiente P&aacute;gina"><i class="fa fa-caret-right"></i></a></li>');
							$('#indice-busqueda').append('<li><a class="page_index" page-target="'+max_page+'" title="Ultima P&aacute;gina"><i class="fa fa-step-forward"></i></a></li>');
						}
					}


                    //En caso de que se este en divisas_conciliacion_manual

                    if($( ".date_pago" ).length){
                        $( ".date_pago" ).datepicker({
                          autoclose: "true",
                          clearBtn: "true",
                          language: 'es',
                          format: 'dd/mm/yyyy',
                          startDate: '01/01/2002',
                          endDate: new Date(),
                        });
                    }
                }
				else{
					//si la busqueda no arroja resultados, entonces se procede a imprimir un mensaje de error
					$('#indice-busqueda').empty();
					$('#tabla-resultado').hide('fade');
			        if (($("#error_fil").html() == undefined || $("#error_fil").html() == "")){
						aux = '<p class="error-center-mensaje" style="color:#CE4744;">No se encontraron resultados <i style="color:#CE4744;" class="fa fa-times-circle-o fa-lg"></i></p>';
						$('#error-filtro').html(aux);
					}
				}
			},
			error: function(results){
				console.log('ERROR');
			}
	    });
	}
	else{

		$('#indice-busqueda').empty();
		$('#tabla-resultado').hide('fade');
		// $('#error-filtro').empty();
	}
});

$(document).on('click', '#btn_filter_form', function(){
	$('#page_id').attr('value', 1);
});
//en este evento se obtiene la página seleccionada por el usuario con la finalidad de ejecutar el filtro a partir de la misma
$(document).on('click', '.page_index', function(){
	$('#page_id').val($(this).attr('page-target'));
	$('#filter_form_id').submit();
});

function empty_fields(data){
	empty = true;

	$.each(data, function(key, value){
		len=typeof(value)=="string" ? value.trim() : value.length;
		if(key != 'page' && key != 'filter_code' && key != 'filter_obj' && len){
			empty = false;
			return false;
		}
	});

	return empty;
}
