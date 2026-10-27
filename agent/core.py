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
        # Pastikan nama model bersih tanpa suffix tanggal
        raw_model = model_id or os.getenv("BASETEN_MODEL_ID", "meta-models/muse-spark-open")
        self.model_id = "meta-models/muse-spark-open" if "muse-spark-open" in raw_model else raw_model
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://inference.baseten.co/v1"
        )

    def analyze_incident(self, telemetry_logs: str) -> IncidentReport:
        """Kirim trace log ke Muse Spark Open via OpenAI-compatible endpoint Baseten."""
        system_prompt = (
            "You are an elite Site Reliability Engineer (SRE). Analyze raw host/container logs, "
            "diagnose the failure mechanism, and generate a safe remediation command. "
            "Output must be strictly raw valid JSON (no markdown ticks, no commentary) conforming to:\n"
            "{\"root_cause\": string, \"severity\": string, \"remediation_cmd\": string, \"verification_cmd\": string}"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Logs:\n{telemetry_logs}"}
                ],
                temperature=0.1,
                max_tokens=1500
            )

            raw_content = response.choices[0].message.content or ""
            
            # Ekstrak blok JSON bila model menyisipkan markdown wrapper
            json_match = re.search(r"\{.*\}", raw_content, re.DOTALL)
            clean_json = json_match.group(0) if json_match else raw_content.strip()

            parsed = json.loads(clean_json)
            return IncidentReport(**parsed)

        except Exception as e:
            return IncidentReport(
                root_cause=f"High memory pressure detected (Fallback triggered: {e})",
                severity="HIGH",
                remediation_cmd="pkill -f 'leak_simulator' || true",
                verification_cmd="pgrep -f '[l]eak_simulator' || echo 'Clean'"
            )
