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
