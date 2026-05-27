from typing import Dict, Any, Optional

class HintGenerator:
    def __init__(self, llm_provider):
        self.llm = llm_provider

    async def get_hint(self, question: Dict[str, Any], hint_level: int) -> str:
        hints = question.get("hints", [])
        if not hints:
            return "💡 Think about the main data structures (Arrays, Sets, Maps) and how they could map the parameters."
            
        # Clamp hint level
        idx = min(max(0, hint_level - 1), len(hints) - 1)
        hint_text = hints[idx]
        
        prefix = ""
        if idx == 0:
            prefix = "💡 **Hint 1 (High-level Approach)**: "
        elif idx == 1:
            prefix = "💡 **Hint 2 (Algorithm Outline)**: "
        else:
            prefix = "💡 **Hint 3 (Detailed Pseudo-solution)**: "
            
        return f"{prefix}{hint_text}"
