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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function save_annotation_ajax() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    var annot_list = [
        {
            "image_base_name": '10000175011',
            "annotation_name": "guardrail",
            "is_present": 'true',
            "comment": 'this is a test'
        },
        {
            "image_base_name": '10000175307',
            "annotation_name": "guardrail",
            "is_present": 'false',
            "comment": 'this is a test'
        }
    ];
    $.ajax({
        type: "POST",
        url: '/save_annotations/',
        data: {
            annotations: JSON.stringify(annot_list)
        },
        success: function (json_response) {
            return true;
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText + ". Error message: " + errmsg);
            return false;
        }
    });
}
