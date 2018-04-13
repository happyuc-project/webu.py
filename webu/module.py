class Module:
    webu = None

    def __init__(self, webu):
        self.webu = webu

    @classmethod
    def attach(cls, target, module_name=None):
        if not module_name:
            module_name = cls.__name__.lower()

        if hasattr(target, module_name):
            raise AttributeError(
                "Cannot set {0} module named '{1}'.  The webu object "
                "already has an attribute with that name".format(
                    target,
                    module_name,
                )
            )

        if isinstance(target, Module):
            webu = target.webu
        else:
            webu = target

        setattr(target, module_name, cls(webu))
