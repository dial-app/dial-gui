# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.datasets import Dataset, TTVSets
from dial_core.utils import Dial
from PySide2.QtGui import QColor
from tensorflow.keras import Model


class TypeColor:
    colors = {
        int: QColor("#B54747"),
        str: QColor("#0056A6"),
        Dataset: QColor("#6666FF"),
        TTVSets: QColor("#1785CF"),
        Dial.KerasLayerListMIME: QColor("#AA0000"),
        Model: QColor("#0000AA"),
    }

    @classmethod
    def get_color_for(cls, port_type):
        try:
            return cls.colors[port_type]
        except KeyError:
            return QColor("#000000")
