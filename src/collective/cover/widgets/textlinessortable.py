# -*- coding: utf-8 -*-

from collective.cover.widgets.interfaces import ITextLinesSortableWidget
from plone.app.uuid.utils import uuidToObject
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import textlines
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
import zope.interface


class TextLinesSortableWidget(textlines.TextLinesWidget):
    """ Widget for adding new keywords and autocomplete with the ones in the
    system.
    """
    zope.interface.implementsOnly(ITextLinesSortableWidget)
    klass = u"textlines-sortable-widget"
    display_template = ViewPageTemplateFile('textlines_sortable_display.pt')
    input_template = ViewPageTemplateFile('textlines_sortable_input.pt')

    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)

    def sort_results(self):
        results = [{'obj': uuidToObject(x), 'uuid': x} for x in self.context['uuids']]

        return results

    def thumbnail(self, item):
        scales = item.restrictedTraverse('@@images')
        try:
            return scales.scale('image', 'tile')
        except:
            return None


@zope.interface.implementer(interfaces.IFieldWidget)
def TextLinesSortableFieldWidget(field, request):
    """IFieldWidget factory for TextLinesWidget."""
    return widget.FieldWidget(field, TextLinesSortableWidget(request))
