import os
import requests

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

    def cleanup(self)-> bool:
        pass

class PublicGlm(LLMSource):
    def __init__(self, model_name="glm-4-air"):
        super().__init__()
        self.model_name = model_name

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

    def cleanup(self):
        return True
    
class LocalOllamaGlm(LLMSource):
    def __init__(self, ollama_generate_ep: str, ollama_model_name: str):
        super().__init__()
        self.endpoint = ollama_generate_ep
        self.model_name = ollama_model_name
    
    @staticmethod
    def check_url_availability(url):
        try:
            response = requests.head(url)
        # 检查服务器响应的状态码是否为 200
            if response.status_code == 200:
                print("URL is accessible.")
                return True
            else:
                print(f"URL returned a status code of {response.status_code}.")
                return False
        except requests.RequestException as e:
            print(f"Failed to reach the URL: {e}")
            return False


    def init_llm(self):
        if not self.check_url_availability(self.endpoint):
            return False
        print("Local Ollama model init success")
    
    def infer(self, prompt: str, **kwargs):
        params = self.default_infer_params.copy()
        params.update(kwargs)
        
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(self.endpoint, json=data)
            response.raise_for_status()  # 检查请求是否成功
            response_data = response.json()
            
            return {
                "response": response_data.get('response'),
                #"usage": response_data.get('usage', {})  # 根据实际API响应调整
                "usage": None
            }
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    def cleanup(self):
        return True


class LocalTfGlm(LLMSource):
    pass

class LocalTgiGlm(LLMSource):
    pass

class LocalVllmGlm(LLMSource):
    pass