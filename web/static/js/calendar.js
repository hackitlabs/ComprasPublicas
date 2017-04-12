  var width, height = 136, cellSize = 15.5; 

function create_calendar(container, _entitid, _year, _start){

  var percent = d3.format(".1%"),
      format = d3.time.format("%Y-%m-%d");
  d3.select(container + " svg").remove();
  var svg = d3.select(container).selectAll("svg")
      .data(d3.range(_year, _end))
    .enter().append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("class", "RdYlGn")
    .append("g")
      .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");

  var rect = svg.selectAll(".day")
      .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
    .enter().append("rect")
      .attr("class", "day")
      .attr("width", cellSize)
      .attr("height", cellSize)
      .attr("x", function(d) { return d3.time.weekOfYear(d) * cellSize; })
      .attr("y", function(d) { return d.getDay() * cellSize; })
      .datum(format);

  rect.append("title")
      .text(function(d) { return d; });

  svg.selectAll(".month")
      .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
    .enter().append("path")
      .attr("class", "month")
      .attr("d", monthPath);
  d3.json("/api/get/graphs/contrats_year/"+_entitid+"/"+_year, function(error, _data) {
    if (error) throw error;

    var _max = d3.max(_data, function(d) { return d.count; });
    var color = d3.scale.linear()
    .domain([0, _max])
    .range(["#f7f5f5", "#ee6e73"]);

    var data = d3.nest()
      .key(function(d) { return d.Date; })
      .rollup(function(d) { return d[0].count; })
      .map(_data);

    rect.filter(function(d) { return d in data; })
        .style("fill", function(d) { return color(data[d]); })
      .select("title")
        .text(function(d) { return data[d]; });
  });

}

function monthPath(t0) {
  var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
      d0 = t0.getDay(), w0 = d3.time.weekOfYear(t0),
      d1 = t1.getDay(), w1 = d3.time.weekOfYear(t1);
  return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
      + "H" + w0 * cellSize + "V" + 7 * cellSize
      + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
      + "H" + (w1 + 1) * cellSize + "V" + 0
      + "H" + (w0 + 1) * cellSize + "Z";
}