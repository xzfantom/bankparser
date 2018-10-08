$(function(){
	$('#btnParse').click(function(){
		
		$.ajax({
			url: '/parse',
			//data: $('form').serialize(),
			dataType: "JSON",
			data: new FormData('form'),
			processData: false,
			contentType: false,
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});