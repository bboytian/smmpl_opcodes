import functools
print = functools.partial(print, flush=True)  # modifying print function

from .decorators import *
from .functions import *
from .params import *
