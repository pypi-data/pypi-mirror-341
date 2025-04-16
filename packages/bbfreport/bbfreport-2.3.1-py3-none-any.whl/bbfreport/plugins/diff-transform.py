"""Diff transform plugin."""

# Copyright (c) 2023-2024, Broadband Forum
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials
#    provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The above license is used as a license under copyright only.
# Please reference the Forum IPR Policy for patent licensing terms
# <https://www.broadband-forum.org/ipr-policy>.
#
# Any moral rights which are necessary to exercise under the above
# license grant are also deemed granted under this license.

import cProfile
import difflib
import pstats
import re
import sys
import time

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union

from ..content import _MacroRefClose
from ..macro import Macro
from ..node import DataTypeRef, Description, _HasContent, Model, _ModelItem, \
    Node, Root, _ValueFacet
from ..path import relative_path
from ..utility import ScopeEnum

Diffs = dict[Union[_ModelItem, _ValueFacet], list['Diff']]

# XXX need to optimize h_elems, which calls h_objects, which calls
#     objpath; h_elems is only needed to associate object addition and
#     deletion with the correct parent; everything is much better if
#     _path_split is cached
time_it = False


# XXX in general should make more use of Enums and dataclasses
class Entity(Enum):
    attr = 1
    elem = 2
    content = 3


class Operation(Enum):
    added = 1
    removed = 2
    changed = 3


# XXX in general should make more use of dataclasses
# XXX note that defining them as nested classes is VERY slow
# XXX there should also be a Diffs class
@dataclass
class Diff:
    old_node: Node
    new_node: Node
    entity: Entity
    operation: Operation
    # XXX python 3.10 _: KW_ONLY = None
    name: Optional[str] = None
    value: Optional[Any] = None
    value2: Optional[Any] = None
    elem: Optional[Node] = None
    is_whitespace: Optional[bool] = False

    @staticmethod
    def append(diffs: Diffs, old_node: Node, new_node: Node, entity: Entity,
               operation: Operation, *, name: Optional[str] = None,
               value: Optional[Any] = None, value2: Optional[Any] = None,
               elem: Optional[Node] = None,
               is_whitespace: bool = False) -> None:
        # we refer to it as a model item, but in fact it can be either a model
        # item (object, parameter, command, event, ...) or a value facet
        # (enumeration, pattern), all of which have descriptions
        model_item_node = \
            new_node.instance_in_path((_ModelItem, _ValueFacet)) or new_node
        diffs.setdefault(model_item_node, []).append(
                Diff(old_node, new_node, entity, operation, name=name,
                     value=value, value2=value2, elem=elem,
                     is_whitespace=is_whitespace))

    def __str__(self):
        name = self.name if self.name else self.elem.typename if self.elem \
            else self.entity.name
        text = '%s %s' % (self.operation.name, name)
        if self.is_whitespace:
            text += ' (W)'
        if self.entity == Entity.attr:
            text += ' %s' % self.value
            if self.operation == Operation.changed:
                text += ' -> %s' % self.value2
        elif self.entity == Entity.elem:
            if str(self.elem) != name:
                text += ' %s' % self.elem
        elif self.entity == Entity.content:
            i1, i2, c1 = self.value
            j1, j2, c2 = self.value2
            if i2 > i1:
                text += ' %r' % Macro.clean(''.join(str(c) for c in c1))
            if i2 > i1 and j2 > j1:
                text += ' ->'
            if j2 > j1:
                text += ' %r' % Macro.clean(''.join(str(c) for c in c2))
        return text

    __repr__ = __str__


# need two files on the command line
# XXX what if there are two models in a single file?
def _post_init_(args, logger) -> Optional[bool]:
    if len(args.file) != 2:
        logger.error('need two files (old and new) on the command line '
                     '(%d were supplied)' % len(args.file))
        return True

    # XXX should this be unconditional?
    logger.debug('auto-enabled --show')
    args.show = True


