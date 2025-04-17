"""Utilitários para manipulação do console."""

import os
from colorama import Fore, init

# Inicializa o colorama
init(autoreset=True)


def clear_screen() -> None:
    """Limpa a tela do console."""
    os.system("cls" if os.name == "nt" else "clear")


def get_logo() -> str:
    """Retorna o logo do programa em ASCII art."""
    return f"""{Fore.WHITE}
    ██╗      █████╗ ███████╗██╗   ██╗{Fore.WHITE}██████╗ ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗
    ██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝{Fore.WHITE}██╔══██╗██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝
    ██║     ███████║  ███╔╝  ╚████╔╝ {Fore.WHITE}██████╔╝█████╗  ███████║██║  ██║██╔████╔██║█████╗
    ██║     ██╔══██║ ███╔╝    ╚██╔╝  {Fore.WHITE}██╔══██╗██╔══╝  ██╔══██║██║  ██║██║╚██╔╝██║██╔══╝
    ███████╗██║  ██║███████╗   ██║   {Fore.WHITE}██║  ██║███████╗██║  ██║██████╔╝██║ ╚═╝ ██║███████╗
    ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   {Fore.WHITE}╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚══════╝
"""


def print_header() -> None:
    """Imprime o cabeçalho do programa."""
    print(get_logo())
    print(f"{Fore.YELLOW}{'='*80}")
    print(f"{Fore.GREEN}✨ Gerador automático de README para seus projetos")
    print(f"{Fore.CYAN}🚀 Crie READMEs profissionais em segundos!")
    print(f"{Fore.YELLOW}{'='*80}\n")
