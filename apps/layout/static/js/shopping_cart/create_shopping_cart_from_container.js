//main class: new-shopping-cart-wrapper

$(document).ready(function () {


    function createList() {
        // console.log($(this));
        var request_form = $('#create-shopping-cart-from-container-form').serializeArray();
        var btn_request = $('#inventory-to-shopping-cart');
        request_form = JSON.stringify(request_form);
        console.log(request_form);
        $.ajax({
            url: btn_request.attr('data-url'),
            method: 'post',
            data: {'data': request_form, 'pk_container': btn_request.val()},
                success:function () {
                    console.log('creado con exito')
                },
                error: function (xhr, errmsg, err) {
                    $('#result-join').html("<div class='alert-box alert radius'" +
                        " data-alert>Oops! Ha ocurrido un error: " + errmsg +
                        "<a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                    console.log('Ocurrio un error' + errmsg)
                }
        });
        alert('creando lista a partir de despensa')
    }

    var dialog = $("#new-shopping-cart-wrapper").dialog({
        autoOpen: false,
        height: 400,
        width: "auto",
        modal: true,
        buttons: {
            "Agregar": createList,
            Cancel: function () {
                dialog.dialog("close");
            }
        },
        close: function () {
            createForm[0].reset();
            dialog.dialog('close');
            $('#id_name').removeClass("ui-state-error");
        }
    });

    var createForm = dialog.find("form").on("submit", function (event) {
        event.preventDefault();
        console.log($(this));
        createList();
    });

    $('#inventory-to-shopping-cart').button().on("click", function () {
        console.log('boton encontrado');
        console.log('abriendo dialogo');
        console.log(dialog);
        dialog.dialog("open");
    });

});