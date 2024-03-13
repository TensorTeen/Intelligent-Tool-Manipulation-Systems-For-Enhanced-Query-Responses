from cog import BasePredictor, Path, Input
import torch
from toolforcer import ToolForcer


class Predictor(BasePredictor):
    def setup(self):
        self.net = ToolForcer('TheBloke/openchat_3.5-AWQ', 'ToolBench/ToolBench_IR_bert_based_uncased', 'cuda', tools=None, load_in_4bit=True, use_vllm=True)

    def predict(self,
                query: str = Input(description="Input query"),
                tools: str = Input(description="Tools to use")
            ) -> str:
        """Run a single prediction on the model"""
        
        output = self.net(query=query, tools=tools, n_retrieved=10)
        
        return output