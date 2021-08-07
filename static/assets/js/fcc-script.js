let data_file = 'https://raw.githubusercontent.com/no-stack-dub-sack/testable-projects-fcc/master/src/data/choropleth_map/for_user_education.json';
let map_file = 'https://raw.githubusercontent.com/no-stack-dub-sack/testable-projects-fcc/master/src/data/choropleth_map/counties.json';

let margin = {
  top: 100,
  right: 50,
  bottom: 50,
  left: 75 },
width = 1100 - margin.left - margin.right,
height = 800 - margin.top - margin.bottom;

let svg = d3.select('#dataContainer').
append('svg').
attr('width', width + margin.left + margin.right).
attr('height', height + margin.top + margin.bottom).
append('g').
attr('transform',
'translate (' + margin.left + ',' + margin.top + ')');

let Tooltip = d3.select('.main').
append("div").
style('width', '175px').
style("opacity", 0).
attr("class", "tooltip").
attr("id", "tooltip").
style("background-color", "gray").
style("color", "white").
style("border", "solid").
style("border-width", "2px").
style("border-radius", "5px").
style("padding", "5px");

//Map and projection
let path = d3.geoPath();

//access data with promise
let promises = [
d3.json(data_file),
d3.json(map_file)];


Promise.all(promises).then(function (values) {

  let eduData = values[0];
  let map = values[1];
  //console.log(eduData[0])
  //console.log(map.objects.counties.geometries)
  let min = d3.min(eduData, d => d.bachelorsOrHigher);
  let max = d3.max(eduData, d => d.bachelorsOrHigher);
  //console.log(max)

  // Color scale
  let color = d3.scaleThreshold().
  domain(d3.range(min, max, 10)).
  range(d3.schemePurples[9]);
  //console.log(color(eduData[101].bachelorsOrHigher))
  //console.log(d3.range(0,100,10))

  svg.
  selectAll("path").
  data(topojson.feature(map, map.objects.counties).features).
  enter().
  append("path").
  attr("d", path).
  attr('class', 'counties').
  attr("fill", function (d) {
    var counties = eduData.filter(function (c) {
      return c.fips == d.id;
    });
    //console.log(education[0])
    if (counties[0]) {
      return color(counties[0].bachelorsOrHigher);
    }
    return color(0);
  }).
  attr("data-education", function (d) {
    var counties = eduData.filter(function (c) {
      return c.fips == d.id;
    });
    if (counties[0]) {
      return counties[0].bachelorsOrHigher;
    }
    return 0;
  }).
  attr("data-fips", function (d) {
    var counties = eduData.filter(function (c) {
      return c.fips == d.id;
    });
    if (counties[0]) {
      return counties[0].fips;
    }
    return 0;
  }).
  on("mouseover", handleMouseOver).
  on("mousemove", handleMouseMove).
  on("mouseleave", handleMouseLeave);

  function handleMouseOver(d, i) {

    Tooltip.style("opacity", .8).
    transition().
    duration(200);

    d3.select(this).
    style("stroke", "black").
    style("stroke-opacity", 1).
    style('fill', 'green');

  }

  function handleMouseMove(d, i) {

    let county = eduData.filter(function (c) {
      return c.fips === d.id;
    });

    let text = county[0].area_name + ', ' +
    county[0].state + '<br/>' +
    county[0].bachelorsOrHigher + '%';


    let xCoord = event.pageX - 100 + 'px';
    let yCoord = event.pageY - 1275 + 'px';

    Tooltip.
    html(text).
    style('transform', 'translate(' + xCoord + ', ' + yCoord + ')');
  }

  function handleMouseLeave(d) {
    Tooltip.style("opacity", 0);
    d3.select(this).
    style("stroke", "black").
    style("stroke-opacity", 0).
    style("fill", function (d) {
      var counties = eduData.filter(function (c) {
        return c.fips == d.id;
      });
      //console.log(education[0])
      if (counties[0]) {
        return color(counties[0].bachelorsOrHigher);
      }
      return color(0);
    });
  }

  //state borders
  svg.append("path").
  attr("stroke", "#fff").
  attr("stroke-width", 2).
  attr("d", path(topojson.mesh(map, map.objects.states, function (a, b) {return a !== b;}))).
  style('fill', 'none');

  //legend
  let legend = svg.append("g").
  attr("id", "legend");

  let rectSize = 40;

  //legend text
  let keys = color.domain();
  svg.selectAll("rect").
  data(keys).
  enter().
  append("text").
  attr("x", function (d, i) {return rectSize + i * rectSize;}).
  attr("y", -45).
  text(function (d) {return d;}).
  style('font-size', '14px').
  style('fill', 'gray');

  //legend bars
  var x = d3.scaleLinear().
  domain([1, 10]).
  rangeRound([600, 860]);

  svg.selectAll("rect").
  data(color.range().map(function (d) {
    d = color.invertExtent(d);
    if (d[0] == null) d[0] = x.domain()[0];
    if (d[1] == null) d[1] = x.domain()[1];
    return d;
  })).
  enter().
  append("rect").
  attr("x", function (d, i) {return 10 + i * rectSize;}).
  attr("y", -80).
  attr("width", rectSize).
  attr("height", 20).
  attr("fill", function (d) {return color(d[0]);}).
  style('stroke', 'gray');

  //min and max
  let maxCounty = eduData.filter(function (c) {
    return c.bachelorsOrHigher === max;
  });

  let maxText = 'Highest: ' + maxCounty[0].area_name + ', ' +
  maxCounty[0].state + ', ' +
  maxCounty[0].bachelorsOrHigher + '%';

  let minCounty = eduData.filter(function (c) {
    return c.bachelorsOrHigher === min;
  });

  let minText = 'Lowest: ' + minCounty[0].area_name + ', ' +
  minCounty[0].state + ', ' +
  minCounty[0].bachelorsOrHigher + '%';

  svg.append("text").
  attr("class", "caption").
  attr("x", 650).
  attr("y", -70).
  attr("fill", "gray").
  attr("font-weight", "bold").
  attr('position', 'absolute').
  attr('z-index', -1).
  text(maxText);

  svg.append("text").
  attr("class", "caption").
  attr("x", 650).
  attr("y", -50).
  attr("fill", "gray").
  attr("font-weight", "bold").
  attr('position', 'absolute').
  attr('z-index', -1).
  text(minText);

});
