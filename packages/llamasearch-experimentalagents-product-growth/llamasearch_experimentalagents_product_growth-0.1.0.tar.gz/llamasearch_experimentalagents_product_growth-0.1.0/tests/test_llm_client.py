"""
Unit tests for the LLM client module.
"""

import json
import unittest
from unittest.mock import patch, MagicMock, ANY

import pytest

from llamasearch_experimentalagents_product_growth.core.llm_client import (
    LLMMessage,
    LLMFunction,
    LLMResponse,
    LLMClient,
    OpenAIClient,
    AnthropicClient,
    LocalModelClient,
    create_client
)
from llamasearch_experimentalagents_product_growth.core.llm_router import LLMProvider


class TestLLMMessage(unittest.TestCase):
    """Tests for the LLMMessage class."""
    
    def test_message_creation(self):
        """Test creating message instances."""
        # Test system message
        system_msg = LLMMessage.system("You are a helpful assistant.")
        self.assertEqual(system_msg.role, "system")
        self.assertEqual(system_msg.content, "You are a helpful assistant.")
        
        # Test user message
        user_msg = LLMMessage.user("Hello, assistant!")
        self.assertEqual(user_msg.role, "user")
        self.assertEqual(user_msg.content, "Hello, assistant!")
        
        # Test assistant message
        assistant_msg = LLMMessage.assistant("Hello, user!")
        self.assertEqual(assistant_msg.role, "assistant")
        self.assertEqual(assistant_msg.content, "Hello, user!")
        
        # Test function message
        function_msg = LLMMessage.function("get_weather", "{'temperature': 72}")
        self.assertEqual(function_msg.role, "function")
        self.assertEqual(function_msg.name, "get_weather")
        self.assertEqual(function_msg.content, "{'temperature': 72}")
    
    def test_to_dict(self):
        """Test converting messages to dictionaries."""
        # System message
        system_dict = LLMMessage.system("System prompt").to_dict()
        self.assertEqual(system_dict, {
            "role": "system",
            "content": "System prompt"
        })
        
        # User message
        user_dict = LLMMessage.user("User input").to_dict()
        self.assertEqual(user_dict, {
            "role": "user",
            "content": "User input"
        })
        
        # Assistant message with function call
        function_call = {"name": "get_weather", "arguments": '{"location": "New York"}'}
        assistant_dict = LLMMessage.assistant(
            "I'll check the weather.", 
            function_call=function_call
        ).to_dict()
        self.assertEqual(assistant_dict, {
            "role": "assistant",
            "content": "I'll check the weather.",
            "function_call": function_call
        })
        
        # Function message
        function_dict = LLMMessage.function(
            "get_weather", 
            '{"temperature": 72}'
        ).to_dict()
        self.assertEqual(function_dict, {
            "role": "function",
            "content": '{"temperature": 72}',
            "name": "get_weather"
        })


class TestLLMFunction(unittest.TestCase):
    """Tests for the LLMFunction class."""
    
    def test_function_creation(self):
        """Test creating function instances."""
        # Define a function
        get_weather = LLMFunction(
            name="get_weather",
            description="Get the current weather for a location",
            parameters={
                "location": {
                    "type": "string",
                    "description": "The location to get weather for (e.g. 'New York')"
                }
            },
            required=["location"]
        )
        
        # Check attributes
        self.assertEqual(get_weather.name, "get_weather")
        self.assertEqual(
            get_weather.description, 
            "Get the current weather for a location"
        )
        self.assertEqual(get_weather.required, ["location"])
    
    def test_to_dict(self):
        """Test converting functions to dictionaries."""
        # Define a function
        get_weather = LLMFunction(
            name="get_weather",
            description="Get the current weather for a location",
            parameters={
                "location": {
                    "type": "string",
                    "description": "The location to get weather for"
                }
            },
            required=["location"]
        )
        
        # Convert to dict
        weather_dict = get_weather.to_dict()
        
        # Check the structure
        self.assertEqual(weather_dict["name"], "get_weather")
        self.assertEqual(
            weather_dict["description"], 
            "Get the current weather for a location"
        )
        self.assertEqual(
            weather_dict["parameters"]["properties"]["location"]["type"], 
            "string"
        )
        self.assertEqual(weather_dict["parameters"]["required"], ["location"])


class TestLLMResponse(unittest.TestCase):
    """Tests for the LLMResponse class."""
    
    def test_response_creation(self):
        """Test creating response instances."""
        # Create a basic response
        response = LLMResponse(
            content="Hello, user!",
            model="gpt-4"
        )
        self.assertEqual(response.content, "Hello, user!")
        self.assertEqual(response.model, "gpt-4")
        self.assertIsNone(response.function_call)
        
        # Create response with function call
        function_response = LLMResponse(
            content="I'll check the weather.",
            function_call={
                "name": "get_weather",
                "arguments": '{"location": "New York"}'
            },
            message_id="msg_123",
            usage={"total_tokens": 100},
            model="gpt-4"
        )
        self.assertEqual(function_response.content, "I'll check the weather.")
        self.assertEqual(
            function_response.function_call["name"], 
            "get_weather"
        )
        self.assertEqual(function_response.message_id, "msg_123")
        self.assertEqual(function_response.usage["total_tokens"], 100)
    
    def test_to_dict(self):
        """Test converting responses to dictionaries."""
        # Create a response with all fields
        response = LLMResponse(
            content="Hello, user!",
            function_call={
                "name": "get_weather",
                "arguments": '{"location": "New York"}'
            },
            message_id="msg_123",
            usage={"total_tokens": 100},
            model="gpt-4"
        )
        
        # Convert to dict
        response_dict = response.to_dict()
        
        # Check the structure
        self.assertEqual(response_dict["content"], "Hello, user!")
        self.assertEqual(
            response_dict["function_call"]["name"], 
            "get_weather"
        )
        self.assertEqual(response_dict["message_id"], "msg_123")
        self.assertEqual(response_dict["usage"]["total_tokens"], 100)
        self.assertEqual(response_dict["model"], "gpt-4")


