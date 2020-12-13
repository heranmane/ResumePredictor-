var dropdownMenu = d3.select("#Dropdown11");

var sub; 

function getData() {
    var job = dropdownMenu.property("value");
    
    var filteredData = sub.filter(item => item.Job_Type === job);
    
    var data = {
        y: filteredData.map(item => parseInt(item.Count)),
        x: filteredData.map(item => item.Skill),
        type: "bar"
    }
    console.log(data)

    var layout = {
        title: "'Bar' Chart",
        height: 600,
        width: 600
    };

    Plotly.newPlot("plot", [data], layout);
}

dropdownMenu.on("change", getData)


d3.json("./Job_Type").then(function (importedData) {
    sub = importedData
    getData()
    console.log(importedData)




}).catch(function (error) {
    console.log(error);
});


var data = [{
    values: [13, 11.3, 8.3, 5.6, 3.9, 57.9],
    labels: ['Consulting and Business Services', 'Internet and Softrware', 'Banks and Financial Services', 'Health Care',
          'Insurance', 'Other Industries'],
    type: 'pie'
  }];
  var layout = {
    height: 400,
    width: 500
  };
  Plotly.newPlot('myDiv', data, layout);