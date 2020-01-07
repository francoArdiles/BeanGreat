$(function () {

    //envia el formulario y actualiza la vista
    function delete_inventory() {
        console.log("delete inventory is working!"); // sanity check
        $.ajax({
            url: "/eliminar-despensa/", // the endpoint
            type: "POST", // http method
            data: {inventory_pk: $('#delete-inventory').val()}, // data sent
            // with the post
            // request
            // handle a successful response
            success: function (json) {
                //redirige a la pagina de despensas
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

    var dialog = $("#dialog-delete-inventory").dialog({
        autoOpen: false,
        resizable: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
            "Eliminar": function () {
                delete_inventory();
                $(this).dialog('close');
            },
            Cancel: function () {
                $(this).dialog("close");
            }
        }
    });

    $("#delete-inventory").button().on("click", function () {
        console.log('boton apretado');
        dialog.dialog("open");
    });

});
