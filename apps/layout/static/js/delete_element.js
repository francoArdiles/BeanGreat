$(document).ready(function () {

    function delete_element(btn_id) {
        console.log("delete element is working!"); // sanity check
        var element = $('#'+btn_id); //Obtiene el boton presionado
        $.ajax({
            url: element.attr('data-url'), // the endpoint
            type: "POST", // http method
            data: {element_pk: element.val()}, // data sent

            success: function (json) {
                //redirige a la pagina a pagina indicada por la vista
                if (json.action === 'redirect'){
                    $(location).attr('href',json.url);
                }
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
    // console.log($('[id^="delete-"][id$="-dialog"]'));

    var dialog = $('[id^="delete-"][id$="-dialog"]').dialog({
        autoOpen: false,
        resizable: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
            "Eliminar": function () {
                console.log($(this).data('btn_id'));
                delete_element($(this).data('btn_id'));
                alert('Removido exitosamente');
                $(this).dialog('close');
            },
            Cancel: function () {
                $(this).dialog("close");
            }
        }
    });

    $('[id^="delete-"][id$="-btn"]').button().on("click", function () {
        console.log('boton apretado');
        var id_dialog ="#delete-"+$(this).attr('prefix')+"-"+$(this).val()+"-dialog";
            // "#delete-{{prefix}}-{{value}}-dialog"
        console.log(id_dialog);
        console.log($(this).attr('id'));
        $(id_dialog)
            .data('btn_id', $(this).attr('id'))
            .dialog("open");
    });

    /**************************************************************************/
    /**************************************************************************/


    /*
    * En este segmento hay funciones que permiten usar csrf con ajax, en
     * para no usar esto, se puede dar la excepcion a la vista @csrf_exempt
    * */

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
            (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});