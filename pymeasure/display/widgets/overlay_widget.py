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
from ...experiment import Procedure

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
import random


class ResultsBox:
    """ Creates a curve loaded dynamically from a file through the Results object. The data can
    be forced to fully reload on each update, useful for cases when the data is changing across
    the full file instead of just appending.
    """

    def __init__(self, results, column, label=None, force_reload=False, wdg=None, **kwargs):
        super().__init__(**kwargs)
        self.results = results
        self.wdg = wdg
        self.column = column
        self.force_reload = force_reload
        self.label = label
        # self.color = self.opts['pen'].color()

    def update_data(self):
        """Updates the data by polling the results"""
        if self.force_reload:
            self.results.reload()
        data = self.results.data  # get the current snapshot
        if data.size: self.label.setText("%g" % data[self.column].iloc[-1])


class OverlayWidget(TabWidget, QtWidgets.QWidget):
    """ Widget to display a Markdown formatted README file

        :param name: Name for the TabWidget
        :param filename: Path to README file
    """
    updated = QtCore.Signal()

    def __init__(self, name, procedure, boxes=None, image=None, refresh_time=0.2,
                 check_status=True, parent=None):
        super().__init__(name, parent)
        self.ResultsClass = ResultsBox
        self.columns = procedure.DATA_COLUMNS
        self.image = image
        self.boxes = boxes
        self.result_boxes = set()
        self.labels = {}
        self.refresh_time = refresh_time
        self.check_status = check_status
        self._setup_ui()

    def _setup_ui(self):
        pixmap = QtGui.QPixmap(self.image)
        label = QtWidgets.QLabel(self)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.setSpacing(0)
        vbox.addWidget(label)

        for i in self.boxes:
            self.labels[i] = QtWidgets.QLineEdit(self)
            self.labels[i].setAlignment(QtCore.Qt.AlignCenter)
            self.labels[i].setReadOnly(True)
            self.labels[i].setMaxLength(5)
            self.labels[i].setFixedSize(56, 25)
            self.labels[i].setText(i[12:])
            self.labels[i].move(self.boxes[i][0], self.boxes[i][1])

        self.setLayout(vbox)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_curves)
        self.timer.timeout.connect(self.updated)
        self.timer.start(int(self.refresh_time * 1e3))

    def update_curves(self):
        first_box = False
        for first_box in self.result_boxes:
            break
        if first_box:
            data = first_box.results.data
            if not data.empty:
                for item in self.result_boxes:
                    if isinstance(item, self.ResultsClass):
                        if self.check_status:
                            if item.results.procedure.status == Procedure.RUNNING:
                                item.label.setText("%g" % data[item.column].iloc[-1])
                        else:
                            item.label.setText("%g" % data[item.column].iloc[-1])

    def sizeHint(self):
        return QtCore.QSize(300, 600)

    def new_curve(self, results, color=pg.intColor(0), **kwargs):
        curves = []
        for column in self.boxes:
            curves.append(
                ResultsBox(results, column, label=self.labels[column], wdg=self, **kwargs))
        return curves

    def load(self, curve):
        curve.update_data()
        self.result_boxes.add(curve)

    def remove(self, curve):
        self.result_boxes.remove(curve)

    def set_color(self, curve, color):
        """ Change the color of the pen of the curve """
        curve.set_color(color)

    def preview_widget(self, parent=None):
        """ Return a widget suitable for preview during loading """
        return None

    def clear_widget(self):
        self.plot.clear()
