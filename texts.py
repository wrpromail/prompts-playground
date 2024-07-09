import random

basic_usage_md="""
## step 1
加载模型:可以使用开放平台，或本地使用 transformers、tgi、vllm 等框架运行的推理服务。注意同时只能加载一个模型，新的模型会覆盖之前的加载内容。
## step 2
查看 prompt 模板内容: 所有 prompt 模板都存储在 raw_prompts 目录下，然后通过 prompt_declare.yml 文件进行声明，在声明文件中，
对 prompt 模板的参数、用途进行描述。可以通过‘模板数据读取’分页来查看声明文件，然后选择需要测试的 prompt 模板名称。
## step 3
通过修改自定义参数，渲染 prompt，然后推理得到结果。后续会添加性能测试、推理对比等功能。
## step 4
gradio 框架提供了 http API，比如你在页面上加载模型，然后可以通过调用以下两个 api 来渲染 prompt 与获取推理结果。
```bash
curl -X POST http://127.0.0.1:7860/call/render_template_content -s -H "Content-Type: application/json" -d '{
  "data": [
    "Hello!!",
    "print('Hello World')"
]}'

curl -X POST http://127.0.0.1:7860/call/template_infer -s -H "Content-Type: application/json" -d '{
  "data": [
    "Hello!!"
]}
```
可以阅读页面底部的‘通过API使用’，gradio 提供 python 与 javascript 客户端，可以方便研发人员快速进行 prompt 调试。
"""


sample_prompt0="""
想象你是一位来自2150年的时间旅行者。请描述你所在时代的日常生活,特别是在能源使用、交通方式和工作模式方面的重大变化。请详细解释这些变化是如何影响人类社会的。
"""

sample_prompt1="""
你是一位著名的美食评论家,被邀请品尝一道融合了中国和墨西哥烹饪元素的创新菜品。请写一篇500字左右的评论,描述这道菜的口感、味道、视觉呈现,以及它如何平衡两种烹饪传统。同时,请分析这种跨文化融合对全球美食趋势的潜在影响。
"""

sample_prompt2="""
设计一个新的棋类游戏,结合了国际象棋和围棋的元素。详细说明游戏规则、棋盘设计、胜利条件,以及每种棋子的移动方式和特殊能力。解释这个新游戏如何平衡策略性和复杂性,以及它可能吸引哪些类型的玩家。最后,探讨这种混合游戏对传统棋类运动可能产生的影响。
"""
def pick_random_sample_prompt():
    import random
    return random.choice(sample_prompts)

sample_prompts = [sample_prompt0, sample_prompt1, sample_prompt2]