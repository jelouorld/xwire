
import typing as tp
import functools
import inspect


from contextlib import contextmanager
from collections import defaultdict

__registry__: dict[str, tp.Any] = {}

__config__registry__: dict[str, dict[str,str]] = defaultdict(dict)  



# parameter 0..n arguments 
def injectable(
        fn_or_class: tp.Optional[tp.Callable[..., tp.Any] | tp.Type[tp.Any]] = None,
        *args:tp.Any, 
        **kwargs: tp.Any
) -> tp.Callable[..., tp.Any]:
    
    if fn_or_class is None:
        return functools.partial(injectable, *args, **kwargs)

    __config__registry__[fn_or_class.__qualname__] |= {'environ': 'main'} | kwargs
    
    # Register injectable
    __registry__[fn_or_class.__qualname__] = fn_or_class

    return fn_or_class
    

class _engine: 


    def run(self, entrypoint: tp.Callable[..., tp.Any], *args:tp.Any, **kwargs:tp.Any)-> tp.Any:
        # todo:
        pass 
    
        
    


@contextmanager
def engine():
    yield _engine()


def run(main: tp.Callable[..., tp.Any]):
    with engine() as e:
        e.run(main)



