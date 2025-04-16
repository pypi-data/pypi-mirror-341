
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

## Dev install
Clone this repo in the standard way.

Requirements are kept with the ```pyproject.toml``` file rather than the standard requirements.txt. So to install all packages need for dev you can:
```
$ python -m venv venv
$ pip install -e .[dev]
```
This will install all packages needed to run the modules within ```src/ai_tools_ct/``` and all of the necessary packages to run unittests, push packages to pypi and more. 

## Code changes
When updating and creating new features please remeber to do the following:
- Add packages needed to the necessary dependencies. If the user needs it to run the package, add to ```pyproject.toml``` in the **dependencies** list. If needed for development, add to again ```pyproject.toml``` in the **[project.optional-dependencies]** list.
- Try to work in a TDD manor meaning **write tests for your code before development!**
- Run ```$ pytest -v``` before making any commits to ensure 0 errors are pushed to prod
## Pushing changes to PyPI
At the moment, this is done in command line within the **master branch** (will try and create an automated system within gitlab todo this).

1. Make sure that the package version is incremented within the ```pyproject.toml``` file. 
2. Running ```$ python -m build```. This will create new files in the ```dist/``` folder with the new version of the package.
3. ```$ python python -m twine upload dist/*``` running this will push to pypi
