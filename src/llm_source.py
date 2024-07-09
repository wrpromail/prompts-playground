import os

from zhipuai import ZhipuAI

class LLMSource:
    def __init__(self):
        self.source = None
        self.default_infer_params = {
            'max_tokens': 1024,
            'temperature': 0.95,
            'top_p': 0.70,
        }

    def init_llm(self):
        pass 

    def infer(self, prompt: str, **kwargs):
        params = self.default_infer_params.copy()
        params.update(kwargs)
        pass 


class PublicGlm(LLMSource):
    def __init__(self):
        super().__init__()

    def _is_valid(self):
        self.api_key = os.environ.get('GLM_API_KEY')
        if self.api_key is None:
            print("GLM_API_KEY is not set")
            return False
        model_name = os.environ.get('GLM_MODEL_NAME')
        if model_name is None or model_name == "":
            self.model_name = "glm-4-air"
        else:
            self.model_name = model_name
        return True

    def init_llm(self):
        if not self._is_valid():
            return False
        self.cli = ZhipuAI(api_key=self.api_key)
        print("GLM init success")
        return True
        
    def infer(self, prompt: str, **kwargs):
        params = self.default_infer_params.copy()
        params.update(kwargs) 
        response = self.cli.chat.completions.create(model=self.model_name, messages=
                                                    [{"role": "user", "content": prompt},],stream=False, **params)
        return {
            "response": response.choices[0].message.content,
            "usage": response.usage.dict() # prompt_tokens completion_tokens total_tokens
        }

class LocalTfGlm(LLMSource):
    pass

class LocalTgiGlm(LLMSource):
    pass