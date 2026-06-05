"""
NotebookLM Service - Business logic layer
Handles notebook operations with error handling and caching
"""
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path

from src.notebooklm import NotebookLMClient, ChatSession
from src.logging_config import configure_logging

logger = configure_logging(__name__)

class NotebookLMService:
    """Service for managing NotebookLM operations"""
    
    def __init__(self, storage_path: str = "notebooks_data.json"):
        self.storage_path = storage_path
        self._client: Optional[NotebookLMClient] = None
        self._cache = {}
    
    async def get_client(self) -> NotebookLMClient:
        """Get or create NotebookLM client (singleton)"""
        if not self._client:
            logger.info("Initializing NotebookLM client...")
            self._client = await NotebookLMClient.from_storage(self.storage_path)
        return self._client
    
    async def create_notebook(self, name: str, description: str = "") -> Dict:
        """Create a new notebook"""
        try:
            client = await self.get_client()
            notebook = await client.create_notebook(name, description)
            logger.info(f"Created notebook: {notebook['id']} - {name}")
            return {"success": True, "notebook": notebook}
        except Exception as e:
            logger.error(f"Failed to create notebook: {e}")
            return {"success": False, "error": str(e)}
    
    async def add_source(self, notebook_id: str, content: str, name: str = None) -> Dict:
        """Add source to notebook"""
        try:
            client = await self.get_client()
            source = await client.add_source(notebook_id, content, name)
            logger.info(f"Added source to {notebook_id}: {source['id']}")
            return {"success": True, "source": source}
        except Exception as e:
            logger.error(f"Failed to add source: {e}")
            return {"success": False, "error": str(e)}
    
    async def ask_notebook(self, notebook_id: str, question: str) -> Dict:
        """Ask a question to the notebook"""
        try:
            client = await self.get_client()
            
            if notebook_id not in client.notebooks:
                return {"success": False, "error": f"Notebook {notebook_id} not found"}
            
            # Create chat session
            chat = ChatSession(client, notebook_id)
            response = await chat.ask(question)
            
            logger.info(f"Asked question to {notebook_id}: {question[:50]}...")
            
            return {
                "success": True, 
                "answer": response.answer,
                "notebook_id": notebook_id,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error asking notebook: {e}")
            return {"success": False, "error": str(e)}
    
    async def list_notebooks(self) -> List[Dict]:
        """List all notebooks"""
        try:
            client = await self.get_client()
            notebooks = [
                {
                    "id": nb_id,
                    "name": nb_data.get("name", "Untitled"),
                    "description": nb_data.get("description", ""),
                    "sources_count": len(nb_data.get("sources", [])),
                    "created_at": nb_data.get("created_at", "")
                }
                for nb_id, nb_data in client.notebooks.items()
            ]
            return notebooks
        except Exception as e:
            logger.error(f"Failed to list notebooks: {e}")
            return []
    
    async def get_notebook_details(self, notebook_id: str) -> Dict:
        """Get detailed information about a notebook"""
        try:
            client = await self.get_client()
            
            if notebook_id not in client.notebooks:
                return {"success": False, "error": "Notebook not found"}
            
            notebook = client.notebooks[notebook_id]
            
            return {
                "success": True,
                "notebook": {
                    "id": notebook["id"],
                    "name": notebook["name"],
                    "description": notebook["description"],
                    "sources": notebook.get("sources", []),
                    "created_at": notebook.get("created_at"),
                    "total_sources": len(notebook.get("sources", [])),
                    "total_notes": len(notebook.get("notes", []))
                }
            }
        except Exception as e:
            logger.error(f"Failed to get notebook details: {e}")
            return {"success": False, "error": str(e)}
    
    async def export_to_markdown(self, notebook_id: str, output_path: str = None) -> str:
        """Export notebook to markdown format"""
        try:
            client = await self.get_client()
            
            if notebook_id not in client.notebooks:
                raise ValueError("Notebook not found")
            
            notebook = client.notebooks[notebook_id]
            
            # Generate markdown
            md = f"# {notebook['name']}\n\n"
            md += f"*{notebook['description']}*\n\n"
            md += f"**Created:** {notebook['created_at']}\n"
            md += f"**Sources:** {len(notebook.get('sources', []))}\n\n"
            md += "## Sources\n\n"
            
            for source in notebook.get('sources', []):
                md += f"### {source['name']}\n"
                md += f"*Added: {source['added_at']}*\n\n"
                md += f"```\n{source['content'][:1000]}\n```\n\n"
            
            # Save to file if output path provided
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(md)
                logger.info(f"Exported notebook to {output_path}")
            
            return md
        except Exception as e:
            logger.error(f"Failed to export notebook: {e}")
            return ""
    
    async def import_from_json(self, json_path: str) -> Dict:
        """Import notebook from JSON file"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            client = await self.get_client()
            
            # Create notebook from imported data
            notebook = await client.create_notebook(
                name=data.get('name', 'Imported Notebook'),
                description=data.get('description', '')
            )
            
            # Add sources
            for source in data.get('sources', []):
                await client.add_source(
                    notebook['id'],
                    source.get('content', ''),
                    source.get('name', 'Imported Source')
                )
            
            logger.info(f"Imported notebook from {json_path}")
            return {"success": True, "notebook_id": notebook['id']}
        except Exception as e:
            logger.error(f"Failed to import notebook: {e}")
            return {"success": False, "error": str(e)}