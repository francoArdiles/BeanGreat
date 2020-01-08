$(function () {

    //envia el formulario y actualiza la vista
    function delete_element() {
        var element = $('[id^="delete-"][id$="-btn"]');
        console.log("delete element is working!"); // sanity check
        $.ajax({
            url: element.attr('data-url'), // the endpoint
            type: "POST", // http method
            data: {element_pk: element.val()}, // data sent

            success: function (json) {
                //redirige a la pagina a pagina indicada por la vista
                $(location).attr('href',json.url);
                dialog.dialog("close");
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius'" +
                    " data-alert>Oops! Ha ocurrido un error: " + errmsg +
                    "<a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    var dialog = $('[id^="delete-"][id$="-dialog"]').dialog({
        autoOpen: false,
        resizable: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
            "Eliminar": function () {
                delete_element();
                $(this).dialog('close');
            },
            Cancel: function () {
                $(this).dialog("close");
            }
        }
    });

    $('[id^="delete-"][id$="-btn"]').button().on("click", function () {
        console.log('boton apretado');
        dialog.dialog("open");
    });

});
