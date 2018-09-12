from __future__ import absolute_import, unicode_literals
from collections import OrderedDict

import re
import json
import base64
import six.moves.urllib as urllib
import xml.etree.cElementTree as ElementTree


def to_b64(data):
    """
    Encoding data string base64 algorithm
    """
    return base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')


def from_b64(data):
    """
    Encoding data string base64 algorithm
    """
    return base64.b64decode(json.dumps(data).encode('utf-8')).decode('utf-8')


def to_xml(data, start='<?xml version="1.0" encoding="UTF-8"?>'):
    """
    :param data: params to convert to xml
    :param start: start xml string
    :return: xml string
    """
    data = OrderedDict(sorted(data.items()))
    return start + _data2xml(data)


def to_json(data):
    """
    to json string
    :param data: params to convert to xml
    :return: json string
    """
    return json.dumps(data)


def to_form(data):
    """
    to form string
    :param data: params to convert to form data
    :return: encoded url string
    """
    data = OrderedDict(sorted(data.items()))
    return urllib.parse.urlencode(data)


def merge_dict(x, y):
    """
    :param x: firs dict
    :param y: second dict
    :return: merged dict
    """
    z = x.copy()
    z.update(y)
    return z


def join_url(url, *paths):
    """
    :param url: api url
    :param paths: endpoint
    :return: full url
    """
    for path in paths:
        url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
    return url


def from_json(json_string):
    """
    :param json_string: json data string to encode
    :return: data dict
    """
    return json.loads(json_string)


def from_form(form_string):
    """
    :param form_string: form data string to encode
    :return: data dict
    """
    return dict(urllib.parse.parse_qsl(form_string))


def from_xml(xml):
    """
    :param xml: xml string to encode
    :return: data dict
    """
    element = ElementTree.fromstring(xml)
    return _xml_to_dict(element.tag, _parse(element), element.attrib)


def _data2xml(d):
    result_list = list()

    if isinstance(d, list):
        for sub_elem in d:
            result_list.append(_data2xml(sub_elem))

        return ''.join(d)

    if isinstance(d, dict):
        for tag_name, sub_obj in d.items():
            result_list.append("<%s>" % tag_name)
            result_list.append(_data2xml(sub_obj))
            result_list.append("</%s>" % tag_name)

        return ''.join(result_list)

    return "%s" % d


def _parse(node):
    tree = {}
    for c in node.getchildren():
        c_tag = c.tag
        c_attr = c.attrib
        ctext = c.text.strip() if c.text is not None else ''
        c_tree = _parse(c)

        if not c_tree:
            c_dict = _xml_to_dict(c_tag, ctext, c_attr)
        else:
            c_dict = _xml_to_dict(c_tag, c_tree, c_attr)
        if c_tag not in tree:
            tree.update(c_dict)
            continue
        atag = '@' + c_tag
        atree = tree[c_tag]
        if not isinstance(atree, list):
            if not isinstance(atree, dict):
                atree = {}
            if atag in tree:
                atree['#' + c_tag] = tree[atag]
                del tree[atag]
            tree[c_tag] = [atree]

        if c_attr:
            c_tree['#' + c_tag] = c_attr

        tree[c_tag].append(c_tree)
    return tree


def _xml_to_dict(tag, value, attr=None):
    ret = {tag: value}
    if attr:
        atag = '@' + tag
        aattr = {}
        for k, v in attr.items():
            aattr[k] = v
        ret[atag] = aattr
        del atag
        del aattr
    return ret
