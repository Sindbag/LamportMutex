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

### Manual mode
To run Lamport Mutex in manual mode:
```
python run.py -m manual.conf -p 0
```

## Analyze stress test' logs
```
python analyzer.py
```
