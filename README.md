# 🚀 Projeto Hello World Terraform

Este repositório contém a infraestrutura como código utilizando **Terraform** para deploy de uma função Lambda na AWS.

## 📌 Fluxo de Trabalho com Git

### 🔀 Branches

- `main`: branch principal e protegida.
- `dev`: branch de desenvolvimento, também protegida.
- Novas funcionalidades ou correções devem ser criadas a partir da branch `dev`.

### 📁 Convenção de Nomes de Branches

Utilize a seguinte convenção ao nomear suas branches:

- `feature/nome-da-feature` – para novas funcionalidades
- `bugfix/nome-do-bug` – para correções de bugs
- `hotfix/nome-do-hotfix` – para correções urgentes em produção
- `release/x.y.z` – para preparação de novas versões

### ✅ Regras de Proteção

- `main` e `dev` são branches **protegidas**.
- **Não é permitido fazer push direto.**
- Todo código deve ser integrado via **Pull Request (PR)**.
- Pull Requests devem ser aprovados por pelo menos **1 revisor** antes de serem integrados.

### 📋 Abertura de Pull Requests

1. Crie sua branch a partir de `dev`:
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/nome-da-sua-feature


## GitHub Actions: Terraform CI/CD

Este projeto possui uma integração contínua com GitHub Actions utilizando Terraform.

### Como funciona:

- O workflow é acionado automaticamente quando há push na branch `dev` ou quando arquivos `.tf` são alterados via pull request.
- Também é possível executar manualmente via aba Actions (graças ao `workflow_dispatch`).

### Pré-requisitos:

Para que o workflow funcione corretamente, é necessário configurar os seguintes **segredos** no repositório:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`

Esses segredos devem ser configurados em **Settings > Secrets and variables > Actions > New repository secret**.

### 🧪 Como rodar os testes e utilitários

```bash
# Executar todos os testes unitários (pytest)
python -m pytest meu-projeto/tests/ -v

# Executar um teste específico
python -m pytest meu-projeto/tests/test_list_tasks.py -v

# Rodar o script de debug local das Lambdas
python debug_local.py

# Padronizar formatação do código Python
black .

# Organizar imports automaticamente
isort .

# Padronizar formatação dos arquivos Terraform
terraform fmt
```

**Dicas:**
- Certifique-se de estar na raiz do projeto para rodar os comandos acima.
- O script `debug_local.py` permite testar suas funções Lambda localmente simulando eventos AWS.
- Use `black` e `isort` para manter o código limpo e padronizado.
- O comando terraform fmt garante que todos os arquivos .tf estejam com a formatação recomendada pelo Terraform, facilitando a leitura e evitando conflitos de formatação em equipe.