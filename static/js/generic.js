// Email y contraseña comparacion bilateral
$("#id_correo_electronico").attr('onblur',"confirmEmail2();");

//Contraseña minimo 8 digitos y que contenga una Mayuscula
$("#id_password").attr('pattern','(?=.*[A-Z]).{8,}')
$("#id_password").attr('onkeypress','return beta(event)');

function validarEmail( email ) {
    expr = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9])+$/;
    if ( expr.test(email)){
        return 1;
    }else{
        return 0;
    }
}

//Evitar espacion en el password
function beta(e) {
     var k;
     document.all ? k = e.keyCode : k = e.which;
     return (k!=32);
}

var letras_mayusculas="ABCDEFGHIJKLMNÑOPQRSTUVWXYZ";

function tiene_mayusculas(texto){
   for(i=0; i<texto.length; i++){
      if (letras_mayusculas.indexOf(texto.charAt(i),0)!=-1){
         return 1;
      }
   }
   return 0;
}


function capfirst(val){

    val = val.charAt(0).toUpperCase() + val.substr(1).toLowerCase();
    return val;
}

function isEmpty( el ){
      return !$.trim(el.html())
  }