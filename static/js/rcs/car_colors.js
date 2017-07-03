
$(document).on('ready',function(){
	color_part($("#CAPT").val(),"capot");
	color_part($("#PARABR").val(), "parabrisas");
	color_part($("#PLAT").val(), "platina-derecha");
	color_part($("#PLAT").val(), "platina-izquierda");
	color_part($("#COC_FRON").val(), "focosdelanteros-izquierdo");
	color_part($("#COC_FRON").val(), "focosdelanteros-derecho");
	color_part($("#PLA_REJ_FRO").val(), "parrilla");
	color_part($("#COMP_TRAS").val(), "puerta-trasera");   
	color_part($("#COMP_TRAS").val(), "puerta-trasera");   
	color_part_hard($("#RET_INT").val(), "retrovisor-interno");   
	color_part($("#RET_EXT").val(), "retrovisor-externosizquierdo");   
	color_part($("#RET_EXT").val(), "retrovisor-externosderecho");   
	color_part($("#PUERT").val(), "puertaderecha-frente");   
	color_part($("#PUERT").val(), "puertaizquierda-frente");   
	color_part($("#PUERT").val(), "puertaderecha-atras");   
	color_part($("#PUERT").val(), "puertaizquierda-atras");   
	color_part($("#TECH").val(), "techo");   
	color_part($("#MANI_CERR").val(), "manilla-izquierdatrasera");   
	color_part($("#MANI_CERR").val(), "manilla-izquierdadelantera");   
	color_part($("#MANI_CERR").val(), "manilla-derechatrasera");   
	color_part($("#MANI_CERR").val(), "manilla-derechadelantera");   
	color_part($("#PAR_CHOQ").val(), "parachoque-trasero");   
	color_part($("#CAUCH").val(), "rueda-traseraizquierda");   
	color_part($("#CAUCH").val(), "rueda-delanteraderecha");   
	color_part($("#CAUCH").val(), "rueda-traseraderecha");   
	color_part($("#CAUCH").val(), "rueda-delanteraizquierda");   
	color_part($("#PLAT").val(), "platina-izquierda");   
	color_part($("#PLAT").val(), "platina-derecha");   
	color_part($("#COMP_TRAS").val(), "manilla-trasera");   
	color_part($("#VENT").val(), "ventana-trasera");   
	color_part($("#VENT").val(), "ventana-derechafrente");   
	color_part($("#VENT").val(), "ventana-izquierdafrente");   
	color_part($("#VENT").val(), "ventana-derechatrasera");   
	color_part($("#VENT").val(), "ventana-izquierdatrasera");   
	// color_part($("#PLAT").val(), "ventana-trasera");   
















});


function color_part(state,part){
	if (state == "B"){
		$('#'+part+' path').css({ fill: "green",opacity:0.5 })
	}
	if (state == "R"){
		$('#'+part+' path').css({ fill: "yellow",opacity:0.5 })
	}
	if (state == "M"){
		$('#'+part+' path').css({ fill: "red",opacity:0.5 })
	}

}

function color_part_hard(state,part){
	if (state == "B"){
		$('#'+part+' path').css({ fill: "green",opacity:0.8 })
	}
	if (state == "R"){
		$('#'+part+' path').css({ fill: "yellow",opacity:0.8 })
	}
	if (state == "M"){
		$('#'+part+' path').css({ fill: "red",opacity:0.8 })
	}

}