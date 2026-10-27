import os
import sys
from rich.console import Console
from rich.panel import Panel

from agent.core import SREAgent
from scenarios.mock_failure import MOCK_OOM_LOGS
from sandbox.executor import app, execute_remediation

console = Console()

def main():
    console.print(Panel.fit("[bold green]OpsAegis[/bold green] - Autonomous SRE Remediation Agent", subtitle="Meta Hackathon 2026"))
    
    agent = SREAgent()
    console.print("[yellow][*] Ingesting telemetry failure trace...[/yellow]")
    console.print(f"[dim]{MOCK_OOM_LOGS.strip()}[/dim]\n")
    
    feedback = None
    max_retries = 2

    with app.run():
        for attempt in range(1, max_retries + 1):
            console.print(f"[cyan][*] Consulting Muse Spark Open (Iteration {attempt})...[/cyan]")
            report = agent.analyze_incident(MOCK_OOM_LOGS, error_feedback=feedback)
            
            console.print(f"[bold red]Root Cause:[/bold red] {report.root_cause}")
            console.print(f"[bold yellow]Severity:[/bold yellow] {report.severity}")
            console.print(f"[bold green]Remediation Script:[/bold green] `{report.remediation_cmd}`")
            console.print(f"[bold blue]Verification Check:[/bold blue] `{report.verification_cmd}`\n")

            console.print("[magenta][*] Dispatching remediation to isolated Modal Sandbox...[/magenta]")
            with console.status("[bold green]Executing & verifying in cloud container...[/bold green]"):
                result = execute_remediation.remote(
                    remediation_cmd=report.remediation_cmd,
                    verification_cmd=report.verification_cmd
                )

            if result["exit_code"] == 0:
                console.print(Panel.fit(
                    f"[bold green]Status:[/bold green] Remediation Succeeded & Verified!\n"
                    f"[bold cyan]Exit Code:[/bold cyan] 0\n"
                    f"[bold cyan]Verification Output:[/bold cyan] {result['verify_stdout'].strip() or 'Healthy'}",
                    title="Modal Sandbox Telemetry"
                ))
                break
            else:
                console.print(Panel.fit(
                    f"[bold red]Status:[/bold red] Execution Failed!\n"
                    f"[bold yellow]Exit Code:[/bold yellow] {result['exit_code']}\n"
                    f"[bold red]Stderr:[/bold red] {result['fix_stderr'] or result['verify_stderr'] or 'Command failed'}",
                    title="Self-Correction Triggered"
                ))
                feedback = f"Exit code {result['exit_code']}: {result['fix_stderr'] or result['verify_stderr']}"

if __name__ == "__main__":
    main()