class TestOpenAIClient:
    """Tests for the OpenAIClient class."""
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm_client.OpenAI')
    def test_complete(self, mock_openai_class):
        """Test generating completions with OpenAI."""
        # Set up mock response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.id = "response_id"
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 20
        mock_response.usage.total_tokens = 30
        
        mock_choice = MagicMock()
        mock_choice.message.content = "Hello, user!"
        mock_response.choices = [mock_choice]
        
        mock_client.chat.completions.create.return_value = mock_response
        
        # Create client and generate completion
        client = OpenAIClient(api_key="test-key")
        response = client.complete(
            messages=[LLMMessage.user("Hello!")],
            temperature=0.7
        )
        
        # Check the response
        assert response.content == "Hello, user!"
        assert response.message_id == "response_id"
        assert response.model == "gpt-3.5-turbo"
        assert response.usage["total_tokens"] == 30
        
        # Check that the API was called correctly
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}],
            temperature=0.7
        )
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm_client.OpenAI')
    def test_complete_with_functions(self, mock_openai_class):
        """Test generating completions with functions."""
        # Set up mock response with function call
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_function_call = MagicMock()
        mock_function_call.name = "get_weather"
        mock_function_call.arguments = '{"location": "New York"}'
        
        mock_choice = MagicMock()
        mock_choice.message.content = None
        mock_choice.message.function_call = mock_function_call
        
        mock_response.choices = [mock_choice]
        mock_response.id = "response_id"
        mock_response.usage.prompt_tokens = 15
        mock_response.usage.completion_tokens = 25
        mock_response.usage.total_tokens = 40
        
        mock_client.chat.completions.create.return_value = mock_response
        
        # Create function
        get_weather = LLMFunction(
            name="get_weather",
            description="Get the current weather for a location",
            parameters={"location": {"type": "string"}},
        )
        
        # Create client and generate completion
        client = OpenAIClient(api_key="test-key")
        response = client.complete(
            messages=[LLMMessage.user("What's the weather in New York?")],
            functions=[get_weather],
            temperature=0.7
        )
        
        # Check the response
        assert response.content == ""  # No content, only function call
        assert response.function_call["name"] == "get_weather"
        assert response.function_call["arguments"] == '{"location": "New York"}'
        
        # Check that the API was called with functions
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        assert "functions" in call_args
        assert call_args["functions"][0]["name"] == "get_weather"


class TestAnthropicClient:
    """Tests for the AnthropicClient class."""
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm_client.anthropic')
    def test_complete(self, mock_anthropic_module):
        """Test generating completions with Anthropic."""
        # Set up mock response
        mock_client = MagicMock()
        mock_anthropic_module.Anthropic.return_value = mock_client
        
        mock_content = MagicMock()
        mock_content.text = "Hello, user!"
        
        mock_response = MagicMock()
        mock_response.content = [mock_content]
        mock_response.id = "response_id"
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 20
        
        mock_client.messages.create.return_value = mock_response
        
        # Create client and generate completion
        client = AnthropicClient(api_key="test-key")
        response = client.complete(
            messages=[LLMMessage.user("Hello!")],
            temperature=0.7
        )
        
        # Check the response
        assert response.content == "Hello, user!"
        assert response.message_id == "response_id"
        assert response.model == "claude-3-sonnet-20240229"
        assert response.usage["input_tokens"] == 10
        assert response.usage["output_tokens"] == 20
        
        # Check that the API was called correctly
        mock_client.messages.create.assert_called_once_with(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": "Hello!"}],
            temperature=0.7
        )


def test_create_client():
    """Test the create_client factory function."""
    # Test with OpenAI
    with patch('llamasearch_experimentalagents_product_growth.core.llm_client.OpenAIClient') as mock_openai:
        mock_openai.return_value = "openai_client"
        client = create_client(LLMProvider.OPENAI, "gpt-4", "test-key")
        assert client == "openai_client"
        mock_openai.assert_called_once_with(model="gpt-4", api_key="test-key")
    
    # Test with Anthropic
    with patch('llamasearch_experimentalagents_product_growth.core.llm_client.AnthropicClient') as mock_anthropic:
        mock_anthropic.return_value = "anthropic_client"
        client = create_client(LLMProvider.ANTHROPIC, "claude-3", "test-key")
        assert client == "anthropic_client"
        mock_anthropic.assert_called_once_with(model="claude-3", api_key="test-key")
    
    # Test with Local
    with patch('llamasearch_experimentalagents_product_growth.core.llm_client.LocalModelClient') as mock_local:
        mock_local.return_value = "local_client"
        client = create_client(LLMProvider.LOCAL, "llama3")
        assert client == "local_client"
        mock_local.assert_called_once_with(model="llama3")
    
    # Test with invalid provider
    with pytest.raises(ValueError):
        create_client("invalid_provider", "model-name") 