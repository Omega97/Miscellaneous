"""
Simple Api template + example
"""


class ApiTemplate:
    """use this template to generate your Api class"""
    def __init__(self, do_report=True):
        self.routine = None     # generator of methods that are called one by one during runtime
        self.set_routine(self.routine_list())
        self.do_report = do_report

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
        if not hasattr(self.routine, '__iter__'):
            raise RuntimeError("Please specify API's routine first via self.set_routine(...)")
        self.report('running Api')
        return self.enter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.report('Api routine successfully completed!')
        else:
            self.report(f'Api interrupted by {exc_type.__name__}')
        self.exit()

    # --- Routine ----------------------------------------------------------------

    def routine_list(self):
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

    def __call__(self, *args, **kwargs):
        """calls next method in routine"""
        try:
            task = API.routine.__next__()
            task()
        except StopIteration:
            pass


# ----------------------------------------------------------------------------------------------------------------------


class Api(ApiTemplate):
    def __init__(self, x=None, **kwargs):
        super().__init__(**kwargs)
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
        print(f'1) {self.x}\n')

    def task_2(self):
        """dummy task 2"""
        print(f'2) {self.x}\n')

    def task_3(self):
        """dummy task 3"""
        print(f'3) {self.x}\n')

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
