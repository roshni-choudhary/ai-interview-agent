"""
Code evaluation service.
Executes user-submitted code against test cases in sandboxed subprocesses.
Supports Python, JavaScript, and C++ with per-test-case timeouts.
"""

import asyncio
import json
import os
import shutil
import tempfile
import time
from typing import Any

from app.sandbox.executor import SandboxExecutor


class CodeEvaluator:
    """Evaluate user code against test cases by running each in a subprocess."""

    TIMEOUT: int = 5  # seconds per test case

    def __init__(self):
        self.sandbox = SandboxExecutor()
        self.sandbox.TIMEOUT = self.TIMEOUT

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def evaluate(
        self,
        code: str,
        language: str,
        test_cases: list[dict],
    ) -> dict:
        """
        Run code against all test_cases and return aggregate results.

        Each test_case is a dict with:
            input: dict of argument name -> value
            expected_output: the expected return value

        Returns:
            {
                passed: int,
                total: int,
                all_passed: bool,
                results: [{input, expected, actual, passed, error, execution_time_ms}],
                overall_time_ms: float
            }
        """
        lang = language.lower().strip()
        dispatch = {
            "python": self.evaluate_python,
            "py": self.evaluate_python,
            "python3": self.evaluate_python,
            "javascript": self.evaluate_javascript,
            "js": self.evaluate_javascript,
            "node": self.evaluate_javascript,
            "cpp": self.evaluate_cpp,
            "c++": self.evaluate_cpp,
        }
        evaluator = dispatch.get(lang)
        if evaluator is None:
            return {
                "passed": 0,
                "total": len(test_cases),
                "all_passed": False,
                "results": [
                    {
                        "input": tc.get("input", {}),
                        "expected": tc.get("expected_output"),
                        "actual": None,
                        "passed": False,
                        "error": f"Unsupported language: {language}",
                        "execution_time_ms": 0,
                    }
                    for tc in test_cases
                ],
                "overall_time_ms": 0.0,
            }
        return await evaluator(code, test_cases)

    # ------------------------------------------------------------------
    # Python evaluator
    # ------------------------------------------------------------------

    async def evaluate_python(self, code: str, test_cases: list[dict]) -> dict:
        results = []
        overall_start = time.perf_counter()

        for tc in test_cases:
            harness = self._create_python_harness(code, tc)
            result = await self.sandbox.execute_python(harness)
            tc_result = self._parse_result(result, tc)
            results.append(tc_result)

        overall_ms = (time.perf_counter() - overall_start) * 1000
        passed = sum(1 for r in results if r["passed"])
        return {
            "passed": passed,
            "total": len(results),
            "all_passed": passed == len(results),
            "results": results,
            "overall_time_ms": round(overall_ms, 2),
        }

    # ------------------------------------------------------------------
    # JavaScript evaluator
    # ------------------------------------------------------------------

    async def evaluate_javascript(self, code: str, test_cases: list[dict]) -> dict:
        results = []
        overall_start = time.perf_counter()

        for tc in test_cases:
            harness = self._create_js_harness(code, tc)
            result = await self.sandbox.execute_javascript(harness)
            tc_result = self._parse_result(result, tc)
            results.append(tc_result)

        overall_ms = (time.perf_counter() - overall_start) * 1000
        passed = sum(1 for r in results if r["passed"])
        return {
            "passed": passed,
            "total": len(results),
            "all_passed": passed == len(results),
            "results": results,
            "overall_time_ms": round(overall_ms, 2),
        }

    # ------------------------------------------------------------------
    # C++ evaluator
    # ------------------------------------------------------------------

    async def evaluate_cpp(self, code: str, test_cases: list[dict]) -> dict:
        results = []
        overall_start = time.perf_counter()

        for tc in test_cases:
            harness = self._create_cpp_harness(code, tc)
            result = await self.sandbox.execute_cpp(harness)
            tc_result = self._parse_result(result, tc)
            results.append(tc_result)

        overall_ms = (time.perf_counter() - overall_start) * 1000
        passed = sum(1 for r in results if r["passed"])
        return {
            "passed": passed,
            "total": len(results),
            "all_passed": passed == len(results),
            "results": results,
            "overall_time_ms": round(overall_ms, 2),
        }

    # ------------------------------------------------------------------
    # Harness generators
    # ------------------------------------------------------------------

    def _create_python_harness(self, code: str, test_case: dict) -> str:
        """
        Create an executable Python script that:
        1. Defines the user's code
        2. Calls the function with test inputs
        3. Prints a JSON result line for parsing
        """
        tc_input = test_case.get("input", {})
        expected = test_case.get("expected_output")

        # Detect function name from the user code
        func_name = self._detect_python_function_name(code)

        # Build argument list
        args_code = ", ".join(
            f"{k}={json.dumps(v)}" for k, v in tc_input.items()
        )

        harness = f'''import json
import sys
import traceback

# --- User code ---
{code}
# --- End user code ---

def __run_test():
    try:
        result = {func_name}({args_code})
        expected = {json.dumps(expected)}
        # Normalize for comparison
        result_normalized = json.loads(json.dumps(result, default=str))
        expected_normalized = json.loads(json.dumps(expected, default=str))

        # For lists that could be in any order (like Two Sum), try sorted comparison too
        passed = result_normalized == expected_normalized
        if not passed and isinstance(result_normalized, list) and isinstance(expected_normalized, list):
            try:
                if sorted(result_normalized) == sorted(expected_normalized):
                    passed = True
            except TypeError:
                # Elements not sortable (e.g., nested lists)
                try:
                    if sorted(map(str, result_normalized)) == sorted(map(str, expected_normalized)):
                        passed = True
                except Exception:
                    pass

        print(json.dumps({{"__result__": result, "__passed__": passed, "__error__": None}}))
    except Exception as e:
        tb = traceback.format_exc()
        print(json.dumps({{"__result__": None, "__passed__": False, "__error__": str(e), "__traceback__": tb}}))

__run_test()
'''
        return harness

    def _create_js_harness(self, code: str, test_case: dict) -> str:
        """Create an executable Node.js script for a test case."""
        tc_input = test_case.get("input", {})
        expected = test_case.get("expected_output")

        func_name = self._detect_js_function_name(code)

        # Build argument list
        args_parts = [json.dumps(v) for v in tc_input.values()]
        args_str = ", ".join(args_parts)

        harness = f'''// --- User code ---
{code}
// --- End user code ---

(function() {{
    try {{
        const result = {func_name}({args_str});
        const expected = {json.dumps(expected)};

        let passed = JSON.stringify(result) === JSON.stringify(expected);
        if (!passed && Array.isArray(result) && Array.isArray(expected)) {{
            try {{
                passed = JSON.stringify([...result].sort()) === JSON.stringify([...expected].sort());
            }} catch(e) {{}}
        }}

        console.log(JSON.stringify({{__result__: result, __passed__: passed, __error__: null}}));
    }} catch(e) {{
        console.log(JSON.stringify({{__result__: null, __passed__: false, __error__: e.message}}));
    }}
}})();
'''
        return harness

    def _create_cpp_harness(self, code: str, test_case: dict) -> str:
        """
        Create a compilable C++ source that wraps user code with a test main().
        This is simplified — works best with standalone function signatures.
        """
        tc_input = test_case.get("input", {})
        expected = test_case.get("expected_output")

        func_name = self._detect_cpp_function_name(code)

        # Build a simple C++ main that calls the function and prints result
        args_parts = []
        setup_lines = []
        for i, (k, v) in enumerate(tc_input.items()):
            cpp_val, cpp_type, setup = self._python_val_to_cpp(v, f"arg{i}")
            args_parts.append(f"arg{i}")
            setup_lines.extend(setup)

        args_str = ", ".join(args_parts)
        setup_code = "\n    ".join(setup_lines)

        expected_cpp, _, expected_setup = self._python_val_to_cpp(expected, "expected")
        expected_setup_code = "\n    ".join(expected_setup)

        harness = f'''#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <sstream>
#include <queue>
#include <stack>
#include <list>

using namespace std;

// --- User code ---
{code}
// --- End user code ---

template<typename T>
void printVal(const T& v) {{ cout << v; }}

template<typename T>
void printVal(const vector<T>& v) {{
    cout << "[";
    for (int i = 0; i < v.size(); i++) {{
        if (i) cout << ",";
        printVal(v[i]);
    }}
    cout << "]";
}}

void printVal(const string& s) {{ cout << "\\"" << s << "\\""; }}
void printVal(bool b) {{ cout << (b ? "true" : "false"); }}

int main() {{
    try {{
        {setup_code}
        {expected_setup_code}

        auto result = {func_name}({args_str});

        bool passed = (result == expected);
        cout << "{{\\"__passed__\\":" << (passed ? "true" : "false") << ",\\"__error__\\":null,\\"__result__\\":";
        printVal(result);
        cout << "}}" << endl;
    }} catch (const exception& e) {{
        cout << "{{\\"__passed__\\":false,\\"__error__\\":\\"" << e.what() << "\\",\\"__result__\\":null}}" << endl;
    }}
    return 0;
}}
'''
        return harness

    # ------------------------------------------------------------------
    # Result parsing
    # ------------------------------------------------------------------

    def _parse_result(self, exec_result: dict, test_case: dict) -> dict:
        """Parse subprocess output into a standardised test-case result."""
        tc_input = test_case.get("input", {})
        expected = test_case.get("expected_output")

        if exec_result.get("timed_out"):
            return {
                "input": tc_input,
                "expected": expected,
                "actual": None,
                "passed": False,
                "error": "Time Limit Exceeded",
                "execution_time_ms": exec_result.get("execution_time_ms", 0),
            }

        stdout = exec_result.get("stdout", "").strip()
        stderr = exec_result.get("stderr", "").strip()

        # Try to parse the JSON output line
        try:
            # Find the last line that looks like JSON
            lines = stdout.split("\n")
            json_line = None
            for line in reversed(lines):
                line = line.strip()
                if line.startswith("{") and "__result__" in line:
                    json_line = line
                    break

            if json_line:
                data = json.loads(json_line)
                return {
                    "input": tc_input,
                    "expected": expected,
                    "actual": data.get("__result__"),
                    "passed": data.get("__passed__", False),
                    "error": data.get("__error__"),
                    "execution_time_ms": exec_result.get("execution_time_ms", 0),
                }
        except (json.JSONDecodeError, Exception):
            pass

        # Fallback: execution error
        error_msg = stderr or stdout or f"Exit code: {exec_result.get('exit_code')}"
        return {
            "input": tc_input,
            "expected": expected,
            "actual": None,
            "passed": False,
            "error": error_msg[:500],
            "execution_time_ms": exec_result.get("execution_time_ms", 0),
        }

    # ------------------------------------------------------------------
    # Function name detection
    # ------------------------------------------------------------------

    @staticmethod
    def _detect_python_function_name(code: str) -> str:
        """Extract the first def'd function name from Python code."""
        import re
        # Look for `def functionName(` but skip __init__, __run, etc.
        for match in re.finditer(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code, re.MULTILINE):
            name = match.group(1)
            if not name.startswith("__"):
                return name
        # Check for class-based solutions
        class_match = re.search(r"class\s+(\w+)", code)
        if class_match:
            return class_match.group(1)
        return "solution"

    @staticmethod
    def _detect_js_function_name(code: str) -> str:
        """Extract function name from JS code."""
        import re
        # function name(
        match = re.search(r"function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(", code)
        if match:
            return match.group(1)
        # const name = (
        match = re.search(r"(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(?:\(|function)", code)
        if match:
            return match.group(1)
        return "solution"

    @staticmethod
    def _detect_cpp_function_name(code: str) -> str:
        """Extract function name from C++ code (outside of class)."""
        import re
        # Look for standalone functions (not inside class)
        matches = re.findall(
            r"(?:int|void|bool|double|float|string|vector\s*<[^>]+>)\s+([a-zA-Z_]\w*)\s*\(",
            code,
        )
        for name in matches:
            if name not in ("main", "Solution"):
                return name
        # Check for class with public method
        method_match = re.search(
            r"class\s+Solution\s*\{[^}]*?(?:int|void|bool|double|float|string|vector\s*<[^>]+>)\s+([a-zA-Z_]\w*)\s*\(",
            code,
            re.DOTALL,
        )
        if method_match:
            return f"Solution().{method_match.group(1)}"
        return "solution"

    # ------------------------------------------------------------------
    # C++ value conversion helpers
    # ------------------------------------------------------------------

    def _python_val_to_cpp(
        self, val: Any, var_name: str
    ) -> tuple[str, str, list[str]]:
        """
        Convert a Python value to C++ variable declaration.
        Returns (cpp_expression, cpp_type, list_of_setup_lines).
        """
        if isinstance(val, bool):
            return str(val).lower(), "bool", [f"bool {var_name} = {str(val).lower()};"]
        if isinstance(val, int):
            return str(val), "int", [f"int {var_name} = {val};"]
        if isinstance(val, float):
            return str(val), "double", [f"double {var_name} = {val};"]
        if isinstance(val, str):
            escaped = val.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"', "string", [f'string {var_name} = "{escaped}";']
        if isinstance(val, list):
            if not val:
                return "{}", "vector<int>", [f"vector<int> {var_name} = {{}};"]
            first = val[0]
            if isinstance(first, list):
                # 2D vector
                inner_type = "int"
                if first and isinstance(first[0], str):
                    inner_type = "string"
                rows = []
                for row in val:
                    if inner_type == "string":
                        items = ", ".join(f'"{x}"' for x in row)
                    else:
                        items = ", ".join(str(x) for x in row)
                    rows.append(f"{{{items}}}")
                init = ", ".join(rows)
                return f"{{{init}}}", f"vector<vector<{inner_type}>>", [
                    f"vector<vector<{inner_type}>> {var_name} = {{{init}}};"
                ]
            if isinstance(first, str):
                items = ", ".join(f'"{x}"' for x in val)
                return f"{{{items}}}", "vector<string>", [
                    f"vector<string> {var_name} = {{{items}}};"
                ]
            if isinstance(first, bool):
                items = ", ".join(str(x).lower() for x in val)
                return f"{{{items}}}", "vector<bool>", [
                    f"vector<bool> {var_name} = {{{items}}};"
                ]
            # Default: int vector
            items = ", ".join(str(x) for x in val)
            return f"{{{items}}}", "vector<int>", [
                f"vector<int> {var_name} = {{{items}}};"
            ]
        if val is None:
            return "0", "int", [f"int {var_name} = 0;"]
        # Fallback
        return str(val), "auto", [f"auto {var_name} = {val};"]
