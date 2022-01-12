function flightautocomplete(inp) {

  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {

      var a, b, i, val = this.value;

      if (val.length > 2){
        const test = async searchText => {
          const res = await fetch('https://api.connectota.com/RIAM_main/panel/airport/autoFill/'+val);
          const arr = await res.json();
          console.log(arr);
          closeAllLists();
          if (!val) { return false;}
          currentFocus = -1;
          /*create a DIV element that will contain the items (values):*/
          a = document.createElement("DIV");
          a.setAttribute("id", this.id + "autocomplete-list");
          a.setAttribute("class", "autocomplete-items");
          a.setAttribute("role", "listbox")

          /*append the DIV element as a child of the autocomplete container:*/
          this.parentNode.appendChild(a);
          /*for each item in the array...*/
          for (i = 0; i < arr.length; i++) {
              /*create a DIV element for each matching element:*/
              b = document.createElement("DIV");
              /*make the matching letters bold:*/
              b.innerHTML = "<strong>" + arr[i]["cityName"] + " - "+arr[i]["code"]+ "</strong>";

              /*insert a input field that will hold the current array item's value:*/
              b.innerHTML += "<input type='hidden' data-iatacode=" + arr[i]["code"] + " value=" + arr[i]["cityName"] + ">";
              /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
                  const selectedinput = this.getElementsByTagName("input")[0]
                  inp.value = selectedinput.value;
                  inp.dataset.iatacode = selectedinput.dataset.iatacode
                  /*insert the value for the autocomplete text field:*/
                  /*inp.value = this.getElementsByTagName("input")[0].value;
                  /*close the list of autocompleted values,
                  (or any other open lists of autocompleted values:*/
                  closeAllLists();
              });
              a.appendChild(b);

          }


        };
        test()
        };

  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}


function trainautocomplete(inp) {

  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {

      var a, b, i, val = this.value;

      if (val.length > 0){
        const test = async searchText => {
          const res = await fetch('/api/autofill/trainstations/'+val);
          const arr = await res.json();
          console.log(arr);
          closeAllLists();
          if (!val) { return false;}
          currentFocus = -1;
          /*create a DIV element that will contain the items (values):*/
          a = document.createElement("DIV");
          a.setAttribute("id", this.id + "autocomplete-list");
          a.setAttribute("class", "autocomplete-items");
          a.setAttribute("role", "listbox")

          /*append the DIV element as a child of the autocomplete container:*/
          this.parentNode.appendChild(a);
          /*for each item in the array...*/
          for (i = 0; i < arr.length; i++) {
              /*create a DIV element for each matching element:*/
              b = document.createElement("DIV");
              /*make the matching letters bold:*/
              b.innerHTML = "<strong>" + arr[i]["StationNameFarsi2"] + " - " + arr[i]["StationNameEnglish"] + "</strong>";

              /*insert a input field that will hold the current array item's value:*/
              b.innerHTML += "<input type='hidden' data-stationcode ="+arr[i]["StationCode"]+ " value=" + arr[i]["StationNameFarsi2"] +">";
              /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
                  /*insert the value for the autocomplete text field:*/
                  const selectedinput = this.getElementsByTagName("input")[0]
                  inp.value = selectedinput.value;
                  inp.dataset.stationcode = selectedinput.dataset.stationcode
                  /*close the list of autocompleted values,
                  (or any other open lists of autocompleted values:*/
                  closeAllLists();
              });
              a.appendChild(b);
          }
        };
        test()
        };

  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

flightautocomplete(document.getElementById("flightoriginbox"));
flightautocomplete(document.getElementById("flightdesbox"));


trainautocomplete(document.getElementById("trainoriginbox"));
trainautocomplete(document.getElementById("traindesbox"));





function radioboxstatus(x) {
  var y = document.getElementById("datepicker-Return");
  if (x.value =="OneWay"){
    y.style.background = "rgb(211, 211, 211)"
    y.disabled = true; 
  }
  else if (x.value =="RoundTrip"){
    y.disabled = false; 
    y.style.background = "none";

  }
}


function flightsearchsubmit(){
  const userinfoform = document.getElementById("flightsearchform")
  console.log(userinfoform)
  const formData = new FormData(userinfoform)

  var flightinfojson = {};

  formData.forEach(function(value, key){
    flightinfojson[key] = value;
  });
  const originiatacode = document.getElementById("flightoriginbox").dataset.iatacode
  const desiatacode = document.getElementById("flightdesbox").dataset.iatacode
  var depdate = flightinfojson["depdate"].replace("/", "-")
  var depdate = depdate.replace("/", "-")
  console.log(flightinfojson)

  window.location.href = "/Search/Flights/"+originiatacode+"/"+desiatacode+"/"+depdate+"/"+"1-0-0"
  

  console.log(depdate)

}


function trainsearchsubmit(){
  const userinfoform = document.getElementById("trainsearchform")
  console.log(userinfoform)
  const formData = new FormData(userinfoform)

  var flightinfojson = {};

  formData.forEach(function(value, key){
    flightinfojson[key] = value;
  });
  const originiatacode = document.getElementById("trainoriginbox").dataset.stationcode
  const desiatacode = document.getElementById("traindesbox").dataset.stationcode
  var depdate = flightinfojson["depdate"].replace("/", "-")
  var depdate = depdate.replace("/", "-")
  console.log(flightinfojson)

  window.location.href = "/Search/Trains/"+originiatacode+"/"+desiatacode+"/"+depdate+"/"+"1/1"
  

  console.log(depdate)

}