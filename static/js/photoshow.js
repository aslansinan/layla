function gettingPhoto(id) {
  var range = document.createRange();
  range.selectNode(document.getElementById(id));
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(range);
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  document.getElementById('photoshow').innerHTML = range;

  var photo = document.getElementById("photoshow");
  photo.innerHTML =  "<img class='gallerymodal' src='"+range+"'>";
}