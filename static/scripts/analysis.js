

var sInput =  "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.";
var phrases = [];
var last = 0;
for(var i = 0; i<sInput.length; i += 1) {
    if(sInput[i] == '.') {
        phrases.push(sInput.slice(last, i));
        last = i+1;
    }
}

var textBox = document.getElementById("firstDiv");
var count = 1;
for(p of phrases) {
    var link = document.createElement("A");
    link.innerHTML = count + " " + p;
    link.dataset.toggle = "popover";
    textBox.appendChild(link);
    textBox.appendChild(document.createElement("BR"));
    textBox.appendChild(document.createElement("BR"));
    count += 1;
}

$('[data-toggle="popover"]').popover({ 
    html: true,
    title: "This is some text", 
    content: "this is some more text"
  });

let myChart = document.getElementById("myChart").getContext("2d");
let massPopChart = new Chart(myChart, {
    type: 'line',
    data: {
        labels: ["1", "2", "3", "4", "5", "6"],
        datasets: [{
            label: "Sentiment",
            data: [6174, 8294, -1245, 3205, -2034, 1859],
            backgroundColor: '#0D6EFD'
        },
        {
            label: "Intonation",
            data: [2394, 2049, -543, 1045, -3042, 3849],
            backgroundColor: '#fe019a',
        }
        ]
    },
    options: {}
});
