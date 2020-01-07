$(document).on('click', '#share-inventory', function () {
    var pk = $(this).val();
    console.log('creando codigo! pk:'+ pk);
    $.ajax({
        url: '/despensa/share-code/',
        method: 'POST',
        data: {inventory_pk: pk},

        success: function (json) {
            console.log('exito en la operacion');
            $('#code-list').prepend(
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