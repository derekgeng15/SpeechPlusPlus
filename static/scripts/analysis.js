


input = JSON.parse(input)
console.log(input['phrases'])
console.log(input['sentiment'])
console.log(input['intonation'])


var textBox = document.getElementById("firstDiv");
var count = 1;
let l = [];

for(p of input['phrases']) {
    var link = document.createElement("A");
    link.innerHTML = count + " " + p;
    link.dataset.toggle = "popover";
    link.dataset.title = p
    link.dataset.content = 'Sentiment: ' + input['sentiment'][count - 1].toString() +'\nIntonation: ' + input['intonation'][count - 1].toString()
    textBox.appendChild(link);
    textBox.appendChild(document.createElement("BR"));
    textBox.appendChild(document.createElement("BR"));
    l.push(count.toString())
    count += 1;
}

ctA = 0
ctB = 0
$('[data-toggle="popover"]').popover({ 
    html:true

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
