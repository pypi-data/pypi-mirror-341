"""
Professional assistant agent implementation for LlamaSearch.

This module implements the main AI assistant functionality, coordinating between
semantic search, embedding generation, and response formatting.
"""

import logging
import json
from typing import List, Dict, Any, Optional, Callable

import openai
from openai import OpenAI
from openai.types.function_definition import FunctionDefinition
from openai.types.function_parameters import FunctionParameters

from ..models.knowledge import KnowledgeBase, RunContextWrapper
from ..models.responses import ProfessionalResponse, SourceReference, SuggestedAction
from .retriever import SemanticRetriever

logger = logging.getLogger(__name__)


class LlamaAssistant:
    """Professional AI assistant with semantic search capabilities."""
    
    def __init__(
        self, 
        knowledge_base: KnowledgeBase,
        openai_client: Optional[OpenAI] = None,
        embedding_model: str = "text-embedding-3-small",
        assistant_model: str = "gpt-4-turbo-preview",
    ):
        """
        Initialize the LlamaAssistant.
        
        Args:
            knowledge_base: The knowledge base to use for semantic search
            openai_client: Optional OpenAI client (created if not provided)
            embedding_model: The OpenAI embedding model to use
            assistant_model: The OpenAI model to use for the assistant
        """
        self.knowledge_base = knowledge_base
        self.client = openai_client or OpenAI()
        self.embedding_model = embedding_model
        self.assistant_model = assistant_model
        
        # Initialize retriever
        self.retriever = SemanticRetriever(knowledge_base)
        
        # Create a run context wrapper
        self.run_context = RunContextWrapper(knowledge_base)
        
        logger.info(f"Initialized LlamaAssistant with {len(knowledge_base)} chunks")
        logger.info(f"Using embedding model: {embedding_model}")
        logger.info(f"Using assistant model: {assistant_model}")
    
    def get_embedding(self, text: str) -> List[float]:
        """Get an embedding vector for a text string."""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text,
        )
        return response.data[0].embedding
    
    def search_knowledge_base(
        self, 
        query: str,
        top_k: int = 3,
        score_threshold: float = 0.6,
        backend: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search the knowledge base for relevant content.
        
        Args:
            query: The search query
            top_k: Number of top results to return
            score_threshold: Minimum similarity score for results
            backend: Preferred backend (mlx, jax, or numpy)
            
        Returns:
            A list of search results with scores
        """
        # Get embedding for the query
        query_embedding = self.get_embedding(query)
        
        # Perform semantic search
        results, backend_used, execution_time_ms = self.retriever.semantic_search(
            query_embedding=query_embedding,
            top_k=top_k,
            score_threshold=score_threshold,
            backend=backend
        )
        
        logger.info(f"Search for '{query}' found {len(results)} results in {execution_time_ms:.2f}ms using {backend_used}")
        return results
    
    def _define_search_function(self) -> FunctionDefinition:
        """Define the search function for OpenAI function calling."""
        return FunctionDefinition(
            name="search_knowledge_base",
            description="Search the knowledge base for relevant information to answer the user's query",
            parameters=FunctionParameters(
                type="object",
                properties={
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant information"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of top results to return",
                        "default": 3
                    }
                },
                required=["query"]
            )
        )
    
    def _format_sources_for_context(self, results: List[Dict[str, Any]]) -> str:
        """Format search results as context for the LLM."""
        if not results:
            return "No relevant information found in the knowledge base."
        
        context = "Here is relevant information from the knowledge base:\n\n"
        for i, result in enumerate(results, 1):
            context += f"[Source {i}: {result['source']}]\n"
            context += f"{result['content']}\n\n"
        
        return context
    
    def _parse_suggested_actions(self, actions_text: str) -> List[SuggestedAction]:
        """Parse suggested actions from the LLM response."""
        try:
            actions_data = json.loads(actions_text)
            if not isinstance(actions_data, list):
                return []
            
            result = []
            for action_data in actions_data:
                if not isinstance(action_data, dict):
                    continue
                
                # Get required fields with defaults
                title = action_data.get("title", "Unnamed action")
                description = action_data.get("description", "No description provided")
                priority = action_data.get("priority", "medium")
                
                # Create and validate the action
                try:
                    action = SuggestedAction(
                        title=title,
                        description=description,
                        priority=priority
                    )
                    result.append(action)
                except ValueError:
                    # Skip invalid actions
                    continue
            
            return result
        except Exception as e:
            logger.warning(f"Failed to parse suggested actions: {e}")
            return []
    
    def generate_response(
        self,
        query: str,
        on_search_start: Optional[Callable[[], None]] = None,
        on_search_complete: Optional[Callable[[List[Dict[str, Any]]], None]] = None,
        on_thinking_start: Optional[Callable[[], None]] = None,
        on_thinking_complete: Optional[Callable[[], None]] = None
    ) -> ProfessionalResponse:
        """
        Generate a professional response to a user query.
        
        Args:
            query: The user query
            on_search_start: Optional callback when search starts
            on_search_complete: Optional callback when search completes
            on_thinking_start: Optional callback when thinking starts
            on_thinking_complete: Optional callback when thinking completes
            
        Returns:
            A professional structured response
        """
        # Define search function
        search_fn = self._define_search_function()
        
        # Initial system prompt
        system_prompt = f"""
        You are a professional AI assistant powered by LlamaSearch.
        Your task is to provide helpful, accurate, and detailed responses to questions based on the knowledge base provided.
        
        When answering:
        1. Be clear, concise, and professional
        2. Cite your sources from the knowledge base when possible
        3. If you don't know something or it's not in the knowledge base, be honest about it
        4. Suggest follow-up actions when appropriate
        
        Knowledge base description: {self.knowledge_base.description}
        """
        
        # Step 1: Call the model to determine if search is needed
        if on_thinking_start:
            on_thinking_start()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        initial_response = self.client.chat.completions.create(
            model=self.assistant_model,
            messages=messages,
            tools=[{"type": "function", "function": search_fn}],
            tool_choice={"type": "function", "function": {"name": "search_knowledge_base"}},
        )
        
        # Extract search parameters
        tool_call = initial_response.choices[0].message.tool_calls[0]
        search_args = json.loads(tool_call.function.arguments)
        search_query = search_args.get("query", query)
        top_k = search_args.get("top_k", 3)
        
        # Step 2: Search knowledge base
        if on_search_start:
            on_search_start()
        
        search_results = self.search_knowledge_base(search_query, top_k=top_k)
        
        if on_search_complete:
            on_search_complete(search_results)
        
        # Step 3: Generate final response with search results
        knowledge_context = self._format_sources_for_context(search_results)
        
        messages.append({
            "role": "assistant", 
            "content": None, 
            "tool_calls": [tool_call]
        })
        
        messages.append({
            "role": "tool", 
            "tool_call_id": tool_call.id,
            "content": knowledge_context
        })
        
        # Additional system instruction for structured output
        messages.append({
            "role": "system", 
            "content": """
            Please format your response as a JSON object with the following structure:
            
            {
                "answer": "Your detailed answer here",
                "confidence": 0.85,  # A float between 0 and 1 representing your confidence in the answer
                "sources": [
                    {
                        "source": "Source identifier",
                        "relevance": 0.9,  # A float between 0 and 1
                        "excerpt": "Brief excerpt if applicable"
                    }
                ],
                "suggested_actions": [
                    {
                        "title": "Action title",
                        "description": "Detailed description of the action",
                