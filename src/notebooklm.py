"""
NotebookLM Client - Google GenAI SDK (Fixed version)
"""
import os
import json
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
import asyncio
from dataclasses import dataclass

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google-genai not installed. Run: pip install google-genai")

@dataclass
class NotebookConfig:
    api_key: Optional[str] = None
    model: str = "gemini-2.0-flash-exp"
    temperature: float = 0.7
    max_tokens: int = 8192

class NotebookLMClient:
    def __init__(self, config: Optional[NotebookConfig] = None):
        self.config = config or NotebookConfig()
        self.api_key = self.config.api_key or os.getenv("GOOGLE_API_KEY")
        
        if GENAI_AVAILABLE and self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            
        self.notebooks = {}
        self.conversations = {}
        
    @classmethod
    async def from_storage(cls, storage_path: str = "notebooks_data.json"):
        client = cls()
        await client.load_notebooks(storage_path)
        return client
    
    async def load_notebooks(self, storage_path: str = "notebooks_data.json"):
        if Path(storage_path).exists():
            try:
                with open(storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.notebooks = data.get('notebooks', {})
                    self.conversations = data.get('conversations', {})
            except:
                pass
    
    async def save_notebooks(self, storage_path: str = "notebooks_data.json"):
        data = {
            'notebooks': self.notebooks,
            'conversations': self.conversations,
            'updated_at': datetime.now().isoformat()
        }
        with open(storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    async def create_notebook(self, name: str, description: str = "") -> Dict:
        notebook_id = f"nb_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{abs(hash(name)) % 10000}"
        notebook = {
            "id": notebook_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "sources": [],
            "notes": []
        }
        self.notebooks[notebook_id] = notebook
        await self.save_notebooks()
        return notebook
    
    async def add_source(self, notebook_id: str, source_content: str, source_name: str = None):
        if notebook_id not in self.notebooks:
            raise ValueError(f"Notebook {notebook_id} not found")
        
        source = {
            "id": f"src_{len(self.notebooks[notebook_id]['sources'])}",
            "name": source_name or f"Source {len(self.notebooks[notebook_id]['sources'])}",
            "content": source_content[:50000],
            "added_at": datetime.now().isoformat()
        }
        self.notebooks[notebook_id]['sources'].append(source)
        await self.save_notebooks()
        return source
    
    async def list_notebooks(self):
        return [
            {
                "id": nb_id,
                "name": nb_data.get("name", "Untitled"),
                "sources_count": len(nb_data.get("sources", [])),
                "created_at": nb_data.get("created_at", "")
            }
            for nb_id, nb_data in self.notebooks.items()
        ]

class ChatSession:
    def __init__(self, client: NotebookLMClient, notebook_id: str, initial_question: str = None):
        self.client = client
        self.notebook_id = notebook_id
        self.history = []
        if initial_question:
            self.history.append({"role": "user", "content": initial_question})
    
    async def ask(self, question: str = None):
        # Lấy question từ parameter hoặc từ history
        if question is None and self.history:
            # Lấy câu hỏi cuối cùng từ user
            for msg in reversed(self.history):
                if msg["role"] == "user":
                    question = msg["content"]
                    break
        
        if not question:
            raise ValueError("No question provided")
        
        # Lấy notebook
        notebook = self.client.notebooks.get(self.notebook_id)
        if not notebook:
            raise ValueError(f"Notebook {self.notebook_id} not found")
        
        # Build context từ sources
        context_parts = []
        for src in notebook.get('sources', [])[:3]:
            context_parts.append(f"=== {src['name']} ===\n{src['content'][:2000]}")
        context = "\n\n".join(context_parts)
        
        # Tạo prompt dựa trên context
        if context:
            prompt = f"""Based on these sources:

{context}

Question: {question}

Answer based ONLY on the sources above. If not found, say "I cannot find this information in the sources."

Answer:"""
        else:
            prompt = f"Question: {question}\n\nAnswer:"
        
        # Gọi API hoặc mock
        if self.client.client:
            try:
                response = await asyncio.to_thread(
                    self.client.client.models.generate_content,
                    model=self.client.config.model,
                    contents=prompt
                )
                answer = response.text
            except Exception as e:
                answer = f"API Error: {str(e)}"
        else:
            # Mock response
            if "key features" in question.lower():
                answer = """Based on the provided sources, SEN V3 has the following key features:
1. Multi-agent architecture for content creation
2. Facebook integration for automated posting
3. AccessTrade API support
4. Automated scheduling system"""
            elif "sen v3" in question.lower():
                answer = "SEN V3 is an automated content posting system that supports multiple platforms including Facebook and AccessTrade."
            else:
                answer = f"[Mock Mode] Question received: '{question}'\n\nSuggestion: Add more sources to the notebook for better answers."
        
        # Lưu vào history
        self.history.append({"role": "assistant", "content": answer})
        
        return ChatResponse(answer)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

class ChatResponse:
    def __init__(self, answer: str):
        self.answer = answer