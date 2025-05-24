/**
 * Visualization components for InsightAI
 * 
 * This file exports all visualization components to make importing them easier.
 */

import FolderTree from './FolderTree';
import DependencyGraph from './DependencyGraph';

// Map visualization types to components
const visualizationMap = {
  folder_tree: FolderTree,
  dependency_graph: DependencyGraph,
  // Add more visualization components as they're developed
  tech_stack: () => <div>Tech Stack Visualization (Placeholder)</div>,
  component_hierarchy: () => <div>Component Hierarchy Visualization (Placeholder)</div>,
  api_flow: () => <div>API Flow Visualization (Placeholder)</div>,
  entity_relationship: () => <div>Entity Relationship Visualization (Placeholder)</div>,
  api_documentation: () => <div>API Documentation Visualization (Placeholder)</div>,
  flow_diagram: () => <div>Flow Diagram Visualization (Placeholder)</div>,
  model_architecture: () => <div>Model Architecture Visualization (Placeholder)</div>,
  pipeline_flow: () => <div>Pipeline Flow Visualization (Placeholder)</div>,
};

/**
 * Visualization component that renders the appropriate visualization based on type
 */
export function Visualization({ type, data, config }) {
  const VisualizationComponent = visualizationMap[type] || (() => (
    <div className="bg-gray-100 p-4 rounded">
      Unknown visualization type: {type}
    </div>
  ));
  
  return <VisualizationComponent data={data} config={config} />;
}

export {
  FolderTree,
  DependencyGraph
};