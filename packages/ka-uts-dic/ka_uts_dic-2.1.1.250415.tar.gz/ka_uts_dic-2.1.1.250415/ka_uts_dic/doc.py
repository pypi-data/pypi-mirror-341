# coding=utf-8
from collections.abc import Callable
from typing import Any

TyArr = list[Any]
TyCallable = Callable[..., Any]
TyDic = dict[Any, Any]
TyAmD = TyArr | TyDic
TyDoC = dict[str, TyCallable]

TnStr = None | str
TnDoC = None | TyDoC
TnCallable = None | TyCallable


class DoC:
    """
    Dictionary of Callables
    """
    @staticmethod
    def sh(doc: TnDoC, key: TnStr) -> TyCallable:
        """
        Show(get) the function as the value of the
        function-dictionary for the given key.
        """
        if not doc:
            msg = f"function table: {doc} is not defined"
            raise Exception(msg)
        if not key:
            msg = f"key: {key} is not defined"
            raise Exception(msg)
        fnc: TnCallable = doc.get(key)
        if not fnc:
            msg = f"key: {key} is not defined in function table: {doc}"
            raise Exception(msg)
        return fnc

    @classmethod
    def ex(cls, doc: TnDoC, key: TnStr, args_kwargs: TyAmD) -> Any:
        """
        Show and execute the function as the value of
        of the function-dictionary for the given key.
        """
        fnc: TyCallable = cls.sh(doc, key)
        return fnc(args_kwargs)
