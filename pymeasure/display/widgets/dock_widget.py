#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2022 PyMeasure Developers
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
from os import path

import json

import logging

from pyqtgraph.dockarea import Dock, DockArea
import pyqtgraph as pg

from .plot_widget import PlotWidget
from ..Qt import QtWidgets
from .tab_widget import TabWidget

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class DockWidget(TabWidget, QtWidgets.QWidget):
    """
    Widget that contains a DockArea with a number of Docks as determined by num_plots.

    :param name: Name for the TabWidget
    :param procedure_class: procedure class describing the experiment (see
        :class:`~pymeasure.experiment.procedure.Procedure`)
    :param x_axis_labels: List of data column(s) for the x-axis of the plot.
    :param y_axis_labels: List of data column(s) for the y-axis of the plot.
    :param num_plots: the number of plots you want displayed in the DockWindow tab
    :param linewidth: line width for plots in
        :class:`~pymeasure.display.widgets.plot_widget.PlotWidget`
    :param parent: Passed on to QtWidgets.QWidget. Default is None
    """

    def __init__(self, name, procedure_class, x_axis_labels=None, y_axis_labels=None, linewidth=1,
                 parent=None):
        self.procedure_class = procedure_class
        self.procedure_name = procedure_class.__name__
        super().__init__(name, parent)

        self.x_axis_labels = x_axis_labels
        self.y_axis_labels = y_axis_labels

        self.num_plots = max(len(self.x_axis_labels), len(self.y_axis_labels))

        self.linewidth = linewidth

        self.dock_area = DockArea()
        self.docks = []
        self.plot_frames = []

        self._setup_ui()
        self._layout()

    def _setup_ui(self):
        for i in range(self.num_plots):
            # Set the default label for current dock from x_axis_labels and y_axis_labels
            # However, if list is smaller than num_plots, repeat last item in the list.
            x_label = self.x_axis_labels[min(i, len(self.x_axis_labels) - 1)]
            y_label = self.y_axis_labels[min(i, len(self.y_axis_labels) - 1)]

            dock = Dock("Dock " + str(i + 1), closable=False, size=(200, 50))
            self.dock_area.addDock(dock)
            self.plot_frames.append(
                PlotWidget("Results Graph", self.procedure_class.DATA_COLUMNS, x_label,
                           y_label, linewidth=self.linewidth))
            dock.addWidget(self.plot_frames[i])
            self.docks.append(dock)

    def save_dock_state(self):
        state = self.dock_area.saveState()
        with open(path.curdir + '/' + self.procedure_name + '_dock_state.json', 'w') as f:
            f.write(json.dumps(state))

    def _layout(self):
        hbox = QtWidgets.QHBoxLayout()
        self.save_layout = QtWidgets.QPushButton('Save Layout', self)
        self.save_layout.clicked.connect(self.save_dock_state)
        hbox.addStretch(5)
        hbox.addWidget(self.save_layout, 1)

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.setSpacing(0)
        vbox.addLayout(hbox)
        vbox.addWidget(self.dock_area)
        self.setLayout(vbox)

        if path.exists(path.curdir + '/' + self.procedure_name + '_dock_state.json'):
            with open(path.curdir + '/' + self.procedure_name + '_dock_state.json', 'r') as f:
                dock_state = f.read()
                # make sure the dock count matches number of plots
                if dock_state.count('dock') == self.num_plots:
                    self.dock_area.restoreState(json.loads(dock_state))

    def new_curve(self, results, color=pg.intColor(0), **kwargs):
        if 'pen' not in kwargs:
            kwargs['pen'] = pg.mkPen(color=color, width=self.linewidth)
        if 'antialias' not in kwargs:
            kwargs['antialias'] = False
        curves = []
        for i in range(self.num_plots):
            curves.append(self.plot_frames[i].new_curve(results, color=pg.intColor(0), **kwargs))
        return curves

    def update_x_column(self, index):
        for i in range(self.num_plots):
            self.plot_frames[i].update_x_column(index)

    def update_y_column(self, index, plot_idx):
        axis = self.columns_y[plot_idx].itemText(index)
        self.plot_frames[plot_idx].change_y_axis(axis)

    def clear(self):
        for i in range(self.num_plots):
            self.plot_frames[i].plot.clear()
