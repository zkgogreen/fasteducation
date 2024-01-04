var wrapper = document.getElementsByClassName("loop");
for(var j=0;j<wrapper.length;j++){
    var myHTML = wrapper[j].innerHTML;
    var result = ""
    for(var i=0;i<5;i++){
        result += myHTML
    }
    wrapper[j].innerHTML = result
}

// var message = document.getElementById("message");
// var bodyperson = document.getElementById("bodyperson");
// var messagetext = document.getElementById("messagetext");
// var messageback = document.getElementById("messageback");

// bodyperson.addEventListener('click', function(){
//     message.classList.add("active")
// })
// messageback.addEventListener('click', function(){
//     message.classList.remove("active")
// })