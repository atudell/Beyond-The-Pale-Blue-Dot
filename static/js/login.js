function validateLogin() {
	
	// Get the form and input elements
	let frm = document.getElementById("frmLogin");
	let username_input = frm.elements["txtUsername"];
	let password_input = frm.elements["txtPassword"];
	
	
	// Clear any previous formatting or error messages from previous attempts
	username_input.style.borderColor = "black";
	password_input.style.borderColor = "black";
	let error_message = document.getElementsByClassName("error");
	if (error_message.length > 0) {
		error_message[0].remove();
	}
	
	// Validate that the password was not left blank
	if (username_input.value == "") {
		let error = new Error(
			"Username may not be left blank", 
			"frmLogin"
			)
		// Insert the error message and highlight the title field
		error.insertError();
		error.highlightField("txtUsername");

		return false;
	}
	
	// Validate that the password was not left blank
	if (password_input.value == "") {
		let error = new Error(
			"Password may not be left blank", 
			"frmLogin"
			)
		// Insert the error message and highlight the title field
		error.insertError();
		error.highlightField("txtPassword");
		
		return false;
	}
	
	
	// If none of the above pass false, assume true
	return true;		
}