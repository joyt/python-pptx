# encoding: utf-8

"""
Custom element classes for presentation-related XML elements.
"""

from __future__ import absolute_import

from .ns import _nsmap, qn
from .xmlchemy import BaseOxmlElement, OxmlElement, ZeroOrOne


class CT_Presentation(BaseOxmlElement):
    """
    ``<p:presentation>`` element, root of the Presentation part stored as
    ``/ppt/presentation.xml``.
    """
    sldMasterIdLst = ZeroOrOne('p:sldMasterIdLst', successors=(
        'p:notesMasterIdLst', 'p:handoutMasterIdLst', 'p:sldIdLst',
        'p:sldSz', 'p:notesSz'
    ))
    sldIdLst = ZeroOrOne('p:sldIdLst', successors=('p:sldSz', 'p:notesSz'))
    sldSz = ZeroOrOne('p:sldSz', successors=('p:notesSz',))


class CT_SlideId(BaseOxmlElement):
    """
    ``<p:sldId>`` element, direct child of <p:sldIdLst> that contains an rId
    reference to a slide in the presentation.
    """
    @property
    def rId(self):
        return self.get(qn('r:id'))


class CT_SlideIdList(BaseOxmlElement):
    """
    ``<p:sldIdLst>`` element, direct child of <p:presentation> that contains
    a list of the slide parts in the presentation.
    """
    def __getitem__(self, idx):
        """
        Provide indexed access, (e.g. 'collection[0]').
        """
        return self.getchildren()[idx]

    def __iter__(self):
        return self.iterchildren()

    def add_sldId(self, rId):
        """
        Return a reference to a newly created <p:sldId> child element having
        its r:id attribute set to *rId*.
        """
        sldId = OxmlElement('p:sldId')
        sldId.set('id', self._next_id)
        sldId.set(qn('r:id'), rId)
        self.append(sldId)
        return sldId

    @property
    def _next_id(self):
        """
        Return the next available slide ID as a string. Valid slide IDs start
        at 256. Unused ids in the sequences starting from 256 are used first.
        """
        id_str_lst = self.xpath('./p:sldId/@id', namespaces=_nsmap)
        used_ids = [int(id_str) for id_str in id_str_lst]
        for n in range(256, 258+len(used_ids)):
            if n not in used_ids:
                return str(n)


class CT_SlideMasterIdList(BaseOxmlElement):
    """
    ``<p:sldMasterIdLst>`` element, child of ``<p:presentation>`` containing
    references to the slide masters that belong to the presentation.
    """
    def __len__(self):
        """
        Return the number of ``<p:sldMasterId>`` child elements
        """
        sldMasterId_lst = self.findall(qn('p:sldMasterId'))
        return len(sldMasterId_lst)

    @classmethod
    def new(cls):
        """
        Return a new ``<p:sldMasterIdLst>`` element.
        """
        return OxmlElement('p:sldMasterIdLst')

    @property
    def sldMasterId_lst(self):
        """
        Sequence of ``<p:sldMasterId>`` child elements
        """
        return self.findall(qn('p:sldMasterId'))


class CT_SlideMasterIdListEntry(BaseOxmlElement):
    """
    ``<p:sldMasterId>`` element, child of ``<p:sldMasterIdLst>`` containing
    a reference to a slide master.
    """
    @property
    def rId(self):
        return self.get(qn('r:id'))


class CT_SlideSize(BaseOxmlElement):
    """
    ``<p:sldSz>`` element, direct child of <p:presentation> that contains the
    width and height of slides in the presentation.
    """
    def __setattr__(self, name, value):
        """
        Override ``__setattr__`` defined in ObjectifiedElement super class
        to intercept messages intended for custom property setters.
        """
        if name in ('cx', 'cy'):
            value_str = str(int(value))
            self.set(name, value_str)
        else:
            super(CT_SlideSize, self).__setattr__(name, value)

    @property
    def cx(self):
        return int(self.get('cx'))

    @property
    def cy(self):
        return int(self.get('cy'))
