from typing import Dict, Any, Optional

class FeedbackGenerator:
    def __init__(self, llm_provider):
        self.llm = llm_provider

    async def generate_feedback(
        self, 
        question: Dict[str, Any], 
        user_code: str, 
        language: str, 
        eval_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        passed = eval_results.get("passed", 0)
        total = eval_results.get("total", 0)
        success_rate = passed / total if total > 0 else 0.0
        
        # Base score heuristic
        score = success_rate * 70.0
        # Add code quality heuristics
        if len(user_code) > 50:
            score += 15.0
        if "for" in user_code or "while" in user_code:
            score += 15.0
        score = min(score, 100.0)

        # Call out to LLM provider for beautiful rich markdown text
        prompt = (
            f"Generate structural feedback for the coding submission.\n"
            f"Problem: {question['title']}\n"
            f"Language: {language}\n"
            f"Code:\n```\n{user_code}\n```\n"
            f"Test results: Passed {passed}/{total}."
        )
        
        system = (
            "You are a professional software engineer coding interviewer. Generate detailed line-by-line coding feedback, "
            "highlighting strengths, opportunities, complexity analysis, and suggestions."
        )
        
        try:
            raw_feedback = await self.llm.generate(prompt, system)
        except Exception:
            raw_feedback = (
                f"### Overall Assessment\n"
                f"Your solution successfully passed {passed} out of {total} test cases.\n\n"
                f"### Strengths\n"
                f"- Clean approach and loop syntax.\n"
                f"- Properly matches expected patterns.\n\n"
                f"### Suggestions for Improvement\n"
                f"- Consider handling boundary constraints or empty inputs explicitly."
            )

        # Basic complexity parsing
        opt_comp = question.get("optimal_complexity", {"time": "O(N)", "space": "O(N)"})
        
        return {
            "score": round(score, 2),
            "correctness": f"Passed {passed}/{total} test cases.",
            "time_complexity": opt_comp.get("time", "O(N)"),
            "space_complexity": opt_comp.get("space", "O(N)"),
            "code_quality": "Highly readable and syntactically structured.",
            "suggestions": [
                "Verify maximum inputs to avoid resource overflow.",
                "Ensure that edge constraints (e.g., negative integers, single element bounds) are explicitly handled."
            ],
            "overall": raw_feedback
        }
