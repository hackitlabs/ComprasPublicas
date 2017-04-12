function create_lines(container, w){

  // Set the dimensions of the canvas / graph
  var margin = {top: 30, right: 20, bottom: 30, left: 50},
  width = w - margin.left - margin.right,
  height = 270 - margin.top - margin.bottom;

  // Parse the date / time
  var parseDate = d3.time.format("%d-%b-%y").parse;

  // Set the ranges
  var x = d3.time.scale().range([0, width]);
  var y = d3.scale.linear().range([height, 0]);

  // Define the axes
  var xAxis = d3.svg.axis().scale(x)
  .orient("bottom").ticks(5);

  var yAxis = d3.svg.axis().scale(y)
  .orient("left").ticks(5);

  // Define the line
  var valueline = d3.svg.line()
  .x(function(d) { console.log(d.date); return x(d.date); })
  .y(function(d) { return y(d.count); });

  // Adds the svg canvas
  var svg = d3.select(container)
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", 
    "translate(" + margin.left + "," + margin.top + ")");

  // Get the data
  d3.json("http://127.0.0.1:5000/api/get/graphs/contrats_year/10/2010", function(error, data) {

    console.log(data);

    data.forEach(function(d) {
      d.date = parseDate(d.date);
      d.count = +d.count;
    });

    //console.log(data);

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.count; })]);

    console.log(valueline(data));

    // Add the valueline path.
    svg.append("path")
    .attr("class", "line")
    .attr("d", valueline(data));

    // Add the X Axis
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

    // Add the Y Axis
    svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);

  });

}