from jinja2 import Environment, FileSystemLoader
from typing import Dict, List, Any

class PromptTemplateManager:
    def __init__(self, template_dir: str):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.templates: Dict[str, List[str]] = {}

    def register_template(self, template_name: str, required_fields: List[str]):
        """注册模板及其必需字段"""
        self.templates[template_name] = required_fields

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """渲染模板，检查必需字段"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not registered")

        missing_fields = [field for field in self.templates[template_name] if field not in context]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        template = self.env.get_template(template_name)
        return template.render(context)

test_src_code = """
package main

import (
    "fmt"
    "strconv"
    "strings"
)

func processText(text string) {
    lines := strings.Split(text, "\n")
    categoryCount := make(map[string]int)
    totalValue := 0.0
    itemCount := 0

    for _, line := range lines {
        parts := strings.Split(line, ",")
        if len(parts) != 3 {
            continue
        }

        category := parts[0]
        valueStr := parts[1]
        value, err := strconv.ParseFloat(valueStr, 64)
        if err != nil {
            continue
        }

        categoryCount[category]++
        totalValue += value
        itemCount++
    }

    if itemCount == 0 {
        fmt.Println("No valid items found.")
        return
    }

    averageValue := totalValue / float64(itemCount)

    fmt.Println("Category Counts:", categoryCount)
    fmt.Println("Total Value:", totalValue)
    fmt.Println("Average Value:", averageValue)

    for category, count := range categoryCount {
        percentage := float64(count) / float64(itemCount) * 100
        fmt.Printf("Category %s constitutes %.2f%% of total items.\n", category, percentage)
    }
}
"""

jp_text = """
はい、以下は長めの日本語のテキストです。
日本は四季折々の美しい自然に恵まれた国である。春には桜が咲き乱れ、夏には緑豊かな山々が広がり、秋には紅葉が赤く染まる。冬にはしんしんと冷えた空気の中、雪化粧をした景色が魅力的だ。
このような自然の美しさはもちろんのこと、日本には伝統的な文化や美意識も根強く残されている。寺社仏閣、武士道、茶道、書道、着物など、古くから大切に受け継がれてきた日本の伝統は世界的にも高い評価を得ている。
また、近代になってからも、漫画、アニメ、ゲーム、テクノロジーなど、日本発の文化が世界中で人気を集めている。日本人の独創性と高い技術力は世界を驚かせ続けている。
一方で、少子高齢化や自然災害への備えなど、日本が抱える課題も少なくない。しかし、日本人の強い絆と絶え間ない努力によって、これらの課題にも確実に取り組んでいる。
このように、自然、文化、そして人々の姿勢など、多様な魅力を併せ持つ日本は、これからも世界からの注目を集め続けるだろう。日本の素晴らしさを様々な形で発信し、世界とのつながりを深めていくことが大切だと思う。"""

abstract = """
金融政策与监管失误
房地产市场的过度投资
企业过度借贷与债务累积
国际环境与市场变化的影响
"""

code_prefix = """
public class PalindromeFinder {

    /**
     * Finds the longest palindromic substring in the given text.
     *
     * @param s The input string.
     * @return The longest palindromic substring.
     */
    public static String findLongestPalindrome(String s) {
        if (s == null || s.length() < 1) {
            return "";
        }

        int n = s.length();
        boolean[][] dp = new boolean[n][n]; // dp[i][j] will be true if the substring s[i...j] is a palindrome.
        int start = 0; // Start index of the longest palindrome found.
        int maxLength = 1; // Length of the longest palindrome found.

        // All substrings of length 1 are palindromes.
        for (int i = 0; i < n; i++) {
            dp[i][i] = true;
        }

"""

full_text = """
在探讨人类文明的进程中，科技的发展无疑是推动社会历史前进的重要动力。从古代的火的发现到现代的互联网革命，每一次科技的跃进都深刻地影响了人类的生活方式和思维方式。然而，科技的发展同时也带来了诸多挑战和思考，特别是在伦理和社会结构的层面。
首先，我们不得不提的是科技在提高生活效率和质量方面的积极影响。例如，医疗科技的进步，使得许多曾经被认为是不治之症的疾病现在可以得到有效治疗。智能手机和互联网的普及，极大地方便了人们的沟通和信息获取，缩短了人与人之间的距离。这些技术的发展极大地提升了人类的生活质量。
然而，科技进步也带来了一系列的伦理问题。例如，在生物技术领域，基因编辑技术如CRISPR的出现，使得人类有能力在基因层面进行设计和修改。这不仅引发了关于“设计婴儿”等伦理问题，也让人们担忧这种技术可能加剧社会不平等，造成基因优越性的分层。此外，人工智能的发展虽然在很多领域显示出巨大的潜力，但同时也可能导致失业问题的加剧，以及决策过程中缺乏人类情感和道德判断的风险。
社会结构的变迁也是科技发展带来的重要议题。随着自动化和智能化技术的应用，传统的工作岗位正在迅速变化或消失，这要求劳动力市场和教育体系做出相应的调整。同时，科技的不均衡发展也加剧了地区之间以及国家内部的经济和社会差异，这可能导致社会不稳定和分裂。
此外，科技的发展还引发了对隐私权的担忧。在大数据和互联网的时代，个人信息的收集和使用变得极为广泛，但同时也存在被滥用的风险。如何在促进技术发展和保护个人隐私之间找到平衡点，是当代社会面临的一大挑战。
总之，科技的发展是一把双刃剑，它既为人类社会带来了前所未有的机遇，也带来了复杂的挑战。在享受科技带来的便利的同时，我们也必须思考如何合理利用科技，解决由此产生的伦理和社会问题，确保科技的发展能够惠及全人类，推动建设一个更加公正、平衡和可持续的世界。
"""

if __name__ == "__main__":
    test_template_dir = "../raw_prompts"
    manager = PromptTemplateManager(template_dir=test_template_dir)
    manager.register_template("a4.txt", ["file_content", "user_requirement"])
    context = {
        "file_content": full_text,
        "user_requirement": "摘要到200字以内"
    }
    rendered_prompt = manager.render_template("a4.txt", context)
    print(rendered_prompt)

    