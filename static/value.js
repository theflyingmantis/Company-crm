function v1()
{
	console.log("In value.YO!!");
	var dlr=document.getElementById("dealers").value;
	console.log(dlr);
	$.ajax({
			type:"GET",//Check and change it to GET
			url:"/ajax_admin",
			data: {dealer: dlr},
			success: function(answer)
			{
				console.log(answer);
				//console.log(answer.comments,answer.id1);
				alert("Change Ackonowledge");
			},
			error: function(err)
			{
				console.log(err);
				alert(err);
				alert("Error");
			}
		});


}





