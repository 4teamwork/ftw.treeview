from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from Products.CMFPlone.browser.navigation import CatalogNavigationTree
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from Acquisition import aq_inner

from navtree import  buildFolderTree



class TreeView(CatalogNavigationTree):

    recurse = ViewPageTemplateFile('recurse.pt')
    
    def render(self):
        """return a html tree for treeview"""
        
        current = context = aq_inner(self.context)
        # Don't travsere to top-level application obj if TreePortlet
        # was added to the Plone Site Root
        if current.Type() == 'Plone Site':
            return current.Title()
        else:  
            while current.Type() != 'RepositoryRoot':
                current = current.aq_parent
        return current.Title()


        queryBuilder = NavtreeQueryBuilder(context)

        #XXX use querybuilder... 
        #query = queryBuilder()
        query = {'path': dict(query='/'.join(current.getPhysicalPath()), depth=-1), 
                 'Type': 'RepositoryFolder'}
        strategy = getMultiAdapter((context, self), INavtreeStrategy)
        data = buildFolderTree(context, obj=context, query=query, strategy=strategy)
        children = data.get('children')[0].get('children')
        html=self.recurse(children=children,level=1, bottomLevel=999)
        return html
        # queryBuilder = NavtreeQueryBuilder
        # strategy = getMultiAdapter((aq_inner(self.context), self),
        #                            INavtreeStrategy)
        # 
        # query=queryBuilder()
        # 
        # data=buildFolderTree(root, query=query, strategy=strategy)
        # html=self.recurse(children=data.get('children', []), level=1, bottomLevel=0)
        # 
        # return html.encode('utf8')
