$(document).ready(function () {
    /***************** CALENDAR PAGE SELECTION ******************/

    /*$('a.festivalitem').click(function(event){

        event.preventDefault();
        console.log('jeej');
        console.log($(this).attr('href'));

        path = window.location.pathname;
        selected = $(this).attr('href');

        request = $.ajax({

            url: path,
            type: 'GET',
            data: {selected: selected},


        });
        request.done(function(response, textStatus, jqXHR){

            console.log('success!');
            //console.log(response);

            $('section#calendar_item').html(response);

        });
        request.fail(function(jqXHR, textStatus, errorThrown){

        });
    });*/
}); 