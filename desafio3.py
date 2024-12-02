class computed_property:
    def __init__(self, *dependencies):
        self.dependencies = dependencies
        self._cache = {}
        self._getter = None
        self._setter = None
        self._deleter = None

    def __call__(self, func):
        self._getter = func
        self.__doc__ = func.__doc__
        return self

    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        cache = self._cache.get(instance)
        if cache is not None:
            cached_value, last_values = cache
            current_values = tuple(getattr(instance, attr, None) for attr in self.dependencies)
            if current_values == last_values:
                return cached_value

        current_values = []
        result = self._getter(instance) 
        for attr in self.dependencies:
            current_values.append(getattr(instance, attr, None))

        current_values = tuple(current_values)
        self._cache[instance] = (result, current_values)
        return result

    def __set__(self, instance, value):
        if self._setter is None:
            raise AttributeError("can't set attribute")
        self._setter(instance, value)
        
        self._cache.pop(instance, None)

    def setter(self, func):
        self._setter = func
        return self

    def __delete__(self, instance):
        if self._deleter is None:
            raise AttributeError("can't delete attribute")
        self._deleter(instance)
        self._cache.pop(instance, None)

    def deleter(self, func):
        self._deleter = func
        return self