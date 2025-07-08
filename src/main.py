import asyncio

from rich.prompt import Prompt

from src.utils.ui_interface import show_menu, run_processing, show_alerts, create_report, show_stats
from src.utils.ui_interface import console
from src.utils.processing import analyzer, logger


def show_ui():

    while True:
        show_menu()
        choice = Prompt.ask("Choisir une option", choices=[str(i) for i in range(1,6)])
        if choice == "1":
            run_processing()
        elif choice == "2":
            if analyzer is None or logger is None:
                console.print("[bold red]⚠️ Veuillez d'abord lancer le traitement des logs ! (Option 1)[/bold red]")
                continue
            show_alerts()
        elif choice == "3":
            if analyzer is None or logger is None:
                console.print("[bold red]⚠️ Veuillez d'abord lancer le traitement des logs ! (Option 1)[/bold red]")
                continue
            create_report()
        elif choice == "4":
            if analyzer is None or logger is None:
                console.print("[bold red]⚠️ Veuillez d'abord lancer le traitement des logs ! (Option 1)[/bold red]")
                continue
            show_stats()
        else:
            console.print("[bold red]👋 Au revoir ![/bold red]")
            break


if __name__ == "__main__":
    show_ui()