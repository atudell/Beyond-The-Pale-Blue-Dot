// Start counting how many times the renderInfiniteScroll function is called
// Count starts at 1, because we assume the function has already been called once on page load
var count = 0;

function renderInfiniteScroll(count) {

	// Assign the main content div to a variable
	let main_content = document.getElementsByClassName("divMainContent")[0];

    fetch("/loadcontent/" + count.toString())
        .then(response => response.json())
        .then(data => {
            
            // if "NONE" is a key with a value 0, no pictures are downloading
            // Simply terminate the function early, so a bunch of title cards with 
            // "undefined" don't populate the page
            if (data["NONE"] == "0") {
                return 0;
            }
            
            // Get the number of images from the data. Usually this is 5, but it can be variable
            // Divide by 3, because data should always come in packets of 3
            let num_images = Object.keys(data).length/3;
            
        	for (i = 0; i < num_images; i++){
            	// Create a new div element, which will become a content card
            	let card = document.createElement("DIV");
            	card.setAttribute("class", "divContentCard")
            	
            	// Create the content for the card
            	let title = document.createElement("H3");
            	title.innerHTML = data["title" + i.toString()];
            	let img = document.createElement("IMG");
            	img.setAttribute("src", "static/uploads/" + data["image_path" + i.toString()]);
            	let caption = document.createElement("P");
            	caption.innerHTML = data["caption" + i.toString()];
            	
            	// Append the card with a title, picture, and caption
            	card.appendChild(title);
            	card.appendChild(img);
            	card.appendChild(caption);
            	
            	// append the card to the main content div
            	main_content.appendChild(card);	
        	}             
                      
            });
        

}

document.addEventListener("scroll", function() {
		
		// Set variable for the bottom of the page
		// The extra 100 is for insurance. Some browsers don't match this formula exactly, but this will catch most of them
		let scrollHeight = document.body.scrollHeight - document.body.clientHeight - 100;

		// if the scroll goes down too far, render the infinite scroll
		if(document.documentElement.scrollTop >= scrollHeight){
			// Add 1 to the count
    		count = count + 1
			renderInfiniteScroll(count);
		}
		
}, false);

