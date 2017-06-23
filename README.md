# Lamport Mutex
Python 3.4+ implementation of Lamport mutex

## Tests

### Unittests
To run unittests:
```
python -m unittest
```

### Stress test
To run stress-test for 10 processes:
```
python run.py stress.conf
```
Results of stress-test are placed in logs/*.txt. N.txt is for each node and common.txt - one for all.

### Manual mode
To run Lamport Mutex in manual mode:
```
python run.py -m manual.conf -p 0
```
Acquire and release from console.

## Analyze stress test' logs
```
python analyzer.py
```
Validate stress-test logs for event and time sequence correctness.