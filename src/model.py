import util
import openai
import time

class EvaluateLLM():

	def __init__(self, model_name, temperature, max_tokens, api_key, method):
		
		self.model_name = model_name
		self.llm = None
		if(self.model_name.startswith("gpt-")):
			self.llm = openai.OpenAI(base_url= "https://api.zhiyunai168.com/v1",
				api_key = api_key)

		self.temperature = temperature
		self.method = method
		self.max_tokens = max_tokens


	def generate(self, model_name, prompt, system_message=None):
		
		response = None

		if(model_name.startswith("gpt-")):

			while True:
				try:
					response = self.llm.chat.completions.create(
						messages=[
							{
								"role": "system",
								"content": system_message
							},

							{
								"role": "user",
								"content": prompt
							}
						],
						model=model_name, temperature=self.temperature,
						max_tokens=self.max_tokens, n=1
					)
					break

				except (openai.APIError, openai.RateLimitError) as e: 
					print("Error: {}".format(e))
					time.sleep(2)
					continue

		
		response = response.choices[0].message.content.strip()
		return response




	def predict_answer(self, story, question, task_type):

		predicted_answer = None

		#find personX
		personX = util.find_personX(question, task_type)

		if(task_type == 'forward_belief'):
			#prompt percept

			percept_message = util.percept_prompt.format(story=story, personX=personX,
									percept_definitional_constraint=util.constraints["percept_definitional_constraint"].format(personX=personX),
									causal_event_definitional_constraint=util.constraints["causal_event_definitional_constraint"])
			
			percept_response = self.generate(model_name=self.model_name,
									prompt=percept_message,
									system_message=util.percept_instruction)

			print('percept_response: \n')
			print(percept_response)
			print('\n')

			percept_response = util.parse_chat_response(percept_response)

			print('parsed percept_response: \n')
			print(percept_response)
			print('\n')

			#answer forward belief question

			forward_belief_task_message = util.forward_belief_task_prompt.format(story=story, personX=personX,
										question=question, belief_definitional_constraint=util.constraints['belief_definitional_constraint'].format(personX=personX),
										belief_dependency_constraint=util.constraints['belief_dependency_constraint'].format(personX=personX),
										causal_event_definitional_constraint=util.constraints["causal_event_definitional_constraint"],
										percept_response=percept_response)

			predicted_answer = self.generate(model_name=self.model_name,
									prompt=forward_belief_task_message,
									system_message=util.tom_task_instruction)

			print('predicted_answer: \n')
			print(predicted_answer)
			print('\n')

			predicted_answer = util.parse_chat_response(predicted_answer)

			print('parsed predicted_answer: \n')
			print(predicted_answer)
			print('\n')

		elif(task_type == 'forward_action'):
			#prompt percept
			percept_message = util.percept_prompt.format(story=story, personX=personX,
									percept_definitional_constraint=util.constraints["percept_definitional_constraint"].format(personX=personX),
									causal_event_definitional_constraint=util.constraints["causal_event_definitional_constraint"])
			
			percept_response = self.generate(model_name=self.model_name,
									prompt=percept_message,
									system_message=util.percept_instruction)

			print('percept_response: \n')
			print(percept_response)
			print('\n')

			percept_response = util.parse_chat_response(percept_response)

			print('parsed percept_response: \n')
			print(percept_response)
			print('\n')

			#prompt belief
			belief_message = util.belief_prompt.format(story=story,personX=personX, belief_definitional_constraint=\
							util.constraints["belief_definitional_constraint"].format(personX=personX),
							belief_dependency_constraint=util.constraints['belief_dependency_constraint'].format(personX=personX),
							causal_event_definitional_constraint=util.constraints["causal_event_definitional_constraint"],
							percept_response=percept_response)

			belief_response = self.generate(model_name=self.model_name,
									prompt=belief_message,
									system_message=util.belief_instruction)

			print('belief_response: \n')
			print(belief_response)
			print('\n')

			belief_response = util.parse_chat_response(belief_response)

			print('parsed belief_response: \n')
			print(belief_response)
			print('\n')
			
			#prompt desire
			desire_message = util.desire_prompt.format(story=story, personX=personX,
					desire_definitional_constraint=util.constraints["desire_definitional_constraint"].format(personX=personX))

			desire_response = self.generate(model_name=self.model_name,
									prompt=desire_message,
									system_message=util.desire_instruction)

			print('desire_response: \n')
			print(desire_response)
			print('\n')

			desire_response = util.parse_chat_response(desire_response)

			print('parsed desire_response: \n')
			print(desire_response)
			print('\n')

			#answer forward action question

			forward_action_task_message = util.forward_action_task_prompt.format(story=story, personX=personX,
						question=question, action_definitional_constraint_2=util.constraints['action_definitional_constraint_2'].format(personX=personX),
						causal_event_definitional_constraint=util.constraints['causal_event_definitional_constraint'],                                                     
						belief_response=belief_response, desire_response=desire_response,
						action_dependency_constraint=util.constraints['action_dependency_constraint'].format(personX=personX))

			predicted_answer = self.generate(model_name=self.model_name,
									prompt=forward_action_task_message,
									system_message=util.tom_task_instruction)

			print('predicted_answer: \n')
			print(predicted_answer)
			print('\n')

			predicted_answer = util.parse_chat_response(predicted_answer)

			print('parsed predicted_answer: \n')
			print(predicted_answer)
			print('\n')

		elif(task_type == 'backward_belief'):
			#prompt desire
			desire_message = util.desire_prompt.format(story=story, personX=personX,
					desire_definitional_constraint=util.constraints["desire_definitional_constraint"].format(personX=personX))

			desire_response = self.generate(model_name=self.model_name,
									prompt=desire_message,
									system_message=util.desire_instruction)
			
			print('desire_response: \n')
			print(desire_response)
			print('\n')

			desire_response = util.parse_chat_response(desire_response)

			print('parsed desire_response: \n')
			print(desire_response)
			print('\n')

			#prompt action
			action_message = util.action_prompt_2.format(story=story, personX=personX,
							action_definitional_constraint_1=util.constraints["action_definitional_constraint_1"].format(personX=personX),
							causal_event_definitional_constraint=util.constraints["causal_event_definitional_constraint"])


			action_response = self.generate(model_name=self.model_name,
									prompt=action_message,
									system_message=util.action_instruction_2)

			print('action_response: \n')
			print(action_response)
			print('\n')

			action_response = util.parse_chat_response(action_response)

			print('parsed action_response: \n')
			print(action_response)
			print('\n')

			#answer backward belief question
			backward_belief_task_message = util.backward_belief_task_prompt.format(story=story, personX=personX,
										question=question, belief_definitional_constraint=\
										util.constraints['belief_definitional_constraint'].format(personX=personX),
										desire_response=desire_response, action_response=action_response,
										action_dependency_constraint=util.constraints['action_dependency_constraint'].format(personX=personX))

			predicted_answer = self.generate(model_name=self.model_name,
									prompt=backward_belief_task_message,
									system_message=util.tom_task_instruction)
			
			print('predicted_answer: \n')
			print(predicted_answer)
			print('\n')

			predicted_answer = util.parse_chat_response(predicted_answer)

			print('parsed predicted_answer: \n')
			print(predicted_answer)
			print('\n')

		else:
			print('Unsupported task type!')
			sys.exit(1)


		return predicted_answer

	def grade_answer(self, query, predicted_answer, true_answer, wrong_answer):
		
		prompt = util.grade_prompt.format(query=query, wrong_answer=wrong_answer, predicted_answer=predicted_answer, true_answer=true_answer)
		
		response = self.generate(model_name=self.model_name, 
			prompt=prompt, system_message=util.grade_instruction)

		response = util.parse_chat_response(response)
		if(response[-1] == '.'): response = response[:-1]
		
		return response

