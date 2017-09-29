benificiaries = []
inventory = []


function login() {
	var uname = document.getElementById('exampleInputEmail1').value;
	var password = document.getElementById('exampleInputPassword1').value;

	if (uname="admin" && password=="admin"){
		window.location.replace('admin.html');
		$("#loginError").css("display", "none");
	}
	else if (uname="abc" && password=="abc"){
		window.location.replace('user.html');
		$("#loginError").css("display", "none");
	}
	else{
		$("#loginError").css("display", "block");
	}
}

function matching(){
	
}