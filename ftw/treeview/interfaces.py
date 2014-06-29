from zope import schema
from zope.interface import Interface


class ITreeviewSettings(Interface):
    """Treeview settings schema interface for plone.app.registry"""

    caching_activ = schema.Bool(
        title=u'Caching activ',
        description=u'Treeview caching active.',
        default=False)
