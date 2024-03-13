from imports import *
from datetime import datetime


class Model:
    def __init__(self,model_name,
                 role='assistant',
                 system=None,
                 gen_kargs={},
                 clear_history_after_call=False,
                 return_json=False,
                 logging=False):
        gen_kargs['response_format'] = { "type": "json_object" } if return_json else None
        self.model_name = model_name
        self.system = system
        self.gen_kargs = gen_kargs
        self.role = role
        self.clear_history_after_call = clear_history_after_call
        self.logging=logging
        self.message_history = [
            {
                "role": "system",
                "content": system or "You are a helpful assistant"
            }
        ]

    def add_message(self,content,role='user'):
        self.message_history.append({"role": role, "content": content})
    
    def clear_history(self):
        self.message_history = [
            {
                "role": "system",
                "content": self.system or "You are a helpful assistant"
            }
        ]

    
    def get_response(self):
        provider = LLMBackend
        response = provider(model=self.model_name,
                              messages = self.message_history,
                              **self.gen_kargs)
        msg = response.choices[0].message.content
        self.add_message(msg,'assistant')
        return msg
    
    def set_system(self,system):
        self.system = system
        self.message_history[0]['content'] = system
    
    def __call__(self, content, role='user'):
        self.add_message(content,role)
        response = self.get_response()
        message_history = copy.deepcopy(self.message_history)
        if self.clear_history_after_call:
            self.clear_history()
        self.log(content,response)
        return {'response':response,'message_history':message_history}
    
    def fill_variables(self,vars):
        for k,v in vars.items():
            self.message_history[0]['content'] = self.message_history[0]['content'].replace(f'${k}$',str(v))
    
    def toggle_return_json_on(self):
        self.gen_kargs['response_format'] = { "type": "json_object" }
    def toggle_return_json_off(self):
        self.gen_kargs['response_format'] = None
    
    def delete_last_round(self):
        self.message_history.pop()
        self.message_history.pop()

    def log(self,msg,response):
        if not self.logging:return
        formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('logs.txt','a') as f:
            f.write('*'*25)
            f.write(f"\nTime: {formatted_datetime}\n\n")
            f.write(f"\n 'Role:\n'{self.role}\n\n 'Message:'{msg}\n\n 'Response:\n'{response}\n\n")
            f.write('*'*25)

