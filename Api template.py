"""
Simple Api template + example
"""


class ApiTemplate:
    """use this template to generate your Api class"""
    def __init__(self):     # note: for sake of simplicity __init__ should avoid having args/kwargs
        self.routine = None     # generator of methods that are called one by one during runtime
        self.do_report = True
        self.report('Api initialized')

    def report(self, message: str):
        if self.do_report:
            print('>', message)

    # --- Context Manager ----------------------------------------------------------------

    def enter(self):
        """gets returned at the end of __enter__()"""
        raise NotImplementedError

    def exit(self):
        """gets returned at the end of __exit__()"""
        raise NotImplementedError

    def __enter__(self):
        # check that routine is defined
        routine = self.routine_list()
        self.report('initializing routine')

        # assert routine_list(self) has been properly implemented
        if not hasattr(routine, '__iter__'):
            raise TypeError(f'{type(routine).__name__} object is not iterable; '
                            f'routine_list must return an iterable')
        for task in routine:
            if not hasattr(task, '__call__'):
                raise TypeError(f'{type(task).__name__} object is not callable; '
                                f'routine_list must return a list of methods')

        self.set_routine(routine)

        self.report('running Api')
        return self.enter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.report('Api routine successfully completed!')
        else:
            self.report(f'Api interrupted by {exc_type.__name__}')
        self.exit()
        self.report('Api successfully shut down')

    # --- Routine ----------------------------------------------------------------

    def routine_list(self):
        """:return list of methods to execute by the Api"""
        raise NotImplementedError

    def set_routine(self, routine: list):
        """assign list of methods to call to self.routine"""
        def gen():
            for task in routine:
                self.report(f'running "{task.__name__}"')
                yield task

        self.routine = gen()

    # --- Execution ----------------------------------------------------------------

    def run(self):
        """run API (execute routine)"""
        for task in self.routine:
            task()

    def __next__(self):
        """execute next task in routine"""
        try:
            task = API.routine.__next__()
            task()
        except StopIteration:
            pass

    # ---- Setters ----------------------------------------------------------------

    def toggle_report(self, b: bool):
        self.do_report = b


# ----------------------------------------------------------------------------------------------------------------------


class Api(ApiTemplate):
    def __init__(self, x=None):
        super().__init__()
        self.x = x

    # --- Context Manager ----------------------------------------------------------------

    def enter(self):
        self.report('enter')
        return self

    def exit(self):
        self.report('exit')

    # ---- Tasks ----------------------------------------------------------------

    def task_1(self):
        """dummy task 1"""
        print(f'\t1) {self.x}\n')

    def task_2(self):
        """dummy task 2"""
        print(f'\t2) {self.x}\n')

    def task_3(self):
        """dummy task 3"""
        print(f'\t3) {self.x}\n')

    # ---- Routine ----------------------------------------------------------------

    def routine_list(self):
        tasks = [self.task_1,
                 self.task_2,
                 self.task_3]
        return tasks


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    with Api('sample') as API:
        API.run()
        # next(API)
