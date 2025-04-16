"""
Unit tests for the LLM router module.
"""

import os
import unittest
from unittest.mock import patch, MagicMock

import pytest

from llamasearch_experimentalagents_product_growth.core.llm_router import (
    LLMProvider,
    LLMModel,
    LLMRouter,
    get_available_models,
    get_model_for_task
)


class TestLLMProvider(unittest.TestCase):
    """Tests for the LLMProvider enum."""
    
    def test_provider_values(self):
        """Test that the provider enum has the expected values."""
        self.assertEqual(LLMProvider.OPENAI, "openai")
        self.assertEqual(LLMProvider.ANTHROPIC, "anthropic")
        self.assertEqual(LLMProvider.LOCAL, "local")


class TestLLMModel(unittest.TestCase):
    """Tests for the LLMModel class."""
    
    def test_model_creation(self):
        """Test creating a model instance."""
        model = LLMModel(
            name="test-model",
            provider=LLMProvider.OPENAI,
            context_size=4096,
            hardware="Test Hardware"
        )
        
        self.assertEqual(model.name, "test-model")
        self.assertEqual(model.provider, LLMProvider.OPENAI)
        self.assertEqual(model.context_size, 4096)
        self.assertEqual(model.hardware, "Test Hardware")
        self.assertTrue(model.available)
    
    def test_model_to_dict(self):
        """Test converting a model to a dictionary."""
        model = LLMModel(
            name="test-model",
            provider=LLMProvider.OPENAI,
            context_size=4096,
            hardware="Test Hardware",
            capabilities=["text", "vision"]
        )
        
        model_dict = model.to_dict()
        
        self.assertEqual(model_dict["name"], "test-model")
        self.assertEqual(model_dict["provider"], LLMProvider.OPENAI)
        self.assertEqual(model_dict["context_size"], 4096)
        self.assertEqual(model_dict["hardware"], "Test Hardware")
        self.assertEqual(model_dict["capabilities"], ["text", "vision"])
        self.assertTrue(model_dict["available"])


@pytest.mark.parametrize(
    "env_vars,expected_providers", [
        # No API keys, only local
        ({}, []),
        # Only OpenAI
        ({"OPENAI_API_KEY": "test-key"}, [LLMProvider.OPENAI]),
        # Only Anthropic
        ({"ANTHROPIC_API_KEY": "test-key"}, [LLMProvider.ANTHROPIC]),
        # Both OpenAI and Anthropic
        ({
            "OPENAI_API_KEY": "test-key",
            "ANTHROPIC_API_KEY": "test-key"
        }, [LLMProvider.OPENAI, LLMProvider.ANTHROPIC]),
    ]
)
def test_router_init_providers(env_vars, expected_providers):
    """Test initializing providers based on environment variables."""
    with patch.dict(os.environ, env_vars, clear=True):
        with patch('llamasearch_experimentalagents_product_growth.core.llm_router.LLMRouter._check_local_available', return_value=False):
            router = LLMRouter()
            assert set(router.providers) == set(expected_providers)


class TestLLMRouterMethods:
    """Tests for the LLMRouter class methods."""
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm_router.os.path.exists')
    @patch('importlib.import_module')
    def test_check_local_available(self, mock_import, mock_exists):
        """Test checking if local models are available."""
        mock_exists.return_value = True
        
        # Test MLX available
        with patch.dict(os.environ, {"LLM_LOCAL_MODEL_PATH": "/path/to/models"}):
            router = LLMRouter()
            mock_import.side_effect = lambda x: None if x != "mlx" else MagicMock()
            result = router._check_local_available()
            assert result is True
        
        # Test llama.cpp available but not MLX
        mock_import.side_effect = [ImportError(), None]
        with patch.dict(os.environ, {"LLM_LOCAL_MODEL_PATH": "/path/to/models"}):
            router = LLMRouter()
            result = router._check_local_available()
            assert result is True
        
        # Test neither available
        mock_import.side_effect = ImportError()
        with patch.dict(os.environ, {"LLM_LOCAL_MODEL_PATH": "/path/to/models"}):
            router = LLMRouter()
            result = router._check_local_available()
            assert result is False
    
    @patch('llamasearch_experimentalagents_product_growth.core.llm_router.LLMRouter._check_openai_available')
    def test_select_model(self, mock_check_openai):
        """Test selecting a model based on capabilities and preferences."""
        mock_check_openai.return_value = True
        
        with patch.object(LLMRouter, 'get_available_models') as mock_get_models:
            # Test models with different capabilities
            mock_get_models.return_value = [
                {
                    "name": "gpt-4",
                    "provider": LLMProvider.OPENAI,
                    "capabilities": ["text", "function_calling"],
                    "available": True
                },
                {
                    "name": "claude-3",
                    "provider": LLMProvider.ANTHROPIC,
                    "capabilities": ["text", "vision"],
                    "available": True
                }
            ]
            
            router = LLMRouter()
            
            # Test selecting model with specific capability
            model = router.select_model("Test task", required_capabilities=["function_calling"])
            assert model["name"] == "gpt-4"
            
            # Test selecting model with preferred provider
            model = router.select_model("Test task", preferred_provider=LLMProvider.ANTHROPIC)
            assert model["name"] == "claude-3"
            
            # Test no matching models
            model = router.select_model("Test task", required_capabilities=["unknown_capability"])
            assert model is None


def test_get_available_models():
    """Test the get_available_models function."""
    with patch('llamasearch_experimentalagents_product_growth.core.llm_router.LLMRouter.get_available_models') as mock_get_models:
        mock_get_models.return_value = [{"name": "test-model"}]
        models = get_available_models()
        assert models == [{"name": "test-model"}]


def test_get_model_for_task():
    """Test the get_model_for_task function."""
    with patch('llamasearch_experimentalagents_product_growth.core.llm_router.LLMRouter.select_model') as mock_select:
        mock_select.return_value = {"name": "test-model"}
        model = get_model_for_task("Test task", preferred_provider="openai")
        assert model == {"name": "test-model"}
        mock_select.assert_called_once() 