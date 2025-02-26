# Playing with Certora prover

## Useful commands
Create python env:
```
python3 -m venv environment
```

Activate python env:
```
source environment/bin/activate
```

Deactivate python env:
```
deactivate
```

Run certora prover:
```
certoraRun Empty.sol --verify Empty:sisters.spec --rule sistersBirthMonths
```
