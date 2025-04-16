from openai import OpenAI
from openai.types.chat import ChatCompletion

class Gpt:
    """
    A wrapper class for interacting with OpenAI's GPT models via the OpenAI SDK.

    Provides convenient access to chat completions, along with model configuration options.
    """

    def __init__(self, api_key: str, temperature: float = 0.7, model: str = "gpt-4o-mini", system_prompt: str = ""):
        """
        Initializes a GPT client for OpenAI chat completions.

        Args:
            api_key (str): The API key used to authenticate with the OpenAI API.
            temperature (float): Sampling temperature (controls randomness). Must be >= 0.
            model (str): The model ID to use (e.g., "gpt-4", "gpt-4o-mini").
            system_prompt (str): The system message used to guide the assistant's behavior.
        """
        self.client = self._create_client(api_key)
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature

    def _create_client(self, api_key: str) -> OpenAI:
        """
        Instantiates the OpenAI client with the provided API key.

        Args:
            api_key (str): OpenAI API key.

        Returns:
            OpenAI: An authenticated OpenAI client instance.
        """
        return OpenAI(api_key=api_key)

    @property
    def model(self) -> str:
        """
        Returns:
            str: The current model in use.
        """
        return self._model

    @model.setter
    def model(self, value: str):
        """
        Validates and sets the GPT model to use.

        Args:
            value (str): The model ID.

        Raises:
            ValueError: If the model is not a string or not found in available models.
        """
        if not isinstance(value, str):
            raise ValueError(f"Model must be a string, got: {type(value)}")
        if value not in [model.id for model in self.client.models.list()]:
            raise ValueError(f"Model '{value}' is not an available model.")
        self._model = value

    @property
    def temperature(self) -> float:
        """
        Returns:
            float: The current temperature setting.
        """
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        """
        Validates and sets the sampling temperature.

        Args:
            value (float): A float >= 0 indicating randomness of completions.

        Raises:
            ValueError: If temperature is not a float or is negative.
        """
        if not isinstance(value, float):
            raise ValueError(f"Temperature must be a float, got: {type(value)}")
        if value < 0:
            raise ValueError(f"Temperature must be greater than or equal to 0, got: {value}")
        self._temperature = value

    @property
    def system_prompt(self) -> str:
        """
        Returns:
            str: The system prompt used for GPT chat completions.
        """
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, value: str):
        """
        Sets the system prompt to guide assistant behavior.

        Args:
            value (str): The system message.

        Raises:
            ValueError: If the input is not a string.
        """
        if not isinstance(value, str):
            raise ValueError(f"System prompt must be a string, got: {type(value)}")
        self._system_prompt = value

    def run(self, prompt: str) -> ChatCompletion:
        """
        Sends a user prompt to the GPT model and retrieves a chat completion.

        Args:
            prompt (str): The user input prompt.

        Returns:
            ChatCompletion: The full response object from OpenAI.
        """
        return self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
