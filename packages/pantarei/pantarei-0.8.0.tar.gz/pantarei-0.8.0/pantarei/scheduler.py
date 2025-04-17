"""
Scheduler
"""
import sys
import time
import subprocess
from .backends import detect
from . import core


class JobScheduler:

    """
    Wrapper to scheduler for execution on a distributed memory environment

    `Scheduler` is entirely decoupled from `Job`. For job submission,
    it only needs a script as a string and the relevant job
    directives.
    """

    # TODO: add custom header or args to __init__ so that we can customize the job at run time

    def __init__(self, host='localhost', verbose=False, backend='auto', jobs_limit=0):
        """
        :param host: hostname of the cluster
        :param verbose: verbose output
        :param backend: backend for scheduler (default is auto-detect)
        :param jobs_limit: maximum number of jobs to run concurrently (if 0 no limit)
        """
        self.host = host
        self.verbose = verbose
        self.path = ''  # working directory?
        self.backend = detect(backend)
        self.jobs_limit = jobs_limit

    def wait(self, job_name=None, max_jobs=None, seconds=5):
        """
        Wait until `job_name` is done or until there are less than `max_jobs`

        The check is done every `seconds` seconds.
        """
        assert not (job_name and max_jobs), 'set only one of these parameters'
        muted = False
        while True:
            reason_to_wait = ''
            if job_name is None:
                if len(self.queue()) > 0 and max_jobs is None:
                    reason_to_wait = 'Waiting for all jobs to end...'
            else:
                # Make sure job_name is a list
                if isinstance(job_name, str):
                    job_name = [job_name]
                if any([self.queued(name) for name in job_name]):
                    n = sum([self.queued(name) for name in job_name])
                    reason_to_wait = f'Waiting for {n} dependent jobs to end...'

            if max_jobs is not None:
                if len(self.queue()) >= max_jobs:
                    n = len(self.queue()) - max_jobs + 1
                    reason_to_wait = f'Waiting for {n} jobs to end...'

            if reason_to_wait:
                if self.verbose and not muted:
                    print(reason_to_wait)
                    muted = True
                if not core.halt:
                    if self.verbose:
                        print('...we exit immediately')
                    sys.exit()
                else:
                    time.sleep(seconds)
            else:
                break

    def queue(self):
        """Return a list of jobs in the scheduler queue"""
        output = subprocess.check_output(self.backend['queue'], shell=True)
        queued_jobs = output.decode().split('\n')[:-1]
        return queued_jobs

    # TODO: this seems redundant, job checks against the fqn so we should test if fqn in queue()
    # This is currently used in Job and in Thread
    def queued(self, job_name):
        """Return `True` the job named `job_name` is queued.

        :param job_name: fqn or a regexp matching a fully qualified name
        """
        import re
        # Check if job_name is fully qualified
        # if re.match('.*-.*', job):
        for queued_job in self.queue():
            # We clear the match afterwards because it cannot be pickled by dill
            match = re.match(job_name, queued_job)
            if match:
                del match
                return True
        return False

    def submit(self, script, job_name, job_output=None, job_error=None, cores=1,
               wall_time=None, memory=None):
        """
        Submit a script for batch execution on the scheduler

        :param script: string of python commands to execute
        :param job_name: name of job
        :param job_output: job output file
        :param job_error: job error file
        :param cores: number of cores for the job
        :param wall_time: wall time limit for the job ([D-]HH:MM:SS)
        :param memory: requested RAM (ex. 5000M or 5G)
        """
        name, output, error = job_name, job_output, job_error
        params = locals()
        # command = 'python -u -'
        # header = ''
        # TODO: not the best place probably
        if self.backend['limit'] and self.jobs_limit == 0:
            ncores = subprocess.check_output(['grep', '-c', '^processor', '/proc/cpuinfo'])
            self.wait(max_jobs=int(ncores))

        if self.jobs_limit > 0:
            self.wait(max_jobs=self.jobs_limit)

        # Assemble script spefications according to backend
        directive = self.backend["directive"]
        args = []
        for name, flag in self.backend['specifications'].items():
            if name not in params:
                continue
            value = params[name]
            if value is not None:
                args.append(f'{directive} {flag} {value}')

        # TODO: strip spaces when preceeded by = (like '-l nodes= 1' should be '-l nodes=1')

        # Define prologue and epilogue
        prologue = ''
        epilogue = ''

        # The backend uses batch jobs
        header = '\n'.join(args)
        # Interpolate script with job header
        if script.startswith('#!'):
            lines = script.split('\n')
            shebang = lines.pop(0)
            body = '\n'.join(lines)
        else:
            body = script
            shebang = '#!/usr/bin/env python'

        # Submit the job
        # TODO: are the env vars propagated here?
        output = subprocess.check_output(f"""{self.backend['submit']} <<'EOF'
{shebang}
{header}
{prologue}
{body}
{epilogue}
EOF""", shell=True)
        if self.verbose:
            print(output.decode().strip())


import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

class ThreadScheduler:

    def __init__(self, max_workers=None):
        self.max_workers = max_workers
        self.pool = ThreadPoolExecutor(max_workers=self.max_workers)
        # self.pool = ProcessPoolExecutor(max_workers=self.max_workers)
        self._futures = []

    def queue(self):
        return [future.name for future in self._futures if not future.done()]
        # self.results = [future.result() for future in futures if not future.done()]

    # TODO: refactor same as JobScheduler -> standalone
    def queued(self, job_name):
        """Return `True` the job named `job_name` is queued.

        :param job_name: fqn or a regexp matching a fully qualified name
        """
        import re
        # Check if job_name is fully qualified
        # if re.match('.*-.*', job):
        for queued_job in self.queue():
            # We clear the match afterwards because it cannot be pickled by dill
            match = re.match(job_name, queued_job)
            if match:
                del match
                return True
        return False

    # This is coupled to Task via qualified name
    def __submit(self, task, *args, **kwargs):
        if len(self.queue()) == 0:
            self.pool.shutdown()
            self.pool = ThreadPoolExecutor(max_workers=self.max_workers)

        f = self.pool.submit(task, *args, **kwargs)
        f.name = task.qualified_name(*args, **kwargs)
        self._futures.append(f)
        return f

    # This is decoupled from Task
    def submit(self, task, name, *args, **kwargs):
        if len(self.queue()) == 0:
            self.pool.shutdown()
            self.pool = ThreadPoolExecutor(max_workers=self.max_workers)
        f = self.pool.submit(task, *args, **kwargs)
        f.name = name
        self._futures.append(f)
        return f

    def wait(self, job_name=None, max_jobs=None, seconds=0):
        assert job_name is None
        assert max_jobs is None
        concurrent.futures.wait(self._futures)


# Factory class
def Scheduler(host='localhost', verbose=False, backend='auto', jobs_limit=0):
    """
    Factory to select an appropriate scheduler

    :param host: hostname of the cluster
    :param verbose: verbose output
    :param backend: backend for scheduler (default is auto-detect)
    :param jobs_limit: maximum number of jobs to run concurrently (if 0 no limit)
    """
    found_backend = detect(backend)
    if backend not in ['auto', None] and found_backend is None:
        raise ValueError(f'cannot find requested scheduler {backend}')
        #return None
    if found_backend:
        return JobScheduler(host=host, verbose=verbose, backend=found_backend,
                            jobs_limit=jobs_limit)
    else:
        return ThreadScheduler(max_workers=jobs_limit if jobs_limit > 0 else None)
