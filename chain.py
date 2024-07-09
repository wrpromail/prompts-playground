from src.llm_source import PublicGlm
from src.templates_manager import PromptTemplateManager

full_text = """
在探讨人类文明的进程中，科技的发展无疑是推动社会历史前进的重要动力。从古代的火的发现到现代的互联网革命，每一次科技的跃进都深刻地影响了人类的生活方式和思维方式。然而，科技的发展同时也带来了诸多挑战和思考，特别是在伦理和社会结构的层面。
首先，我们不得不提的是科技在提高生活效率和质量方面的积极影响。例如，医疗科技的进步，使得许多曾经被认为是不治之症的疾病现在可以得到有效治疗。智能手机和互联网的普及，极大地方便了人们的沟通和信息获取，缩短了人与人之间的距离。这些技术的发展极大地提升了人类的生活质量。
然而，科技进步也带来了一系列的伦理问题。例如，在生物技术领域，基因编辑技术如CRISPR的出现，使得人类有能力在基因层面进行设计和修改。这不仅引发了关于“设计婴儿”等伦理问题，也让人们担忧这种技术可能加剧社会不平等，造成基因优越性的分层。此外，人工智能的发展虽然在很多领域显示出巨大的潜力，但同时也可能导致失业问题的加剧，以及决策过程中缺乏人类情感和道德判断的风险。
社会结构的变迁也是科技发展带来的重要议题。随着自动化和智能化技术的应用，传统的工作岗位正在迅速变化或消失，这要求劳动力市场和教育体系做出相应的调整。同时，科技的不均衡发展也加剧了地区之间以及国家内部的经济和社会差异，这可能导致社会不稳定和分裂。
此外，科技的发展还引发了对隐私权的担忧。在大数据和互联网的时代，个人信息的收集和使用变得极为广泛，但同时也存在被滥用的风险。如何在促进技术发展和保护个人隐私之间找到平衡点，是当代社会面临的一大挑战。
总之，科技的发展是一把双刃剑，它既为人类社会带来了前所未有的机遇，也带来了复杂的挑战。在享受科技带来的便利的同时，我们也必须思考如何合理利用科技，解决由此产生的伦理和社会问题，确保科技的发展能够惠及全人类，推动建设一个更加公正、平衡和可持续的世界。
"""

test_template_dir = "./raw_prompts"
manager = PromptTemplateManager(template_dir=test_template_dir)
manager.register_template("a4.txt", ["file_content", "user_requirement"])
context = {
    "file_content": full_text,
    "user_requirement": "摘要到200字以内"
}
rendered_prompt = manager.render_template("a4.txt", context)
print(rendered_prompt)
glm = PublicGlm()
if glm.init_llm():
    rst = glm.infer(rendered_prompt)
    print(rst)
else:
    print("init failed")