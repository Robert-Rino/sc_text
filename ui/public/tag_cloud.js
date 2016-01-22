var fill = d3.scale.category20();

window.onload = function () {
  tags = ["subnetting", "IP", "class", "遮罩", "更細", "分配", "address", "subnet", "十六次" , "number" , "16"]
  addTagCloud(tags);
};

var addTagCloud = function(tags) {
  d3.layout.cloud().size([300, 300])
      .words(tags.map(function(d) {
        return {text: d, size: 18 + Math.random() * 12};
      }))
      .rotate(function() { return ~~(Math.random() * 2) * 90; })
      .font("Impact")
      .fontSize(function(d) { return d.size; })
      .on("end", draw)
      .start();
};

function draw(words) {
  d3.select("#tag_vis").append("svg")
      .attr("width", 300)
      .attr("height", 300)
    .append("g")
      .attr("transform", "translate(150,150)")
    .selectAll("text")
      .data(words)
    .enter().append("text")
      .style("font-size", function(d) { return d.size + "px"; })
      .style("font-family", "Impact")
      .style("fill", function(d, i) { return fill(i); })
      .attr("text-anchor", "middle")
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function(d) { return d.text; });
}
