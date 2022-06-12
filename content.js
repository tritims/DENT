var body = JSON.stringify(
    document
    .getElementsByClassName('s-prose js-post-body')[0]
    .innerHTML)
    .replace(/\s\s+/g, ' ') 

var title = document.getElementById('question-header').getElementsByTagName('h1')[0].innerText
var DLTags = ['pytorch', 'tensorflow', 'theano', 'caffe', 'keras']

var requestURL = "http://10.21.29.157:3000/"
var requestBody = {
    "title": title, 
    "body": body
    }

// Function to verify tags by deep learning posts. 
function checkIfDL() {
    tags = document.getElementsByClassName('post-tag js-gps-track')
    for(let tag of tags){
        if(DLTags.includes(tag.innerText)){
            return true
        }
    }
    return false
}

if(checkIfDL()){
    var xhr = new XMLHttpRequest();  
    xhr.open("POST", requestURL);  
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.onreadystatechange = function() { 
      // If the request completed, close the extension popup
      if (xhr.readyState == 4)
        if (xhr.status == 200){
            console.log(JSON.parse(xhr.responseText))
            // callback(JSON.parse(xhr.responseText))
        }
    };
    // console.log(requestURL)
    xhr.send(JSON.stringify(requestBody)); 
}