import streamlit as st
import time
from agent.core import SREAgent
from scenarios.mock_failure import MOCK_OOM_LOGS
from sandbox.executor import app as modal_app, execute_remediation

st.set_page_config(page_title="OpsAegis - SRE Agent", layout="wide", page_icon="🛡️")

st.title("🛡️ OpsAegis: Autonomous SRE Remediation Agent")
st.caption("Powered by Meta Muse Spark Open & Modal Serverless Cloud Sandboxes")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📥 Telemetry & Ingestion")
    st.code(MOCK_OOM_LOGS.strip(), language="text")
    trigger = st.button("🚨 Simulate Incident & Trigger Remediation", type="primary")

if trigger:
    agent = SREAgent()
    
    with col_right:
        st.subheader("🧠 Meta Muse Spark Open (Root Cause Analysis)")
        with st.spinner("Analyzing kernel trace via Baseten Inference..."):
            report = agent.analyze_incident(MOCK_OOM_LOGS)
        
        st.markdown(f"**Root Cause:** `{report.root_cause}`")
        st.markdown(f"**Severity:** :red[{report.severity.upper()}]")
        st.code(f"# Remediation Plan\n{report.remediation_cmd}", language="bash")
        st.code(f"# Verification Check\n{report.verification_cmd}", language="bash")

        st.subheader("☁️ Modal Sandbox Execution")
        with st.spinner("Spawning container, injecting failure & executing fix..."):
            with modal_app.run():
                result = execute_remediation.remote(
                    remediation_cmd=report.remediation_cmd,
                    verification_cmd=report.verification_cmd
                )

        if result["exit_code"] == 0:
            st.success("✅ Status: Remediation Succeeded & Verified (Exit Code 0)")
            st.info(f"Verification Output: {result['verify_stdout'].strip() or 'Clean'}")
        else:
            st.error(f"❌ Execution Failed (Exit Code {result['exit_code']})")
            st.code(result["fix_stderr"] or result["verify_stderr"])