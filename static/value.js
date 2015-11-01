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


@app.route("/ajax_admin")
def ajax_admin():
	ans=None
	if (request.method=='POST'):
		dealer=request.form['dealer']
		ans=db.data.find({'name':dealer})
		render_template('admin_main.html',title='Admin',ans=ans)
	return render_template('admin_main.html',title='Admin',ans=ans)



<form action="" method="POST" id="adminform" name="myForm">
<input type="submit" value="Submit">
</form>
<select id="dealers" form="adminform">
{% for dlr1 in dlr %}
<option value="{{dlr1.name}}">{{dlr1.name}}</option>
{%endfor%}
</select>
