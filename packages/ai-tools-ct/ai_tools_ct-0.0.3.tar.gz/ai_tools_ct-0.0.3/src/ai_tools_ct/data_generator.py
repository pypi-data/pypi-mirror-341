# class to be able to generate data using openai
from .gpt import Gpt
import pandas as pd
from tqdm import tqdm


class DataGenerator:
    """
    A class to handle structured data generation using a GPT model backend.
    
    Attributes:
        gpt (Gpt): An instance of the Gpt class, used to generate text completions.
    """
    def __init__(self, gpt: Gpt):
        self.gpt = gpt
        self._generation_results = []

    @property
    def generation_results(self) -> list:
        """
        Returns a copy of the internal generation results list.

        Returns:
            list: A list of dictionaries containing prompt, result, and optional target.
        """
        return self._generation_results.copy()

    @property
    def df_generation_results(self) -> pd.DataFrame:
        """
        Returns the generation results as a pandas DataFrame.

        Returns:
            pd.DataFrame: Tabular format of all generated results.
        """
        return pd.DataFrame.from_records(self.generation_results)

    def single_generation(self, prompt: str, target: str = "", system_prompt: str = ""):
        """
        Generates a single response from the GPT model and stores the result.

        Args:
            prompt (str): The user prompt to send to the GPT model.
            target (str, optional): An optional expected target or label for reference.
            system_prompt (str, optional): Optional system prompt override for this generation.
        """
        if system_prompt:
            self.gpt.system_prompt = system_prompt

        response = self.gpt.run(prompt)

        self._generation_results.append({
            "GPT prompt": prompt,
            "Result": response.choices[0].message.content,
            "Target (optional)": target,
        })

    def bulk_generation(self, prompts: list[str], targets: list[str] = None, system_prompts: list[str] = None):
        """
        Runs multiple prompt generations through looping through single generation, will store all results in generation_results.

        Args:
            prompts (list[str]): A list of user prompts to process.
            targets (list[str], optional): Optional list of targets corresponding to each prompt.
            system_prompts (list[str], optional): Optional list of system prompts per prompt.

        Raises:
            ValueError: If any input list is not valid or mismatched in length.
        """
        if not isinstance(prompts, list) or not all(isinstance(p, str) for p in prompts):
            raise ValueError("prompts must be a list of strings.")
        if targets and len(targets) != len(prompts):
            raise ValueError("targets must match length of prompts.")
        if system_prompts and len(system_prompts) != len(prompts):
            raise ValueError("system_prompts must match length of prompts.")

        for i, prompt in enumerate(tqdm(prompts, desc="Generating with GPT")):
            target = targets[i] if targets else ""
            sys_prompt = system_prompts[i] if system_prompts else self.gpt.system_prompt
            self.single_generation(prompt=prompt, target=target, system_prompt=sys_prompt)







    

