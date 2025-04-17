# Pantarei

[![license](https://img.shields.io/pypi/l/atooms.svg)](https://en.wikipedia.org/wiki/GNU_General_Public_License)
[![pipeline status](https://framagit.org/coslo/pantarei/badges/master/pipeline.svg)](https://framagit.org/coslo/pantarei/-/commits/master)
[![coverage report](https://framagit.org/coslo/pantarei/badges/master/coverage.svg)](https://framagit.org/coslo/pantarei/-/commits/master)

A general-purpose workflow manager - because *everything* flows

## Quick start

Pantarei builds on three kinds of execution units:
- **functions** are stateless, Python callables
- **tasks** are stateful wrapped functions that cache execution results
- **jobs** are stateful wrapped tasks for distributed-memory parallel environments

To see it in action, say you have a Python function
```python
def f(x):
    import time
    time.sleep(2)
    return x
```

Wrap the function with a Task and call it with a range of arguments
```python
from pantarei import Task, Job

task = Task(f)
for x in [1, 2]:
    task(x=x)
```

The task's results are cached: a successive execution will just fetch the results (like `joblib`)
```python
results = task(x=1)
```

We wrap the task with a Job and submit jobs to a local scheduler, such as  `SLURM`
```python
job = Job(task)
for x in [3, 4]:
    job(x=x)
```
Not on a cluster scheduler? No problem: `nohupx` will be used as a fallback scheduler.

If you want to get the jobs' results, wait until they are done
```python
job.scheduler.wait()
results = job(x=3)
```

## Command line interface

Pantarei comes with a command line interface to run and manage jobs. If you like working from the terminal, you'll find yourself at home.

Run a script with some jobs
```bash
rei run script.py
```

Check the status of the jobs
```bash
rei ls -l script.py
```
```
🟩 script.py |████████████████████| 0:00:00 [2/2]
   ✅ f/3de5a949fa3c880e35165fc6820ce82e 0:00:00 f(x=1)
   ✅ f/26766c2fda253b7aeb1adaa02f31e93b 0:00:00 f(x=2)
```

Inspect the jobs' cache (metadata and results)
```bash
rei cat script.py
```

Clear the jobs' cache and artifacts
```bash
rei rm -rf script.py
```

There is much more of course: `rei --help` and `rei <command> --help` are your best friends.

## Documentation

Check out the [tutorial](https://coslo.frama.io/pantarei) for more examples and the [public API](https://coslo.frama.io/pantarei) for full details.

The CLI interface (`rei`) is documented via its own help pages.

## Installation

From pypi
```
pip install pantarei
```

## TODO

- [ ] submit on remote cluster
- [ ] handle task dependencies
- [ ] add Workflow / Queue
- [ ] perhaps add signac-like view() or checkout() method to check out a view of cache as folders

## Contributing

Contributions to the project are welcome. If you wish to contribute, check out [these guidelines]().

## Authors

- Daniele Coslovich
