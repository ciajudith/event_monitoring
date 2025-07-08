import asyncio
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table


from src.utils.processing import process_logs, get_alerts, generate_report, get_level_counts
from src.utils.plot_generation import plot_level_counts

console = Console(force_terminal=True, markup=True)

def show_menu():
    console.clear()
    console.print("[bold cyan]=== Menu Principal ===[/bold cyan]\n")
    console.print("1) Lancer le traitement des logs")
    console.print("2) Afficher les alertes détectées")
    console.print("3) Générer le rapport de fin de traitement")
    console.print("4) Visualiser les statistiques (histogramme)")
    console.print("5) Quitter\n")

def run_processing():
    console.print("[yellow]🔄 Traitement des logs en cours...[/yellow]")
    asyncio.run(process_logs())
    console.print("[green]✅ Traitement terminé ![/green]")
    Prompt.ask("Appuyez sur [bold]Entrée[/] pour continuer")

def show_alerts():
    alerts = get_alerts()
    if not alerts:
        console.print("[bold red]Aucune alerte détectée.[/bold red]")
    else:
        table = Table(title="Alertes détectées")
        table.add_column("Début", style="cyan")
        table.add_column("Fin", style="cyan")
        table.add_column("Count", justify="right")
        for a in alerts:
            table.add_row(a["start"], a["end"], str(a["count"]))
        console.print(table)
    Prompt.ask("Appuyez sur [bold]Entrée[/] pour revenir au menu")

def create_report():
    with console.status("[cyan]Génération du rapport en cours…[/cyan]", spinner="dots"):
        path = generate_report()
    console.print(f"[green]✅ Rapport généré : {path}[/green]")
    Prompt.ask("Appuyez sur [bold]Entrée[/] pour revenir au menu")

def show_stats():
    counts = get_level_counts()
    with console.status("[cyan]Préparation de l’histogramme…[/cyan]", spinner="line"):
        plot_level_counts(
            level_counts=counts,
            save_path=None,
            show=True,
        )
    console.print("[green]📊 Histogramme affiché ![/green]")
    Prompt.ask("Appuyez sur Entrée pour revenir au menu")


