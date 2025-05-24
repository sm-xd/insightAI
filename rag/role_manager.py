"""
Role Manager for InsightAI.

This module manages role templates and their associated analysis tasks.
"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path

class RoleManager:
    """
    Manages role templates and their configurations.
    """
    
    def __init__(self, templates_dir: str = None):
        """
        Initialize the role manager.
        
        Args:
            templates_dir: Optional path to templates directory
        """
        self.templates_dir = templates_dir or os.path.join(
            os.path.dirname(__file__),
            "templates"
        )
        self._load_templates()
    
    def _load_templates(self):
        """Load all role templates from the templates directory."""
        self.templates = {}
        templates_path = Path(self.templates_dir)
        
        if not templates_path.exists():
            # Create templates directory if it doesn't exist
            templates_path.mkdir(parents=True)
            self._create_default_templates()
        
        # Load all JSON files in templates directory
        for template_file in templates_path.glob("*.json"):
            try:
                with open(template_file, 'r') as f:
                    template = json.load(f)
                    self.templates[template['id']] = template
            except Exception as e:
                print(f"Error loading template {template_file}: {str(e)}")
    
    def _create_default_templates(self):
        """Create default role templates."""
        default_templates = {
            "project_manager": {
                "id": "project_manager",
                "name": "Project Manager",
                "description": "Focus on high-level architecture, dependencies, and project structure",
                "prompt_template": """
                As a Project Manager, analyze {focus} and provide insights about {task}.
                Focus on:
                - Project structure and organization
                - Dependencies and integrations
                - Code quality and maintainability
                - Potential risks and technical debt
                """,
                "analysis_tasks": [
                    {
                        "id": "project_structure",
                        "type": "structure",
                        "description": "What is the overall structure of this project?",
                        "visualization": {
                            "type": "folder_tree",
                            "config": {
                                "max_depth": 3
                            }
                        }
                    },
                    {
                        "id": "dependencies",
                        "type": "dependencies",
                        "description": "What are the main dependencies and how are they used?",
                        "visualization": {
                            "type": "dependency_graph",
                            "config": {
                                "show_versions": True
                            }
                        }
                    },
                    {
                        "id": "tech_stack",
                        "type": "technology",
                        "description": "What technologies are used in this project?",
                        "visualization": {
                            "type": "tech_stack",
                            "config": {}
                        }
                    }
                ]
            },
            "frontend_developer": {
                "id": "frontend_developer",
                "name": "Frontend Developer",
                "description": "Focus on UI components, state management, and frontend architecture",
                "prompt_template": """
                As a Frontend Developer, analyze {focus} and provide insights about {task}.
                Focus on:
                - Component architecture and reusability
                - State management patterns
                - UI/UX patterns and implementations
                - Frontend performance considerations
                """,
                "analysis_tasks": [
                    {
                        "id": "component_structure",
                        "type": "components",
                        "description": "How are the UI components organized?",
                        "visualization": {
                            "type": "component_hierarchy",
                            "config": {}
                        }
                    },
                    {
                        "id": "state_management",
                        "type": "state",
                        "description": "How is state managed across the application?",
                        "visualization": {
                            "type": "flow_diagram",
                            "config": {}
                        }
                    },
                    {
                        "id": "frontend_tech",
                        "type": "technology",
                        "description": "What frontend technologies and patterns are used?",
                        "visualization": {
                            "type": "tech_stack",
                            "config": {
                                "focus": "frontend"
                            }
                        }
                    }
                ]
            },
            "backend_developer": {
                "id": "backend_developer",
                "name": "Backend Developer",
                "description": "Focus on API design, data models, and server architecture",
                "prompt_template": """
                As a Backend Developer, analyze {focus} and provide insights about {task}.
                Focus on:
                - API design and patterns
                - Data models and database interactions
                - Server architecture and scalability
                - Backend performance and security
                """,
                "analysis_tasks": [
                    {
                        "id": "api_structure",
                        "type": "api",
                        "description": "How are the APIs structured?",
                        "visualization": {
                            "type": "api_documentation",
                            "config": {}
                        }
                    },
                    {
                        "id": "data_models",
                        "type": "data",
                        "description": "What are the key data models and their relationships?",
                        "visualization": {
                            "type": "entity_relationship",
                            "config": {}
                        }
                    },
                    {
                        "id": "backend_tech",
                        "type": "technology",
                        "description": "What backend technologies and patterns are used?",
                        "visualization": {
                            "type": "tech_stack",
                            "config": {
                                "focus": "backend"
                            }
                        }
                    }
                ]
            },
            "ai_ml_engineer": {
                "id": "ai_ml_engineer",
                "name": "AI/ML Engineer",
                "description": "Focus on ML models, data pipelines, and AI architecture",
                "prompt_template": """
                As an AI/ML Engineer, analyze {focus} and provide insights about {task}.
                Focus on:
                - Machine learning models and algorithms
                - Data processing pipelines
                - Model training and deployment
                - AI/ML infrastructure and scalability
                """,
                "analysis_tasks": [
                    {
                        "id": "model_architecture",
                        "type": "models",
                        "description": "What ML models are used and how are they structured?",
                        "visualization": {
                            "type": "model_architecture",
                            "config": {}
                        }
                    },
                    {
                        "id": "data_pipeline",
                        "type": "pipeline",
                        "description": "How are data pipelines organized?",
                        "visualization": {
                            "type": "pipeline_flow",
                            "config": {}
                        }
                    },
                    {
                        "id": "ai_infrastructure",
                        "type": "infrastructure",
                        "description": "What AI/ML infrastructure and tools are used?",
                        "visualization": {
                            "type": "tech_stack",
                            "config": {
                                "focus": "ai_ml"
                            }
                        }
                    }
                ]
            }
        }
        
        # Save default templates
        for template in default_templates.values():
            template_path = Path(self.templates_dir) / f"{template['id']}.json"
            with open(template_path, 'w') as f:
                json.dump(template, f, indent=2)
    
    def get_template(self, role_id: str) -> Dict[str, Any]:
        """
        Get a role template by ID.
        
        Args:
            role_id: Role template ID
            
        Returns:
            Role template dictionary
            
        Raises:
            ValueError if template not found
        """
        if role_id not in self.templates:
            raise ValueError(f"No template found for role: {role_id}")
        return self.templates[role_id]
    
    def get_available_roles(self) -> List[Dict[str, str]]:
        """
        Get list of available roles.
        
        Returns:
            List of role dictionaries with id, name, and description
        """
        return [
            {
                "id": template["id"],
                "name": template["name"],
                "description": template["description"]
            }
            for template in self.templates.values()
        ]
    
    def add_template(self, template: Dict[str, Any]) -> None:
        """
        Add a new role template.
        
        Args:
            template: Role template dictionary
            
        Raises:
            ValueError if template is invalid
        """
        required_fields = ["id", "name", "description", "prompt_template", "analysis_tasks"]
        missing_fields = [f for f in required_fields if f not in template]
        
        if missing_fields:
            raise ValueError(f"Template missing required fields: {missing_fields}")
        
        # Save template
        template_path = Path(self.templates_dir) / f"{template['id']}.json"
        with open(template_path, 'w') as f:
            json.dump(template, f, indent=2)
        
        self.templates[template['id']] = template
    
    def remove_template(self, role_id: str) -> None:
        """
        Remove a role template.
        
        Args:
            role_id: Role template ID to remove
            
        Raises:
            ValueError if template not found
        """
        if role_id not in self.templates:
            raise ValueError(f"No template found for role: {role_id}")
        
        template_path = Path(self.templates_dir) / f"{role_id}.json"
        template_path.unlink()
        del self.templates[role_id]