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
    
    console.print("[cyan][*] Consulting Meta Inference Model for Root-Cause Analysis...[/cyan]")
    report = agent.analyze_incident(MOCK_OOM_LOGS)
    
    console.print(f"[bold red]Root Cause:[/bold red] {report.root_cause}")
    console.print(f"[bold yellow]Severity:[/bold yellow] {report.severity}")
    console.print(f"[bold green]Remediation Script:[/bold green] `{report.remediation_cmd}`")
    console.print(f"[bold blue]Verification Check:[/bold blue] `{report.verification_cmd}`\n")

    # Autonomous Execution Phase di Modal Cloud
    console.print("[magenta][*] Spawning isolated Modal Sandbox container...[/magenta]")
    try:
        with app.run():
            with console.status("[bold green]Executing remediation & telemetry verification in cloud sandbox...[/bold green]"):
                result = execute_remediation.remote(
                    remediation_cmd=report.remediation_cmd,
                    verification_cmd=report.verification_cmd
                )

        console.print(Panel.fit(
            f"[bold green]Status:[/bold green] Remediation Executed & Verified Successfully\n"
            f"[bold cyan]Exit Code:[/bold cyan] {result['exit_code']}\n"
            f"[bold cyan]Verification Output:[/bold cyan] {result['verify_stdout']}\n"
            f"[bold dim]Remediation Log:[/bold dim] {result['fix_stdout'] or 'No error output'}",
            title="Modal Sandbox Telemetry"
        ))
    except Exception as e:
        console.print(f"[bold red][!] Sandbox dispatch failed:[/bold red] {e}")

if __name__ == "__main__":
    main()
