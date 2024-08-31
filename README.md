# Constrained-Chain-of-ToM
Code for PRICAI 2024 paper *Constrained Reasoning Chains for Enhancing Theory-of-Mind in Large Language Models*.

# Library Requirements: 
1. Python 3.10
2. openai 1.12
3. tqdm 4.64

# Dataset:
BigToM: https://github.com/cicl-stanford/procedural-evals-tom
We use the script generate_conditions.py from the above repo to pre-process the BigToM dataset, and the processed dataset should be saved in data/conditions/ under the main directory, whereas the code should be in src/ under the main directory.

# Usage:
Run the following command for testing:
```
python -u main.py \
--data_dir ../data \
--variable [variable] \
--condition [condition] \
--model_name [llm_name] \
--method [prompting method] 
```
Here is an example:
```
python -u main.py \
--data_dir ../data \
--variable forward_belief \
--condition true_belief \
--model_name gpt-3.5-turbo-0125 \
--method 0shot
```
And here is an example for computing the score of the tested llm and prompting method:
'''
python -u compute_final_score.py \
--data_dir ../data \
--variable forward_belief \
--model_name gpt-3.5-turbo-0125 \
--method 0shot
'''

Notice that *0shot* corresponds to the prompting method proposed by us.
See the comments within the soure code for more details about using the code.


