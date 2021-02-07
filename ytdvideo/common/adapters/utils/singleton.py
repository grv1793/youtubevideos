import functools


class Singleton:
    """Singleton can now be used as a decorator.
    eg:
    ---- Regular Class ----
    class ATS:
        pass

    obj1 = ATS()
    obj2 = ATS()

    obj1 is obj2

    This evaluates to False

    ---- Singleton Class -----
    @Singleton
    class ATS:
        pass

    obj1 = ATS()
    obj2 = ATS()

    obj1 is obj2

    This evaluates to True.

    Why was this change necessary?
    - Better separation of concerns.
        `Singleton` decorator is responsible for making sure that only one instance exists.
    - Don't have to worry about how the Singleton is implemented. We just have to write the code for a class,
        The Singleton decorator will make sure that only one instance exists
    - Better Readability
    - More Pythonic.

    I'm using a singleton for the ElasticSearch Adapter. Refer `ElasticSearchDBMultiNodeCluster2Adapter` in ATS.
    `ElasticSearchDBMultiNodeCluster2Adapter` is just a plain class. Without the Singleton decorator, it will
    act like a regular class

    Cons:
        - Methods cannot be set dynamically to a class. They need to be already defined in the class.
        eg:
        -----------
        @Singleton
        class Klass1:
            pass

        def func1():
            pass

        Klass1().func1 = func1 # This works

        Klass1.func1 = func1 # Error
        --------
        "Klass.func1 = func" :-> You cannot do this. As far as I know, nobody would do something like this,
        but still just putting it out there.

        - eval() on the repr on The Klass don't work. Again, not a big deal, just putting it out there.
        - I can only think of one tradeoff and that's mentioned above. We update as and when necessary
    """

    def __init__(self, klass):
        self.klass = klass
        self.instance = None
        functools.update_wrapper(self, klass, updated=[])

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.klass(*args, **kwargs)
        return self.instance

    def __getattr__(self, item):
        return getattr(self.klass, item)

    def __repr__(self):
        return f"<Singleton: {repr(self.klass)}>"

    def __str__(self):
        return f"<Singleton: {str(self.klass)}>"
