function myFunction() {
    var x = document.getElementById("waiting");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
    var y = document.getElementById("botao");
    if (y.style.display === "none") {
      y.style.display = "block";
    } else {
      y.style.display = "none";
    }     
    var z = document.getElementById("theme");
    if (z.style.display === "none") {
      z.style.display = "block";
    } else {
      z.style.display = "none";
    }
    var w = document.getElementById("labelbox");
    if (w.style.display === "none") {
      w.style.display = "block";
    } else {
      w.style.display = "none";
    }         
  }
    window.onload = function(){
    document.getElementById("waiting").style.display='none';
};