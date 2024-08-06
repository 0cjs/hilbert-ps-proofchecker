''' This module provides decorators for lazily initialised properties and
    methods that cache their initial return value and return that
    thereafter. Note that, unlike `functools.cached_property`, here the
    cached value is held in the object (and disposed of when the object
    is GC'd) rather than in a global per-method cache indexed by object.

    The `lazyproperty` decorator converts a method to a read-only property
    that is initialised once on first access. The `lazymethod` decorator
    converts a method to one that is called only once.

    These are useful mainly for objects that are at least partially
    "immutable," i.e., that have data that is set when the object is
    instantiated and not changed thereafter.
'''

__all__ = ['lazyproperty', 'lazymethod']

class LazyProperty:

    def __init__(self, f):
        self.f = f
        self.name = self.f.__name__
        self.cacheattr = '__' + self.name       # should be one _ or two?

    def __get__(self, obj, objtype=None):
        if hasattr(obj, self.cacheattr):
            return getattr(obj, self.cacheattr)
        else:
            setattr(obj, self.cacheattr, self.f(obj))
            return getattr(obj, self.cacheattr)

    def __set__(self, obj, value):
        #   Message stolen from Python docs:
        #   https://docs.python.org/3/howto/descriptor.html#properties
        raise AttributeError(f'property {self.name!r}'
            f' of {type(obj).__name__!r} object has no setter')

def lazyproperty(f):
    ''' When used to decorate a method taking only `self`, this turns it
        into a read-only property that is lazily initialised and, after the
        first read, returns a cached copy of the generated value. E.g.::

            class C:
                @lazyproperty
                def p(self):
                    return self.some_expensive_calculation()

        The first time that `C().p` is read, the decorated `p()` will be
        called, its return value cached in a freshly created attribute
        `__p`, and that value returned. Subsequent reads of the property
        will return the cached value.

        Obviously the property value should depend only on other data
        in the object that are considered immutable.

        This differs from the `functools.cached_property` decorator in
        that it it creates a read-only property, rather than allowing
        the property to be set.
    '''
    return LazyProperty(f)

def lazymethod(f):
    ''' When used to decorate a method taking only `self`, this turns it
        into a method that on the first call is run and has its return
        value cached and on subsequent calls just returns the cached value.

            class C:
                @lazymethod
                def m(self):
                    return self.some_expensive_calculation()

        The first time that `C().m()` is called, the decorated `m()` will
        be called, its return value cached in a freshly created attribute
        `__m`, and that value returned. Subsequent calls of the method will
        return the cached value.

        Obviously the method's return value should depend only on other
        data in the object that are considered immutable. Nor may it
        change its return value based on parameters, which is why the
        method may not take any (except `self`).
    '''
    name = f.__name__
    cacheattr = '__' + name       # should be one _ or two?
    def m(obj):
        if hasattr(obj, cacheattr):
            return getattr(obj, cacheattr)
        else:
            setattr(obj, cacheattr, f(obj))
            return getattr(obj, cacheattr)
    return m


