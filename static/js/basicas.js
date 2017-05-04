if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function() 
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}


$.fn.serializeObject = function(){
    var o = {};
    var a = this.serializeArray();

    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });

    var file_data = this.find('input[type=file]');

    $(file_data).each(function(key, value){
      o[$(value).attr('name')] = $(value)[0].files[0];

      /*$($(value)[0].files[0]).each(function(x, y)){
        file_info.append(y);
      });*/
    });

    return o;
};


$(document).on('submit', '.modal-form', function(event){
  event.preventDefault();

  method = $(this).attr('method');
  action = $(this).attr('action');
  next_page = $(this).attr('target-page');
  msg_modal = $(this).attr('target-modal');
  modal_aux = $(this).parents('.modal');
  form_data = {};
  if($(this).find('input[type="file"]').length){
    form_data = new FormData(this);
    ajax_submit_file_data(form_data, action, msg_modal, modal_aux);
  }
  else{
    form_data = $(this).serializeObject();
    ajax_submit_data(form_data, method, action, msg_modal, modal_aux);
  }
});

//Nota: por ahora este AJAX solo funciona via POST
function ajax_submit_file_data(form_data, action, msg_modal, modal_aux){
  $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
  $(document).ajaxStop($.unblockUI);

  $.ajax({
    url: action,
    type: 'POST',
    data: form_data,
    cache: false,
    processData: false,
    contentType: false,
    success: function(data){
      // console.log(data);
      if(data['errors']){
        // console.log('errors');
        $('.error').empty();
        $.each(data['errors'], function(key, value){
          $('#' + key + '_error').html(value);
        });
      }
      else if (data['aviso']) {
          // console.log('aviso');
          if (data['aviso']['target']) {
            $('#btn_aceptar').attr('data-target', data['aviso']['target']);
            $('#btn_aceptar').attr('data-toggle', 'modal');

          }
          if (data['aviso']['redirect']){
            $('#btn_aceptar').attr('data-href',data['aviso']['redirect']);
          }
          if (data['aviso']['titulo']){
            $('#modal-confirmacion-titulo').html(data['aviso']['titulo']);
          }
          $('#modal-aviso-msj').html(data['aviso']['msj']);
          $('#modal-aviso').modal('show');

      }
      else{
        console.log('SUCCESS');
        if(msg_modal){
          if(modal_aux)
            modal_aux.modal('hide');

          $('#' + msg_modal).modal('show');
        }
        else
          window.location.href = next_page;

        if(data['pdf'])
          window.open(data['pdf'], '_blank');
      }
    },
    error: function(data){
      console.log('ERROR');
    }
  });
}

function ajax_submit_data(json, method, action, msg_modal, modal_aux){
  $.blockUI({ message: '<i class="fa fa-spinner fa-pulse" style="color:#444444"></i> Espere por favor...' });
  $(document).ajaxStop($.unblockUI);

  $.ajax({
    url: action,
    type: method,
    data: json,
    success: function(data){
      // console.log(data);
      //console.log('SUCCESS');
      if(data['errors']){
        $('.error').empty();
        $.each(data['errors'], function(key, value){
          $('#' + key + '_error').html(value);
        });
      }else if (data['aviso']) {
          // console.log('aviso');
          if (data['aviso']['redirect']){
            $('#id_declaracion_creada').attr('href', data['aviso']['redirect']);
            $('#btn_aceptar').attr('data-href',data['aviso']['redirect']);
          }
          if (data['aviso']['titulo']){
            $('<div id="modal-confirmacion-titulo"></div>').html(data['aviso']['titulo']);
          }
          $('#modal-aviso-msj').html(data['aviso']['msj']);
          if (data['aviso']['id']){
            $('#'+data['aviso']['id']).modal('show');
          }else{
            $('#modal-aviso').modal('show');
          }

      }
      else{
        if(msg_modal){
          if(modal_aux)
            modal_aux.modal('hide');

          $('#' + msg_modal).modal('show');
        }
        else
          window.location.href = next_page;

        if(data['pdf'])
          window.open(data['pdf'], '_blank');
      }
    },
    error: function(data){
      console.log('ERROR');
    }
  });
}