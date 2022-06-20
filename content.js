// Global Variables
var CUTOFF = 0.5
var QUESTION_BODY_CLASSNAME =  'post-layout'
var TAGS_CLASSNAME = 'post-tag js-gps-track'
var BASE_URL = 'https://rishalab.github.io/dl_energy_patterns/'

var body = JSON.stringify(
    document
    .getElementsByClassName('s-prose js-post-body')[0]
    .innerHTML)
    .replace(/\s\s+/g, ' ') 

var title = document.getElementById('question-header').getElementsByTagName('h1')[0].innerText
var DLTags = ['pytorch', 'tensorflow', 'theano', 'caffe', 'keras']

var requestURL = "http://localhost:3000/"
var requestBody = {
    "title": title, 
    "body": body
    }

// Function to verify tags by deep learning posts. 
function checkIfDL() {
    tags = document.getElementsByClassName(TAGS_CLASSNAME)
    for(let tag of tags){
        if(DLTags.includes(tag.innerText)){
            return true
        }
    }
    return false
}

function getPatternURLOffset(tagname){
    switch(tagname){
        case 'checkpoint': return 'checkpoint.html';
        case 'pruning': return 'pruning.html';
        case 'quantization': return 'quantization.html'; 
        case 'distillation': return 'distillation.html';
        case 'efficient read write': return 'read-write.html';
        case 'memory leaks': return 'leaks.html'; 
        case 'pretrained networks': return 'pretrained.html';
        case 'tensor operations': return 'tensor-operations.html';
        default: return '';
    }
}

function generateTag(tagname){
    e = document.createElement('div')
    a = document.createElement('a')
    e.className = 'energytag'
    e.innerText = tagname
    a.target = '_blank'
    a.href = BASE_URL + getPatternURLOffset(tagname)
    a.appendChild(e)
    return a
}

function prependTagToQuestion(e){
    document.getElementsByClassName(QUESTION_BODY_CLASSNAME)[0].prepend(e)
}

function tagQuestion(res){
    if (res.pattern && res.score){
        if(res.score > CUTOFF){
            tagElement = generateTag(res.pattern)
            prependTagToQuestion(tagElement)
        }
    }
}

if(checkIfDL()){
    var xhr = new XMLHttpRequest();  
    xhr.open("POST", requestURL);  
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.onreadystatechange = function() { 
      if (xhr.readyState == 4)
        if (xhr.status == 200){
            res = JSON.parse(xhr.responseText)
            tagQuestion(res)
            // callback(JSON.parse(xhr.responseText))
        }
    };
    // console.log(requestURL)
    xhr.send(JSON.stringify(requestBody)); 
}
