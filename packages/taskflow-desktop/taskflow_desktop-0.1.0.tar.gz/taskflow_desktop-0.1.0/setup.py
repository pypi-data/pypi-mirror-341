#!/usr/bin/env python3
"""
Configuração de instalação para o projeto TaskFlow.
Este script delega a configuração para o pyproject.toml.
"""

if __name__ == "__main__":
    try:
        from setuptools import setup  # type: ignore
        setup()
    except Exception as e:
        import sys
        print(f"Erro durante o setup: {str(e)}", file=sys.stderr)
        sys.exit(1)
