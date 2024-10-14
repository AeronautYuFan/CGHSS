const width = 960, height = 600;

const svg = d3.select("svg"),
      g = svg.append("g").attr("transform", "translate(0,0)");

const zoom = d3.zoom()
    .scaleExtent([0.5, 3])
    .on("zoom", (event) => {
        g.attr("transform", event.transform);
        g.selectAll("circle").attr("r", 12 / event.transform.k);
        g.selectAll("text").attr("font-size", `${10 / event.transform.k}px`);
    });

svg.call(zoom);

svg.append("defs").selectAll("marker")
    .data(["red", "green"])
  .enter().append("marker")
    .attr("id", d => d === "red" ? "arrow-red" : "arrow-green")
    .attr("viewBox", "0 0 10 10")
    .attr("refX", 10)
    .attr("refY", 5)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M0,0 L10,5 L0,10 L3,5 Z")
    .attr("fill", d => d);

const nodes = [{ name: "US Coast Guard", type: "coastguard" }];
const links = [];

for (const [event, powers] of Object.entries(graphData)) {
    nodes.push({ name: event, type: "event" });
    links.push({ source: "US Coast Guard", target: event, color: "red" });

    for (const [power, citations] of Object.entries(powers)) {
        nodes.push({ name: power, citations, type: "power" });
        links.push({ source: event, target: power, color: "green" });
    }
}

const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink().id(d => d.name).distance(100))
    .force("charge", d3.forceManyBody().strength(-200))
    .force("center", d3.forceCenter(width / 2, height / 2));

const link = g.append("g")
    .attr("class", "links")
  .selectAll("line")
  .data(links)
  .enter().append("line")
    .attr("class", "link")
    .attr("marker-end", d => d.color === "red" ? "url(#arrow-red)" : "url(#arrow-green)")
    .attr("stroke", d => d.color)
    .attr("stroke-opacity", d => d.color === "red" ? 0.4 : 0.6);

const node = g.append("g")
    .attr("class", "nodes")
  .selectAll("g")
  .data(nodes)
  .enter().append("g")
    .attr("class", "node");

    node.append("circle") // this changes the node size
    .attr("r", 7) 
    .attr("fill", d => {
        if (d.type === "coastguard") return "orange";
        if (d.type === "event") return "red";
        if (d.type === "power") return "green";
        return "gray";
    });


node.append("text")
    .text(d => d.name)
    .attr("y", 15)
    .attr("font-size", "10px")
    .attr("text-anchor", "middle");

const tooltip = d3.select(".tooltip");

node.on("mouseover", (event, d) => {
    if (d.type === "power" && d.citations) {
        const citationsList = d.citations.join('<br>');
        tooltip.style("visibility", "visible")
               .html(`Citations:<br>${citationsList}`);
    }
}).on("mousemove", (event) => {
    tooltip.style("top", (event.pageY - 10) + "px")
           .style("left", (event.pageX + 10) + "px");
}).on("mouseout", () => {
    tooltip.style("visibility", "hidden");
});

let activeNode = null;

node.on("click", (event, d) => {
    event.stopPropagation();

    if (activeNode === d) {
        resetGraph();
        activeNode = null;
    } else {
        activeNode = d;

        g.selectAll(".link")
            .attr("stroke-opacity", l => {
                return (l.source.name === d.name || l.target.name === d.name) ? 0.9 : 0.05;
            });
    }
});

svg.on("click", () => {
    resetGraph();
});

function resetGraph() {
    g.selectAll(".link")
      .attr("stroke-opacity", d => d.color === "red" ? 0.4 : 0.6);
    activeNode = null;
}

simulation
    .nodes(nodes)
    .on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("transform", d => `translate(${d.x}, ${d.y})`);
    });

simulation.force("link").links(links);
