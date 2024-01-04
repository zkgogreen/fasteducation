const loop3 = document.getElementsByClassName("loop-3");

for (var i = 0; i < loop3.length; i++) {
    let getloop = loop3[i].children[0].cloneNode(true); // Clone the first child
    for (var j = 0; j < 2; j++) {
      loop3[i].appendChild(getloop.cloneNode(true)); // Append the cloned element
    }
  }