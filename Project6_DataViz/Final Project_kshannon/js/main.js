    var width = 1000,
        height = 600;
    
// Chart1 - box plot count for Baseball Data Set

    var svg1 = dimple.newSvg("#chart1", width, height);
    d3.csv("baseball_data_v2.csv", function(data){
        var chart = new dimple.chart(svg1, data);

        var x = chart.addCategoryAxis("x", "handedness");
        x.title = "Batting Stance";
        x.fontSize = "12px";
        
        var y = chart.addMeasureAxis("y", "count");
        y.title = "MLB Player Count";
        y.fontSize = "12px";
        
        chart.addSeries(["handedness"], dimple.plot.bar); // updates tool tip too!
        chart.addLegend(850, 120, 40, 400, "right")
        chart.assignColor("Right Handed","#fb8072");
        chart.assignColor("Left Handed","#80b1d3");
        chart.assignColor("Switch Hitter","#fdb462");
        //chart.assignColor("handedness", [], stroke, .25) //this break my first chart.. worked before.

        svg1.append("text")
            .attr("x", chart._xPixels() + chart._widthPixels() / 2)
            .attr("y", chart._yPixels() - 5)
            .style("text-anchor", "middle")
            .style("font-weight", "bold")
            .style("font-size", "20px")
            .text("Batting Stances of MLB Players");

    chart.draw();
    }); 

// Chart2 - scatter plot count for Baseball Data Set

    var svg2 = dimple.newSvg("#chart2", width, height);
    d3.csv("baseball_data_v2.csv", function(data){
            var chart2 = new dimple.chart(svg2, data);

            var x2 = chart2.addMeasureAxis("x", "HR");
            x2.title = "Number of Home Runs";
            x2.fontSize = "12px";

            
            var y2 =chart2.addMeasureAxis("y", "avg");
            y2.title = "Batting Average";
            y2.fontSize = "12px";
            y2.ticks = 10;
            y2.tickFormat = ',.3f';

            //chart2.addMeasureAxis("z", "Operating Profit");
            chart2.addSeries(["name", "handedness"], dimple.plot.bubble);
            //chart2.addLegend(850, 120, 40, 400, "right")
            var Legend2 = chart2.addLegend(850, 480, 40, 400, "right");


        svg2.append("text")
            .attr("x", chart2._xPixels() + chart2._widthPixels() / 2)
            .attr("y", chart2._yPixels() - 5)
            .style("text-anchor", "middle")
            .style("font-weight", "bold")
            .style("font-size", "20px")
            .text("Batting Average and Home Run Trend by Handedness");

            
            chart2.draw();

        // Doing this we orphan the legend. This
        // means it will not respond to graph updates.  Without this the legend
        // will redraw when the chart refreshes removing the unchecked item and
        // also dropping the events we define below.
            chart2.legends = [];

        // This block simply adds the legend title. 
            svg2.selectAll("title_text")
              .data(["Click legend to","show/hide stances:"])
              .enter()
              .append("text")
                .attr("x", 800)
                .attr("y",  function (d, i) { return 470 + i * 14; })
                .style("font-family", "sans-serif")
                .style("font-size", "10px")
                .style("color", "Black")
                .text(function (d) { return d; });

            // Get a unique list of Owner values to use when filtering
            var filterValues = dimple.getUniqueValues(data, "handedness");

            // Get all the rectangles from our now orphaned legend
            Legend2.shapes.selectAll("rect")

        
              // Add a click event to each rectangle
              .on("click", function (e) {
                // This indicates whether the item is already visible or not
                var hide = false;
                var newFilters = [];
                // If the filters contain the clicked shape hide it
                filterValues.forEach(function (f) {
                  if (f === e.aggField.slice(-1)[0]) {
                    hide = true;
                  } else {
                    newFilters.push(f);
                  }
                });
                // Hide the shape or show it
                if (hide) {
                  d3.select(this).style("opacity", 0.2);
                } else {
                  newFilters.push(e.aggField.slice(-1)[0]);
                  d3.select(this).style("opacity", 0.8);
                }
                // Update the filters
                filterValues = newFilters;
                // Filter the data
                chart2.data = dimple.filterData(data, "handedness", filterValues);
                // Passing a duration parameter makes the chart animate. Without
                // it there is no transition
                chart2.draw(); 
            });
        });

// colors for basic dimple charts
// Blue #80b1d3
// Red #fb8072
// Yellow #fdb462