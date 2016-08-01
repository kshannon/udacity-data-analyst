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
        chart.assignColor("handedness", []], stroke, .25)

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
          d3.csv("baseball_data_v2.csv", function (data) {
            //data = dimple.filterData(data, "Date", "01/12/2012");
            var chart2 = new dimple.chart(svg2, data);
            //chart2.setBounds(60, 30, 500, 330)
            var x2 = chart2.addMeasureAxis("x", "HR");
            x2.title = "Number of Home Runs";
            x2.fontSize = "12px";
            
            var y2 =chart2.addMeasureAxis("y", "avg");
            y2.title = "Batting Average";
            y2.fontSize = "12px";

            //chart2.addMeasureAxis("z", "Operating Profit");
            chart2.addSeries(["name", "handedness"], dimple.plot.bubble);
            //chart2.addLegend(850, 120, 40, 400, "right")
            chart2.addLegend(850, 480, 40, 400, "right");
            
            /*svg2.append("text")
            .attr("x", chart._xPixels() + chart._widthPixels() / 2)
            .attr("y", chart._yPixels() - 5)
            .style("text-anchor", "middle")
            .style("font-weight", "bold")
            .style("font-size", "20px")
            .text("Batting Average vs Home Runs by Handedness "); */

    chart2.draw();
    });


    /*
    // Bubble Chart for Baseball Data Set
    var width = 1000,
        height = 600;
    var svg1 = dimple.newSvg("#chart1", width, height);
    d3.csv("baseball_data.csv", function(data){
        var chart = new dimple.chart(svg1, data);
        chart.addPctAxis("x", "avg"); 
        chart.addMeasureAxis("y", "HR");
        chart.addMeasureAxis("z", "height");
        chart.addSeries("name", dimple.plot.bubble);
        chart.addColorAxis("handedness", "#FF0000")
        svg1.append("text")
         .attr("x", chart._xPixels() + chart._widthPixels() / 2)
         .attr("y", chart._yPixels() - 20)
         .style("text-anchor", "middle")
         .style("font-weight", "bold")
         .text("Batting Lefty: Advantage?");
    chart.addLegend(65, 10, 510, 20, "right");
    chart.draw();
    });
*/