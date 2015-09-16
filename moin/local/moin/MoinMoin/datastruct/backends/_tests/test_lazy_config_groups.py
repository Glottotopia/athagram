# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - MoinMoin.backends.config_lazy_groups tests

    @copyright: 2009 by MoinMoin:DmitrijsMilajevs
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.datastruct.backends._tests import GroupsBackendTest
from MoinMoin.datastruct.backends.config_lazy_groups import ConfigLazyGroups
from MoinMoin.datastruct import ConfigGroups, CompositeGroups, GroupDoesNotExistError
from MoinMoin._tests import wikiconfig


class TestLazyConfigGroups(GroupsBackendTest):

    test_groups = {u'EditorGroup': [u'John', u'JoeDoe', u'Editor1'],
                   u'AdminGroup': [u'Admin1', u'Admin2', u'John'],
                   u'OtherGroup': [u'SomethingOther'],
                   u'EmptyGroup': []}

    expanded_groups = test_groups

    class Config(wikiconfig.Config):

        def groups(self, request):
            groups = TestLazyConfigGroups.test_groups
            return ConfigLazyGroups(request, groups)

    def test_contains_group(self):
        """
        ConfigLazyGroups can not contain other group members.

        This test does not make sense.
        """


class TestCompositeAndLazyConfigGroups(GroupsBackendTest):

    class Config(wikiconfig.Config):

        def groups(self, request):
            config_groups = {u'EditorGroup': [u'AdminGroup', u'John', u'JoeDoe', u'Editor1', u'John'],
                             u'RecursiveGroup': [u'Something', u'OtherRecursiveGroup'],
                             u'OtherRecursiveGroup': [u'RecursiveGroup', u'Anything', u'NotExistingGroup'],
                             u'ThirdRecursiveGroup': [u'ThirdRecursiveGroup', u'Banana'],
                             u'CheckNotExistingGroup': [u'NotExistingGroup']}

            lazy_groups = {u'AdminGroup': [u'Admin1', u'Admin2', u'John'],
                           u'OtherGroup': [u'SomethingOther'],
                           u'EmptyGroup': []}

            return CompositeGroups(request,
                                   ConfigGroups(request, config_groups),
                                   ConfigLazyGroups(request, lazy_groups))


coverage_modules = ['MoinMoin.datastruct.backends.config_lazy_groups']
