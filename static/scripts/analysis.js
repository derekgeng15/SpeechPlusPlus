

var sInput =  "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.";
var phrases = [];
var last = 0;

input = JSON.parse(input)
console.log(input['phrases'])
console.log(input['sentiment'])
console.log(input['intonation'])
for(var i = 0; i<sInput.length; i += 1) {
    if(sInput[i] == '.') {
        phrases.push(sInput.slice(last, i));
        last = i+1;
    }
}

var textBox = document.getElementById("firstDiv");
var count = 1;
let l = [];
for(p of input['phrases']) {
    var link = document.createElement("A");
    link.innerHTML = count + " " + p;
    link.dataset.toggle = "popover";
    textBox.appendChild(link);
    textBox.appendChild(document.createElement("BR"));
    textBox.appendChild(document.createElement("BR"));
    l.push(count.toString())
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
        labels: l,
        datasets: [{
            label: "Sentiment",
            data: input['sentiment'],
            backgroundColor: '#0D6EFD'
        },
        {
            label: "Intonation",
            data: input['intonation'],
            backgroundColor: '#fe019a',
        }
        ]
    },
    options: {}
});


iaverage = 0
saverage = 0
for(i of input['intonation'])
    iaverage += i;
for(s of input['sentiment'])
    saverage += s;
iaverage /= count;
saverage /= count;
document.getElementById('sentimentbar').style.width= (saverage / 2 + 50).toString() + '%'
document.getElementById('intonationbar').style.width= (iaverage / 2 + 50).toString() + '%'
