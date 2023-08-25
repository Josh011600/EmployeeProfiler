document.addEventListener("DOMContentLoaded", function() {
    // Get references to the button and dropdown content
    const dropdownButton = document.getElementById("dropdownButton");
    const dropdownContent = document.getElementById("dropdownContent");
    
    // Add click event listener to the button
    dropdownButton.addEventListener("click", function() {
        // Toggle the visibility of the dropdown content
        dropdownContent.classList.toggle("show");
    });
    
    // Close the dropdown if the user clicks outside of it
    window.addEventListener("click", function(event) {
        if (!event.target.matches(".dropbtn")) {
            if (dropdownContent.classList.contains("show")) {
                dropdownContent.classList.remove("show");
            }
        }
    });
});
