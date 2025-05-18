/**
 * @title Volcano Plot
 * @fileoverview Volcano plot component
 * @path /components/visualizations/VolcanoPlot.tsx
 */

"use client";

import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { BarChart } from "lucide-react";

interface Gene {
  gene_id: string;
  log2FoldChange: number;
  padj: number;
  significant: boolean;
}

interface VolcanoPlotProps {
  data: Gene[];
  width?: number;
  height?: number;
  treatment: string;
}

export const VolcanoPlot: React.FC<VolcanoPlotProps> = ({
  data,
  width = 800,
  height = 600,
  treatment
}) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!data || !svgRef.current) return;

    // Clear existing plot
    d3.select(svgRef.current).selectAll("*").remove();

    const margin = { top: 40, right: 30, bottom: 60, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // Create scales
    const xScale = d3.scaleLinear()
      .domain(d3.extent(data, d => d.log2FoldChange) as [number, number])
      .range([0, innerWidth]);

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => -Math.log10(d.padj)) as number])
      .range([innerHeight, 0]);

    // Create SVG
    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add axes
    g.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(xScale))
      .append('text')
      .attr('x', innerWidth / 2)
      .attr('y', 40)
      .attr('fill', 'black')
      .text('log2 Fold Change');

    g.append('g')
      .call(d3.axisLeft(yScale))
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -40)
      .attr('x', -innerHeight / 2)
      .attr('fill', 'black')
      .text('-log10(adjusted p-value)');

    // Add points
    g.selectAll('circle')
      .data(data)
      .enter()
      .append('circle')
      .attr('cx', d => xScale(d.log2FoldChange))
      .attr('cy', d => yScale(-Math.log10(d.padj)))
      .attr('r', 3)
      .attr('fill', d => d.significant ? '#dc3545' : '#6c757d')
      .attr('opacity', 0.6);

    // Add title
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', margin.top / 2)
      .attr('text-anchor', 'middle')
      .style('font-size', '16px')
      .text(`Volcano Plot: ${treatment} vs Control`);

  }, [data, width, height, treatment]);

  return <svg ref={svgRef}></svg>;
};

export default VolcanoPlot;


