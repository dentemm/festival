$(document).ready(function () {

   	// Change appearance of selected category button and ajax call to fetch subcategories
	$('#loadmore').click(function() {

		ajax_call();
	});

	function ajax_call() {

		console.log('JEEEEEEEEEJ');

		$.ajax({
			//url:"/products/overview/products/",
			url:"/index/",
			type: "GET",
			success: my_handler,

			error: function(xhr, ajaxOptions, thrownError) {
				console.log(xhr.status);
				alert(thrownError);
			}
		});
	};

	function my_handler (data) {

		console.log('success handler');

	};
})