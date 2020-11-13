// var svg = d3.select('svg');
// var svgContainer = d3.select('body');


var svgWidth = 800;
var svgHeight = 450;

var margin = 80;
var width = 800 - 2 * margin;
var height = 400 - 2 * margin;

var chartMargin = {
  top: 60,
  right: 40,
  bottom: 40,
  left: 40
};

// Define dimensions of the chart area
var chartWidth = svgWidth - chartMargin.left - chartMargin.right;
var chartHeight = svgHeight - chartMargin.top - chartMargin.bottom;

// Select body, append SVG area to it, and set the dimensions

var Job_Type = ""


changejobType("")
function changejobType(jobtype) {
  d3.select("#vis-container").html("")
  var svg = d3
    .select("#vis-container")
    .append("svg")
    .attr("height", svgHeight)
    .attr("width", svgWidth)
    .style("fill", "#DBBF1B");
  

  // Append a group to the SVG area and shift ('translate') it to the right and down to adhere
  // to the margins set in the "chartMargin" object.
  var chartGroup = svg.append("g")
    .attr("transform", `translate(${chartMargin.left}, ${chartMargin.top})`);

  d3.json("./heran")
    .then(function (raw_importedData) {
      console.log(raw_importedData)
      var chart = svg.append('g')
        .attr('transform', `translate(${margin}, ${margin})`);

      var importedData = raw_importedData;
      if (jobtype !== "") {
        importedData = raw_importedData.filter(data => data.Job_Type === jobtype)
      } 

      // var length = Object.values(importedData).length
      // // console.log(length)

      // group data by salary 
      var nested_data = d3.nest()
        .key(function (d) {

          return d.Queried_Salary;

        })
        .rollup(function (ids) {
          return ids.length;
        })
        .entries(importedData);
      
// sort the x axis keys for each filters 
      var sorted_nested_data = [];
      var array = ["<80000", "80000-99999", "100000-119999", "120000-139999", "140000-159999", ">160000"]
      array.forEach((k) => {
        nested_data.forEach((o) => {
          if (o["key"] === k) {
            sorted_nested_data.push(o)
          }
        })
      });
      nested_data = sorted_nested_data;

      // Configure a band scale for the horizontal axis with a padding of 0.1 (10%)
      var xScale = d3.scaleBand()
        .domain(nested_data.map(data => data.key))
        .range([0, width])
        .padding(0.3)

      var yScale = d3.scaleLinear()
        .domain([0, d3.max(nested_data.map(data => data.value))])
        // .domain([0, d3.max(data => data.value)])
        .range([height, 0])



      var jobType = importedData.filter(j => j.Job_Type)
      // console.log(jobType)

      var makeYLines = () => d3.axisLeft()
        .scale(yScale)

      var makeXLines = () => d3.axisBottom()
        .scale(xScale)

      chart.append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(d3.axisBottom(xScale));

      chart.append('g')
        .call(d3.axisLeft(yScale));

      // chart.append('g')
      //   .attr('class', 'grid')
      //   .attr('transform', `translate(0, ${height})`)
      //   .call(makeXLines()
      //     .tickSize(-height, 0, 0)
      //     .tickFormat('')
      //   )

      chart.append('g')
        .attr('class', 'grid')
        .call(makeYLines()
          .tickSize(-width, 0, 0)
          .tickFormat('')
        )

      var barGroups = chart.selectAll()
        .data(nested_data)
        .enter()
        .append('g')

      barGroups
        .append('rect')
        .attr('class', 'bar')
        .attr('x', (g) => xScale(g.key))
        .attr('y', (g) => yScale(g.value))
        .attr('height', (g) => height - yScale(g.value))
        .attr('width', xScale.bandwidth())
        .on('mouseenter', function (actual, i) {
          d3.selectAll('.value')
            .attr('opacity', 0)

          d3.select(this)
            .transition()
            .duration(300)
            .attr('opacity', 0.7)
            .attr('x', (a) => xScale(a.key))
            .attr('width', xScale.bandwidth())

          var y = yScale(actual.value)

          // chart.append('line')
          //     .attr('id', 'limit')
          //     .attr('x1', 0)
          //     .attr('y1', y)
          //     .attr('x2', width)
          //     .attr('y2', y)

          barGroups.append('text')
            .attr('class', 'divergence')
            .attr('x', (a) => xScale(a.key) + xScale.bandwidth() / 2)
            .attr('y', (a) => yScale(a.value) -2)
            .attr('fill', 'white')
            .attr("font-size", "12px")
            .attr('text-anchor', 'middle')

            .html(function (d) {
              return (`${Math.round(d.value / 5716 * 100)} % job listings`)
              // return (`${d.value}  jobs`)


            });

        })
        .on('mouseleave', function () {
          d3.selectAll('.value')
            .attr('opacity', 1)

          d3.select(this)
            .transition(1)
            .duration(300)
            .attr('opacity', 1)
            .attr('x', (a) => xScale(a.key))
            .attr('width', xScale.bandwidth())

          chart.selectAll('#limit').remove()
          chart.selectAll('.divergence').remove()
        })

      barGroups
        .append('text')
        .attr('class', 'value')
        .attr('x', (a) => xScale(a.key) + xScale.bandwidth() / 2)
        .attr('y', (a) => yScale(a.value) + 20)
        .attr('text-anchor', 'middle')
        .text((a) => `${a.value}%`)

      svg
        .append('text')
        .attr('class', 'label')
        .attr('x', -(height / 2) - margin)
        .attr('y', margin / 2.4)
        .attr('transform', 'rotate(-90)')
        .attr('text-anchor', 'middle')
        .text('Number of Job Listings')

      // svg.append('text')
      //   .attr('class', 'label')
      //   .attr('x', width / 2 + margin)
      //   .attr('y', height + margin * 1.7)
      //   .attr('text-anchor', 'middle')
      //   .text('Salary Brackets')

      svg.append('text')
        .attr('class', 'title')
        .attr('x', width / 2 + margin)
        .attr('y', 40)
        .attr('text-anchor', 'middle')
        .text(`Salary by Job Type `)
      
      
      // chart.exit()
      //   .transition()
      //   .delay()
      //   .remove();

    })

    // .catch(function (error) {
    //   console.log(error);
    // });
}


