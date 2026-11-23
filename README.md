# Clínica Santiago

Sistema web para gerenciar um consultório médico: pacientes, consultas e
estoque de medicamentos.

Projeto Integrador — MedTec 2026 (UC30 a UC35) — Caio Flávio

## Funcionalidades

- Cadastro, edição e exclusão de pacientes
- Agendamento de consultas ligadas ao paciente
- Busca de consulta por data
- Controle de estoque de medicamentos (alerta de estoque baixo e vencido)
- API JSON em `/api/pacientes`, `/api/consultas` e `/api/medicamentos`

## Tecnologias

- Python 3 + Flask
- Jinja2 (templates)
- SQLite
- HTML + CSS (responsivo)

## Como rodar localmente

```bash
git clone [github.com](https://github.com/seu-usuario/clinica-santiago.git)
cd clinica-santiago
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
