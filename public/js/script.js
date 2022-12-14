$(document).ready(function(){
	console.log("test");
	$("#twit").mousedown(function(){
		console.log("Checked");
		if($("#twit").is(":checked") ) {
			$("#twitter").val("");
		} else if($("#twit").not(":checked") ){
			$("#twitter").val("Twitter");
		}
	});

	$("#red").mousedown(function(){
		console.log("Checked");
		if($("#red").is(":checked") ) {
			$("#reddit").val("");
		} else if($("#red").not(":checked") ){
			$("#reddit").val("Reddit");
		}
	});

	$("#trend").mousedown(function(){
		console.log("Checked");
		if($("#trend").is(":checked") ) {
			$("#trending").val("");
		} else if($("#trend").not(":checked") ){
			$("#trending").val("Trending");
		}
	});
});

