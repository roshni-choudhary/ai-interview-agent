import subprocess
import tempfile
import os
import sys
import time
from typing import Dict, Any

class SandboxExecutor:
    async def execute_python(self, code: str, timeout: float = 5.0) -> Dict[str, Any]:
        # Safely execute python in an isolated subprocess to capture standard output/errors
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code.encode("utf-8"))
            tmp_path = tmp.name

        start_time = time.time()
        try:
            # Run the python file in a subprocess with resource limits (timeout)
            process = subprocess.Popen(
                [sys.executable, tmp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                exit_code = process.returncode
                timed_out = False
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                exit_code = -1
                timed_out = True

            elapsed = (time.time() - start_time) * 1000.0
            
            return {
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": exit_code,
                "execution_time_ms": round(elapsed, 2),
                "timed_out": timed_out
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1,
                "execution_time_ms": 0.0,
                "timed_out": False
            }
        finally:
            # Clean up the temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
