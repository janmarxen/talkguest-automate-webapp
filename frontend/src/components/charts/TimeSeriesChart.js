import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

function TimeSeriesChart({ data, xKey, lines, height = 300 }) {
  const svgRef = useRef();
  const containerRef = useRef();

  useEffect(() => {
    if (!data || data.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const container = containerRef.current;
    const width = container.clientWidth;
    const margin = { top: 40, right: 30, bottom: 80, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const g = svg
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const x = d3.scaleBand()
      .domain(data.map(d => d[xKey]))
      .range([0, innerWidth])
      .padding(0.1);

    const allValues = lines.flatMap(line => data.map(d => d[line.key]));
    const y = d3.scaleLinear()
      .domain([0, d3.max(allValues) * 1.1])
      .nice()
      .range([innerHeight, 0]);

    // X axis
    g.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .attr('transform', 'rotate(-45)')
      .attr('text-anchor', 'end')
      .attr('dx', '-0.5em')
      .attr('dy', '0.5em')
      .style('font-size', '10px');

    // Y axis
    g.append('g')
      .call(d3.axisLeft(y).ticks(5).tickFormat(d => `€${d.toLocaleString()}`))
      .selectAll('text')
      .style('font-size', '11px');

    // Grid lines
    g.append('g')
      .attr('class', 'grid')
      .call(d3.axisLeft(y).ticks(5).tickSize(-innerWidth).tickFormat(''))
      .selectAll('line')
      .attr('stroke', '#e5e7eb')
      .attr('stroke-dasharray', '2,2');

    g.select('.grid .domain').remove();

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

    // Draw bars for each line as grouped bars
    const barWidth = x.bandwidth() / lines.length;

    lines.forEach((line, lineIndex) => {
      g.selectAll(`.bar-${line.key}`)
        .data(data)
        .enter()
        .append('rect')
        .attr('class', `bar-${line.key}`)
        .attr('x', d => x(d[xKey]) + lineIndex * barWidth)
        .attr('width', barWidth - 2)
        .attr('y', innerHeight)
        .attr('height', 0)
        .attr('fill', line.color)
        .attr('rx', 2)
        .on('mouseover', function(event, d) {
          d3.select(this).attr('opacity', 0.8);
          tooltip
            .style('opacity', 1)
            .html(`<strong>${d[xKey]}</strong><br/>${line.label}: €${d[line.key].toLocaleString()}`);
        })
        .on('mousemove', function(event) {
          tooltip
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 20) + 'px');
        })
        .on('mouseout', function() {
          d3.select(this).attr('opacity', 1);
          tooltip.style('opacity', 0);
        })
        .transition()
        .duration(800)
        .delay(lineIndex * 100)
        .attr('y', d => y(d[line.key]))
        .attr('height', d => innerHeight - y(d[line.key]));
    });

    // Legend
    const legend = g.append('g')
      .attr('transform', `translate(${innerWidth - 150}, -25)`);

    lines.forEach((line, i) => {
      const legendItem = legend.append('g')
        .attr('transform', `translate(${i * 120}, 0)`);

      legendItem.append('rect')
        .attr('width', 12)
        .attr('height', 12)
        .attr('rx', 2)
        .attr('fill', line.color);

      legendItem.append('text')
        .attr('x', 18)
        .attr('y', 10)
        .attr('font-size', '11px')
        .attr('fill', '#4b5563')
        .text(line.label);
    });

    return () => {
      tooltip.remove();
    };
  }, [data, xKey, lines, height]);

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

export default TimeSeriesChart;
