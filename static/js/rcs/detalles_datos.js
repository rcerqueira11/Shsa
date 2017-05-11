// $("#tabla_detalles").hide()
$("#id_submit_detalles").hide()

$(document).ready(function(){
	cant_en_tabla =$('#detalles_table_body').children('tr').length;
	if (cant_en_tabla){
		$("#contador_agregados").val(cant_en_tabla)
	}else{
		$("#tabla_detalles").hide()
	}

});
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

	codigo_input =$('<input>',{class:'form-control numeros' , id:'codigo_'+(indice), name:'codigo_'+(indice), type:'text'});
    codigo_input_error = $('<center>').html($('<div>',{id:'codigo_input_error_'+(indice), class:'error'}));
    td_c = $('<td>').append(codigo_input).append(codigo_input_error)
    tabla_body.append(td_c);

	pieza_input =$('<input>',{class:'form-control' , name:'pieza_'+(indice), id:'pieza_'+(indice), type:'text'});
    pieza_input_error = $('<center>').html($('<div>',{id:'pieza_input_error_'+(indice), class:'error'}));
    tabla_body.append($('<td>').append(pieza_input).append(pieza_input_error));

	dano_input =$('<input>',{class:'form-control' , name:'dano_'+(indice), id:'dano_'+(indice), type:'text'});
    dano_input_error = $('<center>').html($('<div>',{id:'dano_input_error_'+(indice), class:'error'}));
    tabla_body.append($('<td>').append(dano_input).append(dano_input_error));

	costo_input =$('<input>',{class:'form-control numeros' , name:'costo_'+(indice), id:'costo_'+(indice), type:'text'});
    costo_input_error = $('<center>').html($('<div>',{id:'costo_input_error_'+(indice), class:'error'}));
    tabla_body.append($('<td>').append(costo_input).append(costo_input_error));

    i_botton = $('<center>').html($('<i>',{class:'fa fa-trash white-icon',style:"color: white;"}))
    boton= $('<botton>',{id:"id_eliminar_celda_"+indice,class:"btn btn-danger",type:"button",onclick:"eliminar_celda(this);"})
    tabla_body.append($('<td>').html(boton.append(i_botton)));

	$("#detalles_table_body").append(tabla_body)
	$("#contador_agregados").val(parseInt($("#contador_agregados").val()) + 1) 

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
		if($('#detalles_table_body').children('tr').length){
			$('#form_detalles_vehiculo').submit();
			
		} else {
			console.log("nada que enviar")
		}
		
	}


	
}
