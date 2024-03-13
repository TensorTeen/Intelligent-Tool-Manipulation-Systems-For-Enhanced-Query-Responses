from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Retriever:
    def __init__(self):
        pass
    
    
class STRetriever(Retriever):
    def __init__(self, path):
        """
        Initializes the Retriever object using a sentence transformers model.

        Parameters:
            path (str): The path to the sentence transformer model.

        Returns:
            None
        """
        #super(Retriever, self).__init__()
        self.retriever_model = SentenceTransformer(path)
    
    def __call__(self, tool_set, queries, n_retrieved):
        """
        Accepts a list of tools, and a query/list of queries
        Returns an array of sorted tools of shape (n_queries x n_tools)
        """
        tool_emb = self.retriever_model.encode(tool_set)
        if type(queries)== list:
            pass
        else:
            queries=[queries]
        query_emb = self.retriever_model.encode(queries)
        cos_dist = 1-cosine_similarity(tool_emb, query_emb)
        indices = np.argsort(cos_dist, axis=0)
        sorted_tools=np.array(tool_set)[indices]
        
        return sorted_tools[:n_retrieved,:].T