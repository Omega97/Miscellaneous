
class ApiTemplate:
    def __init__(self):
        self.routine = None

    # --- Routine ----------------------------------------------------------------

    def set_routine(self, routine: list):
        """assign list of methods to call during routine"""
        def gen():
            print('> running Api')
            for i in routine:
                yield i
            print('> Api routine completed!')

        self.routine = gen()

    # --- Execution ----------------------------------------------------------------

    def run(self):
        """run API"""

        # no routine specified
        if not hasattr(self.routine, '__iter__'):
            raise RuntimeError("Please specify API's routine first via self.set_routine(...)")

        # execute routine
        for task in self.routine:
            print(f'> running "{task.__name__}"')
            task()

    def __call__(self, *args, **kwargs):
        """calls next method in routine"""
        try:
            task = API.routine.__next__()
            print(f'> running "{task.__name__}"')
            task()
        except StopIteration:
            pass

# ----------------------------------------------------------------------------------------------------------------------


class Api(ApiTemplate):
    def __init__(self, x=None):
        super().__init__()
        self.x = x

    # ---- Tasks ----------------------------------------------------------------

    def task_1(self):
        print('1) ', self.x)

    def task_2(self):
        print('2) ', self.x)

    def task_3(self):
        print('3) ', self.x)

    # ---- Routine ----------------------------------------------------------------

    def setup(self):
        tasks = [self.task_1,
                 self.task_2,
                 self.task_3]
        self.set_routine(tasks)


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    API = Api('input')
    API.setup()
    API.run()
