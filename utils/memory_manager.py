import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from config import Config

class MemoryManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.memory_file = "data/chat_history.json"
        self.personality_file = "data/personality_profile.json"
        
        # Initialize FAISS vector store
        self.vector_store = None
        self.chat_history = []
        self.personality_profile = {}
        
        self._load_memory()
        self._initialize_vector_store()
    
    def _load_memory(self):
        """Load chat history and personality profile from files"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.chat_history = json.load(f)
            except:
                self.chat_history = []
        
        if os.path.exists(self.personality_file):
            try:
                with open(self.personality_file, 'r') as f:
                    self.personality_profile = json.load(f)
            except:
                self.personality_profile = {}
    
    def _initialize_vector_store(self):
        """Initialize FAISS vector store with existing messages"""
        if self.chat_history:
            user_messages = [msg for msg in self.chat_history if msg['role'] == 'user']
            if user_messages:
                documents = [Document(page_content=msg['content'], 
                                   metadata={"timestamp": msg['timestamp']}) 
                           for msg in user_messages]
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
        
        if self.vector_store is None:
            # Create empty vector store
            dummy_doc = Document(page_content="initialization", metadata={})
            self.vector_store = FAISS.from_documents([dummy_doc], self.embeddings)
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to memory"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.chat_history.append(message)
        
        # Add to vector store if it's a user message
        if role == "user":
            doc = Document(page_content=content, metadata={"timestamp": message["timestamp"]})
            self.vector_store.add_documents([doc])
        
        # Keep memory under limit
        if len(self.chat_history) > Config.MAX_MEMORY_ITEMS:
            self.chat_history = self.chat_history[-Config.MAX_MEMORY_ITEMS:]
        
        self._save_memory()
    
    def get_similar_messages(self, query: str, k: int = 3) -> List[str]:
        """Get similar user messages based on semantic similarity"""
        if not self.vector_store or not query or not query.strip():
            return []
        
        try:
            similar_docs = self.vector_store.similarity_search(query.strip(), k=k)
            return [doc.page_content for doc in similar_docs if doc.page_content != "initialization"]
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []
    
    def get_conversation_context(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation context"""
        return self.chat_history[-limit:] if self.chat_history else []
    
    def get_user_message_count(self) -> int:
        """Get count of user messages"""
        return len([msg for msg in self.chat_history if msg['role'] == 'user'])
    
    def get_personality_traits(self) -> Dict[str, Any]:
        """Get current personality profile"""
        return self.personality_profile.copy()
    
    def update_personality_profile(self, traits: Dict[str, Any]):
        """Update personality profile"""
        self.personality_profile.update(traits)
        self.personality_profile['last_updated'] = datetime.now().isoformat()
        self._save_personality()
    
    def get_user_messages_for_analysis(self, limit: int = 50) -> List[str]:
        """Get recent user messages for personality analysis"""
        user_messages = [msg['content'] for msg in self.chat_history 
                        if msg['role'] == 'user']
        return user_messages[-limit:] if user_messages else []
    
    def _save_memory(self):
        """Save chat history to file"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.chat_history, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def _save_personality(self):
        """Save personality profile to file"""
        os.makedirs(os.path.dirname(self.personality_file), exist_ok=True)
        try:
            with open(self.personality_file, 'w') as f:
                json.dump(self.personality_profile, f, indent=2)
        except Exception as e:
            print(f"Error saving personality: {e}")
    
    def clear_memory(self):
        """Clear all memory"""
        self.chat_history = []
        self.personality_profile = {}
        self._initialize_vector_store()
        self._save_memory()
        self._save_personality()
    
    def export_data(self) -> Dict[str, Any]:
        """Export all data for backup"""
        return {
            "chat_history": self.chat_history,
            "personality_profile": self.personality_profile,
            "export_timestamp": datetime.now().isoformat()
        }