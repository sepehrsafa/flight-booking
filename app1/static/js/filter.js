$('#systemflights').on('ifChecked', function(event){
  console.log(event);
  x = document.getElementById("systemflights");
  console.log(x);
  alert(event.type + ' callback');
});

$('#charterflights').on('ifChecked', function(event){
  console.log(event);
  //x = document.getElementById("system");
  //console.log(x);
  alert(event.type + ' callback');
});
