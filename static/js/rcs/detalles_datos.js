// $("#tabla_detalles").hide()
$("#id_submit_detalles").hide()

$(document).on('ready',(function(){
	$('.decimal_mask').inputmask('[9]{11}.{0,1}[9]{0,2}', {placeholder: '',"greedy": false,});    
	$('.integer_mask').inputmask('[9]{19}',  {placeholder: '', "greedy": false,});    
	cant_en_tabla =$('#detalles_table_body').children('tr').length;
	if (cant_en_tabla){
		$("#contador_agregados").val(cant_en_tabla)
	}else{
		$("#tabla_detalles").hide()
	}

	$(".no-space").keypress(function(e){if(e.which === 32){return false}});

}));

function agregar_detalle(id_tabla){

	$("#detalles_table_body").html()
	cant_en_tabla =$('#detalles_table_body').children('tr').length;
	if (!cant_en_tabla){
		$("#tabla_detalles").show('slide')
		$("#id_submit_detalles").show('slide')


	} 
	indice = (parseInt($("#contador_agregados").val()) + 1)

	// for (i=1;i<cant_en_tabla;i++){
	// 	if (!$("#id_celda_"+i).length){
	// 		indice = i
	// 		break
	// 	}
	// }

	tabla_body = $('<tr>',{id:'id_celda_'+indice,class:'cont_tr'});

	codigo_input =$('<input>',{class:'form-control codigo_evaluar no-space' , id:'codigo_'+(indice), name:'codigo_'+(indice), type:'text'});
    codigo_input_error = $('<center>').html($('<div>',{id:'codigo_input_error_'+(indice), class:'error'}));
    td_c = $('<td>').append(codigo_input).append(codigo_input_error)
    tabla_body.append(td_c);

	pieza_input =$('<input>',{class:'form-control' , name:'pieza_'+(indice), id:'pieza_'+(indice), type:'text'});
    pieza_input_error = $('<center>').html($('<div>',{id:'pieza_input_error_'+(indice), class:'error'}));
    tabla_body.append($('<td>').append(pieza_input).append(pieza_input_error));

	dano_input =$('<input>',{class:'form-control' , name:'dano_'+(indice), id:'dano_'+(indice), type:'text'});
    dano_input_error = $('<center>').html($('<div>',{id:'dano_input_error_'+(indice), class:'error'}));
    tabla_body.append($('<td>').append(dano_input).append(dano_input_error));

	costo_input =$('<input>',{class:'form-control decimal_mask' , name:'costo_'+(indice), id:'costo_'+(indice), type:'text'});
    costo_input_error = $('<center>').html($('<div>',{id:'costo_input_error_'+(indice), class:'error'}));
    tabla_body.append($('<td>').append(costo_input).append(costo_input_error));

    i_botton = $('<center>').html($('<i>',{class:'fa fa-trash white-icon',style:"color: white;"}))
    boton= $('<botton>',{id:"id_eliminar_celda_"+indice,class:"btn btn-danger",type:"button",onclick:"eliminar_celda(this);"})
    tabla_body.append($('<td>').html(boton.append(i_botton)));

	$("#detalles_table_body").append(tabla_body)
	$("#contador_agregados").val(parseInt($("#contador_agregados").val()) + 1) 
	// #falta
	load_validators()

}

function eliminar_celda(tag){
	id_eliminar = $("#"+tag.id).parent().parent()[0].id
	$("#"+id_eliminar).remove()	
	cant_en_tabla =$('#detalles_table_body').children('tr').length;
	if (!cant_en_tabla){
		$("#tabla_detalles").hide('slide')
		$("#id_submit_detalles").hide('slide')

	} 
}


