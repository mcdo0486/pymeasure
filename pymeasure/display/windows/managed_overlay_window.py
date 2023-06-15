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

from ..widgets.overlay_widget import OverlayWidget
from ..widgets.log_widget import LogWidget
from .managed_window import ManagedWindowBase

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class ManagedOverlayWindow(ManagedWindowBase):
    """
    Display experiment output with multiple docking windows with
    :class:`~pymeasure.display.widgets.dock_widget.DockWidget` class.

    :param procedure_class: procedure class describing the experiment (see
        :class:`~pymeasure.experiment.procedure.Procedure`)
    :param log_fmt: formatting string for the log-widget
    :param log_datefmt: formatting string for the date in the log-widget
    :param \\**kwargs: optional keyword arguments that will be passed to
        :class:`~pymeasure.display.windows.managed_window.ManagedWindowBase`
    """

    def __init__(self, procedure_class, boxes=None, image=None,
                 log_fmt=None, log_datefmt=None, **kwargs):

        measure_quantities = procedure_class.DATA_COLUMNS

        self.log_widget = LogWidget("Experiment Log", fmt=log_fmt, datefmt=log_datefmt)
        self.overlay_widget = OverlayWidget("Overlay", procedure_class, boxes, image)

        if "widget_list" not in kwargs:
            kwargs["widget_list"] = ()
        kwargs["widget_list"] = kwargs["widget_list"] + (self.overlay_widget, self.log_widget)

        super().__init__(procedure_class, **kwargs)

        self.browser_widget.browser.measured_quantities.update(measure_quantities)

        logging.getLogger().addHandler(self.log_widget.handler)
        log.setLevel(self.log_level)
        log.info("DockWindow connected to logging")
