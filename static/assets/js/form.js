$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				Results : $('#message').val(),
			},
			type : 'POST',
			url : '/predict'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.Results).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});