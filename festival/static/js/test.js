$(document).ready(function () {

   	// Change appearance of selected category button and ajax call to fetch subcategories
	$('#loadmore').click(function() {

		var count = $('div.festlist').size();

		var page = count / 6;


		console.log('count');
		console.log(count);
		console.log('page');
		console.log(page)

		ajax_call(page + 1);
	});

	function ajax_call(page) {

		console.log('JEEEEEEEEEJ');

		$.ajax({
			//url:"/products/overview/products/",
			url:"/index/test/",
			type: "GET",
			data: {
				'page': page,
			},
			success: my_handler,

			error: function(xhr, ajaxOptions, thrownError) {
				console.log(xhr.status);
				alert(thrownError);
			}
		});
	};

	function my_handler(data) {

		console.log('success handler');
		//console.log(data);

		$('#fest-list-items').append(data);

	};
})