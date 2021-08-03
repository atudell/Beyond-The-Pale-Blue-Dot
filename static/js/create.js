function validateCreateAccount() {
	
	// Get the form and input elements
	let frm = document.getElementById("frmCreate");
	let n_username_input = frm.elements["txtNewUsername"];
	let n_password_input = frm.elements["txtNewPassword"];
	let c_password_input = frm.elements["txtConfirmPassword"];
	
	// Clear any previous formatting or error messages from previous attempts
	n_username_input.style.borderColor = "black";
	n_password_input.style.borderColor = "black";
	c_password_input.style.borderColor = "black";
	let error_message = document.getElementsByClassName("error");
	if (error_message.length > 0) {
		error_message[0].remove();
	}
	
	// Create new input objects
	let n_username = new Input(n_username_input.value);
	let n_password = new Input(n_password_input.value);
	let c_password = new Input(c_password_input.value);
	
	// Check if the username is composed of all ASCII characters
	if (!n_username.isAscii()) {
		
		// Create a new error object from the error class
		let error = new Error(
			"A non-ASCII character, such as an emoji or other unusual symbol was detected. Please remove and use standard letters and symbols.",
			"frmCreate"
			)	
		// Insert the error message and highlight the title field
		error.insertError();
		error.highlightField("txtNewUsername");
		
		return false;
	}
	
	// Check if the password is composed of all ASCII characters
	// The second password will not be checked, because it should match the first, anyway
	if (!n_password.isAscii()) {
		
		// Create a new error object from the error class
		let error = new Error(
			"A non-ASCII character, such as an emoji or other unusual symbol was detected. Please remove and use standard letters and symbols.",
			"frmCreate"
			)	
		// Insert the error message and highlight the title field
		error.insertError();
		error.highlightField("txtNewPassword");
		
		return false;
	}
	
	// Check if the username is between 1 and 50 characters (limited by the database)
	if (!n_username.isCorrectLength(0, 50)) {
		let error = new Error(
			"The username must be between 1-50 characters.", 
			"frmCreate"
			)
		// Insert the error message and highlight the title field
		error.insertError();
		error.highlightField("txtNewUsername");
		
		return false;
	}
	
	// Check if the password is between 1 and 50 characters (limited by the database)
	if (!n_password.isCorrectLength(0, 50)) {
		let error = new Error(
			"The password must be between 1-50 characters.", 
			"frmCreate"
			)
		// Insert the error message and highlight the title field
		error.insertError();
		error.highlightField("txtNewPassword");
		
		return false;
	}
	
	// Check the passwords match
	if (n_password.string !== c_password.string) {
		
		let error = new Error(
			"The passwords do not match.", 
			"frmCreate"
			)
			
		// Insert the error message and highlight the title field
		error.insertError();
		error.highlightField("txtNewPassword");	
		error.highlightField("txtConfirmPassword");
		
		return false;
	}
	
	// If none of the above pass false, assume true
	return true;		
}