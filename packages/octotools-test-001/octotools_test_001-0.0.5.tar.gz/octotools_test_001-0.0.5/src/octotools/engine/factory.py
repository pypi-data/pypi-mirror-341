from typing import Any, Union
from .openai import ChatOpenAI
from .anthropic import ChatAnthropic
from .together import ChatTogether
from .deepseek import ChatDeepseek

def create_llm_engine(model_string: str, use_cache: bool = False, is_multimodal: bool = True) -> Any:
    """Factory function to create appropriate LLM engine instance."""
    if any(x in model_string for x in ["gpt", "o1", "o3"]):
        return ChatOpenAI(model_string=model_string, use_cache=use_cache, is_multimodal=is_multimodal)
    
    elif "claude" in model_string:
        return ChatAnthropic(model_string=model_string, use_cache=use_cache, is_multimodal=is_multimodal)
    
    elif model_string == "deepseek-chat" or model_string == "deepseek-reasoner":
        return ChatDeepseek(model_string=model_string, use_cache=use_cache)
    
    elif any(x in model_string for x in ["meta-llama", "deepseek-ai", "mistralai", "Qwen", 
                                        "databricks", "microsoft", "nvidia", "google"]):
        return ChatTogether(model_string=model_string, use_cache=use_cache)
    else:
        try:
            return ChatTogether(model_string=model_string, use_cache=use_cache)
        except:
            raise ValueError(f"Unknown LLM engine: {model_string}")

