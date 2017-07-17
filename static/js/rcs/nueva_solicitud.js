$('#id_marca').change(function(event){
		marca_codigo = $(this).val();
		$.ajax({
			type: 'GET',
			url: '/rcs/obtener_modelos',
			dataType: 'json',
			data: {
			'marca_codigo': marca_codigo
			},
			success: function(data){
				aux = '';
				$(data).each(function(key, value){
					aux += '<option value="'+value.id+'">'+value.nombre_modelo+'</option>';
				});
				$('#id_modelo').html(aux);
				$('#id_modelo').trigger('chosen:updated');
				console.log('Cambiando');
			},
			error: function(data){
				console.log("ERROR");
			}
		});
	});
