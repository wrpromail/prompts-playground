

introduce_md = """
"""

model_load_md = """
public_api 是指调用智谱公开 api 进行推理\n
local_transformer 是指使用 transformers 库加载本地权重\n
如果选择 public_api，请在 model_source 中填写 api_key。如果选择 local_transformer，请在 model_source 中填写权重路径。
"""

ppt_outline_generate_md = """
#### PPT 生成 prompt
由于语言模型只能生成文本，不可能直接生成 ppt，所以 ppt 生成任务需要进行拆分为两步。第一步根据需求按页生成 ppt 大纲，第二步是根据每一页的大纲生成具体的 ppt 内容。
"""

