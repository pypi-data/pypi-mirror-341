"""Ponto de entrada da aplicação TaskFlow."""

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from taskflow.config import Config
from taskflow.ui import MainWindow


def main() -> None:
    """Função principal da aplicação."""
    # Carrega configuração
    config_path = Path("config/development.yaml")
    if not config_path.exists():
        config_path = Path("config/production.yaml")

    config = Config(config_path)

    # Inicia aplicação Qt
    app = QApplication(sys.argv)

    # Cria e exibe janela principal
    window = MainWindow(config)
    window.show()

    # Executa loop de eventos
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
