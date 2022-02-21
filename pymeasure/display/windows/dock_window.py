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

from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import Dock, DockArea
from PyQt5.QtCore import QFile, QTextStream

from .managed_window import ManagedWindowBase
from ..browser import BrowserItem
from ..manager import Manager, Experiment
from ..Qt import QtCore, QtGui
from ..widgets import (
    PlotWidget,
    BrowserWidget,
    InputsWidget,
    LogWidget,
    ResultsDialog,
    SequencerWidget,
    DirectoryLineEdit,
    EstimatorWidget,
)
from .multiplot_window import MultiPlotWindow
from ...experiment import Results, Procedure

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

        self.dock_area = DockArea()
        self.dock_area.name = 'Dock Tab'
        self.docks = []

        self.plot_widgets = []

        if "widget_list" not in kwargs:
            kwargs["widget_list"] = ()
        kwargs["widget_list"] = kwargs["widget_list"] + (self.dock_area, self.log_widget)

        super().__init__(
            procedure_class=procedure_class,
            setup=False,
            *args,
            **kwargs
        )

        for i in range(self.num_plots):
            self.plot_widgets.append(
                PlotWidget("Results Graph", procedure_class.DATA_COLUMNS, self.x_axis, self.y_axis))
            dock = Dock("Dock", closable=False, size=(200, 50))
            self.dock_area.addDock(dock)
            dock.addWidget(self.plot_widgets[i])
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

        self._setup_ui()
        self._layout()
        self.browser_widget.browser.measured_quantities = [self.x_axis, self.y_axis]
