# imports
import os
import time
import re
import copy
import json
import numpy as np
import random
import warnings
warnings.filterwarnings('ignore')
from litellm import embedding as EmbeddingBackend
from litellm import completion as LLMBackend, completion_cost, token_counter
from config import Config


os.environ['REPLICATE_API_TOKEN'] = Config.REPLICATE_TOKEN
os.environ["OPENAI_API_KEY"] = Config.OPENAI_TOKEN