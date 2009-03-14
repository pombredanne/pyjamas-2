# Copyright 2006 James Tauber and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __pyjamas__ import JS
from pyjamas import DOM

from pyjamas.ui.SimplePanel import SimplePanel
from pyjamas.ui.Event import Event

class ScrollPanel(SimplePanel):
    def __init__(self, child=None):
        SimplePanel.__init__(self)
        self.scrollListeners = []

        self.setAlwaysShowScrollBars(False)
        self.sinkEvents(Event.ONSCROLL)

        if child != None:
            self.setWidget(child)

    def addScrollListener(self, listener):
        self.scrollListeners.append(listener)

    def ensureVisible(self, item):
        scroll = self.getElement()
        element = item.getElement()
        self.ensureVisibleImpl(scroll, element)

    def getScrollPosition(self):
        return DOM.getIntAttribute(self.getElement(), "scrollTop")

    def getHorizontalScrollPosition(self):
        return DOM.getIntAttribute(self.getElement(), "scrollLeft")

    def onBrowserEvent(self, event):
        type = DOM.eventGetType(event)
        if type == "scroll":
            for listener in self.scrollListeners:
                listener.onScroll(self, self.getHorizontalScrollPosition(), self.getScrollPosition())

    def removeScrollListener(self, listener):
        self.scrollListeners.remove(listener)

    def setAlwaysShowScrollBars(self, alwaysShow):
        if alwaysShow:
            style = "scroll"
        else:
            style = "auto"
        DOM.setStyleAttribute(self.getElement(), "overflow", style)

    def setScrollPosition(self, position):
        DOM.setIntAttribute(self.getElement(), "scrollTop", position)

    def setHorizontalScrollPosition(self, position):
        DOM.setIntAttribute(self.getElement(), "scrollLeft", position)

    def ensureVisibleImpl(self, scroll, e):
        JS("""
        if (!e) return;

        var item = e;
        var realOffset = 0;
        while (item && (item != scroll)) {
            realOffset += item.offsetTop;
            item = item.offsetParent;
            }

        scroll.scrollTop = realOffset - scroll.offsetHeight / 2;
        """)

