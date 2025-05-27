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

### Comando para testar:

```bash
 python -m pytest meu-projeto/tests/test_list_tasks.py -v
```