"""
Unit tests for the high-level LLM utility functions.
"""

import json
import unittest
from unittest.mock import patch, MagicMock

import pytest

from llamasearch_experimentalagents_product_growth.core.llm import (
    complete_prompt,
    chat_completion,
    analyze_text,
    generate_strategies
)
from llamasearch_experimentalagents_product_growth.core.llm_client import LLMResponse, LLMMessage


class TestCompletionFunctions:
    """Tests for the high-level completion functions."""
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm.get_model_for_task')
    @patch('llamasearch_experimentalagents_product_growth.core.llm.create_client')
    def test_complete_prompt(self, mock_create_client, mock_get_model):
        """Test the complete_prompt function."""
        # Mock responses
        mock_get_model.return_value = {
            "provider": "openai",
            "name": "gpt-4"
        }
        
        mock_client = MagicMock()
        mock_client.complete.return_value = LLMResponse(
            content="This is a test response.",
            model="gpt-4"
        )
        mock_create_client.return_value = mock_client
        
        # Call function
        response = complete_prompt(
            prompt="Test prompt",
            system_prompt="You are a test assistant.",
            temperature=0.5
        )
        
        # Verify function behavior
        assert response == "This is a test response."
        mock_get_model.assert_called_once_with(
            task="Text completion",
            preferred_provider=None
        )
        mock_create_client.assert_called_once_with(
            provider="openai", 
            model="gpt-4"
        )
        
        # Verify client was called correctly with messages
        call_args = mock_client.complete.call_args[1]
        assert len(call_args["messages"]) == 2
        assert call_args["messages"][0].role == "system"
        assert call_args["messages"][0].content == "You are a test assistant."
        assert call_args["messages"][1].role == "user"
        assert call_args["messages"][1].content == "Test prompt"
        assert call_args["temperature"] == 0.5
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm.get_model_for_task')
    @patch('llamasearch_experimentalagents_product_growth.core.llm.create_client')
    def test_chat_completion(self, mock_create_client, mock_get_model):
        """Test the chat_completion function."""
        # Mock responses
        mock_get_model.return_value = {
            "provider": "anthropic",
            "name": "claude-3"
        }
        
        mock_client = MagicMock()
        expected_response = LLMResponse(
            content="I'll help you with that.",
            model="claude-3"
        )
        mock_client.complete.return_value = expected_response
        mock_create_client.return_value = mock_client
        
        # Create test messages
        messages = [
            LLMMessage.system("You are a helpful assistant."),
            LLMMessage.user("Can you help me?")
        ]
        
        # Call function
        response = chat_completion(
            messages=messages,
            temperature=0.8,
            max_tokens=100
        )
        
        # Verify function behavior
        assert response == expected_response
        mock_get_model.assert_called_once_with(
            task="Chat completion",
            preferred_provider=None,
            required_capabilities=["text"]
        )
        mock_create_client.assert_called_once_with(
            provider="anthropic", 
            model="claude-3"
        )
        
        # Verify client was called correctly
        mock_client.complete.assert_called_once_with(
            messages=messages,
            functions=None,
            temperature=0.8,
            max_tokens=100
        )
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm.get_model_for_task')
    @patch('llamasearch_experimentalagents_product_growth.core.llm.create_client')
    def test_chat_completion_with_functions(self, mock_create_client, mock_get_model):
        """Test chat_completion with function calling."""
        # Mock responses
        mock_get_model.return_value = {
            "provider": "openai",
            "name": "gpt-4"
        }
        
        mock_client = MagicMock()
        expected_response = LLMResponse(
            content="",
            function_call={
                "name": "get_weather",
                "arguments": '{"location": "New York"}'
            },
            model="gpt-4"
        )
        mock_client.complete.return_value = expected_response
        mock_create_client.return_value = mock_client
        
        # Create test messages and functions
        messages = [
            LLMMessage.user("What's the weather in New York?")
        ]
        functions = [
            {
                "name": "get_weather",
                "description": "Get current weather",
                "parameters": {
                    "location": {"type": "string"}
                }
            }
        ]
        
        # Call function
        response = chat_completion(
            messages=messages,
            functions=functions
        )
        
        # Verify function behavior
        assert response == expected_response
        mock_get_model.assert_called_once_with(
            task="Chat completion",
            preferred_provider=None,
            required_capabilities=["text", "function_calling"]
        )
        
        # Verify client was called correctly
        mock_client.complete.assert_called_once_with(
            messages=messages,
            functions=functions,
            temperature=0.7,
            max_tokens=None
        )


