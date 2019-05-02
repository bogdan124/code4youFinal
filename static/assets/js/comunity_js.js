var myVar;

function myFunction(i) {
if(i==1){
   showPage();
}
  myVar = setTimeout(blurPage, 1000);
}

function blurPage() {
document.getElementById("loader").style.display = "none";
document.getElementById("row_for_show").style.filter = "inherit";
}
function showPage() {
document.getElementById("loader").style.display = "initial";
document.getElementById("row_for_show").style.filter = "blur(7px)";
}
