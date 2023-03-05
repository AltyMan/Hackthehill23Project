window.onload = function() {
  formGrid();
  gridElement = document.getElementById("grid");
  // createText("Read Me", "read-me", 0);
  // createText("Read Me", "read-me-1", 1);
}

// document.getElementById("cards").onmousemove = e => {
//     for(const card of document.getElementsByClassName("card")) {
//       const rect = card.getBoundingClientRect(),
//             x = e.clientX - rect.left,
//             y = e.clientY - rect.top;
  
//       card.style.setProperty("--mouse-x", `${x}px`);
//       card.style.setProperty("--mouse-y", `${y}px`);
//     };
//   }

var gridElement = document.getElementById("grid");
var elmHold = "";
var lastSelected = "";
var currSelected = "";
var currLocation = "";

var count = 0;

var horzGrid = Math.floor(screen.width / 84) - 1;
var vertGrid = Math.floor(screen.height / 100) - 2;

function formGrid() {
  for (let i = 1; i < horzGrid * vertGrid; i++) {
    var grid = document.getElementById("grid-box").cloneNode(true);
    document.getElementById("grid").appendChild(grid);
  }
  var autoCount = "";
  for (let i = 0; i < horzGrid; i++) {
    autoCount += "auto ";
  }
  document.getElementById("grid").style.gridTemplateColumns = autoCount;
}

function generateContent(text) {
  console.log(text);
  for (let i = 0; i < text.length; i++) {
    console.log(gridElement);
    var num = 0;
    for (let i = 0; i < gridElement.childElementCount; i++) {
      if (gridElement.children[i].id != "grid-box-full") {
        break;
      }
      num++;
    }
    createText(String(text[0].filename), "text-" + String(count), num);
    count++;
  }
}

function deleteElement(elm) {
  elm.parentNode.id = "grid-box";
  elm.remove();
}

function createText(name, givenId, gridPos) {
  var text = document.getElementById("default-text").cloneNode(true);
  text.id = "text-" + givenId;
  var child = text.childNodes;
  child[3].textContent = name;
  var pos = document.getElementById("grid").children[gridPos];
  text.style.display = "inline-block";
  pos.appendChild(text);
  pos.id = "grid-box-full";
}

function createImg(name, givenId, img, gridPos) {
  var app = document.getElementById("default-img").cloneNode(true);
  app.id = "img-" + givenId;
  var child = app.childNodes;
  child[3].textContent = name;
  child[1].src = img;
  var pos = document.getElementById("grid").children[gridPos];
  app.style.display = "inline-block";
  pos.appendChild(app);
  pos.id = "grid-box-full";
}

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev, elm) {
  elm.parentNode.id = "grid-box";
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev, elm) {
  ev.preventDefault();
  if (ev.target.id == "grid-box") {
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
    ev.target.id = "grid-box-full";
  } else if (elm.id == "grid-box-full" && elm.children[0].id == "recycle-bin" && currSelected.id != "recycle-bin" && currSelected.id != "app-background-settings" && currSelected.id != "app-google-chrome") {
    deleteElement(currSelected);
  } else {
    elmHold.parentNode.id = "grid-box-full";
  }
}