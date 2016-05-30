$(document).ready(function () {
    /***************** CALENDAR PAGE SELECTION ******************/

    $('#submitbutton').on('click', function(event){

    	event.preventDefault();

    	console.log('ready to post');
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
            dataType: 'json',

            success: function(data) {
                console.log(data);
                // Hide the comment form
                $('#comment-form').addClass('hidden');
                // Add the new comment to the comment list
                //$('#comment-list')
            },
        });

    });
}); 