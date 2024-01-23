class Prompter():

    def lamp_prompt(self, dataset, k=True):
        if dataset == 2:
            return """Your task is to categorize an article by choosing from one of the provided categories. You will only output the category name and nothing else.
                Article: 
                {article}
                Categories: [women, religion, politics, style & beauty, entertainment, culture & arts, sports, science & technology, travel, business, crime, education, healthy living, parents, food & drink]"""
        
        elif dataset == 3:
            if k:
                return """
                Here are a couple of review-rating pairs of a user. 
                <EXAMPLES>
                {examples}
                </EXAMPLES>
                With the given examples, give a score between [1, 2, 3, 4, 5] to the following review by the same user. Only output the score and nothing else.
                Review: 
                {prof_text}
                Score:
                """
            else:
                return """
                Give a score between [1, 2, 3, 4, 5] to the following review. Only output the score and nothing else.
                Review: 
                {prof_text}
                Score:
                """  
        elif dataset == 5:
            if k:
                return """Here are a couple of abstract-title pairs of an author:
                <EXAMPLES>
                {examples}
                </EXAMPLES>
                With the given examples, generate a title for the given abstract by the same author. Only output the title and nothing else:
                Abstract:
                {prof_text}
                Title:"""
            else:
                return """Your task is to generate a title for the given abstract. You will only output the title and nothing else.
                Abstract:
                {prof_text}
                Title:"""

    def eval_qa_prompt(self):
        return """Your job is to evaluate an answer given the question and the solution. You will output a score between 0 and 10 for the following categories:
        -Correctness: How correct is the answer given the solution? The answer does not have to exactly be the same as the solution but the context should be similar and it should include most of the information given in the solution. If the answer does not mention most of the solution, give it a low score. The answer should not include any false information.
        -Relevance: How relevant is the answer for the question, given the solution? You will check if the answer goes of topic and starts mentioning unrelated information to the question.
        -Coherence: Is the answer coherent? Does it repeats the same sentence over and over or starts talking about completely unrelated and illogical things? How relevant is the answer for the question (This should be a priority, give a low score to answers with irrelevant information)?
        You will first analyze the solution for the mentioned categories and explain what are its pros and cons, then you will output your score for the given categories. You are a very strict evaluator and would only give a score above 7.5 if the answer is perfect. If the answer is not perfect but still acceptable, give a score around 5. If the answer does not resemble the solution and talks about irrelevant stuff, give a score close to 0. Your output will be as follows:
        Analysis: <your analysis>
        Correctness: <correctness_score>
        Relevance: <relevance_score>
        Coherence: <coherence_score>
        Question: 
        {question}
        Solution: 
        {solution}
        Answer:
        {answer}"""
    
    def gen_sim_queries(self, test_id):
        # Prompt to generate similar questions. This prompt works best with Claude 2.0, so it may not produce 
        # desirable outputs in different chatbots.
        if test_id == 1:
            return """Your task is to create 10 sentences that have a very similar meaning to the question provided. The same question can be formatted very differently depending on the user, the length and the level of formality can vary, and there can be grammatical errors or typos. Sometimes, users don't even form sentences or ask clear questions, so some of your generations should resemble that. The newly created sentences should resemble sentences generally inputted to chatbots by customers, so mimic that style. Put the generated sentences in a Python list.
            Question: {question}"""
        elif test_id == 2:
            return """Your task is to change the spellings and change the casing of the characters for a given sentence. You also can also remove or repeat the punctutaion mark at the end of the sentecen. You will create 10 new sentences from the original one. Put the generated sentences in a Python list.                  
            Original sentence: {sentence}
            Variations:"""
        else:
            print("No such test id!")

    def qa_prompt(self):
        return """Your job is to give an answer to the user input at the end. You can use the following pieces of context and the chat history to give an answer. The context and chat history are to help you give a satisfactory answer to the user input, but if the user input is irrelevant to the context and history, you don't have to use them to answer it. If you don't know the answer to the input, don't try to make up an answer.
        Context:
        {context}
                                     
        Chat History:
        {chat_history}
                                     
        User Input:
        {question}"""
    
    def conv_agent_prompt(self):
        return """You are an agent that has a conversation with a user. Information related to the user input is going to be provided to you during the conversation. If you think that the information is relevant to answer the user, you can use it. Sometimes, the information may be unrelated or may not contain the answer the user is looking for. For those cases, do not use the provided information. Therefore, you need to decide whether the related information is actually useful to give the user a satisfactory answer. The provided information may contradict what you know. In those cases, provided information has priority. A summary of the chat history between you and the user is also going to be included after the related information to inform you about the current state of the conversation. Your answer should be in the style of a conversational assistant. Do not mention that you have used the provided information or the chat history for your answer. If you do not know the answer, do not say that the information is not provided, state that you do not know the answer.
        Here is the related information:
        {info}
        Here is the summary of the chat history:
        {chat_history}
        Here is the user input:
        {user_input}"""

    def query_gen_prompt(self):
        return """Your task is to transform user inputs into web search queries. The queries should not be longer than 10 words. If the input is already in the format of a query, output the user input without any modifications. Do not output anything expect the query and do not give an explanation. For the following situations, do not transform the input into a query and output only "NO QUERY": 1) If the user input is directing a question to someone using a pronoun\n2)If the input is composed of a single word like a number or an object.
        Here are some examples:
        <EXAMPLES>
        User Input: Project_Proposal.pdf
        Query: Project_Proposal.pdf
        User Input: 5
        Query: NO QUERY
        User Input: Which teams were in the finals of the last world cup
        Query: Last world cup finalists
        User Input: Why does he act like this?
        Query: NO QUERY
        User Input: Why did the colossus fall over?
        Query: colossus fall reasons
        User Input: best new year resolutions
        Query: best new year resolutions
        User Input: Apple
        Query: NO QUERY
        </EXAMPLES>
        Here is the user input:
        User Input: {user_input}
        Query:"""
    
    def condense_q_prompt(self):
        return """Output the given summary of the conversation history and the question, as is. Do not change anything.                                     
        Summary of the conversation history:
        {chat_history}
        Question:
        {question}"""
    
    def memory_summary(self):
        return """Your task is to summarize a conversation between a user and an assistant. The current summary and the new lines in the conversation will be provided to you. Progressively summarize the lines of conversation provided, adding onto the previous summary. The new summary should include key information that may come up later in the conversation, such as what the user asked and what did the user and the assistant talked previously. If there is no current summary, only use the new lines of conversation for the summary. Do not output anything except the summary, and do not make it very long, keep it short. It should not exceed 256 words.
        Here is the current summary:
        {summary}
        Here are the new lines of conversation:
        {new_lines}
        New summary:"""
    
    def multi_query_prompt(self, n=3):
        return """You are an AI language model assistant. Your task is to generate {n} different versions of the given user question to retrieve relevant documents from a vector database. By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. Provide these alternative questions seperated by newlines. Do not output anything besides the questions, and don't put a blank line between the questions.
        Original question: {question}""".format(n=n)
    
    def csv_prompt(self):
        return """A user wants to gain insights about a pandas dataframe. Your job is to translate the user command into Python code so that they can run the code to learn more about the dataframe. The csv is already loaded into the dataframe, and you are going to refer to the dataframe as "df". You are going to output the code inside "```". You are not going to output anything except the code. Include a print function to show the output of the code. Here is an example:
        User Input: How many rows are there?
        Output: 
        ```
        print(df.shape[0])
        ```
        Here is the chat history between you and the user:
        {chat_history}
         
        {user_input}
        Output:"""