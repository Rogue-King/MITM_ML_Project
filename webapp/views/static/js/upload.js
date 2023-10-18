// Get references to the button and the file input element
const uploadButton = document.getElementById('fileSubmit');
const fileInput = document.getElementById('formFile');

// Function to handle form submission
function handleFormSubmission() {
  // Create a FormData object and append the file input data
  var formData = new FormData();

  if (fileInput.files.length > 0) {
    formData.append('file', fileInput.files[0]);

    // Send an AJAX request to handle the form submission
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);

    xhr.onload = function() {
      if (xhr.status === 200) {
        // Handle the response from the server (e.g., display a message to the user)
        console.log(xhr.responseText);
      } else {
        // Handle errors
        console.error('Server Error: ' + xhr.status);
      }
    };

    xhr.send(formData);
  } else {
    // Handle the case where no file is selected
    console.error('No file selected');
  }
}

// Add an event listener to the button
uploadButton.addEventListener('click', handleFormSubmission);