def visit(root: Root, args, logger) -> Optional[bool]:
    # get the models from the command-line documents
    models = []
    for xml_file in root.xml_files:
        dm_document = xml_file.dm_document
        for model in dm_document.models:
            models.append(model)

    if len(models) != 2 or models[0] is models[1]:
        logger.error('need two models to compute diffs')
        return True

    # enable profiling?
    profile = None
    if time_it:
        profile = cProfile.Profile()
        profile.enable()

    # we need to traverse the two models, comparing them
    # XXX this isn't yet comparing referenced items such as data types
    def key_str(mod: Model) -> str:
        return '{%s}%s' % mod.key

    logger.info('comparing %s and %s' % (
        key_str(models[0]), key_str(models[1])))
    start = time.time()
    diffs = node_diffs(models[0], models[1], logger=logger)
    logger.info('compared %s and %s in %d ms' % (
        key_str(models[0]), key_str(models[1]), (time.time() - start) * 1000))

    # disable profiling?
    if time_it:
        profile.disable()
        stats = pstats.Stats(profile, stream=sys.stderr)
        stats.strip_dirs()
        stats.sort_stats('time')
        stats.print_stats(50)
        # XXX it doesn't seem possible to control the caller/callee order?
        stats.print_callers(20)
        stats.print_callees(20)

    # hide the entire node tree
    root.hide()

    # {{diffs}} macro argument formatting helpers
    def emph_str(txt: str) -> str:
        return '*%s*' % txt if txt else '""'

    def elem_typ(nod: Node) -> str:
        # omitting 'dataTypeRef' is cosmetic
        return {'dataTypeRef': ''}.get(nod.typename, nod.typename)

    def elem_str(nod: Node) -> str:
        return relative_path(nod.objpath, new_node.objpath,
                             scope=ScopeEnum('absolute')) \
            if isinstance(nod, _ModelItem) else val if (val := str(nod)) \
            else ''

    def elem_ref(nod: Node) -> str:
        # XXX there should be a method/utility for this
        macro = nod.typename.replace('parameter', 'param')
        # noinspection PyProtectedMember
        return '{{%s|%s|object}}' % (macro, elem_str(nod)) \
            if isinstance(nod, _ModelItem) and macro in Macro._macros \
            else emph_nod(nod)

    def emph_nod(nod: Node) -> str:
        return '*%s*' % val if (val := elem_str(nod)) else ''

    def elem_flt(ctx: str, val: str, term: str = '') -> str:
        return val + term if val not in ctx else ''

    # add {{diffs}} macros to the second model
    # XXX and content changes
    counts = {}
    for model_item, model_item_diffs in diffs.items():
        str_model_item = str(model_item)
        macro_args = []
        body = []
        new_node = None
        new_body = None
        j = 0
        any_attr_diff = any(d.entity == Entity.attr for d in model_item_diffs)
        any_elem_diff = any(d.entity == Entity.elem for d in model_item_diffs)
        any_cont_diff = any(d.entity == Entity.content
                            and not d.is_whitespace for d in model_item_diffs)
        for model_item_diff in model_item_diffs:
            old_node, new_node, entity, operation, name, value, value2 = (
                model_item_diff.old_node, model_item_diff.new_node,
                model_item_diff.entity, model_item_diff.operation,
                model_item_diff.name, model_item_diff.value,
                model_item_diff.value2)

            # these are used for various tests and messages
            node = old_node if operation == Operation.removed else new_node
            str_node = str(node)

            # ignore some data type changes; this is primarily intended to
            # ignore Alias -> _AliasUSP changes (and currently these are the
            # only changes that it catches)
            if isinstance(old_node, DataTypeRef) and \
                    str(new_node) == str(old_node) and \
                    new_node.base != old_node.base:
                logger.info('%s: ignored %s %s -> %s change' % (
                    node.nicepath, node.typename, old_node.base,
                    new_node.base))
                continue

            # omit dataTypeRef base when ref is also specified (cosmetic)
            if isinstance(old_node, DataTypeRef) and (entity, name) == (
                    Entity.attr, 'base') and node.ref:
                logger.info('%s: ignored attribute base = %s because ref '
                            '= %s is specified' % (
                                node.nicepath, value, node.ref))
                continue

            # ignore some attribute removals
            if (entity, operation, name, str(value)) in {
                (Entity.attr, Operation.removed, 'access', 'readOnly'),
                (Entity.attr, Operation.removed, 'minEntries', '1'),
                (Entity.attr, Operation.removed, 'maxEntries', '1')}:
                logger.info('%s: ignored removed attribute %s = %s' % (
                    node.nicepath, name, value))
                continue

            # if the node matches --debugpath, log at the info level
            logger_func = logger.info if args.debugpath and re.search(
                    args.debugpath, new_node.debugpath) else logger.debug
            logger_func('%s %s %s' % (node.nicepath, node.typename,
                                      model_item_diff))

            # unhide the changed node and its ancestors (and their
            # description elements)
            if any_attr_diff or any_elem_diff or any_cont_diff:
                new_node.h_unhide(description=True, upwards=True)
                # logger.debug('%s %s (and up) unhidden' % (
                #     new_node.nicepath, new_node.typename))

            # provide some additional context if the model item node isn't the
            # new node (the node that changed); it will always be an ancestor
            context = ''
            if str_node != str_model_item:
                # don't include content (e.g, descriptions) in the context;
                # also don't include it if it essentially duplicates typename
                if not isinstance(node, _HasContent) and str_node != \
                        '' and node.typename not in str_node and \
                        (value2 or '') != str_node:
                    context += '*%s* ' % str_node
                context += '%s ' % node.typename

            if entity == Entity.attr:
                # XXX I can't decide whether to include 'attribute ' here
                include_attribute = False
                attribute = 'attribute ' if include_attribute else ''
                macro_arg = '%s %s%s%s = %s%s' % (
                    operation.name.capitalize(), context, attribute, name,
                    emph_str(value), ' &rArr; %s' % emph_str(
                            value2) if value2 is not None else '')
                macro_args.append(macro_arg)

            elif entity == Entity.elem:
                elem = model_item_diff.elem
                if operation == Operation.added:
                    ref = elem_flt(context, elem_ref(elem), term=' ')
                    typ = elem_flt(context, elem_typ(elem))

                    # try to convert 'Removed OLD TYP' and 'Added NEW TYP' to
                    # 'Changed TYP = OLD -> NEW'
                    # XXX it would be nice if this could handle promotion of
                    #     diagnostic OBJ. to OBJ() command ... but it can't
                    new_arg = 'Added %s%s%s' % (context, ref, typ)
                    if macro_args and (old_arg := macro_args[-1]):
                        old_words, new_words = old_arg.split(), new_arg.split()
                        if len(old_words) > 2 and len(new_words) > 2 and \
                                old_words[0] == 'Removed' and new_words[2] == \
                                old_words[2]:
                            new_arg = 'Changed %s = %s -> %s' % (
                                new_words[2], old_words[1], new_words[1])
                            del macro_args[-1]

                    macro_args.append(new_arg)
                    # unhide the new elem, its children and ancestors
                    elem.h_unhide(upwards=False)
                    elem.h_unhide(upwards=True)
                    # logger.debug('%s %s (and down and up) unhidden' % (
                    #     elem.nicepath, elem.typename))
                elif operation == Operation.removed:
                    # we won't try to reference it; it's no longer there!
                    val = elem_flt(context, emph_nod(elem), term=' ')
                    typ = elem_flt(context, elem_typ(elem))
                    macro_args.append('Removed %s%s %s' % (context, val, typ))

            elif entity == Entity.content:
                assert operation == Operation.changed, \
                    'invalid operation %s' % operation.name
                old_body = old_node.content.get_body_as_list(collapse=True)
                new_body = new_node.content.get_body_as_list(collapse=True)

                # XXX should use better variable names
                tag = name
                i1, i2, _ = value
                j1, j2, _ = value2

                # if the first in new_body is a close(), move it to body; this
                # avoids problems when inserting (e.g.) '}} {{enum|X'
                # XXX this isn't a proper fix; the diffs need to be more
                #     macro-aware
                if j2 > j1 and isinstance(new_body[j1], _MacroRefClose):
                    j1 += 1

                # add items since the last run to body
                if j1 > j:
                    body.extend(new_body[j:j1])

                # convert 'old' to a string and escape special characters,
                # because it might reference deprecated, obsoleted or
                # deleted items
                old = ''.join(Macro.escape(str(s)) for s in old_body[i1:i2])
                new = ''.join(str(s) for s in new_body[j1:j2])
                if tag == 'replace':
                    # XXX this can cause problems when old closes a macro and
                    #     opens another one (same for new?); for example,
                    #     [close(param), ' ', 'and', open(param), 'B'] -> [];
                    #     this will happen with '{{param|A}} and {{param|B}}'
                    #     -> '{{param|A}}' (I thought that including a macro
                    #     nesting level might help, but I don't think it does)
                    body.append('{{replaced|%s|%s}}' % (old, new))
                    # body.append('{{removed|%s}}' % old)
                    # body.append('{{inserted|%s}}' % new)
                elif tag == 'delete':
                    body.append('{{removed|%s}}' % old)
                elif tag == 'insert':
                    body.append('{{inserted|%s}}' % new)

                j = j2

            counts.setdefault((model_item_diff.entity,
                               model_item_diff.operation), 0)
            counts[(model_item_diff.entity, model_item_diff.operation)] += 1

        if macro_args:
            if not model_item.description:
                # XXX it's necessary to create the content like this, or else
                #     to call merge(); you can't just do something like
                #     node.description.content = Content() because this ends
                #     up with two Content objects; such things should be
                #     detected
                model_item.description = Description(data=(('content', ()),))
            footer = '{{diffs|%s}}' % '|'.join(macro_args)
            model_item.description.content.footer = footer
            logger.debug('%s %s footer %r' % (
                model_item.nicepath, model_item.typename, footer))

        if new_node:
            if new_body and 0 < j < len(new_body):
                body.extend(new_body[j:])
            if body:
                content = ''.join(str(s) for s in body)
                footer = model_item.description.content.footer
                model_item.description.content = content
                model_item.description.content.footer = footer

    logger.debug('appended {{diffs}} macro refs: %s' % ', '.join(
            '%s %s = %s' % (ent.name, op.name, val) for (ent, op), val in
            sorted(counts.items(), key=lambda i: [x.name for x in i[0]])))


