from . import scenario_map, injection_map

def scenario(**params):
    def decorator(clazz):
        scenario_map[clazz.__name__]["scenario"] = params
        return clazz
    return decorator

def process(*params):
    def decorator(func):
        qualname = func.__qualname__.split(".")
        if scenario_map[qualname[0]]["process"]:
            scenario_map[qualname[0]]["process"] += list(params)
        else:
            scenario_map[qualname[0]]["process"] = list(params)
        return func
    return decorator

def inject(**params):
    def decorator(func):
        def execd(self, *args, **kwargs):
            add_kwargs = {}
            for k, v in params.items():
                if v in injection_map:
                    add_kwargs[k] = injection_map[v]
            return func(self, **{**kwargs, **add_kwargs})
        return execd
    return decorator
