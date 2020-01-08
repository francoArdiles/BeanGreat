$(document).on('click', '#share-object', function () {
    var pk = $(this).val();
    var prefix = $(this).attr('prefix');
    console.log('creando codigo! pk:'+ pk);
    console.log();
    $.ajax({
        url: $(this).attr('data-url'),
        method: 'POST',
        data: {element_pk: pk},

        success: function (json) {
            console.log('exito en la operacion');
            $('#' + prefix + '-list').prepend(
                    '<li>' + json.code + '</li>'
                );
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    })
});

function copyToClipboard(element) {
  var $temp = $("<input>");
  console.log('copiando');
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  $temp.remove();
}