// ``````````````````````````PIE``````````````````````````
var data = [{
  values: [13, 11.3, 8.3, 5.6, 3.9, 57.9],
  labels: ['Consulting and Business Services', 'Internet and Softrware', 'Banks and Financial Services', 'Health Care',
    'Insurance', 'Other Industries'],
  type: 'pie',
  textinfo: "label+percent",
  textposition: "outside",
  automargin: true,
  marker: { colors: ['rgb(242, 227, 146)','rgb(8, 103, 136)','rgb(219, 191, 27)','rgb(7, 160, 195)',  'rgb(237, 198, 91)','rgb(6, 88, 134)'],
            width: [3,3,3,3,3,3] }
}];
var layout = {
  height: 400,
  width: 700,
  margin: { "t": 0, "b": 0, "l": 0, "r": 0 },
  showlegend: false,
  paper_bgcolor: "#00000000",
  plot_bgcolor: "#00000000",
  font: { color: "#FFFFFF" }
};
Plotly.newPlot('myDiv', data, layout);


// `````````````````````````Colin`````````````````````````
var dropdownMenu = d3.select("#Dropdown11");

var sub;

function getData() {
  var job = dropdownMenu.property("value");

  var filteredData = sub.filter(item => item.Job_Type === job);

  var data = {
    y: filteredData.map(item => parseInt(item.Count)),
    x: filteredData.map(item => item.Skill),
    type: "bar",
    marker:{color: 'rgb(219, 191, 27)'}
  }
  console.log(data)

  var layout = {
    title: "'Bar' Chart",
    height: 400,
    width: 700,
    paper_bgcolor: "#00000000",
    plot_bgcolor: "#00000000",
    font: { color: "#FFFFFF" }
  };

  Plotly.newPlot("plot", [data], layout);
}

dropdownMenu.on("change", getData)


d3.json("./Job_Type").then(function (importedData) {
  sub = importedData
  getData()
  console.log(importedData)




})
//   .catch(function (error) {
//   console.log(error);
// });