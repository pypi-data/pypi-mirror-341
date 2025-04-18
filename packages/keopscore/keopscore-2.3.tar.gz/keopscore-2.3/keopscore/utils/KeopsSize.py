from keopscore.utils.misc_utils import KeOps_Error


def prod(x):
    # product of all elements in list of integers
    res = 1
    for item in x:
        res *= item
    return res


def select(x, ind):
    # indexing of list via list of integers
    return [x[i] for i in ind]


def delete(x, ind):
    # delete items given by indices in list
    n = len(x)
    indkeep = list(set(range(n)) - set(ind))
    indkeep.sort()
    return select(x, indkeep)


def cumprod_array(x):
    # special cumulative product
    if len(x) == 0:
        return x
    else:

        def cumprod(x):
            res = x.copy()
            for i in range(1, len(x)):
                res[i] *= res[i - 1]
            return res

        return cumprod(x[1:][::-1])[::-1] + [1]


def permutation(perm, arr):
    if perm is None:
        return arr
    else:
        tmp = sorted(range(len(perm)), key=perm.__getitem__)
        return select(arr, tmp)


class KeopsSize:
    """
    This class implement a Size object for symbolic tensor
    """

    _shape = tuple()

    def __init__(self, shape):
        # Check all elements of shape are int
        for i in shape:
            if (not isinstance(i, int)) and (i > 0):
                raise KeOps_Error("Shape must be a tuple/list of int")

        self._shape = tuple(shape)

    @property
    def shape(self):
        return self._shape

    @property
    def strides(self):
        """
        Return the strides of the tensor
        """
        return cumprod_array(self._shape)

    def broadcast(self, other):
        """
        Broadcast the shape of the current object with the shape of the other object
        """
        if len(self.shape) > len(other.shape):
            return self, KeopsSize(self.shape)
        elif len(self.shape) < len(other.shape):
            return KeopsSize(other.shape), other
        else:
            return self, other


if __name__ == "__main__":
    a = KeopsSize((1, 2, 3))
    b = KeopsSize((4, 2, 3))

    print(a.shape)
    print(a.strides)

    a.broadcast(b)
