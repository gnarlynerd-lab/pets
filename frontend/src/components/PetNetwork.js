import React, { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';
import './PetNetwork.css';

const PetNetwork = ({ networkData, isConnected, onPetSelect, pets, environment }) => {
  const svgRef = useRef(null);
  const [highlightedPet, setHighlightedPet] = useState(null);
  
  // Handle rendering of the pet network using D3
  useEffect(() => {
    if (!svgRef.current || !networkData || !isConnected) return;
    
    const width = 800;
    const height = 600;
    
    // Clear any existing visualization
    d3.select(svgRef.current).selectAll("*").remove();
    
    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height);
      
    // Create background that represents time of day
    const timeOfDay = environment?.time_of_day || 12;
    let backgroundColor;
    if (timeOfDay >= 6 && timeOfDay < 10) {
      // Morning
      backgroundColor = "#FFF4D9";
    } else if (timeOfDay >= 10 && timeOfDay < 17) {
      // Daytime
      backgroundColor = "#E0F2FF";
    } else if (timeOfDay >= 17 && timeOfDay < 21) {
      // Evening
      backgroundColor = "#FFE0B5";
    } else {
      // Night
      backgroundColor = "#1A2436";
    }
    
    svg.append("rect")
      .attr("width", width)
      .attr("height", height)
      .attr("fill", backgroundColor);
      
    // Add sun/moon based on time
    const celestialBodySize = 50;
    const celestialX = width * 0.1 + (width * 0.8 * (timeOfDay % 24) / 24);
    const celestialY = height * 0.2 + Math.sin((timeOfDay % 24) / 24 * Math.PI) * height * 0.3;
    
    // Draw sun or moon
    if (timeOfDay >= 6 && timeOfDay < 18) {
      // Sun
      svg.append("circle")
        .attr("cx", celestialX)
        .attr("cy", celestialY)
        .attr("r", celestialBodySize)
        .attr("fill", "yellow")
        .attr("opacity", 0.8);
    } else {
      // Moon
      svg.append("circle")
        .attr("cx", celestialX)
        .attr("cy", celestialY)
        .attr("r", celestialBodySize)
        .attr("fill", "white")
        .attr("opacity", 0.8);
    }
    
    // Create force simulation
    const simulation = d3.forceSimulation(networkData.nodes)
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("link", d3.forceLink(networkData.links)
        .id(d => d.id)
        .distance(100))
      .force("collision", d3.forceCollide().radius(40));
    
    // Draw links
    const link = svg.append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(networkData.links)
      .join("line")
      .attr("stroke-width", d => Math.sqrt(Math.abs(d.strength) * 2))
      .attr("stroke", d => d.strength > 0 ? "#4CAF50" : "#F44336");
    
    // Create node groups
    const node = svg.append("g")
      .selectAll(".node")
      .data(networkData.nodes)
      .join("g")
      .attr("class", "node")
      .call(drag(simulation))
      .on("click", (event, d) => {
        if (d.type === "pet") {
          onPetSelect(d.id);
          setHighlightedPet(d.id);
        }
      });
    
    // Draw different shapes based on node type
    node.each(function(d) {
      const g = d3.select(this);
      
      if (d.type === "pet") {
        // Draw pet as circle with emotion
        g.append("circle")
          .attr("r", 30)
          .attr("fill", getPetColor(d))
          .attr("stroke", d.id === highlightedPet ? "#FFD700" : "#fff")
          .attr("stroke-width", d.id === highlightedPet ? 3 : 1);
        
        // Add eyes
        const eyeY = -5;
        g.append("circle")
          .attr("cx", -10)
          .attr("cy", eyeY)
          .attr("r", 5)
          .attr("fill", "#000");
        
        g.append("circle")
          .attr("cx", 10)
          .attr("cy", eyeY)
          .attr("r", 5)
          .attr("fill", "#000");
        
        // Add mouth based on mood
        const mood = d.attributes?.mood || 50;
        const mouthWidth = 20;
        const mouthHeight = mood > 70 ? 10 : (mood > 30 ? 0 : -10);
        
        g.append("path")
          .attr("d", `M -${mouthWidth/2},10 Q 0,${10 + mouthHeight} ${mouthWidth/2},10`)
          .attr("stroke", "#000")
          .attr("stroke-width", 2)
          .attr("fill", "none");
        
        // Add label
        g.append("text")
          .attr("dy", 50)
          .attr("text-anchor", "middle")
          .attr("font-size", "12px")
          .text(d.id.split("_")[0]);
      } else if (d.type === "user") {
        // Draw user as diamond
        g.append("polygon")
          .attr("points", "0,-30 20,0 0,30 -20,0")
          .attr("fill", "#9C27B0")
          .attr("stroke", "#fff")
          .attr("stroke-width", 1);
        
        // Add label
        g.append("text")
          .attr("dy", 45)
          .attr("text-anchor", "middle")
          .attr("font-size", "12px")
          .text("User");
      }
      
      // Add health bar
      if (d.type === "pet") {
        const health = d.attributes?.health || 0;
        const barWidth = 40;
        const barHeight = 5;
        
        g.append("rect")
          .attr("x", -barWidth / 2)
          .attr("y", -45)
          .attr("width", barWidth)
          .attr("height", barHeight)
          .attr("fill", "#eee")
          .attr("stroke", "#000")
          .attr("stroke-width", 1);
        
        g.append("rect")
          .attr("x", -barWidth / 2)
          .attr("y", -45)
          .attr("width", barWidth * (health / 100))
          .attr("height", barHeight)
          .attr("fill", getHealthColor(health));
      }
    });
    
    // Update positions on simulation tick
    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
      
      node.attr("transform", d => `translate(${d.x},${d.y})`);
    });
    
    // Drag functionality for nodes
    function drag(simulation) {
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }
      
      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }
      
      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }
      
      return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    }
    
  }, [networkData, isConnected, onPetSelect, highlightedPet, environment]);
  
  // Helper functions for visualization
  const getPetColor = (pet) => {
    if (!pet.attributes) return "#64B5F6";
    
    const stage = pet.attributes.stage;
    switch(stage) {
      case "infant": return "#BBDEFB";
      case "child": return "#64B5F6";
      case "adolescent": return "#2196F3";
      case "adult": return "#1976D2";
      case "elder": return "#0D47A1";
      default: return "#64B5F6";
    }
  };
  
  const getHealthColor = (health) => {
    if (health > 70) return "#4CAF50";
    if (health > 30) return "#FFC107";
    return "#F44336";
  };
  
  return (
    <div className="pet-network-container">
      {!isConnected && <div className="loading-overlay">Waiting for connection...</div>}
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default PetNetwork;
