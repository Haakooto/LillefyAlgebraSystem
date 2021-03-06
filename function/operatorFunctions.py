import numpy as np
import sys
from numbers import Number


from .Variable import Variable, Struct
from .parents import parentFunction, parentOperator


class Add(parentOperator):
    arglen = None
    callType = "both"
    argNo = 0

    def call(self, *args, **kwargs):
        res, coeff = self.res_coeff(*args, **kwargs)

        for obj in args:
            res += obj * coeff
        return res

    def string(self, *args):
        res = ""
        for thing, coeff in self.structure.items():
            if coeff == 0:
                continue
            if thing == "number" and coeff != 0:
                res += str(coeff)
            if isinstance(thing, Variable):
                if res != "":
                    res += " + "
                if coeff == 1:
                    res += f"{str(thing)}"
                else:
                    res += f"{str(coeff)}{str(thing)}"
            if (isinstance(thing, parentFunction)) or (
                isinstance(thing, parentOperator)
            ):
                if res != "":
                    res += " + "
                if coeff == 1:
                    res += f"{str(thing)}"
                else:
                    res += f"{str(coeff)}{str(thing)}"

        return res


class Mul(parentOperator):
    arglen = None
    null_value = 1
    callType = "both"
    argNo = 0

    def call(self, *args, **kwargs):
        res, coeff = self.res_coeff(*args, **kwargs)

        for obj in args:
            res *= obj ** coeff

        return res

    def string(self, *args):
        res = ""
        for thing, coeff in self.structure.items():
            if coeff == 0:
                continue
            if thing == "number" and coeff != 1:
                res += str(coeff)
            if isinstance(thing, Variable):
                if res != "":
                    res += "*"

                if coeff == 1:
                    res += f"{str(thing)}"
                else:

                    res += f"{str(thing)}^({str(coeff)})"
            if (isinstance(thing, parentFunction)) or (
                isinstance(thing, parentOperator)
            ):
                if res != "":
                    res += "*"

                if isinstance(thing, add) and len(thing.structure) > 1:
                    if coeff == 1:
                        res += f"({str(thing)})"
                    else:

                        res += f"({str(thing)})^({str(coeff)})"
                else:
                    if coeff == 1:
                        res += f"{str(thing)}"
                    else:

                        res += f"{str(thing)}^({str(coeff)})"

        return res


class Sub(Add):
    arglen = 2

    def init(self):
        a, b = self.original_structure

        if isinstance(a, Number):
            self.structure["number"] = a
        else:
            self.structure[a] = 1
        if isinstance(b, Number):
            self.structure["number"] -= b
        else:
            self.append_to_structure(b, "sd")


class Div(Mul):
    arglen = 2

    def init(self):
        a, b = self.original_structure

        if isinstance(a, Number):
            self.structure["number"] = a
        else:
            self.structure[a] = 1
        if isinstance(b, Number):
            self.structure["number"] /= b
        else:
            self.append_to_structure(b, "sd")

    def string(self, *args):
        res = ""
        for thing, coeff in self.structure.items():
            coeff = abs(coeff)
            if thing == "number" and coeff != self.null_value:
                res += str(coeff)
            elif isinstance(thing, (parentFunction, parentOperator, Variable)):
                print(res)
                if res != "":
                    res += "/"
                if coeff == 1:
                    c = ""
                else:
                    c = f"^{coeff}"

                if isinstance(thing, Variable):
                    d = str(thing)
                else:
                    d = f"({str(thing)})"
                res += f"{d}{c}"
        return res


class Pow(parentOperator):
    arglen = 2
    null_value = 1
    callType = "both"
    argNo = 1

    def call(self, *args, **kwargs):
        if "res" not in kwargs:
            res = self.null_value
        else:
            res = kwargs["res"]
        if "coeff" not in kwargs:
            coeff = 1
        else:
            coeff = kwargs["coeff"]
        for obj in args:
            res *= obj ** coeff

        return res
