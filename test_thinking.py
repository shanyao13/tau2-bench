import sys
import os

# 确保能正确导入 src 目录下的包
sys.path.insert(0, os.path.abspath("src"))

import litellm
# 保持调试打印以便我们能看清网络请求和响应
litellm._turn_on_debug()

from tau2.utils.llm_utils import generate
from tau2.data_model.message import UserMessage

model = "anthropic/claude-opus-4-5-20251101-hz"
kwargs = {
    "temperature": 1.0, 
    "max_tokens": 65536, 
    "api_base": "http://10.200.95.16:30300", 
    "thinking": {"type": "enabled", "budget_tokens": 62000}
}

# 故意给一道很绕的逻辑题，强迫模型使用深度思考功能
messages = [
    UserMessage(role="user", content="请一步一步仔细思考下这道题：农夫有 100 只羊，除了 20 只之外全部逃跑了，那他现在还剩下几只牛？")
]

if __name__ == "__main__":
    print(f"正在向测试节点 {kwargs['api_base']} 发起测试请求...\n请稍候...")
    try:
        response = generate(model=model, messages=messages, **kwargs)
        
        print("\n\n============= 最终解析结果 =============")
        print("回答内容 (Content):")
        print(response.content)
        
        raw_dict = response.raw_data
        
        print("\n底层元数据 (Raw Data info):")
        # 由于我们用的 tau2 自带的 Message 对象，我们去原始字典探查
        if "provider_specific_fields" in raw_dict:
            print("发现 provider_specific_fields !")
            print(raw_dict["provider_specific_fields"])
        
        # 判断思考逻辑保存在哪里：
        if response.content and "<think>" in response.content:
            print("\n结论：✅ 大模型使用了 thinking，并将思考过程作为纯文本的 <think> 标签写在了 Content 里（可能是 DeepSeek 架构或套壳处理）。")
        elif raw_dict.get("provider_specific_fields", {}).get("thinking_blocks"):
             print("\n结论：✅ 大模型使用了 thinking，并且是采用的标准 Anthropic 协议返回了专用的 thinking_blocks字段。")
        else:
            print("\n结论：❌ 不出所料！网关服务端接收了您的请求但没有吐出任何思考过程！大概率是那个自定义节点后端模型（Opus4.5等）原生就不支持 extended thinking，直接退化回普通闲聊模式作答了。")
    except Exception as e:
         print(f"请求发生报错: {e}")
