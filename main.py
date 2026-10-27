import sys
from rich.console import Console
from rich.panel import Panel
from agent.core import SREAgent
from scenarios.mock_failure import MOCK_OOM_LOGS

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
    console.print(f"[bold blue]Verification Check:[/bold blue] `{report.verification_cmd}`")

if __name__ == "__main__":
    main()
