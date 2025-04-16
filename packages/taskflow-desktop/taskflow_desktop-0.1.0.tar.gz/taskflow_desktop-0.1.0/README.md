# TaskFlow: Comprehensive Task Management Application

![Project Status](https://img.shields.io/badge/status-alpha-yellow)
![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/github/actions/workflow/status/ertonmiranda/taskflow/ci.yml)
![Coverage](https://img.shields.io/codecov/c/github/ertonmiranda/taskflow)
![Last Commit](https://img.shields.io/github/last-commit/ertonmiranda/taskflow)

## 🚀 Visão Geral do Projeto

TaskFlow é uma aplicação de gerenciamento de tarefas desenvolvida em Python, utilizando PyQt6 para interface gráfica e SQLAlchemy para persistência de dados.

### 🌟 Recursos Principais

- Interface gráfica moderna com PyQt6
- Gerenciamento de tarefas robusto
- Persistência de dados com SQLAlchemy
- Suporte a múltiplas plataformas
- Configurações de segurança avançadas

## 📋 Requisitos do Sistema

- **Sistema Operacional**: Windows 10/11, Linux, macOS
- **Python**: 3.8 - 3.10
- **Dependências**: Listadas em `requirements.txt`

## 🛠️ Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

1. **Python**: Instale Python 3.8+
   - [Download Python](https://www.python.org/downloads/)
   - Certifique-se de adicionar Python ao PATH do sistema

2. **Ferramentas Necessárias**:
   - Git
   - PowerShell (para Windows)
   - Pre-commit

### Configuração Automática (Recomendado)

#### Windows

1. Abra o PowerShell como Administrador
2. Clone o repositório:

   ```powershell
   git clone https://github.com/seu-usuario/taskflow.git
   cd taskflow
   ```

3. Execute o script de configuração:

   ```powershell
   .\scripts\setup_env.ps1
   ```

#### Linux/macOS

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/taskflow.git
   cd taskflow
   ```

2. Execute o script de configuração:

   ```bash
   ./scripts/setup_env.sh
   ```

### Configuração Manual

1. Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

2. Ative o ambiente virtual:
   - Windows: `.venv\Scripts\Activate`
   - Linux/macOS: `source .venv/bin/activate`

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. Instale o projeto em modo editável:

   ```bash
   pip install -e .
   ```

5. Configure pre-commit:

   ```bash
   pre-commit install
   ```

## 🧪 Executando Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura de código
pytest --cov=src
```

## 🔍 Ferramentas de Desenvolvimento

- **Formatação**: Black
- **Linting**: Flake8, Pylint
- **Tipagem**: Mypy
- **Testes**: Pytest
- **Pré-commit**: Verificações de qualidade de código

### Comandos Úteis

```bash
# Formatar código
black .

# Verificar tipos
mypy .

# Executar linters
flake8 .

# Verificar importações
isort .
```

## 📦 Estrutura do Projeto

```diretorio
taskflow/
│
├── src/                # Código fonte principal
│   └── taskflow/
│       ├── models/
│       ├── views/
│       ├── controllers/
│       └── utils/
│
├── tests/              # Testes automatizados
├── scripts/            # Utilitários e scripts
├── docs/               # Documentação
├── config/             # Configurações
└── .venv/              # Ambiente virtual
```

## 🔒 Políticas de Segurança

- Senhas criptografadas com bcrypt
- Validação de entrada
- Logging de segurança
- Controle de acesso baseado em função

## 🤝 Contribuindo

1. Faça fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Diretrizes de Contribuição

- Siga os padrões de código do projeto
- Escreva testes para novas funcionalidades
- Mantenha a cobertura de código acima de 80%
- Documente suas alterações

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

### **Erton Miranda**

- Email: <erton.miranda@example.com>
- GitHub: [@ertonmiranda](https://github.com/ertonmiranda)

---Texto
**Última Atualização**: $(date +'%Y-%m-%d')

## Static Code Analysis

The TaskFlow project uses multiple tools to ensure code quality and maintain high standards:

### Tools Used

- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Linting
- **Pylint**: Advanced linting
- **MyPy**: Static type checking
- **Bandit**: Security analysis

### Running Static Analysis

To run all static analysis tools:

```bash
python scripts/static_analysis.py
```

### Pre-commit Hooks

We use pre-commit hooks to automatically run checks before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Set up pre-commit hooks
pre-commit install
```

### Configuration

Static analysis tools are configured in:

- `pyproject.toml`: Tool-specific configurations
- `.pre-commit-config.yaml`: Pre-commit hook settings

### Code Quality Standards

- Maximum line length: 88 characters
- Minimum test coverage: 80%
- Strict type checking
- Security vulnerability scanning

## 🚀 Continuous Integration & Deployment (CI/CD)

### Workflow Overview

Our CI/CD pipeline ensures code quality, security, and seamless deployment:

#### Stages

1. **Code Quality Checks**
   - Code formatting (Black)
   - Import sorting (isort)
   - Linting (Flake8, Pylint)
   - Type checking (MyPy)

2. **Security Analysis**
   - Vulnerability scanning (Bandit)
   - Dependency security checks (Safety)
   - Software Bill of Materials (SBOM) generation

3. **Testing**
   - Unit tests across multiple Python versions
   - Cross-platform testing (Linux, Windows, macOS)
   - Code coverage reporting

4. **Build & Publish**
   - Automatic package building
   - PyPI publication
   - GitHub release creation

### Deployment Triggers

- **Main Branch**: Automatic deployment
- **Pull Requests**: Validation checks

### Secrets Configuration

Configure the following GitHub Secrets:

- `PYPI_USERNAME`: PyPI username
- `PYPI_PASSWORD`: PyPI token
- `SLACK_WEBHOOK`: Slack notification webhook (optional)

### Manual Deployment

```bash
# Trigger semantic release manually
npx semantic-release
```

### Monitoring

- **Coverage**: Codecov integration
- **Notifications**: Slack alerts
- **Release Notes**: Automatically generated
