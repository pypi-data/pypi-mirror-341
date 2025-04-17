class Parallel:

    def __init__(self, task_or_func, tag="", scheduler=None, cores=1, wall_time=None,
                 output=None, error=None, memory=None, **kwargs):
        """
        :param task_or_func: the `Task` or function to execute
        :param tag: string to identify the task, relevant if task_or_func is a `Task`
        :param scheduler: the scheduler to usel if `None` it will be auto-detected
        :param cores: number of cores to use
        :param wall_time: the maximum wall time
        :param memory: requested memory (RAM)
        :param output: output file
        :param error: error file
        """
        from .core import scheduler
        from .thread import ThreadScheduler

        if self.scheduler is None:
            self.scheduler = ThreadScheduler()
            #self.strategy = Thread
        else:
            self.scheduler = scheduler
            #self.strategy = Job
        self.strategy = None
            
    def _submit(self):
        self.strategy._submit(self)
            
