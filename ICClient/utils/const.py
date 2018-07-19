def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()
    return property(fget, fset)


class _Const(object):
    @constant
    def end_session():
        return "end_session"

    @constant
    def invalid():
        return "invalid"

    @constant
    def projectNameSlot():
        return "projectNameSlot"

    @constant
    def dirNameSlot():
        return "dirNameSlot"

    @constant
    def emptySlot():
        return "emptySlot"

    @constant
    def relativeDirNameSlot():
        return "relativeDirNameSlot"

    @constant
    def stopIntent():
        return "AMAZON.StopIntent"


CONST = _Const()
