import re

import markdown

from graph_comparison import GraphTester
from util import splitcode

HEADER_R = re.compile(r'^h[1-9]$', re.I)

graphtester = GraphTester()


def t_function(data, title):
    assert len(data) > 1
    assert data[0][0].lower() == 'xml', data
    for (format, code, args) in data:
        graph, errors = graphtester.process_line(
            format, code, args)
        assert not errors, title + ' ' + repr(errors)


def test_document():
    m = markdown.Markdown()
    data = open('documentation.md').read().decode('utf-8')
    root = m.parser.parseDocument(data.split('\n')).getroot()
    data = []
    title = ''
    for element in root.getiterator():
        if HEADER_R.match(element.tag):
            if data:
                yield t_function, data, title
                data = []
            title = element.text
        if element.tag == 'pre':
            sub = list(element)
            assert len(sub) == 1 and sub[0].tag == 'code'
            format, text, args = splitcode(sub[0].text)
            if format:
                data.append((format, text, args))
    if data:
        yield t_function, data, title
