import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const DEFAULT_COLORS = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
  '#06b6d4', '#ec4899', '#14b8a6', '#f97316', '#6366f1'
];

function PieChart({ data, valueKey, labelKey, height = 300, colors = DEFAULT_COLORS }) {
  const svgRef = useRef();
  const containerRef = useRef();

  useEffect(() => {
    if (!data || data.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const container = containerRef.current;
    const width = container.clientWidth;
    const radius = Math.min(width, height) / 2 - 40;

    const g = svg
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`);

    // Color scale
    const color = d3.scaleOrdinal()
      .domain(data.map(d => d[labelKey]))
      .range(colors);

    // Pie generator
    const pie = d3.pie()
      .value(d => d[valueKey])
      .sort(null);

    // Arc generator
    const arc = d3.arc()
      .innerRadius(radius * 0.5)
      .outerRadius(radius);

    const hoverArc = d3.arc()
      .innerRadius(radius * 0.5)
      .outerRadius(radius * 1.05);

    // Tooltip
    const tooltip = d3.select('body')
      .append('div')
      .attr('class', 'chart-tooltip')
      .style('position', 'absolute')
      .style('background', 'rgba(0,0,0,0.8)')
      .style('color', 'white')
      .style('padding', '8px 12px')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('opacity', 0)
      .style('z-index', 1000);

    // Calculate total for percentages
    const total = d3.sum(data, d => d[valueKey]);

    // Draw arcs
    const arcs = g.selectAll('.arc')
      .data(pie(data))
      .enter()
      .append('g')
      .attr('class', 'arc');

    arcs.append('path')
      .attr('d', arc)
      .attr('fill', d => color(d.data[labelKey]))
      .attr('stroke', 'white')
      .attr('stroke-width', 2)
      .style('opacity', 0)
      .transition()
      .duration(800)
      .style('opacity', 1)
      .attrTween('d', function(d) {
        const i = d3.interpolate({ startAngle: 0, endAngle: 0 }, d);
        return function(t) {
          return arc(i(t));
        };
      });

    // Hover effects
    arcs.selectAll('path')
      .on('mouseover', function(event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('d', hoverArc);
        
        const percent = ((d.data[valueKey] / total) * 100).toFixed(1);
        tooltip
          .style('opacity', 1)
          .html(`<strong>${d.data[labelKey]}</strong><br/>${d.data[valueKey].toLocaleString()} (${percent}%)`);
      })
      .on('mousemove', function(event) {
        tooltip
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 20) + 'px');
      })
      .on('mouseout', function() {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('d', arc);
        tooltip.style('opacity', 0);
      });

    // Labels
    const labelArc = d3.arc()
      .innerRadius(radius * 0.8)
      .outerRadius(radius * 0.8);

    arcs.append('text')
      .attr('transform', d => `translate(${labelArc.centroid(d)})`)
      .attr('text-anchor', 'middle')
      .attr('font-size', '10px')
      .attr('fill', '#374151')
      .style('opacity', 0)
      .transition()
      .delay(800)
      .duration(300)
      .style('opacity', 1)
      .text(d => {
        const percent = (d.data[valueKey] / total) * 100;
        return percent > 5 ? `${percent.toFixed(0)}%` : '';
      });

    // Legend
    const legend = svg.append('g')
      .attr('transform', `translate(${width - 120}, 20)`);

    const legendItems = legend.selectAll('.legend-item')
      .data(data.slice(0, 6))
      .enter()
      .append('g')
      .attr('class', 'legend-item')
      .attr('transform', (d, i) => `translate(0, ${i * 20})`);

    legendItems.append('rect')
      .attr('width', 12)
      .attr('height', 12)
      .attr('rx', 2)
      .attr('fill', d => color(d[labelKey]));

    legendItems.append('text')
      .attr('x', 18)
      .attr('y', 10)
      .attr('font-size', '10px')
      .attr('fill', '#4b5563')
      .text(d => d[labelKey].length > 12 ? d[labelKey].substring(0, 10) + '...' : d[labelKey]);

    return () => {
      tooltip.remove();
    };
  }, [data, valueKey, labelKey, height, colors]);

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400">
        No data available
      </div>
    );
  }

  return (
    <div ref={containerRef} className="w-full">
      <svg ref={svgRef}></svg>
    </div>
  );
}

export default PieChart;