class TestAnalysisFunctions:
    """Tests for the analysis utility functions."""
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm.complete_prompt')
    def test_analyze_text_sentiment(self, mock_complete_prompt):
        """Test the analyze_text function for sentiment analysis."""
        # Mock response
        mock_complete_prompt.return_value = json.dumps({
            "score": 0.8,
            "label": "positive",
            "explanation": "The text is highly positive."
        })
        
        # Call function
        result = analyze_text(
            text="I love this product! It's amazing.",
            analysis_type="sentiment"
        )
        
        # Verify result
        assert result["score"] == 0.8
        assert result["label"] == "positive"
        assert "explanation" in result
        
        # Verify prompt construction
        call_args = mock_complete_prompt.call_args[1]
        assert "sentiment" in call_args["prompt"].lower()
        assert "I love this product" in call_args["prompt"]
        assert call_args["temperature"] == 0.1  # Low temperature for consistent results
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm.complete_prompt')
    def test_analyze_text_themes(self, mock_complete_prompt):
        """Test the analyze_text function for theme extraction."""
        # Mock response
        mock_complete_prompt.return_value = json.dumps([
            {"name": "usability", "relevance": 0.9},
            {"name": "performance", "relevance": 0.7}
        ])
        
        # Call function
        result = analyze_text(
            text="The app is very easy to use but sometimes slow.",
            analysis_type="themes"
        )
        
        # Verify result
        assert len(result) == 2
        assert result[0]["name"] == "usability"
        assert result[1]["name"] == "performance"
        
        # Verify prompt construction
        call_args = mock_complete_prompt.call_args[1]
        assert "themes" in call_args["prompt"].lower()
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm.complete_prompt')
    def test_analyze_text_invalid_json(self, mock_complete_prompt):
        """Test handling invalid JSON responses."""
        # Mock invalid JSON response
        mock_complete_prompt.return_value = "This is not valid JSON"
        
        # Call function
        result = analyze_text(
            text="Sample text",
            analysis_type="sentiment"
        )
        
        # Verify fallback behavior
        assert "raw_response" in result
        assert result["raw_response"] == "This is not valid JSON"
    
    def test_analyze_text_invalid_type(self):
        """Test handling invalid analysis type."""
        with pytest.raises(ValueError):
            analyze_text(
                text="Sample text",
                analysis_type="invalid_type"
            )


class TestStrategyGeneration:
    """Tests for the strategy generation function."""
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm.complete_prompt')
    def test_generate_strategies(self, mock_complete_prompt):
        """Test the generate_strategies function."""
        # Mock response
        mock_complete_prompt.return_value = json.dumps([
            {
                "feature": "Improved UI",
                "priority": "high",
                "sentiment_score": -0.3,
                "expected_impact": 0.8,
                "gtm_strategies": ["product-led-growth"]
            },
            {
                "feature": "Performance Optimization",
                "priority": "medium",
                "sentiment_score": -0.5,
                "expected_impact": 0.7,
                "gtm_strategies": ["customer-advocacy"]
            }
        ])
        
        # Create test feedback analysis
        feedback_analysis = {
            "num_clusters": 3,
            "cluster_sentiments": {"0": 0.5, "1": -0.3, "2": -0.7},
            "cluster_themes": {
                "0": ["pricing"],
                "1": ["interface"],
                "2": ["performance"]
            }
        }
        
        # Call function
        strategies = generate_strategies(
            feedback_analysis=feedback_analysis,
            max_strategies=3,
            provider="openai"
        )
        
        # Verify result
        assert len(strategies) == 2
        assert strategies[0]["feature"] == "Improved UI"
        assert strategies[0]["priority"] == "high"
        assert strategies[1]["feature"] == "Performance Optimization"
        
        # Verify prompt construction
        call_args = mock_complete_prompt.call_args[1]
        assert "strategy" in call_args["prompt"].lower()
        assert "3" in call_args["prompt"]  # max_strategies
        assert call_args["temperature"] == 0.8  # Higher temperature for creativity
        assert call_args["provider"] == "openai"
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm.complete_prompt')
    def test_generate_strategies_invalid_json(self, mock_complete_prompt):
        """Test handling invalid JSON responses."""
        # Mock invalid JSON response
        mock_complete_prompt.return_value = "This is not valid JSON"
        
        # Call function
        strategies = generate_strategies(
            feedback_analysis={"num_clusters": 1},
            max_strategies=2
        )
        
        # Verify fallback behavior
        assert len(strategies) == 1
        assert strategies[0]["error"] == "Failed to generate strategies"
        assert strategies[0]["raw_response"] == "This is not valid JSON" 