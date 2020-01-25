var data = [{'Genre': 'Arts & Photography', 'Accuracy': 13.5},
{'Genre': 'Biographies & Memoirs', 'Accuracy': 23},
{'Genre': 'Business & Money', 'Accuracy': 19.5},
{'Genre': 'Calendars', 'Accuracy': 43},
{'Genre': "Children's Books", 'Accuracy': 48},
{'Genre': 'Comics & Graphic Novels', 'Accuracy': 56.5},
{'Genre': 'Computers & Technology', 'Accuracy': 34},
{'Genre': 'Cookbooks, Food & Wine', 'Accuracy': 49},
{'Genre': 'Crafts, Hobbies & Home', 'Accuracy': 19},
{'Genre': 'Christian Books & Bibles', 'Accuracy': 10},
{'Genre': 'Engineering & Transportation', 'Accuracy': 28},
{'Genre': 'Health, Fitness & Dieting', 'Accuracy': 5},
{'Genre': 'History', 'Accuracy': 23.5},
{'Genre': 'Humor & Entertainment', 'Accuracy': 8},
{'Genre': 'Law', 'Accuracy': 29.5},
{'Genre': 'Literature & Fiction', 'Accuracy': 8.5},
{'Genre': 'Medical Books', 'Accuracy': 20},
{'Genre': 'Mystery, Thriller & Suspense', 'Accuracy': 42},
{'Genre': 'Parenting & Relationships', 'Accuracy': 21.5},
{'Genre': 'Politics & Social Sciences', 'Accuracy': 2.5},
{'Genre': 'Reference', 'Accuracy': 9},
{'Genre': 'Religion & Spirituality', 'Accuracy': 14.5},
{'Genre': 'Romance', 'Accuracy': 55},
{'Genre': 'Science & Math', 'Accuracy': 11},
{'Genre': 'Science Fiction & Fantasy', 'Accuracy': 42},
{'Genre': 'Self-Help', 'Accuracy': 27},
{'Genre': 'Sports & Outdoors', 'Accuracy': 18},
{'Genre': 'Teen & Young Adult', 'Accuracy': 4.5},
{'Genre': 'Test Preparation', 'Accuracy': 68},
{'Genre': 'Travel', 'Accuracy': 37}];
var margin = {top: 20, right: 20, bottom: 30, left: 150},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// set the ranges
var y = d3.scaleBand()
          .range([height, 0])
          .padding(0.1);

var x = d3.scaleLinear()
          .range([0, width]);       
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("#svg-area").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");
  // format the data
  data.forEach(function(d) {
    d.Accuracy = +d.Accuracy;
  });
  // Scale the range of the data in the domains
  x.domain([0, d3.max(data, function(d){ return d.Accuracy; })])
  y.domain(data.map(function(d) { return d.Genre; }));
  //y.domain([0, d3.max(data, function(d) { return d.Accuracy; })]);
  // append the rectangles for the bar chart
  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      //.attr("x", function(d) { return x(d.Accuracy); })
      .attr("width", function(d) {return x(d.Accuracy); } )
      .attr("y", function(d) { return y(d.Genre); })
      .attr("height", y.bandwidth());
  // add the x Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));
  // add the y Axis
  svg.append("g")
      .call(d3.axisLeft(y));