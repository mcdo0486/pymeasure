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

from ..Qt import QtCore, QtWidgets, QtGui
from .tab_widget import TabWidget
from .plot_frame import PlotFrame

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class BarResultsCurve(pg.BarGraphItem):
    """ Creates a curve loaded dynamically from a file through the Results object. The data can
    be forced to fully reload on each update, useful for cases when the data is changing across
    the full file instead of just appending.
    """

    def __init__(self, results, x, height=None, columns=None, force_reload=False, wdg=None,
                 width=0.5, brushes=None, **kwargs):
        super().__init__(x=x, height=height, width=width, brushes=brushes)
        self.x = x
        self.height = height
        self.width = width
        self.results = results
        self.wdg = wdg
        self.pen = kwargs.get('pen', None)
        self.columns = columns
        self.force_reload = force_reload
        self.update_data()

    def update_data(self):
        """Updates the data by polling the results"""
        if self.force_reload:
            self.results.reload()
        data = self.results.data  # get the current snapshot

        if data.size:
            self.height = [data[i].iloc[-1] for i in self.columns]

    def set_color(self, color):
        self.pen.setColor(color)
        self.updateItems(styleUpdate=True)


class BarFrame(PlotFrame):
    ResultsClass = BarResultsCurve
    LABEL_STYLE = {'font-size': '16pt', 'font-family': 'Arial', 'color': '#000000'}


    def __init__(self, x_axis=None, y_axis=None, refresh_time=0.2, check_status=True, labels=None,
                 parent=None):
        super().__init__(x_axis, y_axis, refresh_time, check_status, parent)
        self.refresh_time = refresh_time
        self.check_status = check_status

        if labels:
            self.plot.setLabel('left', labels['left']['label'], units=labels['left']['units'],
                               **self.LABEL_STYLE)
            self.plot.setLabel('bottom', labels['bottom']['label'], units=labels['bottom']['units'],
                               **self.LABEL_STYLE)

    def update_curves(self):
        for item in self.plot.items:
            if isinstance(item, self.ResultsClass):
                self.plot.clear()
                item.update_data()
                brushes = [pg.mkBrush(color=pg.intColor(i, hues=len(item.columns) + 1)) for i in
                           range(len(item.columns))]
                self.plot.addItem(BarResultsCurve(item.results, x=item.x, height=item.height,
                                                  columns=item.columns, brushes=brushes))
                break


class BarGraphWidget(TabWidget, QtWidgets.QWidget):
    """ Extends :class:`PlotFrame<pymeasure.display.widgets.plot_frame.PlotFrame>`
    to allow different columns of the data to be dynamically chosen
    """

    def __init__(self, name, columns, x_axis, x_axis_label=None, limit=None, refresh_time=0.2,
                 check_status=True, linewidth=1, parent=None, labels=None, **kwargs):
        super().__init__(name, parent)
        self.columns = columns
        self.refresh_time = refresh_time
        self.check_status = check_status
        self.linewidth = linewidth
        self.x_axis = x_axis
        self.limit = limit
        self.labels = labels
        self._setup_ui()
        self._layout()

    def _setup_ui(self):

        self.plot_frame = BarFrame(
            self.x_axis,
            None,
            self.refresh_time,
            self.check_status,
            labels=self.labels,
            parent=self,
        )
        self.updated = self.plot_frame.updated
        self.plot = self.plot_frame.plot
        self.plot.addLegend(frame=True)
        self.plot.getAxis('left').setTextPen('black')
        self.plot.getAxis('bottom').setTextPen('black')
        font = QtGui.QFont()
        font.setPixelSize(20)
        self.plot.getAxis("bottom").setStyle(tickFont=font)
        self.plot.getAxis("left").setStyle(tickFont=font)

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
        self.clear_widget()
        if 'pen' not in kwargs:
            kwargs['pen'] = pg.mkPen(color=color, width=self.linewidth)
        if 'antialias' not in kwargs:
            kwargs['antialias'] = False

        cols = []
        for cdx, c in enumerate(self.columns[:self.limit]):
            if c != self.x_axis:
                cols.append(c)
        curve = BarResultsCurve(results,
                                wdg=self,
                                x=range(1, len(cols) + 1),
                                height=[0] * len(cols),
                                columns=cols,
                                brushes=[pg.mkBrush(color=pg.intColor(i, hues=len(cols) + 1),
                                                    width=self.linewidth) for i in
                                         range(len(cols))],
                                )
        return curve

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
        return BarGraphWidget("Plot preview",
                              self.columns,
                              self.x_axis,
                              parent=parent,
                              )

    def clear_widget(self):
        self.plot.clear()
