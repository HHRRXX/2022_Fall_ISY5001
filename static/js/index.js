
const image = document.getElementById('image'); 
const canvas = document.getElementById('canvas');
const dropContainer = document.getElementById('container');
const warning = document.getElementById('warning');
const fileInput = document.getElementById('fileUploader');

document.getElementById("Submit-btn").onclick = function(){
  document.getElementById("response").innerHTML = '';
  fetch('/getCategoryByName?bookName=' + document.getElementById("bookNameInput").value)
    .then(function(response) {
        return response.json()
      })
      .then(function(r) {
        document.getElementById("bookNameInput").value = '';
        document.getElementById("response2").innerHTML = 'Category is: '+r.category;
      })
      .catch(function(err) {
        document.getElementById("response").innerHTML = 'error!!!';
      });
};

function preventDefaults(e) {
  e.preventDefault()
  e.stopPropagation()
};


function windowResized() {
  let windowW = window.innerWidth;
  if (windowW < 480 && windowW >= 200) {
    dropContainer.style.display = 'block';
  } else if (windowW < 200) {
    dropContainer.style.display = 'none';
  } else {
    dropContainer.style.display = 'block';
  }
}

['dragenter', 'dragover'].forEach(eventName => {
  dropContainer.addEventListener(eventName, e => dropContainer.classList.add('highlight'), false)
});

['dragleave', 'drop'].forEach(eventName => {
  dropContainer.addEventListener(eventName, e => dropContainer.classList.remove('highlight'), false)
});

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropContainer.addEventListener(eventName, preventDefaults, false)
});

dropContainer.addEventListener('drop', gotImage, false)

// send image to server, then receive the result, draw it to canvas.
function communicate(img_base64_url) {
document.getElementById("response4").innerHTML ='Loading...';
  var form = new FormData();
  form.append("imageBase64Str",img_base64_url);
  $.ajax({
    url: '/getPopularity',
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({"imageBase64Str": img_base64_url}),
    dataType: "json"
  }).done(function(response_data) {
      document.getElementById("response4").innerHTML = "Popularity rank: " + response_data.popularity+'<br/> Predicted Genre: '+ response_data.Genre ;
      //drawResult(response_data.results);
  });
}

// handle image files uploaded by user, send it to server, then draw the result.
function parseFiles(files) {
  const file = files[0];
  const imageType = /image.*/;
  if (file.type.match(imageType)) {
    warning.innerHTML = '';
    const reader = new FileReader();
    reader.readAsDataURL(file);

    reader.onloadend = () => {
      image.src = reader.result;
      // send the img to server
      communicate(reader.result);
    }
  } else {
    warning.innerHTML = 'Please drop an image file.';
  }

}

// call back function of drag files.
function gotImage(e) {
  const dt = e.dataTransfer;
  const files = dt.files;
  if (files.length > 1) {
    console.error('upload only one file');
  }
  parseFiles(files);
}

// callback function of input files.
function handleFiles() {
  parseFiles(fileInput.files);
}

// callback fuction of button.
function clickUploader() {
  fileInput.click();
}

