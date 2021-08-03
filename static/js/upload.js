function validateUploadInput() {
	
	// Get the form and input elements
	let frm = document.getElementById("frmUpload");
	let title_input = frm.elements["txtTitle"];
	let caption_input = frm.elements["txtCaption"]; 
	let file_input = frm.elements["fileUpload"];
	
	// Clear any previous formatting or error messages from previous attempts
	title_input.style.borderColor = "black";
	caption_input.style.borderColor = "black";
	let error_message = document.getElementsByClassName("error");
	if (error_message.length > 0) {
		error_message[0].remove();
	}
	
	// Create new input objects
	let title = new Input(title_input.value)
	let caption = new Input(caption_input.value)
	
	// Check if the title is composed of all ASCII characters
	if (!title.isAscii()) {
		
		// Create a new error object from the error class
		let error = new Error(
			"A non-ASCII character, such as an emoji or other unusual symbol was detected. Please remove and use standard letters and symbols.",
			"frmUpload"
			)	
		// Insert the error message and highlight the title field
		error.insertError();
		error.highlightField("txtTitle");
		
		return false;
	}
	
	// Check if the caption is composed of all ASCII characters
	if (!caption.isAscii()) {
		
		// Create a new error object from the error class
		let error = new Error(
			"A non-ASCII character, such as an emoji or other unusual symbol was detected. Please remove and use standard letters and symbols.",
			"frmUpload"
			)
		// Insert the error and highlight the caption field
		error.insertError();
		error.highlightField("txtCaption");
		
		return false;
	}
	
	// Check if the title is between 0 and 50 characters (limited by the database)
	if (!title.isCorrectLength(0, 50)) {
		let error = new Error(
			"The title must be between 1-50 characters.", 
			"frmUpload"
			)
		// Insert the error message and highlight the title field
		error.insertError();
		error.highlightField("txtTitle");
		
		return false;
	}
	
	// Check if the caption is between 0 and 100 characters (limited by the database)
	if (!caption.isCorrectLength(0, 100)) {
		let error = new Error(
			"The caption must be between 1-100 characters.", 
			"frmUpload"
			)
		// Insert the error and highlight the caption field
		error.insertError();
		error.highlightField("txtCaption");
		
		return false;
	}
	
	// Check if there's a file attached
	if (file_input.value == "") {
		let error = new Error (
			"No file attached.",
			"frmUpload"
		)
		// Insert error message
		error.insertError();
		
		return false;
	}
	
	// Check if the extension matches an accepted format
	let file_extensions = ["jpg", "jpeg", "png", "gif"]
	let file_ext = file_input.value.split(".").pop()
	if (!file_extensions.includes(file_ext)) {
		let error = new Error (
			"Only .jpg, .jpeg, .png. and .gif file permitted",
			"frmUpload"
		)
		// Insert error message
		error.insertError();
		
		return false;
	}
	
	// If none of the above pass false, assume true
	return true;
} 

