import csv
import argparse
import os


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_dir', type=str, required=True)
	parser.add_argument('--variable', type=str, default='forward_belief')
	parser.add_argument('--model_name', type=str, default='gpt-4-0613')
	parser.add_argument('--temperature', type=float, default=0.0)
	parser.add_argument('--method', type=str, default='0shot')
	parser.add_argument('--init_belief', type=int, default=0)
	args = parser.parse_args()

	CONDITION_DIR = os.path.join(args.data_dir, 'conditions')
	RESULTS_DIR = os.path.join(args.data_dir, 'results')
	init_belief = args.init_belief
	variable = args.variable
	file_model_name = args.model_name.replace('/', '_')
	temperature = args.temperature
	method = args.method

	
	tb_grade_rows = None
	fb_grade_rows = None

	condition = 'true_belief'
	accuracy_file = os.path.join(RESULTS_DIR, f'{init_belief}_{variable}_{condition}/accuracy_{file_model_name}_{temperature}_{method}_{variable}_{condition}.csv')

	with open(accuracy_file, "r") as f_tb:
		reader = csv.reader(f_tb, delimiter=";")
		tb_grade_rows = list(reader)


	condition = 'false_belief'
	accuracy_file = os.path.join(RESULTS_DIR, f'{init_belief}_{variable}_{condition}/accuracy_{file_model_name}_{temperature}_{method}_{variable}_{condition}.csv')

	with open(accuracy_file, "r") as f_fb:
		reader = csv.reader(f_fb, delimiter=";")
		fb_grade_rows = list(reader)


	true_count = 0 

	for tb_row, fb_row in zip(tb_grade_rows, fb_grade_rows):
		if(tb_row[0] == 'True' and fb_row[0] == 'True'):
			true_count+=1
		

	accuracy = true_count / len(fb_grade_rows)

	print('true count: ', true_count)
	print(f"ACCURACY: {accuracy:.2%}")




	





if __name__ == '__main__':
	main()