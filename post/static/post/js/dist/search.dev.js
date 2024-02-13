"use strict";

var headers;

input.oninput = function () {
  fetch("/search/?query=".concat(input.value)).then(function (response) {
    return response.text();
  }).then(function (data) {
    var parser = new DOMParser();
    var doc = parser.parseFromString(data, 'text/html');
    headers = doc.querySelectorAll('.result');
    res.innerHTML = '';

    for (var i = 0; i < 3; i++) {
      res.innerHTML += "<li>".concat(headers[i].innerHTML, "</li>");
    }
  });
};
//# sourceMappingURL=search.dev.js.map
