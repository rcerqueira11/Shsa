$("#tabla_detalles").hide()
function agregar_detalle(id_tabla){

	$("#detalles_table_body").html()
	cant_en_tabla =$('#detalles_table_body').children('tr').length;
	if (!cant_en_tabla){
		$("#tabla_detalles").show('slide')
		console.log("cant_en_tabla");
				console.log(cant_en_tabla);

	}
	indice = (parseInt($("#contador_agregados").val()) + 1)

	// for (i=1;i<cant_en_tabla;i++){
	// 	if (!$("#id_celda_"+i).length){
	// 		indice = i
	// 		break
	// 	}
	// }

	tabla_body = $('<tr>',{id:'id_celda_'+indice,class:'cont_tr'});

	codigo_input =$('<input>',{class:'form-control numeros' , name:'codigo_'+(indice), type:'text'});
    codigo_input_error = $('<center>').html($('<div>',{id:'codigo_input_error_'+(indice), class:'error'}));
    tabla_body.append($('<td>').html(codigo_input.append(codigo_input_error)));

	pieza_input =$('<input>',{class:'form-control' , name:'pieza_'+(indice), type:'text'});
    pieza_input_error = $('<center>').html($('<div>',{id:'pieza_input_error_'+(indice), class:'error'}));
    tabla_body.append($('<td>').html(pieza_input.append(pieza_input_error)));

	dano_input =$('<input>',{class:'form-control' , name:'dano_'+(indice), type:'text'});
    dano_input_error = $('<center>').html($('<div>',{id:'dano_input_error_'+(indice), class:'error'}));
    tabla_body.append($('<td>').html(dano_input.append(dano_input_error)));

	costo_input =$('<input>',{class:'form-control numeros' , name:'costo_'+(indice), type:'text'});
    costo_input_error = $('<center>').html($('<div>',{id:'costo_input_error_'+(indice), class:'error'}));
    tabla_body.append($('<td>').html(costo_input.append(costo_input_error)));

    i_botton = $('<center>').html($('<i>',{class:'fa fa-trash white-icon',style:"color: white;"}))
    boton= $('<botton>',{id:"id_eliminar_celda_"+indice,class:"btn btn-danger",type:"button",onclick:"eliminar_celda(this);"})
    tabla_body.append($('<td>').html(boton.append(i_botton)));

	$("#detalles_table_body").append(tabla_body)
	$("#contador_agregados").val(parseInt($("#contador_agregados").val()) + 1) 

}

function eliminar_celda(tag){
	id_eliminar = $("#"+tag.id).parent().parent()[0].id
	$("#"+id_eliminar).remove()	
}
