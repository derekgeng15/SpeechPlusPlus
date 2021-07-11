

$(function () {
    $('[data-toggle="popover"]').popover();
  });


$('.popover-dismiss').popover({
  trigger: 'focus'
})

var uploadBtn = document.getElementById("uploadBtn");
var loadingBtn = document.getElementById("loadingBtn");
var input = document.getElementById("fileInput");
var fileInputLabel = document.getElementById("fileInputLabel");


function changeFileName() {
  fileInputLabel.innerText = input.files[0].name;
}