function submit_detalles(){

	datos_vacios = false

	$('#tabla_detalles > tbody  > tr').each(function() {
	
		id_tr = $( this )[0].id
		arr = id_tr.split("_")
		numero = arr[arr.length-1]
		
		if ($("#codigo_"+numero).val().trim() == ""){
 			$("#codigo_input_error_"+numero).html("Este campo no puede ir vacío")
 			datos_vacios = true
		} else {
 			$("#codigo_input_error_"+numero).html('')
		}

		if ($("#pieza_"+numero).val().trim() == ""){
 			$("#pieza_input_error_"+numero).html("Este campo no puede ir vacío")
 			datos_vacios = true
		} else {
 			$("#pieza_input_error_"+numero).html('')
		}
		
		if ($("#dano_"+numero).val().trim() == ""){
 			$("#dano_input_error_"+numero).html("Este campo no puede ir vacío")
 			datos_vacios = true
		} else {
 			$("#dano_input_error_"+numero).html('')
		}
		
		if ($("#costo_"+numero).val().trim() == ""){
 			$("#costo_input_error_"+numero).html("Este campo no puede ir vacío")
 			datos_vacios = true
		} else {
 			$("#costo_input_error_"+numero).html('')
		}
		

	});

	console.log("datos_vacios");
	console.log(datos_vacios);
	
	if(datos_vacios){

	} else {
		// #si la tabla no esta vacia

		if(verificar_codigo_duplicado()){

		}else {

			if($('#detalles_table_body').children('tr').length){
				$('#form_detalles_vehiculo').submit();
				
			} else {
				console.log("nada que enviar")
			}
		}
		
	}


	
}

function get_codigos(){
	arr_codigos = []
	cont= 0
	$('#tabla_detalles > tbody  > tr').each(function() {
	    
			id_tr = $( this )[0].id
			arr = id_tr.split("_")
			numero = arr[arr.length-1]
			
			arr_codigos[cont]=($("#codigo_"+numero).val().trim())
	    cont= cont+1
		})
	console.log("arr_codigos:",arr_codigos);
	
	return arr_codigos
}

function se_repite_algun_codigo(arr){
	console.log("arr.length:",arr.length);
	
	for (i=0; i< arr.length;i++){
		console.log("i:",i);
		
		arr[i]
		for (j=0; j< arr.length;j++){	
			if (i!=j){
				// console.log("arr[i].toString()");
					// console.log(arr[i].toString());
					// console.log("arr[j].toString()",arr[j].toString());
				if(arr[i].toString()==arr[j].toString()){
					
					
					return arr[i]

				}
			}
		}
	}
	$('#tabla_detalles > tbody  > tr').each(function() {
		
			id_tr = $( this )[0].id
			// console.log("id_tr");
			// console.log(id_tr);
			
			arr = id_tr.split("_")
			// console.log("arr");
			// console.log(arr);
			

			numero = arr[arr.length-1]
			// console.log("numero");
			// console.log(numero);
			
			
			if ($("#codigo_input_error_"+numero).html()=="El codigo no puede estar duplicado"){
	 			$("#codigo_input_error_"+numero).html('')
			}

		})
	return ""
}

function verificar_codigo_duplicado(){
	arr_codigos = get_codigos()

	repetido = se_repite_algun_codigo(arr_codigos)
	console.log("repetido:",repetido);
	algun_codigo_repetido = false
	if(repetido.trim() != "" ){

		$('#tabla_detalles > tbody  > tr').each(function() {
		
			id_tr = $( this )[0].id
			arr = id_tr.split("_")
			numero = arr[arr.length-1]
			
			if ($("#codigo_"+numero).val().trim()==repetido){
	 			$("#codigo_input_error_"+numero).html("El codigo no puede estar duplicado")
	 			algun_codigo_repetido = true
			}

		})
	}
	console.log("algun_codigo_repetido");
	console.log(algun_codigo_repetido);
	
	return algun_codigo_repetido
}

$(".codigo_evaluar").focusout(function() {
	// this.value

	verificar_codigo_duplicado()
})

function load_validators(){
	$('.decimal_mask').inputmask('[9]{11}.{0,1}[9]{0,2}', {placeholder: '',"greedy": false,});  
	$('.integer_mask').inputmask('[9]{19}',  {placeholder: '', "greedy": false,});    
	$(".no-space").keypress(function(e){if(e.which === 32){return false}});
	
	$(".codigo_evaluar").focusout(function() {
		// this.value

		verificar_codigo_duplicado()
	})

}
