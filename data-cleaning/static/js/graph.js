// graph.js

// Define radius and layout constants
const radiusCenter = 100;
const radiusEvent = 200;
const radiusPower = 450;
const width = 960, height = 600;

// SVG setup
const svg = d3.select("svg"),
      g = svg.append("g").attr("transform", `translate(${width / 2}, ${height / 2})`);

// Define zoom behavior
const zoom = d3.zoom()
    .scaleExtent([0.5, 3])
    .on("zoom", (event) => {
        g.attr("transform", event.transform);
        g.selectAll("circle").attr("r", 7 / event.transform.k);
        g.selectAll("text").attr("font-size", `${10 / event.transform.k}px`);
    });
svg.call(zoom);

// Arrow definitions for edges
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

// Parse nodes and links
const nodes = [{ name: "US Coast Guard", type: "coastguard" }];
const links = [];

// Track selection state
let selectedNode = null;

// Build nodes and links from graphData
let eventIndex = 0, powerIndex = 0;
for (const [event, powers] of Object.entries(graphData)) {
    nodes.push({ name: event, type: "event", fx: radiusEvent * Math.cos(eventIndex), fy: radiusEvent * Math.sin(eventIndex) });
    links.push({ source: "US Coast Guard", target: event, color: "red" });
    eventIndex += (2 * Math.PI) / Object.keys(graphData).length;

    for (const [power, citations] of Object.entries(powers)) {
        if (!nodes.some(node => node.name === power)) {
            const fxPos = radiusPower * Math.cos(powerIndex);
            const fyPos = radiusPower * Math.sin(powerIndex);

            nodes.push({
                name: power,
                citations,
                type: "power",
                fx: fxPos,
                fy: fyPos,
            });
            powerIndex += (2 * Math.PI) / Object.values(powers).length;
        }
        links.push({ source: event, target: power, color: "green" });
    }
}

// D3 force simulation
const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink().id(d => d.name).distance(d => d.color === "red" ? radiusEvent - radiusCenter : radiusPower - radiusEvent))
    .force("charge", d3.forceManyBody().strength(-100))
    .force("center", d3.forceCenter(0, 0))
    .force("collide", d3.forceCollide(25))
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

// Render links
const link = g.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(links)
    .enter().append("line")
    .attr("class", "link")
    .attr("marker-end", d => d.color === "red" ? "url(#arrow-red)" : "url(#arrow-green)")
    .attr("stroke", d => d.color)
    .attr("stroke-opacity", d => d.color === "red" ? 0.4 : 0.6);

// Render nodes
const node = g.append("g")
    .attr("class", "nodes")
    .selectAll("g")
    .data(nodes)
    .enter().append("g")
    .attr("class", "node");

// Node circles
node.append("circle")
    .attr("r", 7)
    .attr("fill", d => d.type === "coastguard" ? "orange" : d.type === "event" ? "red" : "green")
    .on("click", (event, d) => {
        event.stopPropagation(); // Prevents click from bubbling up to the SVG
        if (selectedNode === d) {
            // Deselect node if clicked again
            selectedNode = null;
            node.selectAll("circle").style("opacity", 1);
            link.style("opacity", 1);
        } else {
            // Select new node
            selectedNode = d;

            // Highlight only adjacent nodes and edges
            node.selectAll("circle").style("opacity", node => {
                return node === d || links.some(link => (link.source === d && link.target === node) || (link.target === d && link.source === node)) ? 1 : 0.1;
            });

            link.style("opacity", link => {
                return link.source === d || link.target === d ? 1 : 0.1;
            });
        }
    });

// Node labels
node.append("text")
    .text(d => d.name)
    .attr("y", 15)
    .attr("font-size", "10px")
    .attr("text-anchor", "middle");

// Tooltip functionality
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

// Reset the graph when clicking on the SVG background
svg.on("click", () => {
    selectedNode = null;
    node.selectAll("circle").style("opacity", 1);
    link.style("opacity", 1);
});
