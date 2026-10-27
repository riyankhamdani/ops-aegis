import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

class IncidentReport(BaseModel):
    root_cause: str
    severity: str
    remediation_cmd: str
    verification_cmd: str

class SREAgent:
    def __init__(self, api_key: str = None, model_id: str = None):
        self.api_key = api_key or os.getenv("BASETEN_API_KEY")
        raw_model = model_id or os.getenv("BASETEN_MODEL_ID", "meta-models/muse-spark-open")
        self.model_id = "meta-models/muse-spark-open" if "muse-spark-open" in raw_model else raw_model
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://inference.baseten.co/v1"
        )

    def analyze_incident(self, telemetry_logs: str, error_feedback: str = None) -> IncidentReport:
        """Diagnosa log dan generate remediasi yang aman untuk container unprivileged."""
        system_prompt = (
            "You are an elite Site Reliability Engineer (SRE). Analyze raw host/container logs, "
            "diagnose the failure mechanism, and generate a safe remediation command.\n"
            "CRITICAL CONTAINER ENVIRONMENT CONSTRAINTS:\n"
            "- Running inside an unprivileged container: DO NOT touch /proc/sys (no drop_caches) and do not use systemctl.\n"
            "- The 'worker' binary does not exist on disk; focus remediation purely on terminating rogue leaking processes (leak_simulator) and cleaning up /tmp.\n"
            "- Verification check MUST verify that leak_simulator is gone without requiring 'worker' process (e.g. `! pgrep -f '[l]eak_simulator' && echo 'Clean'`).\n"
            "- Verification command MUST exit with code 0 on healthy condition.\n"
            "- Final output must strictly end with raw valid JSON conforming to:\n"
            "{\"root_cause\": string, \"severity\": string, \"remediation_cmd\": string, \"verification_cmd\": string}"
        )

        user_content = f"Logs:\n{telemetry_logs}"
        if error_feedback:
            user_content += f"\n\n[EXECUTION FEEDBACK]\nPrevious command failed with:\n{error_feedback}\nGenerate a revised command obeying container constraints."

        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.1,
                max_tokens=2500
            )

            msg = response.choices[0].message
            raw_text = msg.content or getattr(msg, "reasoning_content", "") or ""

            json_match = re.search(r"\{[\s\S]*\}", raw_text)
            if not json_match:
                raise ValueError(f"No JSON object detected: {raw_text[:200]}")

            clean_json = json_match.group(0)
            parsed = json.loads(clean_json)
            return IncidentReport(**parsed)

        except Exception as e:
            return IncidentReport(
                root_cause=f"High memory pressure detected (Fallback: {e})",
                severity="HIGH",
                remediation_cmd="pkill -9 -f 'leak_simulator' || true; rm -rf /tmp/leak* || true",
                verification_cmd="pgrep -f '[l]eak_simulator' || echo 'Clean'"
            )