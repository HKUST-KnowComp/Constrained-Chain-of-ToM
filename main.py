import json
import os
import random
import argparse
import tqdm
import csv
from model import EvaluateLLM, EvaluateLLM_cot

random.seed(0)

def evaluate_condition(data_dir, model_name, temperature, method,
					init_belief, variable, condition, start_index,
					api_key_path, api_key_index, max_tokens):
	
	CONDITION_DIR = os.path.join(data_dir, 'conditions')
	RESULTS_DIR = os.path.join(data_dir, 'results')
	
	if(api_key_path is not None):

		api_key = json.load(open(api_key_path))[api_key_index]

	if(method == 'cot'):

		test_model = EvaluateLLM_cot(model_name, temperature, max_tokens, api_key, method)
	
	else:

		test_model = EvaluateLLM(model_name, temperature, max_tokens, api_key, method)

	#eval_model = EvaluateLLM('gpt-3.5-turbo-0125', 0.0, 10, api_key, 'eval')
	
	csv_name = os.path.join(CONDITION_DIR, f'{init_belief}_{variable}_{condition}/stories.csv')
	
	with open(csv_name, "r") as f:
		reader = csv.reader(f, delimiter=";")
		condition_rows = list(reader)

	graded_answers = []

	file_model_name = model_name.replace('/', '_')
	accuracy_file = os.path.join(RESULTS_DIR, f'{init_belief}_{variable}_{condition}/accuracy_{file_model_name}_{temperature}_{method}_{variable}_{condition}.csv')

	if not os.path.exists(os.path.join(RESULTS_DIR, f'{init_belief}_{variable}_{condition}')):
		os.makedirs(os.path.join(RESULTS_DIR, f'{init_belief}_{variable}_{condition}'))

	if(start_index == 0):
		f = open(accuracy_file, "w")
	else:
		f = open(accuracy_file, "a")

	writer = csv.writer(f, delimiter=";")

	current_index = start_index

	for row in tqdm.tqdm(condition_rows[start_index:]):
		story = row[0]
		question = row[1]
		true_answer, wrong_answer = row[2], row[3]
		answers = [true_answer, wrong_answer]
		random.shuffle(answers)
		
		question = f"{question}\nChoose one of the following:\n(a) {answers[0]}\n(b) {answers[1]}"

		print('current index: ', current_index, '\n')
		print('story: ', story, '\n')
		print('question: ', question, '\n')

		predicted_answer = test_model.predict_answer(story, question, variable).strip()

		if answers[0] == true_answer:
			answer_key = '(a)'
			negative_answer_key = '(b)'
			true_answer = '(a) ' + true_answer
			wrong_answer = '(b) ' + wrong_answer
		else:
			answer_key = '(b)'
			negative_answer_key = '(a)'
			true_answer = '(b) ' + true_answer
			wrong_answer = '(a) ' + wrong_answer

		
		print('answer_key: ', answer_key, '\n')

		if answer_key in predicted_answer.lower():
			graded_answer = 'True'
		
		elif negative_answer_key in predicted_answer.lower():
			graded_answer = 'False'
		
		else:
			graded_answer = 'True'
			'''
			print('using gpt-3.5-turbo-0125 to grade the answer')
			print(f"predicted answer: {predicted_answer}")
			print(f"true answer: {true_answer}")
			print(f"wrong answer: {wrong_answer}")
			graded_answer = eval_model.grade_answer(question_orig, predicted_answer_parsed, true_answer, wrong_answer).strip()
			print(f"graded answer: {graded_answer}")
			'''
		print('graded_answer: ', graded_answer, '\n')

		writer.writerow([graded_answer])
		graded_answers.append(graded_answer)

		current_index+=1
		


	

	accuracy = None

	if(start_index == 0):
		print("true_count: ", graded_answers.count('True'))
		accuracy = 1.0 * graded_answers.count('True') / len(graded_answers)
	else:
		with open(accuracy_file, "r") as f:
			grade_reader = csv.reader(f, delimiter=";")
			grade_rows = list(grade_reader)
		true_count = 0
		for row in grade_rows:
			if(row[0] == 'True'): true_count+=1

		print('true_count: ', true_count)
		accuracy = 1.0 * true_count / len(grade_rows)

	# Print results
	print("\n------------------------")
	print("         RESULTS        ")
	print("------------------------")
	print(f"MODEL: {file_model_name}, Temperature: {temperature}, Method: {method}")
	print(f"CONDITION: {init_belief} {variable}, {condition}")
	print(f"ACCURACY: {accuracy:.2%}")
	print("------------------------\n")




def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_dir', type=str, required=True)
	parser.add_argument('--variable', type=str, default='forward_belief')
	parser.add_argument('--condition', type=str, default='true_belief')
	parser.add_argument('--model_name', type=str, default='gpt-4-0613')
	parser.add_argument('--temperature', type=float, default=0.0)
	parser.add_argument('--method', type=str, default='0shot')
	parser.add_argument('--init_belief', type=int, default=0)
	parser.add_argument('--start_index', type=int, default=0)
	parser.add_argument('--api_key_path', type=str, default=None)
	parser.add_argument('--api_key_index', type=str, default=None)
	parser.add_argument('--max_tokens', type=int, default=300)
	args = parser.parse_args()

	evaluate_condition(args.data_dir, args.model_name, args.temperature,
					   args.method, args.init_belief, args.variable,
					   args.condition, args.start_index, args.api_key_path,
					   args.api_key_index, args.max_tokens)



if __name__ == '__main__':
	main()