# attr names and node typenames to ignore when comparing nodes
# XXX I'm not sure whether or not to include 'functional' here
# XXX it would be better not to ignore them, but not always to report them
# XXX profiles are complicated, so ignore them for now
ignored_attrnames = {'action', 'activeNotify', 'dmr_previousParameter',
                     'dmr_previousObject', 'dmr_previousCommand',
                     'dmr_previousEvent', 'dmr_previousProfile', 'dmr_version',
                     'functional', 'targetParent', 'version'}
ignored_typenames = {'cdata', 'componentRef', 'profile'}


# XXX this should be a _Node method and should use comparison operators, where
#     (a <= b, a == b, a > b) mean (b is a valid later version of a, b is the
#     same as a, b is an invalid extension of a); there should also be
#     functional versions of the comparison operators that return the diffs)
def node_diffs(old_node: Node, new_node: Node, *,
               diffs: Optional[Diffs] = None, logger, level: int = 0) -> Any:
    if diffs is None:
        diffs = {}

    # sanity check
    assert type(old_node) is type(new_node)

    # attributes have names, so it's easy to tell what's been added etc.
    attrs_changed = {name: (value, new_node.attrs[name]) for name, value in
                     old_node.attrs.items() if name not in ignored_attrnames
                     and name in new_node.attrs
                     and new_node.attrs[name] != value}
    attrs_removed = {name: value for name, value in old_node.attrs.items()
                     if name not in ignored_attrnames
                     and name not in new_node.attrs}
    attrs_added = {name: value for name, value in new_node.attrs.items()
                   if name not in ignored_attrnames
                   and name not in old_node.attrs}

    if attrs_changed:
        for name, (old_, new_) in attrs_changed.items():
            Diff.append(diffs, old_node, new_node, Entity.attr,
                        Operation.changed, name=name, value=old_, value2=new_)
    if attrs_removed:
        for name, value in attrs_removed.items():
            Diff.append(diffs, old_node, new_node, Entity.attr,
                        Operation.removed, name=name, value=value)
    if attrs_added:
        for name, value in attrs_added.items():
            Diff.append(diffs, old_node, new_node, Entity.attr,
                        Operation.added, name=name, value=value)

    # elements are a bit harder (it depends on whether they're keyed)
    elem2s_both = set()
    for elem1 in old_node.h_elems:
        # should this element be ignored?
        if elem1.typename in ignored_typenames:
            continue

        # XXX new_node won't contain an item with the same key; need to know
        #     how many components to ignore; for now, assume 1 (the name of
        #     the file that defined the model; see node.py Model._calckey())
        elem2s = [elem2 for elem2 in new_node.h_elems if
                  elem2.typename == elem1.typename and (
                          not elem2.key or elem2.key[1:] == elem1.key[1:])]

        # if there are multiple matches, try str()
        if len(elem2s) > 1:
            elem2s = [elem2 for elem2 in new_node.h_elems if
                      elem2.typename == elem1.typename and
                      str(elem2) == str(elem1)]

        # if there are no matches, it's been removed (this should be
        # highlighted by the format)
        if not elem2s:
            # report at the info level because it's not a key aspect of this
            # transform, and because the difflint transform will report it
            logger.info('%s: removed %s %s' % (
                old_node.nicepath, elem1.typename, elem1.keylast or elem1))
            Diff.append(diffs, old_node, new_node, Entity.elem,
                        Operation.removed, elem=elem1)
            continue

        # if there are multiple matches, it's an error
        if len(elem2s) > 1:
            elem2s_for_report = [elem2.keylast or elem2 for elem2 in elem2s]
            logger.error('%s: multiple %s matches %s' % (
                old_node.nicepath, elem1.typename, elem2s_for_report))
            continue

        elem2 = elem2s[0]
        node_diffs(elem1, elem2,
                   diffs=diffs, logger=logger, level=level + 1)

        elem2s_both.add(elem2)

    # check for added elems
    elem2s_added = [elem2 for elem2 in new_node.h_elems if
                    elem2.typename not in ignored_typenames and
                    elem2 not in elem2s_both]
    for elem2 in elem2s_added:
        Diff.append(diffs, old_node, new_node, Entity.elem, Operation.added,
                    elem=elem2)

    # check for changed content
    # XXX should move the difflib logic to Content
    if isinstance(old_node, _HasContent):
        assert isinstance(new_node, _HasContent)
        cont1 = old_node.content
        cont2 = new_node.content
        if not cont1 or not cont2 or cont2 != cont1:
            body1 = cont1.get_body_as_list(collapse=True)
            body2 = cont2.get_body_as_list(collapse=True)
            matcher = difflib.SequenceMatcher(None, body1, body2)
            done_header = False
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                chunk1 = body1[i1:i2]
                chunk2 = body2[j1:j2]

                # whitespace-only changes are added here, but can be ignored
                # when rendering the diffs
                is_whitespace = False

                # ignore unchanged chunks
                if tag == 'equal':
                    continue

                # check for a whitespace-only change
                if all(isinstance(s, str) and (not s or s.isspace()) for s in
                       chunk1) and all(
                        isinstance(s, str) and (not s or s.isspace()) for s in
                        chunk2):
                    is_whitespace = True

                # this is a whitespace-only change, and is due to paragraph
                # wrapping
                # XXX for now, take the easy way out and compare them as
                #     strings (will redo this later)
                # XXX should generalize this to check for any 'close then
                #     open' within a chunk, because this is harder to handle
                para_sep = '[close(div), open(div), call(classes), argsep(|)]'
                space_set = {r"[' ']", r"['\n\n']", r"[' ', '\n\n']",
                             r"[call(nl)]", r"[call(np)]"}
                if str(chunk1) in space_set and str(chunk2) == para_sep:
                    is_whitespace = True

                # this is another whitespace-only change, and is due to using
                # status="append" to append to a description
                # XXX see the XXX comments to the above case
                if str(chunk1) == para_sep and str(chunk2) in space_set:
                    is_whitespace = True

                # debug: output header if not already done
                if not done_header:
                    logger.debug('%s' % new_node.nicepath)
                    logger.debug('  %d body1 %s' % (len(body1), body1))
                    logger.debug('  %d body2 %s' % (len(body2), body2))
                    done_header = True

                # debug: report chunk
                white = '(W)' if is_whitespace else '...'
                logger.debug('    %-7s value[%d:%d] -> value2[%d:%d] %s '
                             '%r -> %r' % (
                                 tag, i1, i2, j1, j2, white, chunk1, chunk2))

                # append the diff
                # XXX it would probably be better to add a single diff outside
                #     this loop (it would make the logic clearer)
                Diff.append(diffs, old_node, new_node, Entity.content,
                            Operation.changed, name=tag,
                            value=(i1, i2, chunk1), value2=(j1, j2, chunk2),
                            is_whitespace=is_whitespace)
    return diffs
