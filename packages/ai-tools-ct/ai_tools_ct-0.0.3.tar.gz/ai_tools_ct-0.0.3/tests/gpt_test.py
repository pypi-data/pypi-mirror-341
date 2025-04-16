import pytest
from unittest.mock import patch, MagicMock
from src.ai_tools_ct.gpt import Gpt  


@pytest.fixture
def mock_openai_client():
    with patch("src.ai_tools_ct.gpt.OpenAI") as MockOpenAI:  # Adjust the path
        mock_client = MagicMock()
        # Set up available model list
        mock_client.models.list.return_value = [MagicMock(id="gpt-4o-mini"), MagicMock(id="gpt-3.5-turbo")]
        MockOpenAI.return_value = mock_client
        yield mock_client


class TestGpt:

    def test_initialization_valid(self, mock_openai_client):
        gpt = Gpt(api_key="test-key", temperature=0.5, model="gpt-4o-mini", system_prompt="Hello!")
        assert gpt.model == "gpt-4o-mini"
        assert gpt.temperature == 0.5
        assert gpt.system_prompt == "Hello!"

    def test_invalid_model(self, mock_openai_client):
        with pytest.raises(ValueError, match="is not an available model"):
            Gpt(api_key="test-key", model="invalid-model")

    def test_invalid_temperature_type(self, mock_openai_client):
        with pytest.raises(ValueError, match="Temperature must be a float"):
            Gpt(api_key="test-key", temperature="not-a-float", model="gpt-4o-mini")

    def test_negative_temperature(self, mock_openai_client):
        with pytest.raises(ValueError, match="greater than or equal to 0"):
            Gpt(api_key="test-key", temperature=-1.0, model="gpt-4o-mini")

    def test_invalid_system_prompt_type(self, mock_openai_client):
        gpt = Gpt(api_key="test-key", model="gpt-4o-mini")
        with pytest.raises(ValueError, match="System prompt must be a string"):
            gpt.system_prompt = 1234

    def test_run_chat_completion(self, mock_openai_client):
        # Mock the chat completion response
        mock_completion = MagicMock()
        mock_openai_client.chat.completions.create.return_value = mock_completion

        gpt = Gpt(api_key="test-key", model="gpt-4o-mini", system_prompt="Hello")
        response = gpt.run("Tell me a joke.")
        mock_openai_client.chat.completions.create.assert_called_once()
        assert response == mock_completion