"use strict";

add_cat.onclick = function () {
  var option = document.createElement('option');
  var li = document.createElement('li');
  var btn = document.createElement('button');
  btn.innerHTML = '-';
  btn.classList.add('btn');

  btn.onclick = function (e) {
    e.currentTarget.parentNode.remove(); //document.querySelector(`#${e.currentTarget.previousSibling.innerHTML}`).remove()

    console.log(e.currentTarget.previousSibling);
    document.getElementById(e.currentTarget.previousSibling);
  };

  option.id = option.name = li.innerHTML = input_cat.value;
  input_cat.value = '';
  select_cat.append(option);
  ul_cat.append(li);
  li.append(btn);
};
//# sourceMappingURL=add_article.dev.js.map
