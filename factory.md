# Factory Configuration
## Goal
A simple Python CLI todo app
## Scope
### Modifiable
- todo/**/*.py
- tests/**/*.py
### Read-only
- factory.md
## Guards
- Do not delete tests
## Eval
### Command
python eval/score.py
### Threshold
0.5
## Target Branch
main
## Smoke Test
cd /Users/colehurwitz/refactory-projects/testrepo3 && python -m pytest tests/ -q
