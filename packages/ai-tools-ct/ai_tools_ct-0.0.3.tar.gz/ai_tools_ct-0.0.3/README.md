
# AI TOOLS CT

  
This repo is a collection of classes that will help users with ai tasks regarding the use of OpenAi for data generation. 

## Installation
``` $ pip install ai_tools_ct```

## Usage
At the moment, you will need an **openai api key** which you can find [here](https://platform.openai.com/docs/quickstart?api-mode=responses). 

```
from ai_tools_ct.gpt import Gpt
from ai_tools_ct.data_generator import DataGenerator as Dg

gpt = Gpt(api_key=your_api_key)
dg = Dg(gpt)

# for single prompt generation 
dg.single_generation(prompt="give me 10 random words")

# or do a bulk generation with multiple prompts
prompts = ["give me a random word", "give me a random number"]
targets = ["word", "number"]
system_prompts = ["you are a word generator", "you are a number generator"]
dg.bulk_generation(prompts = prompts, targets=targets, system_prompts=system_prompts)

# access results either through python list of pandas df
dg.generation_results
dg.df_generation_results
```