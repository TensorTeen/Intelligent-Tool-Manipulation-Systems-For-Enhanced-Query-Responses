from imports import *
import numpy as np
import copy

class Retriever:
    def __init__(self, model_name):
        self.model_name = model_name
        self._tools = []
        self._tool_names = set()

    def embed(self, texts):
        # Assuming EmbeddingBackend accepts a list of texts and returns a list of embeddings
        embeddings_data = EmbeddingBackend(self.model_name, texts).data
        return np.array([item['embedding'] for item in embeddings_data])

    def get_doc(self, tool):
        s = tool['tool_description']
        for arg in tool['args']:
            s += ' ' + arg['arg_description']
        return s

    def index(self, tools):
        tools = copy.deepcopy(tools)
        embed_calls = 0
        new_tools = [tool for tool in tools if tool['tool_name'] not in self._tool_names]
        embed_calls += len(new_tools) 
        # Extract documents from new tools
        docs_to_embed = [self.get_doc(tool) for tool in new_tools]
        docs_embeded = ' '.join(docs_to_embed)
        if not docs_to_embed:return 0, []
        # Get embeddings for all new documents in one batch
        embeddings = self.embed(docs_to_embed)
        
        
        # Assign the corresponding embedding to each tool and update internal structures
        for i, tool in enumerate(new_tools):
            tool['embedding'] = embeddings[i]
            self._tool_names.add(tool['tool_name'])
            self._tools.append(tool)
        return embed_calls,docs_embeded

    def embedding_similarity(self, query_embedding, tool_embedding):
        return (query_embedding.T @ tool_embedding)

    def __call__(self, query, tools=None, k=8):
        if tools is not None:
            embed_calls,docs_embeded = self.index(tools)
                    
        query_embed = self.embed([query])[0]  # Embed the single query text
        embed_calls+=1
        query_embeded = query
        
        # Calculate similarity scores between the query embedding and all indexed tools' embeddings.
        for tool in self._tools:
            tool['similarity'] = self.embedding_similarity(query_embed, tool['embedding'])
            
         # Sort tools by similarity score and filter out those that are not part of the input 'tools' if provided.
        return_tools = sorted(self._tools,key=lambda x: x['similarity'],reverse=True).copy()
        if tools is not None:
            return_tools = [tool for tool in return_tools if tool in tools]
        return {'embed_calls':embed_calls,
                'return_tools':return_tools[:k],
                'query_embeded':query_embeded,
                'docs_embeded':docs_embeded}

    @staticmethod
    def strip_embeddings(tools):
       stripped_tools = copy.deepcopy(tools)
       for tool in stripped_tools:
           del tool['embedding']
           del tool['similarity']
       return stripped_tools