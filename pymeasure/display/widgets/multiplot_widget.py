#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2023 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging

import pyqtgraph as pg

from ..Qt import QtCore, QtWidgets
from .tab_widget import TabWidget
from ..curves import ResultsCurve
from .plot_frame import PlotFrame

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class MultiPlotWidget(TabWidget, QtWidgets.QWidget):
    """ Extends :class:`PlotFrame<pymeasure.display.widgets.plot_frame.PlotFrame>`
    to allow different columns of the data to be dynamically chosen
    """

    def __init__(self, name, columns, x_axis, limit=None, refresh_time=0.2,
                 check_status=True, linewidth=1, parent=None, **kwargs):
        super().__init__(name, parent)
        self.columns = columns
        self.refresh_time = refresh_time
        self.check_status = check_status
        self.linewidth = linewidth
        self.x_axis = x_axis
        self.limit = limit
        self._setup_ui()
        self._layout()

    def _setup_ui(self):

        self.plot_frame = PlotFrame(
            self.x_axis,
            None,
            self.refresh_time,
            self.check_status,
            parent=self,
        )
        self.updated = self.plot_frame.updated
        self.plot = self.plot_frame.plot
        self.plot.addLegend(pen=pg.mkPen(color='black', width=self.linewidth),
                            brush=pg.mkBrush((255, 255, 255, 255)))

    def _layout(self):
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.setSpacing(0)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(10)
        hbox.setContentsMargins(-1, 6, -1, 6)

        vbox.addLayout(hbox)
        vbox.addWidget(self.plot_frame)
        self.setLayout(vbox)

    def sizeHint(self):
        return QtCore.QSize(300, 600)

    def new_curve(self, results, color=pg.intColor(0), **kwargs):
        if 'pen' not in kwargs:
            kwargs['pen'] = pg.mkPen(color=color, width=self.linewidth)
        if 'antialias' not in kwargs:
            kwargs['antialias'] = False
        curves = []
        cols = self.columns[:self.limit]
        pens = [pg.mkPen(color=pg.intColor(i, hues=len(cols) + 1), width=self.linewidth) for i in
                range(len(cols))]
        for cdx, c in enumerate(cols):
            if c != self.x_axis:
                curve = ResultsCurve(results,
                                     wdg=self,
                                     x=self.x_axis,
                                     y=c,
                                     pen=pens[cdx],
                                     name=c
                                     )
                curve.setSymbol(None)
                curve.setSymbolBrush(None)
                curves.append(curve)
        return curves

    def update_x_column(self, index):
        axis = self.columns_x.itemText(index)
        self.plot_frame.change_x_axis(axis)

    def update_y_column(self, index):
        axis = self.columns_y.itemText(index)
        self.plot_frame.change_y_axis(axis)

    def load(self, curve):
        # curve.x = self.columns_x.currentText()
        # curve.y = self.columns_y.currentText()
        curve.update_data()
        self.plot.addItem(curve)

    def remove(self, curve):
        self.plot.removeItem(curve)

    def set_color(self, curve, color):
        """ Change the color of the pen of the curve """
        curve.set_color(color)

    def preview_widget(self, parent=None):
        """ Return a widget suitable for preview during loading """
        return MultiPlotWidget("Plot preview",
                               self.columns,
                               self.x_axis,
                               parent=parent,
                               )

    def clear_widget(self):
        self.plot.clear()
