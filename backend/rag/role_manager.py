"""
Role management for code analysis system.
"""
from typing import List, Dict, Any

class RoleManager:
    """Manages different AI roles and their prompts."""
    
    ROLES = {
        "architect": {
            "name": "Software Architect",
            "description": "Analyzes system architecture and design patterns",
            "prompt_template": """As a Software Architect, analyze this codebase focusing on:
1. Overall architecture and design patterns
2. System components and their interactions
3. Technical debt and architectural improvements
4. Scalability and maintainability concerns

Context: {context}
Question: {question}"""
        },
        "security": {
            "name": "Security Expert",
            "description": "Identifies security vulnerabilities and best practices",
            "prompt_template": """As a Security Expert, analyze this codebase focusing on:
1. Security vulnerabilities and risks
2. Authentication and authorization
3. Data protection and privacy
4. Security best practices

Context: {context}
Question: {question}"""
        },
        "performance": {
            "name": "Performance Engineer",
            "description": "Analyzes performance and optimization opportunities",
            "prompt_template": """As a Performance Engineer, analyze this codebase focusing on:
1. Performance bottlenecks
2. Resource usage and efficiency
3. Optimization opportunities
4. Scalability concerns

Context: {context}
Question: {question}"""
        }
    }
    
    def get_roles(self) -> List[Dict[str, str]]:
        """Get list of available roles."""
        return [
            {"id": role_id, **{k: v for k, v in role.items() if k != "prompt_template"}}
            for role_id, role in self.ROLES.items()
        ]
    
    def get_prompt(self, role_id: str, context: str, question: str) -> str:
        """Get role-specific prompt with context."""
        if role_id not in self.ROLES:
            raise ValueError(f"Invalid role: {role_id}")
            
        template = self.ROLES[role_id]["prompt_template"]
        return template.format(context=context, question=question)