class EvaluateLLM_cot():

	def __init__(self, model_name, temperature, max_tokens, api_key, method):
		
		self.model_name = model_name
		self.llm = None
		if(self.model_name.startswith("gpt-")):
			self.llm = openai.OpenAI(base_url= "https://api.zhiyungpt.com/v1",
				api_key = api_key)

		self.temperature = temperature
		self.method = method
		self.max_tokens = max_tokens


	def generate(self, model_name, prompt, system_message=None):
		
		response = None

		if(model_name.startswith("gpt-")):

			while True:
				try:
					response = self.llm.chat.completions.create(
						messages=[
							{
								"role": "system",
								"content": system_message
							},

							{
								"role": "user",
								"content": prompt
							}
						],
						model=model_name, temperature=self.temperature,
						max_tokens=self.max_tokens, n=1
					)
					break

				except (openai.APIError, openai.RateLimitError) as e: 
					print("Error: {}".format(e))
					time.sleep(2)
					continue

		
		response = response.choices[0].message.content.strip()
		return response




	def predict_answer(self, story, question, task_type):

		predicted_answer = None

		prompt = """Story: {story}\nQuestion: {question}""".format(
			story=story, question=question)


		predicted_answer = self.generate(model_name=self.model_name,
									prompt=prompt,
									system_message=util.cot_instruction)

		print('predicted_answer: \n')
		print(predicted_answer)
		print('\n')

		predicted_answer = util.parse_chat_response(predicted_answer)

		print('parsed predicted_answer: \n')
		print(predicted_answer)
		print('\n')
		


		return predicted_answer
