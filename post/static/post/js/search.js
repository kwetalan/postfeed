let headers;
input.oninput = function(){
  fetch(`/search/?query=${input.value}`)
    .then(response => response.text())
    .then(data => {
      let parser = new DOMParser();

      let doc = parser.parseFromString(data, 'text/html');

      headers = doc.querySelectorAll('.result');

      res.innerHTML = '';

      for(let i = 0; i < 3; i++){
        res.innerHTML += `<li>${headers[i].innerHTML}</li>`
      }
    })
}