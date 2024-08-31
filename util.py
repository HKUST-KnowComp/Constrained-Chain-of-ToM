import sys

constraints = {
	"causal_event_definitional_constraint": "Causal event is the event that changes the state of the environment.",
	"action_definitional_constraint_1": "Action of {personX} is what {personX} does after the causal event.",
    "action_definitional_constraint_2": "Action of {personX} is what {personX} will do after the causal event.",
	"desire_definitional_constraint":"Desire of {personX} is what {personX} wants.",
	"belief_definitional_constraint": "Belief of {personX} is what {personX} believes about the state of the environment.",
	"action_dependency_constraint": "Action of {personX} is determined by the belief of {personX} and the desire of {personX}.",
	"percept_definitional_constraint": "Percept of {personX} is whether or not {personX} perceives the causal event.",
	"belief_dependency_constraint": "Belief of {personX} is determined by the percept of {personX}."
}

percept_instruction = "Answer the question based on the context and the constraints. Reason step by step before answering in 'Thought: Let's think step by step'. Write your final answer as 'Answer: <answer>'. Do not say there is not enough information."

percept_prompt = """Story: {story}
Question: What is the percept of {personX}?
Constraints:
1. {percept_definitional_constraint}
2. {causal_event_definitional_constraint}"""


belief_instruction = "Answer the question based on the context, the constraints, and the theory of mind dimensions. Reason step by step before answering in 'Thought: Let's think step by step'. Write your final answer as 'Answer: <answer>'. Do not say there is not enough information."
belief_prompt = """Story: {story}
Question: What is the belief of {personX}?
Constraints:
1. {belief_definitional_constraint}
2. {belief_dependency_constraint}
3. {causal_event_definitional_constraint}
Theory of mind dimension:
1. ###Percept of {personX}###: {percept_response}"""


desire_instruction = "Answer the question based on the context and the constraints. Reason step by step before answering in 'Thought: Let's think step by step'. Write your final answer as 'Answer: <answer>'. Do not say there is not enough information."
desire_prompt = """Story: {story}
Question: What is the desire of {personX}?
Constraints:
1. {desire_definitional_constraint}"""

action_instruction_1 = "Answer the question based on the context and the constraints. Reason step by step before answering in 'Thought: Let's think step by step'. Write your final answer as either 'Answer: Yes.' or 'Answer: No.'. Do not say that there is not enough information."
action_prompt_1 = """Story: {story}
Question: Is the action of {personX} explicitly stated in the context?
Constraints:
1. {action_definitional_constraint_1}
2. {causal_event_definitional_constraint}"""

action_instruction_2 = "Answer the question based on the context and the constraints. Reason step by step before answering in 'Thought: Let's think step by step'. Write your final answer as 'Answer: <answer>'."
action_prompt_2 = """Story: {story}
Question: What is the action of {personX}?
Constraints:
1. {action_definitional_constraint_1}
2. {causal_event_definitional_constraint}"""


tom_task_instruction = "Answer the question based on the context, the constraints, and the theory of mind dimensions. Reason step by step before answering in 'Thought: Let's think step by step'. Write your final answer as 'Answer: (<option>) <answer>'. Always pick an option, do not say none of the above or that there is not enough information."

forward_action_task_prompt = """Story: {story}
Question: {question}
Constraints:
1. Action of {personX} is the answer to the question.
2. {action_definitional_constraint_2}
3. {causal_event_definitional_constraint}
4. {action_dependency_constraint}
Theory of mind dimensions:
1. ###Belief of {personX}###: {belief_response}
2. Desire of {personX}: {desire_response}"""

backward_belief_task_prompt = """Story: {story}
Question: {question}
Constraints:
1. Belief of {personX} is the answer to the question.
2. {belief_definitional_constraint}
3. {action_dependency_constraint}
Theory of mind dimensions:
1. Desire of {personX}: {desire_response}
2. ###Action of {personX}###: {action_response}"""

forward_belief_task_prompt = """Story: {story}
Question: {question}
Constraints:
1. Belief of {personX} is the answer to the question.
2. {belief_definitional_constraint}
3. {belief_dependency_constraint}
4. {causal_event_definitional_constraint}
Theory of mind dimensions:
1. ###Percept of {personX}###: {percept_response}"""


grade_prompt = '''Question: {query}
True answer: {true_answer}
False answer: {wrong_answer}
Predicted answer: {predicted_answer}
Is the true answer more similar to the predicted answer than the false answer is?'''

grade_instruction = '''You are given a question, the true answer, the false answer, and the predicted answer.
You are asked to score the predicted answer as either True or False based on its similarity to the true answer and the false answer.
We only care about semantic similarity, ignore whitespace, typos, punctuation, etc. and focus only on the meaning of the answer.
Mark as False if the answer says lack of information or None of the above.
Mark as False if the answer has irrelevant information.
If a single character is given, match it to the true answer or the false answer and mark as True or False accordingly.
Write your answer as either 'Answer: True' or 'Answer: False'.'''



cot_instruction = "Answer the questions based on the context. Reason step by step before answering in 'Thought: Let's think step by step'. Write your final answer as 'Answer: (<option>) <answer>'. Always pick an option, do not say none of the above or that there is not enough information."



def parse_chat_response(response):
	answer_idx = response.find('Answer:')
	return response[answer_idx+7:].strip()

def find_personX(question, task_type):

	personX = None

	if(task_type == 'forward_action'):
		personX= question.split()[2]

	elif(task_type == 'forward_belief' or \
		task_type == 'backward_belief'):
		personX = question.split()[1]

	else:
		print('Unsupported task type!')
		sys.exit(1)


	return personX


