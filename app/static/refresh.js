function getdm(id){
  var messages = document.getElementById("messages");
  fetch("/friends/"+id+"/thischat").then(function(json){
    return json.text();
  }).then(function(textresponse){
    messages.innerHTML = textresponse;
  })
}

function getgroup(id){
  var messages = document.getElementById("messages");
  fetch("/groups/"+id+"/thischat").then(function(json){
    return json.text();
  }).then(function(textresponse){
    messages.innerHTML = textresponse;
  })
}
