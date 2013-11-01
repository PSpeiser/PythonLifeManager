/*
 Required JS:
 jquery
 d3js


 Required HTML elements:
 #weight_graph_wrapper: element that the svg will be appended to

 */

$(document).ready(function () {
    var parseDate = d3.time.format("%Y-%m-%d").parse;
    var margin = { 'left': 40, 'bottom': 20, 'top': 15, 'right': 0 },
        width = 640,
        height = 240,
        w = width - margin.left - margin.right,
        h = height - margin.top - margin.bottom,
        clip = null;

    var maxWidth = margin.width;
    var dataPointWidth = 5;
    var xAxis = null;
    var yAxis = null;
    var line = null;

    function rescale(tx, ty) {
        //rescale path
        weight_svg.select('.data').attr('d', line);
        //rescale axes
        weight_svg.select("g.x.axis").call(xAxis);
        weight_svg.select("g.y.axis").call(yAxis);
        //rescale dots
        weight_svg.selectAll(".dot").attr("transform", "translate(" + tx + "," + ty + ")");
    }
    if(typeof weight_graph_max_weeks == 'undefined')
    {
        weight_graph_max_weeks = 0;
    }
    d3.json("weights.json?max_weeks=" + weight_graph_max_weeks, function (error, data) {
        data.forEach(function (d) {
            d.date = parseDate(d.date);
            d.kcal = +d.kg;
            d.text = d.text;
        });

        weight_svg = d3.select("#weight_graph_wrapper")
            .append("svg")
            .attr("id", "weight_graph")
            .attr("width", width)
            .attr("height", height)
            .attr('cursor', 'move')
            .append("svg:g");

        var dateExtent = d3.extent(data, function (d) {
            return d.date
        });
        var timeDiff = Math.abs(dateExtent[0].getTime() - dateExtent[1].getTime());
        var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
        maxWidth = Math.max(diffDays * dataPointWidth,w);

        var xscale = d3.time.scale().domain(dateExtent).range([20, maxWidth]);
        var kcalExtent = d3.extent(data, function (d) {
            return d.kcal;
        })
        var yscale = d3.scale.linear()
            .range([h, 0])
            .domain([kcalExtent[0]*0.9, kcalExtent[1] * 1.1]);

        line = d3.svg.line()
            .x(function (d) {
                return xscale(d.date);
            })
            .y(function (d) {
                return yscale(d.kcal);
            });

        //add a background rectangle to enable panning and background coloring
        weight_svg.append("rect")
            .attr("id", "background_rect")
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", width)
            .attr("height", height)

        //add path clipping element
        weight_svg.append("g").append("clipPath")
            .attr("id", "clip")
            .append("rect")
            .attr("width", maxWidth)
            .attr("height", h)
            .attr("transform", "translate(" + margin.left + "," + 0 + ")")

        //draw path
        weight_svg.append('g')
            .attr("clip-path", "url(#clip)")
            .datum(data)
            .append('path')
            .attr('class', 'data')
            .attr('d', line);


        xAxis = d3.svg.axis()
            .scale(xscale)
            .orient("bottom")
            .ticks(d3.time.weeks, 1);

        weight_svg.append("g")
            .attr("clip-path", "url(#clip)")
            .attr("class", "x axis")
            .attr("transform", "translate(" + 0 + "," + h + ")")
            .call(xAxis);

        yAxis = d3.svg.axis()
            .scale(yscale)
            .orient("left")
            .tickFormat(d3.format("f"))

        //draw y axis
        weight_svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .attr("transform", "translate(" + margin.left + "," + 0 + ")")
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.5em")
            .append("text")
            .text("KCal");

        //draw dots for data points
        weight_svg.append("g").attr("clip-path", "url(#clip)")
            .selectAll(".dot")
            .data(data)
            .enter().append("circle")
            .attr("class", "dot")
            .attr("r", 2.5)
            .attr("cx", function (d) {
                return xscale(d.date);
            })
            .attr("cy", function (d) {
                return yscale(d.kcal);
            })
            .style("fill", function (d) {
                return 'black';
            })
            .append("svg:title")
            .text(function (d) {
                return d.text;
            });

        var zoom = d3.behavior.zoom()
            .scaleExtent([1, 1])
            .x(xscale)
            .y(yscale)
            .on('zoom', function () {
                var t = zoom.translate(),
                    tx = t[0],
                    ty = t[1];

                tx = Math.min(tx, dataPointWidth * 10);
                tx = Math.max(tx, width - maxWidth - dataPointWidth * 10);
                //lock y in place
                ty = 0;
                zoom.translate([tx, ty]);
                rescale(tx, ty);

            });
        //pan all the way to the right initially
        var tx = width - maxWidth - dataPointWidth * 10;
        var ty = 0;
        zoom.translate([tx, ty]);
        rescale(tx, ty);
        weight_svg.call(zoom);

        //bind a reload handler
        $("#weight_graph").bind("reload", function () {
            //this will keep the layout of the page intact during the reload
            $("#weight_graph").replaceWith("<div id='weight_graph_placeholder' style='float:left;width:" + $("#weight_graph").width()
                + "px;height:" + $("#weight_graph").height() + "px'>&nbsp;</div>");
            $.getScript('weight_graph.js');
        });

        //remove the placeholder if this script was reloaded
        $("#weight_graph_placeholder").remove();
    })
});