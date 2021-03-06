$(document).ready(function () {

    /***************** CALENDAR PAGE SELECTION ******************/
    $('a.festivalitem').click(function(event){

        // 1. disable active classes:
        $(this).find('div.temm').removeClass('fa_passive');
        $(this).find('div.temm').addClass('fa_active');
        $(this).children('div.item').css('opacity', '1.0');

        event.preventDefault();
        //console.log('jeej');
        //console.log($(this).attr('href'));

        path = window.location.pathname;
        selected = $(this).attr('href');

        request = $.ajax({

            url: path,
            type: 'GET',
            data: {selected: selected},

        });
        request.done(function(response, textStatus, jqXHR){

            var selected = $('div#current_item').text();

            $("a[href=" + selected + "]").find('div.temm').addClass('fa_passive');
            $("a[href=" + selected + "]").find('div.temm').removeClass('fa_active');
            $("a[href=" + selected + "]").children('div.item').css('opacity', '0.3');

            $('section#calendar_item').html(response);
            $('#festrating').barrating({
                theme: 'fontawesome-stars-o',
                initialRating: $('#festrating').data('initial'),
                showSelectedRating: false,
                readonly: true,
            }); 
        });
        request.fail(function(jqXHR, textStatus, errorThrown){

        });
    });

   /***************** RELATED FESTIVALS FUNCTIONALITY ******************/
    $('a.searchtag').click(function(event){

        // 1. disable active classes:
        event.preventDefault();

        $('a.searchtag').removeClass('active');
        $(this).addClass('active');

        //console.log($(this).attr('href'));

        path = $(this).attr('href')

        request = $.ajax({

            url: path,
            type: 'GET',

        });
        request.done(function(response, textStatus, jqXHR){

            //console.log(response)

            $('#related-festivals').html(response)
        });
        request.fail(function(jqXHR, textStatus, errorThrown){

        });
    });

}); 