from imports import *
from .model import Model
from .retriever import Retriever
from config import Config
import tiktoken
import time

class Pipeline:
    def __init__(self,config):
        self.config = config
        self.rtr = Retriever(config.embedding_model)
        self.model = Model(self.config)
    def __call__(self, query, tools, examples):
        tic = time.time()
        output = self.rtr(query, tools, self.config.num_retrieved)
        _output = self.model(query, self.rtr.strip_embeddings(output['return_tools']), examples)
        output.update(_output)
        output['solution'] = json.loads(output['response'])
        del output['response']
        toc = time.time()
        time_taken = toc - tic
        output['time_taken'] = time_taken
        output['openai_model'] = self.config.openai_model.replace('openai/', '')
        output['embedding_model'] = self.config.embedding_model.replace('openai/', '')


        query_embeded = output['query_embeded']
        docs_embeded = output['docs_embeded']
        message_history = output['message_history']


        # Count openai tokens
        output['num_embedding_tokens_query'] = self.count_openai_tokens(output['embedding_model'],query_embeded)
        output['num_embedding_tokens_tool'] = self.count_openai_tokens(output['embedding_model'],docs_embeded)


        inputs = 'System ' + message_history[0]['content'] + ' User ' + message_history[1]['content']
        outputs = message_history[2]['content']

        output['num_output_tokens'] = self.count_openai_tokens(output['openai_model'],outputs)
        output['num_input_tokens'] = self.count_openai_tokens(output['openai_model'],inputs)
        
        # calculate cost
        output['embedding_cost_query'] = output['num_embedding_tokens_query'] * \
                            Config.CostMap[output['embedding_model']]['input']
        output['embedding_cost_tool'] = output['num_embedding_tokens_tool'] * \
                            Config.CostMap[output['embedding_model']]['input']

        output['gpt_input_cost'] = output['num_input_tokens'] * \
                                    Config.CostMap[output['openai_model']]['input']
        
        output['gpt_output_cost'] = output['num_output_tokens'] * \
                                    Config.CostMap[output['openai_model']]['output']

        output['total_inference_cost'] = output['gpt_input_cost'] + \
                                        output['gpt_output_cost'] + \
                                        output['embedding_cost_query']
        output['tool_setup_cost'] = output['embedding_cost_tool']
        del output['docs_embeded']
        del output['message_history']
        del output['query_embeded']
        return output
    
    @staticmethod
    def count_openai_tokens(model_name,text):
        if not text:return 0
        enc = tiktoken.encoding_for_model(model_name)
        return len(enc.encode(text))
    


        














    # retrieved_tools = output['return_tools']
    # embed_calls = output['embed_calls']
    # query_embedded = output['query_embedded']
    # docs_embedded = output['docs_embedded']

    # output = self.model(query, self.rtr.strip_embeddings(retrieved_tools), examples)
    # message_history = output['message_history']
    # solution = json.loads(output['response'])

    # solution['embed_calls'] = embed_calls

    # toc = time.time()
    # time_taken = toc - tic
    # solution['time_taken'] = time_taken
    # solution['openai_model'] = self.config.openai_model.replace('openai/', '')
    # solution['embedding_model'] = self.config.embedding_model.replace('openai/', '')



    # # Count openai tokens
    # inputs = 'System ' + message_history[0]['content'] + ' User ' + message_history[1]['content']
    # outputs = message_history[2]['content']
    # enc = tiktoken.encoding_for_model(solution['openai_model'])
    # solution['num_output_tokens'] = len(enc.encode(outputs))
    # solution['num_input_tokens'] = len(enc.encode(inputs))

    # # count text embedding tokens
    # enc = tiktoken.encoding_for_model(solution['embedding_model'])
    # if docs_embedded:
    #     solution['num_embedding_tokens_tool'] = len(enc.encode(docs_embedded))
    # else:
    #     solution['num_embedding_tokens_tool'] = 0
    # solution['num_embedding_tokens_query'] = len(enc.encode(query_embedded))
    # solution['embedding_cost_query'] = solution['num_embedding_tokens_query'] * Config.CostMap[solution['embedding_model']]['input']
    # solution['embedding_cost_tool'] = solution['num_embedding_tokens_tool'] * Config.CostMap[solution['embedding_model']]['input']

    # solution['gpt_input_cost'] = solution['num_input_tokens'] * Config.CostMap[solution['openai_model']]['input']
    # solution['gpt_output_cost'] = solution['num_output_tokens'] * Config.CostMap[solution['openai_model']]['output']

    # solution['total_inference_cost'] = solution['gpt_input_cost'] + solution['gpt_output_cost'] + solution['embedding_cost_query']
    # solution['tool_setup_cost'] = solution['embedding_cost_tool']
    # return solution
    


