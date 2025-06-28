import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const AgentNetwork = ({ networkData, isConnected }) => {
  const svgRef = useRef();
  const width = 500;
  const height = 400;

  useEffect(() => {
    if (!networkData || !networkData.nodes || !networkData.links) {
      return;
    }

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove(); // Clear previous content

    // Set up the SVG
    svg.attr("width", width).attr("height", height);

    // Create simulation
    const simulation = d3.forceSimulation(networkData.nodes)
      .force("link", d3.forceLink(networkData.links).id(d => d.id).distance(80))
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(20));

    // Color scale for different agent types
    const colorScale = d3.scaleOrdinal()
      .domain(["ward", "staff", "equipment", "patient"])
      .range(["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4"]);

    // Add links
    const link = svg.append("g")
      .selectAll("line")
      .data(networkData.links)
      .enter().append("line")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .attr("stroke-width", d => Math.sqrt(d.strength * 5));

    // Add nodes
    const node = svg.append("g")
      .selectAll("circle")
      .data(networkData.nodes)
      .enter().append("circle")
      .attr("r", d => 8 + (d.resources || 0))
      .attr("fill", d => colorScale(d.type))
      .attr("stroke", "#fff")
      .attr("stroke-width", 2)
      .style("cursor", "pointer")
      .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

    // Add labels
    const text = svg.append("g")
      .selectAll("text")
      .data(networkData.nodes)
      .enter().append("text")
      .text(d => d.id.split('_')[0])
      .attr("font-size", 10)
      .attr("font-family", "Arial, sans-serif")
      .attr("fill", "#333")
      .attr("text-anchor", "middle")
      .attr("dy", 3);

    // Add tooltips
    node.append("title")
      .text(d => `${d.id}\nType: ${d.type}\nResources: ${d.resources || 0}\nEnergy: ${d.energy || 0}`);

    // Update positions on simulation tick
    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

      text
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });

    // Drag functions
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Cleanup on unmount
    return () => {
      simulation.stop();
    };
  }, [networkData]);

  return (
    <div className="agent-network">
      {isConnected ? (
        <div>
          <svg ref={svgRef}></svg>
          <div className="network-legend">
            <div className="legend-item">
              <div className="legend-color" style={{backgroundColor: '#ff6b6b'}}></div>
              <span>Ward</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{backgroundColor: '#4ecdc4'}}></div>
              <span>Staff</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{backgroundColor: '#45b7d1'}}></div>
              <span>Equipment</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{backgroundColor: '#96ceb4'}}></div>
              <span>Patient</span>
            </div>
          </div>
        </div>
      ) : (
        <div className="placeholder">
          <p>Waiting for network data...</p>
        </div>
      )}
      
      <style jsx>{`
        .agent-network {
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        
        .network-legend {
          display: flex;
          justify-content: center;
          gap: 20px;
          margin-top: 15px;
          font-size: 12px;
        }
        
        .legend-item {
          display: flex;
          align-items: center;
          gap: 5px;
        }
        
        .legend-color {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          border: 1px solid #ccc;
        }
        
        .placeholder {
          display: flex;
          align-items: center;
          justify-content: center;
          height: 400px;
          color: #666;
          font-style: italic;
        }
      `}</style>
    </div>
  );
};

export default AgentNetwork;
