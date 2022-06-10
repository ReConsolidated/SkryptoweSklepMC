var element = document.getElementById('nick_input');
var addError = function() {
console.log("adding error");

element.classList.add('error');

 setTimeout(function () {
        element.classList.remove('error');
    }, 2000);
 };
