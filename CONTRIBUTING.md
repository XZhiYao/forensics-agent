# Contributing

## Branch convention

```
main          ← stable, tagged releases
dev           ← integration branch
feature/<name>  ← new features
week<N>/<desc>  ← weekly progress (e.g. week1/ela-detector)
```

## Commit message format

```
<type>(<scope>): <short summary>

type:  feat | fix | eval | docs | refactor | chore
scope: detectors | agent | mcp | api | eval | deps

Examples:
  feat(detectors): implement ELA detector with Pillow
  eval(detection): add CASIA batch evaluation script
  fix(agent): handle tool timeout in detector_node
```

## Before pushing

```bash
ruff check .          # lint
pytest tests/ -q      # unit tests
```

## Reproducing experiments

All evaluation runs require:
1. Model weights in paths defined in `configs/.env`
2. Datasets in paths defined in `configs/.env`
3. Git SHA recorded alongside results (see `experiments/README.md`)
