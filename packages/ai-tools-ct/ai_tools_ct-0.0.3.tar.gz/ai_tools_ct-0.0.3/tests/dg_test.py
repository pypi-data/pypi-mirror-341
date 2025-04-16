import pytest
import pandas as pd
from unittest.mock import MagicMock
from src.ai_tools_ct.data_generator import DataGenerator 
from src.ai_tools_ct.gpt import Gpt 
from unittest.mock import patch


@pytest.fixture
def mock_gpt():
    """Fixture to mock the Gpt instance and its response."""
    gpt_mock = MagicMock(spec=Gpt)
    gpt_mock.run.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Generated response"))]
    )
    gpt_mock.system_prompt = "default system prompt"
    return gpt_mock


class TestDataGenerator:

    def test_initialization(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        assert isinstance(gen.gpt, Gpt)
        assert gen.generation_results == []

    def test_single_generation_appends_result(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        gen.single_generation(prompt="Say something", target="Greeting", system_prompt="Be nice")

        results = gen.generation_results
        assert len(results) == 1
        assert results[0]["GPT prompt"] == "Say something"
        assert results[0]["Result"] == "Generated response"
        assert results[0]["Target (optional)"] == "Greeting"
        mock_gpt.run.assert_called_once_with("Say something")
        assert gen.df_generation_results.shape[0] == 1

    def test_bulk_generation_basic(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        prompts = ["prompt 1", "prompt 2"]
        targets = ["target 1", "target 2"]

        gen.bulk_generation(prompts=prompts, targets=targets)

        results = gen.generation_results
        assert len(results) == 2
        assert results[0]["GPT prompt"] == "prompt 1"
        assert results[1]["Target (optional)"] == "target 2"

    def test_bulk_generation_with_system_prompts(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        prompts = ["what is AI?", "explain gravity"]
        system_prompts = ["Talk like a teacher", "Talk like a scientist"]

        gen.bulk_generation(prompts=prompts, system_prompts=system_prompts)

        assert mock_gpt.system_prompt == "Talk like a scientist"
        assert gen.df_generation_results.shape[0] == 2

    def test_bulk_generation_invalid_prompts_type(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        with pytest.raises(ValueError, match="prompts must be a list of strings"):
            gen.bulk_generation(prompts="not a list")

    def test_bulk_generation_mismatched_targets(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        with pytest.raises(ValueError, match="targets must match length of prompts"):
            gen.bulk_generation(prompts=["a", "b"], targets=["only one"])

    def test_bulk_generation_mismatched_system_prompts(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        with pytest.raises(ValueError, match="system_prompts must match length of prompts"):
            gen.bulk_generation(prompts=["a", "b"], system_prompts=["only one"])
    
    def test_generation_results_returns_copy(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)

        # Generate one result
        gen.single_generation(prompt="Hello", target="Greeting")

        results = gen.generation_results
        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0]["GPT prompt"] == "Hello"

        # Modify the returned list – it should not affect the original
        results.append({"GPT prompt": "Fake", "Result": "Bad", "Target (optional)": "Oops"})
        assert len(results) == 2
        assert len(gen.generation_results) == 1  # Still 1 internally

    def test_df_generation_results_format(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)

        gen.single_generation(prompt="What is AI?", target="Definition")
        df = gen.df_generation_results

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert set(df.columns) == {"GPT prompt", "Result", "Target (optional)"}
        assert df.iloc[0]["GPT prompt"] == "What is AI?"

    def test_bulk_generation_uses_tqdm(self, mock_gpt):
        prompts = ["one", "two", "three"]
        with patch("src.ai_tools_ct.data_generator.tqdm") as mock_tqdm:
            mock_tqdm.side_effect = lambda x, **kwargs: x  # Just return the original iterable
            gen = DataGenerator(gpt=mock_gpt)
            gen.bulk_generation(prompts)

            mock_tqdm.assert_called_once_with(prompts, desc="Generating with GPT")