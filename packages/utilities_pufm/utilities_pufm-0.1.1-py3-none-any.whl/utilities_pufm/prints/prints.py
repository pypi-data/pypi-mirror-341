import sys
import io
from contextlib import contextmanager

@contextmanager
def redirect_stdout(f):
    try:
        _stdout = sys.stdout
        sys.stdout = f
        yield
    finally:
        sys.stdout = _stdout


    f = io.StringIO()
    with redirect_stdout(f):
        do_something()
    out = f.getvalue()


    from io import StringIO 
    import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout