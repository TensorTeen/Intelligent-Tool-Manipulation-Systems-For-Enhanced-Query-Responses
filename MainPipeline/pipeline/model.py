from imports import *
from .base_model import Model as BaseModel

class Model(BaseModel):
    def __init__(self,config):
        self.config = config
        super().__init__(self.config.openai_model,system='',clear_history_after_call=True,gen_kargs={'temperature':self.config.temperature},return_json=True)

    def __call__(self,query, tools,examples):
        system = self.config.system_template.format(tools=json.dumps(tools),examples=self.format_examples(examples))
        prompt = self.config.prompt_template.format(query=query)
        self.set_system(system)
        return super().__call__(prompt)
    
    @staticmethod
    def format_examples(examples):
        formatted_examples = "\n\n".join(
    f"{i+1}) {json.dumps(d, indent=4)}" for i, d in enumerate(examples)
)
        return formatted_examples