from typing import List, Dict, Any

class DifficultyAdapter:
    def calculate_next_difficulty(self, recent_attempts: List[Dict[str, Any]], current: str) -> str:
        if not recent_attempts:
            return current
            
        # Look at last attempt
        last = recent_attempts[-1]
        score = last.get("score", 0.0)
        hints = last.get("hints_used", 0)
        
        difficulties = ["easy", "medium", "hard"]
        curr_idx = difficulties.index(current.lower()) if current.lower() in difficulties else 0
        
        # If scored above 85% with 0 or 1 hints, try upgrading difficulty
        if score >= 85.0 and hints <= 1:
            next_idx = min(curr_idx + 1, len(difficulties) - 1)
            return difficulties[next_idx]
            
        # If scored below 50% or used 3+ hints, degrade difficulty
        elif score < 50.0 or hints >= 3:
            next_idx = max(curr_idx - 1, 0)
            return difficulties[next_idx]
            
        return current
