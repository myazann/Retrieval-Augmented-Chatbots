from RAG.utils import strip_all

class Prompter():

    def __init__(self):

        self.prompt_dict = {
            "condense": self.condense_q_prompt(),
            "qa": self.qa_prompt(),
            "eval_qa": self.eval_qa_prompt(),
            "multi_query": self.multi_query_prompt(),
            "memory_summary": self.memory_summary(),
            "csv": self.csv_prompt()
        }

    def stripped_prompts(self, prompt):
        return strip_all(prompt)
    
    def eval_qa_prompt(self):
        return self.stripped_prompts("""Your job is to evaluate an answer given the question and the solution. You will output a score between 0 and 100 for the following categories:
        -Correctness: How correct is the answer given the solution? The answer does not have to exactly be the same as the solution but the context should be similar and it should include most of the information given in the solution. If the answer does not mention most of the solution, give it a low score. Also, the answer should not include any false information.
        -Relevance: How relevant is the answer for the question, given the solution? You will check if the answer goes of topic and starts mentioning unrelated information to the question.
        -Coherence: Is the answer coherent? Does it repeats the same sentence over and over or starts talking about completely unrelated and illogical things? How relevant is the answer for the question (This should be a priority, give a low score to answers with irrelevant information)?
        You are a very strict evaluator and would only give a score above 75 if the answer is perfect. If the answer is not perfect but still acceptable, give a score between 50-100. If the answer does not resemble the solution and talks about irrelevant stuff, give a score below 50. Finally, you are going to give a brief explanation about the scores you gave. Your output will be as follows:
        Correctness: <correctness_score>
        Relevance: <relevance_score>
        Coherence: <coherence_score>
        Explanation: <your explanation about why you gave those score>
        Question: 
        {question}
        Solution: 
        {solution}
        Answer:
        {answer}""")
    
    def gen_sim_queries(self, test_id):
        # Prompt to generate similar questions. This prompt works best with Claude 2.0, so it may not produce 
        # desirable outputs in different chatbots.
        if test_id == 1:
            return self.stripped_prompts("""Your task is to create 10 sentences that have a very similar meaning to the question provided. The same question can be formatted very differently depending on the user, the length and the level of formality can vary, and there can be grammatical errors or typos. Sometimes, users don't even form sentences or ask clear questions, so some of your generations should resemble that. The newly created sentences should resemble sentences generally inputted to chatbots by customers, so mimic that style. Put the generated sentences in a Python list.
            Question: {question}""")
        elif test_id == 2:
            return self.stripped_prompts("""Your task is to change the spellings and change the casing of the characters for a given sentence. You also can also remove or repeat the punctutaion mark at the end of the sentecen. You will create 10 new sentences from the original one. Put the generated sentences in a Python list.                  
            Original sentence: {sentence}
            Variations:""")
        else:
            print("No such test id!")

    def qa_prompt(self):
        return self.stripped_prompts("""Your job is to give an answer to the user input at the end. You can use the following pieces of context and the chat history to give an answer. The context and chat history are to help you give a satisfactory answer to the user input, but if the user input is irrelevant to the context and history, you don't have to use them to answer it. If you don't know the answer to the input, don't try to make up an answer. 
        Context:
        {context}
                                     
        Chat History:
        {chat_history}
                                     
        User Input:
        {question}""")

    def condense_q_prompt(self):
        return self.stripped_prompts("""Output the given summary of the conversation history and the question, as is. Do not change anything.                                     
        Summary of the conversation history:
        {chat_history}
        Question:
        {question}""")
    
    def memory_summary(self):
        return self.stripped_prompts("""Progressively summarize the lines of conversation provided, adding onto the previous summary returning a new summary. Do not output anything except the summary. Do not make a very long summary, keep it short.
        EXAMPLE
        Current summary:
        The human asks what the AI thinks of artificial intelligence. The AI thinks artificial intelligence is a force for good.

        New lines of conversation:
        Human: Why do you think artificial intelligence is a force for good?
        AI: Because artificial intelligence will help humans reach their full potential.

        New summary:
        The human asks what the AI thinks of artificial intelligence. The AI thinks artificial intelligence is a force for good because it will help humans reach their full potential.
        END OF EXAMPLE

        Current summary:
        {summary}

        New lines of conversation:
        {new_lines}

        New summary:""")
    
    def multi_query_prompt(self):
        return self.stripped_prompts("""You are an AI language model assistant. Your task is to generate three different versions of the given user question to retrieve relevant documents from a vector database. By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. Provide these alternative questions seperated by newlines. Do not output anything besides the questions, and don't put a blank line between the questions.
        Original question: {question}""")
    
    def csv_prompt(self):
        return self.stripped_prompts("""A user wants to gain insights about a csv file that is imported as a Python dictionary. The keys of the dictionary hold the columns of the csv file, and each key has a list as the value. The lists correspond to the values in the corresponding column of the csv. The user wants you to translate their command into Python code so that they can run the code to learn more about the dictionary. You are going to refer to the dictionary as "csv_dict", and you are going to output the code inside "```". You are not going to output anything except the code. You don't have to wrap the code inside a "print" function. Use double quotes instead of single ones in the code. Here is an example:
        EXAMPLE
        User Input: How many rows are there?
        Output: ```df.shape[0]```
        END_EXAMPLE
        Here is the chat history between you and the user:
        {chat_history}
        Here is the first 5 rows of the csv file and the User Input:         
        {user_input}
        Output:""")

    def merge_with_template(self, chatbot, prompt_type):

        prompt = self.prompt_dict[prompt_type]
        template = chatbot.prompt_template()
        if template is not None:
            prompt = template.format(prompt=prompt)
        return prompt