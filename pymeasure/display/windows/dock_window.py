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

import logging

from pyqtgraph.dockarea import Dock, DockArea

from .managed_window import ManagedWindowBase
from ..Qt import QtCore, QtGui
from ..widgets import (
    PlotWidget,
    LogWidget
)

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class DockWindow(ManagedWindowBase):
    """
    Display experiment output with an :class:`~pymeasure.display.widget.PlotWidget` class.

    """

    def __init__(self, procedure_class, x_axis=None, y_axis=None, num_plots=1, *args, **kwargs):

        self.x_axis = x_axis
        self.y_axis = y_axis
        self.num_plots = num_plots

        self.log_widget = LogWidget("Experiment Log")
        self.widget_list = []

        super().__init__(
            procedure_class=procedure_class,
            setup=False,
            widget_list=self.widget_list,
            *args,
            **kwargs
        )

        self._setup_ui()
        self._layout()
        self.browser_widget.browser.measured_quantities = [self.x_axis, self.y_axis]

    def _layout(self):
        self.main = QtGui.QWidget(self)

        inputs_dock = QtGui.QWidget(self)
        inputs_vbox = QtGui.QVBoxLayout(self.main)

        hbox = QtGui.QHBoxLayout()
        hbox.setSpacing(10)
        hbox.setContentsMargins(-1, 6, -1, 6)
        hbox.addWidget(self.queue_button)
        hbox.addWidget(self.abort_button)
        hbox.addStretch()

        if self.directory_input:
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(self.directory_label)
            vbox.addWidget(self.directory_line)
            vbox.addLayout(hbox)

        if self.inputs_in_scrollarea:
            inputs_scroll = QtGui.QScrollArea()
            inputs_scroll.setWidgetResizable(True)
            inputs_scroll.setFrameStyle(QtGui.QScrollArea.NoFrame)

            self.inputs.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
            inputs_scroll.setWidget(self.inputs)
            inputs_vbox.addWidget(inputs_scroll, 1)

        else:
            inputs_vbox.addWidget(self.inputs)

        if self.directory_input:
            inputs_vbox.addLayout(vbox)
        else:
            inputs_vbox.addLayout(hbox)

        inputs_vbox.addStretch(0)
        inputs_dock.setLayout(inputs_vbox)

        dock = QtGui.QDockWidget('Input Parameters')
        dock.setWidget(inputs_dock)
        dock.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        if self.use_sequencer:
            sequencer_dock = QtGui.QDockWidget('Sequencer')
            sequencer_dock.setWidget(self.sequencer)
            sequencer_dock.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, sequencer_dock)

        if self.use_estimator:
            estimator_dock = QtGui.QDockWidget('Estimator')
            estimator_dock.setWidget(self.estimator)
            estimator_dock.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, estimator_dock)

        self.tabs = QtGui.QTabWidget(self.main)

        self.dock_area = DockArea()
        self.dock_area.name = 'Dock Tab'
        self.docks = []

        self.tabs.addTab(self.dock_area, self.dock_area.name)

        for i in range(self.num_plots):
            self.widget_list.append(
                PlotWidget("Results Graph", self.procedure_class.DATA_COLUMNS, self.x_axis,
                           self.y_axis))
            dock = Dock("Dock " + str(i + 1), closable=False, size=(200, 50))
            self.dock_area.addDock(dock)
            dock.addWidget(self.widget_list[i])
            dock.nStyle = """
                          Dock > QWidget {
                              border: 1px solid #ff6600;
                              border-radius: 5px;
                          }"""
            dock.dragStyle = """
                          Dock > QWidget {
                              border: 14px solid #ff6600;
                              border-radius: 15px;
                          }"""
            dock.updateStyle()
            self.docks.append(dock)

        self.tabs.addTab(self.log_widget, self.log_widget.name)

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.tabs)
        splitter.addWidget(self.browser_widget)

        vbox = QtGui.QVBoxLayout(self.main)
        vbox.setSpacing(0)
        vbox.addWidget(splitter)

        self.main.setLayout(vbox)
        self.setCentralWidget(self.main)
        self.main.show()
        self.resize(1000, 800)
