// Even though text validation is done server-side, client-side validations will also be done
// These will reduce use of the server and make things easier for users
class Input {
	
	// Construct the object with just a string
	constructor(string) {
		this.string = string;
	}
	
	// Method to check is string contains all ASCII characterSet
	// Char Code is used instead of RegEx, because its easier to maintain
	isAscii() {
		// cycle through the charactes in the string
		for (var i = 0; i < this.string.length; i++) {
			// If the character code is greater than 127, it's not ASCII
			if (this.string.charCodeAt(i) > 127) {
				return false;
			}
		}
		
		// If none of the values return false, the string must have only ASCII characters
		return true;
	}
	
	// Function to determine that the string is the correct length
	isCorrectLength(min_length, max_length) {
		
		// Get the length of the string
		let string_length = this.string.length;
		
		// if the string is greater than the minimum and less than the maximum, the string is the incorrect length
		if (string_length > min_length && string_length < max_length) {
			return true;
		} else {
			return false;
		}
	}
	
}

// Create a class for outputting errors
class Error {
	
	// Construct the object with an error message
	constructor(error, form_id) {
		this.error = error;
		this.form_id = form_id;
	}
	
	// Writes a method that inserts a new paragraph tag before a specified part of the document
	insertError() {
		
		// Create new paragraph tag
		let error_tag = document.createElement("p")
		
		// Create and add text to the new tag
		let error_message = document.createTextNode(this.error);
		error_tag.appendChild(error_message);
		
		// Set the class of the error message to error
		error_tag.setAttribute("class", "error");
	
		// get the form element
		let form_tag = document.getElementById(this.form_id);

		// Insert the error message
		form_tag.appendChild(error_tag);
	}
	
	highlightField(field_name) {
		
		// get form element
		let form_tag = document.getElementById(this.form_id);
		
		// get the relevant field
		let field = form_tag.elements[field_name]
		
		// Change the border colorDepth
		field.style.borderColor = "red";

	}
	
}