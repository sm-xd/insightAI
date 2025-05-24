import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';

/**
 * DependencyGraph component visualizes dependencies between modules in a codebase.
 * 
 * @param {Object} props - Component props
 * @param {Object} props.data - Dependency graph data
 * @param {Object} props.config - Configuration options
 */
function DependencyGraph({ data, config }) {
  const canvasRef = useRef(null);
  
  // In a real implementation, this would use a proper graph visualization library
  // like D3.js, Cytoscape.js, or react-force-graph
  
  useEffect(() => {
    if (!canvasRef.current) return;
    
    const ctx = canvasRef.current.getContext('2d');
    
    // Mock data for placeholder - in real implementation, this would be real dependency data
    const mockNodes = [
      { id: 'frontend', x: 150, y: 100, radius: 40, color: '#3b82f6' },
      { id: 'backend', x: 350, y: 100, radius: 40, color: '#10b981' },
      { id: 'rag', x: 250, y: 250, radius: 35, color: '#f59e0b' },
      { id: 'parsers', x: 150, y: 350, radius: 30, color: '#8b5cf6' },
      { id: 'agents', x: 350, y: 350, radius: 25, color: '#ec4899' }
    ];
    
    const mockEdges = [
      { source: 'frontend', target: 'backend', width: 3 },
      { source: 'backend', target: 'rag', width: 5 },
      { source: 'backend', target: 'parsers', width: 4 },
      { source: 'rag', target: 'parsers', width: 3 },
      { source: 'rag', target: 'agents', width: 2 },
      { source: 'backend', target: 'agents', width: 1 }
    ];
    
    // Draw dependency graph
    const drawGraph = () => {
      // Clear canvas
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      
      // Draw edges
      for (const edge of mockEdges) {
        const source = mockNodes.find(n => n.id === edge.source);
        const target = mockNodes.find(n => n.id === edge.target);
        
        if (source && target) {
          ctx.beginPath();
          ctx.moveTo(source.x, source.y);
          ctx.lineTo(target.x, target.y);
          ctx.strokeStyle = '#9CA3AF';
          ctx.lineWidth = edge.width;
          ctx.stroke();
          
          // Draw arrow
          const angle = Math.atan2(target.y - source.y, target.x - source.x);
          const arrowSize = 8;
          
          // Adjust endpoint to be at the edge of the target circle
          const dx = target.x - source.x;
          const dy = target.y - source.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          const endX = target.x - (target.radius * dx / dist);
          const endY = target.y - (target.radius * dy / dist);
          
          ctx.beginPath();
          ctx.moveTo(
            endX - arrowSize * Math.cos(angle - Math.PI / 6),
            endY - arrowSize * Math.sin(angle - Math.PI / 6)
          );
          ctx.lineTo(endX, endY);
          ctx.lineTo(
            endX - arrowSize * Math.cos(angle + Math.PI / 6),
            endY - arrowSize * Math.sin(angle + Math.PI / 6)
          );
          ctx.fillStyle = '#9CA3AF';
          ctx.fill();
        }
      }
      
      // Draw nodes
      for (const node of mockNodes) {
        // Draw circle
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, 2 * Math.PI);
        ctx.fillStyle = node.color;
        ctx.fill();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Draw label
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(node.id, node.x, node.y);
      }
    };
    
    drawGraph();
    
    // In a real implementation, we'd handle interactions here:
    // - Zoom in/out
    // - Pan
    // - Click on nodes to highlight related dependencies
    // - Show tooltips with additional info
  }, [data, config]);
  
  return (
    <div className="dependency-graph border rounded-md p-4 bg-white">
      <h3 className="font-medium mb-2">Dependency Graph</h3>
      <p className="text-sm text-gray-500 mb-4">
        Showing relationships between major components
        {config?.show_versions && ' with version information'}
      </p>
      
      <div className="canvas-container relative w-full h-80">
        <canvas 
          ref={canvasRef}
          width={500}
          height={400}
          className="mx-auto border border-gray-200 rounded"
        ></canvas>
        
        {/* In a real implementation, we'd have interactive controls here */}
        <div className="absolute bottom-2 right-2 flex space-x-2">
          <button className="p-1 bg-gray-200 rounded text-xs">
            Reset
          </button>
          <button className="p-1 bg-gray-200 rounded text-xs">
            Zoom In
          </button>
          <button className="p-1 bg-gray-200 rounded text-xs">
            Zoom Out
          </button>
        </div>
      </div>
      
      <div className="legend mt-4 flex flex-wrap gap-4 justify-center">
        <div className="flex items-center">
          <span className="block w-3 h-3 rounded-full bg-blue-500 mr-1"></span>
          <span className="text-xs">Frontend</span>
        </div>
        <div className="flex items-center">
          <span className="block w-3 h-3 rounded-full bg-green-500 mr-1"></span>
          <span className="text-xs">Backend</span>
        </div>
        <div className="flex items-center">
          <span className="block w-3 h-3 rounded-full bg-yellow-500 mr-1"></span>
          <span className="text-xs">RAG Pipeline</span>
        </div>
        <div className="flex items-center">
          <span className="block w-3 h-3 rounded-full bg-purple-500 mr-1"></span>
          <span className="text-xs">Parsers</span>
        </div>
        <div className="flex items-center">
          <span className="block w-3 h-3 rounded-full bg-pink-500 mr-1"></span>
          <span className="text-xs">Agents</span>
        </div>
      </div>
    </div>
  );
}

DependencyGraph.propTypes = {
  data: PropTypes.oneOfType([PropTypes.string, PropTypes.object]).isRequired,
  config: PropTypes.shape({
    show_versions: PropTypes.bool
  })
};

DependencyGraph.defaultProps = {
  config: {
    show_versions: false
  }
};

export default DependencyGraph;