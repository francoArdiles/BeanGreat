$(function () {

    //envia el formulario y actualiza la vista
    function joinElement() {
        console.log("join inventory is working!"); // sanity check
        var joiner = $('[id^="join-"][id$="-form-wrapper"]');

        var joinPrefix = joiner.attr('prefix');
        var joinURL = joiner.attr('data-url');

        console.log(joinURL);

        $.ajax({
            url: joiner.attr('data-url'), // the endpoint
            type: "POST", // http method
            data: {join_data: $('#'+joinPrefix+'-input').val()}, // data
            success: function (json) {
                //redirige a la pagina de despensas
                if (json.url){
                    console.log(json.url);
                    $(location).attr('href',json.url);}
                else
                    $('result-join').html(json.outdated);
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#result-join').html("<div class='alert-box alert radius'" +
                    " data-alert>Oops! Ha ocurrido un error: " + errmsg +
                    "<a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    /**************************************************************************/
    /**************************************************************************/

    function createElement() {
        console.log("create post is working!"); // sanity check
        var creator = $('[id^="create-"][id$="-form-wrapper"]');
        console.log(creator);
        var createPrefix = creator.attr('prefix');
        $.ajax({
            url: creator.attr('data-url'), // the endpoint
            type: "POST", // http method
            data: {create_data: $('#id_name').val()}, // data sent
            // handle a successful response
            success: function (json) {
                // Actualiza lo que se muestra en pantalla
                $('#id_name').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                $('#' + createPrefix + '-list').prepend(
                    '<li><div>' +
                    '<a href="' + json.abs_url + '">' + json.name + '</a>' +
                    '<p>' + json.count_items + ' items</p>' +
                    '<p>' + json.count_user + ' user(s)</p>' +
                    '</div></li>'
                );
                console.log('success');
                dialogCreate.dialog("close");
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#create-results').html("<div class='alert-box alert radius'" +
                    " data-alert>Oops! Ha ocurrido un error: " + errmsg +
                    "<a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    var joiner = $('[id^="join-"][id$="-form-wrapper"]');
    var creator = $('[id^="create-"][id$="-form-wrapper"]');

    //    Muestra el formulario como una ventana de dialogo
    var dialogCreate = creator.dialog({
        autoOpen: false,
        height: 200,
        width: 400,
        modal: true,
        buttons: {
            "Crear": createElement,
            Cancel: function () {
                dialogCreate.dialog("close");
            }
        },
        close: function () {
            createForm[0].reset();
            dialogCreate.dialog('close');
            $('#id_name').removeClass("ui-state-error");
        }
    });

        //    Muestra el formulario como una ventana de dialogo
    var dialogJoin = joiner.dialog({
        autoOpen: false,
        height: 200,
        width: 400,
        modal: true,
        buttons: {
            "Unirse": joinElement,
            Cancel: function () {
                dialogJoin.dialog("close");
            }
        },
        close: function () {
            joinForm[0].reset();
            dialogJoin.dialog('close');
            $('#'+joiner.attr('prefix')+'-input').removeClass("ui-state-error");
        }
    });

    var createForm = dialogCreate.find("form").on("submit", function (event) {
        event.preventDefault();
        createElement();
    });

    var joinForm = dialogJoin.find("form").on("submit", function (event) {
        event.preventDefault();
        joinElement();
    });

    $('[id^="create-"][id$="-btn"]').button().on("click", function () {
        console.log('abriendo creador de instancia');
        dialogCreate.dialog("open");
    });

    $('[id^="join-"][id$="-btn"]').button().on("click", function () {
        console.log('abriendo joiner de ususarios');
        dialogJoin.dialog("open");
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
