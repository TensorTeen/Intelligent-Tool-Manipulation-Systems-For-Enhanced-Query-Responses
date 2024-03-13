import os


class Config:
    OPENAI_TOKEN = os.environ.get('OPENAI_API_KEY')
    REPLICATE_TOKEN = os.environ.get('REPLICATE_API_TOKEN')
    GPT_4 = 'openai/gpt-4-1106-preview'
    GPT_3_5 = 'openai/gpt-3.5-turbo-1106'
    INSTRUCT = 'openai/gpt-3.5-turbo-instruct'
    OPENCHAT = 'replicate/nateraw/openchat_3.5-awq:ded16ea9889fe7c536c105b0b5f5142db79e4e38f92db2703e0ff59da1c10999'
    CostMap = {'gpt-3.5-turbo-1106': {
        'input': 0.0030 / 1000,
        'output': 0.0060 / 1000
    },
        'text-embedding-ada-002': {
            'input': 0.0001 / 1000
        }
    }