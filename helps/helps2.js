str = str.replace(/\s+/g, '');
​$('no-space').on('keypress',(function( e ) {
    if(e.which === 32) 
        return false;
}))​​​​​;​




arr2=[]
cont=0
$('#tabla_detalles > tbody  > tr').each(function() {
      console.log("------------------------------------")
			id_tr = $(this)[0].id
      console.log("id_tr:",id_tr);
			
			
			arr = id_tr.split("_")
      console.log("arr:", arr);
			
			

			numero = arr[arr.length-1]
      console.log("numero:",numero);
			
  console.log("codigo: " ,$("#codigo_"+numero).val().trim())
       arr2[cont]=$("#codigo_"+numero).val().trim()
       cont= cont+1
		})
console.log("arr:",arr2)

arr[1]==arr[2]