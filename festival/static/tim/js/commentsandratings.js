$(document).ready(function () {
    /***************** CALENDAR PAGE SELECTION ******************/

    $('#commentsubmit').on('click', function(event){

    	event.preventDefault();

    	console.log('ready to post comments');
    	console.log($('input#id_comment').val())

    	var formData = {

    		'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'title'   : $('#id_title').val(),
            'comment' : $('#id_comment').val(),
            'honeypot' : $('#id_honeypot').val(),
            'content_type': $('#id_content_type').val(),
            'object_pk' :$('#id_object_pk').val(),
            'timestamp' : $('#id_timestamp').val(),
            'security_hash' : $('#id_security_hash').val()
        };

         $.ajax({
            url: '/comments/post/',
            type: 'POST',
            data: formData,
            dataType: 'html',

            success: function(data) {
                console.log(data);
                // Hide the comment form
                $('#comment-form').addClass('hidden');
                $('#comment-list ul').append(data);
                // Add the new comment to the comment list
                //$('#comment-list')
            },
        });
    });

    $('input.rating-form').on('click', function(event){

        event.preventDefault();

        console.log('ready to post ratings');
        
        formCount = $('div.br-wrapper').length;
        console.log('formcount: ' + formCount)

        var formData = {}

        formData['form-MIN_NUM_FORMS'] = $('#id_form-MIN_NUM_FORMS').val();
        formData['form-MAX_NUM_FORMS'] = $('#id_form-MAX_NUM_FORMS').val();
        formData['form-TOTAL_FORMS'] = $('#id_form-TOTAL_FORMS').val();
        formData['form-INITIAL_FORMS'] = $('#id_form-INITIAL_FORMS').val();
        formData['csrfmiddlewaretoken'] = $('input[name=csrfmiddlewaretoken]').val();

        for (i = 0; i < formCount; i++) {

            formData['form-' + i + '-object_id'] = $('#id_form-' + i + '-object_id').val();
            formData['form-' + i + '-content_type'] = $('#id_form-' + i + '-content_type').val();
            formData['form-' + i + '-score'] = $('#id_form-' + i + '-score option:selected').val();
        }

        console.log(formData)

         $.ajax({
            url: '/ratings/test/',
            type: 'POST',
            data: formData,
            dataType: 'html',

            success: function(data) {
                console.log(data);
                // Hide the comment form
                $('#rating-form').html(data);

                $(function() {
                    $('.example').barrating({
                        theme: 'fontawesome-stars',
                        initialRating: -7,
                        showSelectedRating: true,
                    });
               });
            },
        });
    });
}); 