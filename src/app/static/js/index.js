$(function(){
	$('#btnParse').click(function(){
		
		$.ajax({
			url: '/parse',
			data: $('form').serialize(),
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