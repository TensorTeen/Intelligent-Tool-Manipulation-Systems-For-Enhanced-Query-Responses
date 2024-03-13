class Config:
    OPENAI_TOKEN = '<openAI_API_Key>'
    REPLICATE_TOKEN = '<Replicate_Token>'
    GPT_4 = 'openai/gpt-4-1106-preview'
    GPT_3_5 = 'openai/ft:gpt-3.5-turbo-1106:interiit:jsn2jsn-ak-11-12:8UXjCkwg'
    INSTRUCT = 'openai/gpt-3.5-turbo-instruct'
    OPENCHAT = 'replicate/nateraw/openchat_3.5-awq:ded16ea9889fe7c536c105b0b5f5142db79e4e38f92db2703e0ff59da1c10999'
    CostMap = {'gpt-3.5-turbo-1106':{
    'input':0.0030/1000,
    'output':0.0060/1000
},
'text-embedding-ada-002':{
    'input': 0.0001/1000
},
'ft:gpt-3.5-turbo-1106:interiit:jsn2jsn-ak-11-12:8UXjCkwg':{
      'input':0.0090/1000,
    'output':0.0180/1000
}
}