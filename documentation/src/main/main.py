from flask import Flask, make_response, request
from os import path
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.formatter import Formatter
from pygments.lexer import RegexLexer, words
from pygments.style import Style
from pygments.token import *
from pygments.token import Keyword, Whitespace, Name, Comment, String, Number, Literal, Punctuation
from sys import argv


# inherited from TangoStyle (https://kite.com/docs/python/pygments.styles.tango.TangoStyle)
class LSFStyle(Style):
    background_color = "#ffffff"
    default_style = ""

    styles = {
        Whitespace:                "#ffffff",        # class: 'w'
        Comment:                   "#808080", 		 # class: 'c'
        Keyword:                   "bold #336699",   # class: 'k'

        Name:                      "#000000",        # class: 'n'
        Name.Decorator:            "#ff1493",	     # class: 'nd'

        Number:                    "#009900",        # class: 'm'
        Number.Float:              "#009900",        # class: 'mf'
        Number.Integer:            "#009900",        # class: 'mi'
        Number.Integer.Long:       "#009900",        # class: 'il'

        Literal:                   "#009900",        # class: 'l'
        Literal.Date:              "#009900",        # class: 'ld'

        Punctuation:               "#000000",		 # class: 'p'

        String:                    "#009900",        # class: 's'
    }


class HabrLSFStyle(Style):
    background_color = "#ffffff"
    default_style = ""

    styles = {
        Comment:                   "italic #808080",  # class: 'c'
        Keyword:                   "#a626a4",		 # class: 'k'

        Name:                      "#000000",        # class: 'n'
        Name.Decorator:            "#4078f2",	     # class: 'nd'

        Number:                    "#986801",        # class: 'm'
        Number.Float:              "#986801",        # class: 'mf'
        Number.Integer:            "#986801",        # class: 'mi'
        Number.Integer.Long:       "#986801",        # class: 'il'

        Literal:                   "#986801",        # class: 'l'
        Literal.Date:              "#986801",        # class: 'ld'

        Punctuation:               "#000000",		 # class: 'p'

        String:                    "#50a14f",        # class: 's'
    }


class LSFLexer(RegexLexer):
    """
    For `LS Fusion <http://lsfusion.ru/>`_ files.
    .. versionadded:: 1.0
    """
    name = 'LSF'
    aliases = ['lsf']
    filenames = ['*.lsf']
    mimetypes = ['text/lsf']

    tokens = {
        'root': [
            (r"//.*$", Comment.Single),                 # comments
            (r"\'(?:\\'|\\\\|[^\n\r'])*\'", String),    # string literal
            (r"#{2,3}", Name.Decorator),                # lexems concatenate
            (r"@[a-zA-Z]\w*\b", Name.Decorator),        # metacode usage
            (r"\b\d{4}_\d\d_\d\d(?:_\d\d:\d\d)?\b", Number.Integer),  # DATE, DATETIME
            (r"\b\d\d:\d\d\b", Number.Integer),         # TIME
            (r"\b\d+\.\d*(?:D|d)?\b", Number.Float),    # NUMERIC, DOUBLE
            (r"\b\d+(?:l|L)?\b", Number.Integer),       # INTEGER, LONG
            (r"#[0-9A-Fa-f]{6}", Number.Integer),       # COLOR
            (words(('INTEGER', 'DOUBLE', 'LONG', 'BOOLEAN', 'DATE', 'DATETIME', 'TEXT', 'STRING', 'ISTRING',
                    'VARISTRING', 'VARSTRING', 'TIME', 'RICHTEXT',
                    'ABSTRACT', 'ACTION', 'ACTIVE', 'ACTIVATE', 'NEW', 'AFTER', 'AGGR', 'ALL', 'AND', 'APPEND', 'APPLY',
                    'AS', 'ASON', 'ASYNCUPDATE', 'ATTACH', 'ATTR', 'AUTO', 'AUTOREFRESH', 'AUTOSET', 'BACKGROUND',
                    'BCC', 'BEFORE', 'BODY', 'BOTTOM', 'BREAK', 'BY', 'CANCEL', 'CANONICALNAME', 'CASE', 'CC', 'CENTER',
                    'CHANGE', 'CHANGECLASS', 'CHANGEABLE', 'CHANGED', 'CHANGEKEY', 'CHANGEWYS', 'CHARSET', 'CHECK',
                    'CHECKED', 'CLASS', 'CLIENT', 'CLOSE', 'COLOR', 'COLUMNS', 'COMPLEX', 'CONCAT', 'CONFIRM',
                    'CONNECTION', 'CONSTRAINT', 'CONTAINERH', 'CONTAINERV', 'CONTEXTMENU', 'CSV', 'CSVFILE', 'CSVLINK',
                    'CUSTOM', 'CYCLES', 'DATA', 'DBF', 'DEFAULT', 'DEFAULTCOMPARE', 'DELAY', 'DELETE', 'DESC', 'DESIGN',
                    'DIALOG', 'DO', 'DOC', 'DOCKED', 'DOCX', 'DRAWROOT', 'DROP', 'DROPCHANGED', 'ECHO', 'EDIT', 'ELSE',
                    'EMAIL', 'END', 'ESCAPE', 'EQUAL', 'EVAL', 'EVENTID', 'EVENTS', 'EXCELFILE', 'EXCELLINK',
                    'EXCEPTLAST', 'EXCLUSIVE', 'EXEC', 'EXPORT', 'EXTEND', 'EXTERNAL', 'FALSE', 'FIELDS', 'FILE',
                    'FILTER', 'FILTERGROUP', 'FILTERS', 'FINALLY', 'FIRST', 'FIXED', 'FOLDER', 'FOOTER', 'FOR', 'FORCE',
                    'FOREGROUND', 'FORM', 'FORMEXTID', 'FORMS', 'FORMULA', 'FROM', 'FULL', 'GET', 'GOAFTER', 'GRID', 'GROUP',
                    'GROUPCHANGE', 'HALIGN', 'HEADER', 'HEADERS', 'HEADERSTO', 'HIDE', 'HIDESCROLLBARS', 'HIDETITLE', 'HINTNOUPDATE',
                    'HINTTABLE', 'HORIZONTAL', 'HTML', 'HTMLFILE', 'HTMLLINK', 'HTTP', 'IF', 'IMAGE', 'IMAGEFILE',
                    'IMAGELINK', 'IMPORT', 'IMPOSSIBLE', 'IN', 'INDEX', 'INDEXED', 'INIT', 'INITFILTER', 'INLINE',
                    'INTERNAL', 'INPUT', 'IS', 'JAVA', 'JOIN', 'JSON', 'JSONFILE', 'JSONLINK', 'KEYPRESS', 'LAST',
                    'LEFT', 'LIKE', 'LINK', 'LIMIT', 'LIST', 'LOCAL', 'LSF', 'LOGGABLE', 'MANAGESESSION', 'MAX', 'MEMO',
                    'MESSAGE', 'META', 'MIN', 'MODULE', 'MOVE', 'MS', 'MULTI', 'NAGGR', 'NAME', 'NAMESPACE',
                    'NAVIGATOR', 'NESTED', 'NEW', 'NEWEXECUTOR', 'NEWSESSION', 'NEWSQL', 'NEWTHREAD', 'NO', 'NOCANCEL',
                    'NOESCAPE', 'NOHEADER', 'NOHINT', 'NONULL', 'NODEFAULT', 'NOT', 'NOWAIT', 'NULL', 'NUMERIC',
                    'OBJECT', 'OBJECTS', 'OK', 'ON', 'OPTIMISTICASYNC', 'OR', 'ORDER', 'OVERRIDE', 'PAGESIZE', 'PANEL',
                    'PARENT', 'PARTITION', 'PASSWORD', 'PDF', 'PDFFILE', 'POST', 'RAWFILE', 'PDFLINK', 'RAWLINK',
                    'PERIOD', 'MATERIALIZED', 'PG', 'POSITION', 'PREV', 'PRINT', 'PRIORITY', 'PROPERTIES', 'PROPERTY',
                    'PROPORTION', 'PUT', 'QUERYOK', 'QUERYCLOSE', 'QUICKFILTER', 'READ', 'READONLY', 'READONLYIF',
                    'RECURSION', 'REFLECTION', 'REGEXP', 'REMOVE', 'REPORT', 'REPORTFILES', 'REQUEST', 'REQUIRE',
                    'RESOLVE', 'RETURN', 'RGB', 'RIGHT', 'ROOT', 'ROUND', 'RTF', 'SCHEDULE', 'SCROLL', 'SEEK',
                    'SELECTOR', 'SESSION', 'SET', 'SETCHANGED', 'SETDROPPED', 'SHOW', 'SHOWIF', 'SINGLE', 'SHEET',
                    'SPLITH', 'SPLITV', 'SQL', 'STEP', 'STRETCH', 'STRICT', 'STRUCT', 'SUBJECT', 'SUM', 'TAB', 'TABBED',
                    'TABLE', 'TABLEFILE', 'TABLELINK', 'TAG', 'TEXTHALIGN', 'TEXTVALIGN', 'THEN', 'THREADS', 'THROW',
                    'TIME', 'TO', 'DRAW', 'TOOLBAR', 'TOP', 'TRAILING', 'TREE', 'TRUE', 'TRY', 'UNGROUP', 'VALIGN',
                    'VALUE', 'VERTICAL', 'VIEW', 'WHEN', 'WHERE', 'WHILE', 'WINDOW', 'WORDFILE', 'WORDLINK', 'WRITE',
                    'XLS', 'XLSX', 'XML', 'XMLFILE', 'XMLLINK', 'XOR', 'YES'), prefix=r'\b', suffix=r'\b'),
             Keyword),
            (r".", Text),
        ]
    }


special_comment_prefix = '//#'
default_id = 'default'


def start_fragment_comment(name):
    return special_comment_prefix + name


def end_fragment_comment(name):
    return special_comment_prefix + name + ' end'


def filter_lines(lines):
    return [line for line in lines if not line.startswith(special_comment_prefix)]


def join_lines(lines):
    return '\n'.join(lines)


def filtered_code(lines):
    return join_lines(filter_lines(lines))


def get_code_fragment(lines, block_id):
    filtered_lines = 0
    line_index = 0
    start_line = None
    result_start_line = 0

    for line in lines:
        if line.startswith(special_comment_prefix):
            filtered_lines += 1
            if line.strip() == end_fragment_comment(block_id):
                return filtered_code(lines[start_line:line_index]), result_start_line
            elif line.strip() == start_fragment_comment(block_id) and start_line is None:
                start_line = line_index + 1
                result_start_line = start_line - filtered_lines + 1
        line_index += 1

    if start_line is not None:
        return filtered_code(lines[start_line:]), result_start_line
    else:
        return None, None


# tries to get the fragment, if fails then returns entire filtered code
def extract_code_fragment(code, block_id=default_id):
    lines = code.splitlines()
    result_code, start_line = get_code_fragment(lines, block_id)
    if result_code is None:
        return filtered_code(lines), 1
    else:
        return result_code, start_line


app = Flask(__name__)


@app.route("/samphighl", methods=['GET', 'POST'])
def index():
    files_path = argv[1]
    rel_path = argv[2]
    def_project_name = argv[3]
    file_location = request.args.get('file', 'Test') + '.lsf'
    blockid = request.args.get('block', 'default')
    original_lines = request.args.get('original')

    file_elements = file_location.split("/")
    if len(file_elements) > 1:
        project_name = file_elements[0]
        file_name = file_elements[1]
    else:
        project_name = def_project_name
        file_name = file_location

    with open(path.join(files_path, project_name, rel_path, file_name)) as file:
        code = file.read()

    fragment, start_line = extract_code_fragment(code, blockid)

    if original_lines is None:
        start_line = 1

    formatter = HtmlFormatter(style=LSFStyle, linenos='table', noclasses=True, linenostart=start_line)
    html = highlight(fragment, LSFLexer(), formatter)
    return make_response(html)


# Based on http://pygments.org/docs/formatterdevelopment/
class OldHtmlFormatter(Formatter):

    def __init__(self, **options):
        Formatter.__init__(self, **options)

        # create a dict of (start, end) tuples that wrap the
        # value of a token so that we can use it in the format
        # method later
        self.styles = {}

        # we iterate over the `_styles` attribute of a style item
        # that contains the parsed style values.
        for token, style in self.style:
            start = end = ''
            # a style item is a tuple in the following form:
            # colors are readily specified in hex: 'RRGGBB'
            if style['color']:
                start += '<font color="#%s">' % style['color']
                end = '</font>' + end
            if style['bold']:
                start += '<b>'
                end = '</b>' + end
            if style['italic']:
                start += '<i>'
                end = '</i>' + end
            if style['underline']:
                start += '<u>'
                end = '</u>' + end
            self.styles[token] = (start, end)

    def format(self, tokensource, outfile):
        # lastval is a string we use for caching
        # because it's possible that an lexer yields a number
        # of consecutive tokens with the same token type.
        # to minimize the size of the generated html markup we
        # try to join the values of same-type tokens here
        lastval = ''
        lasttype = None

        for ttype, value in tokensource:
            # if the token type doesn't exist in the stylemap
            # we try it with the parent of the token type
            # eg: parent of Token.Literal.String.Double is
            # Token.Literal.String
            while ttype not in self.styles:
                ttype = ttype.parent
            if ttype == lasttype:
                # the current token type is the same of the last
                # iteration. cache it
                lastval += value
            else:
                # not the same token as last iteration, but we
                # have some data in the buffer. wrap it with the
                # defined style and write it to the output file
                if lastval:
                    stylebegin, styleend = self.styles[lasttype]
                    outfile.write(stylebegin + lastval + styleend)
                # set lastval/lasttype to current values
                lastval = value
                lasttype = ttype

        # if something is left in the buffer, write it to the
        # output file, then close the opened <pre> tag
        if lastval:
            stylebegin, styleend = self.styles[lasttype]
            outfile.write(stylebegin + lastval + styleend)


def add_nbsp(text):
    result = ""
    inside_tag = False
    for c in text:
        if not inside_tag and c == ' ':
            result += '&nbsp'
        else:
            result += c
            if c == '>':
                inside_tag = False
            elif c == '<':
                inside_tag = True
    return result


@app.route("/habr", methods=['GET', 'POST'])
def generate_habr_code():
    code = request.data
    code = code.replace('<', '&lt').replace('>', '&gt')

    prefix = "<table><tr><td>"
    suffix = "</td></tr></table>"

    formatter = OldHtmlFormatter(style=HabrLSFStyle)
    html = highlight(code, LSFLexer(), formatter)
    html = prefix + add_nbsp(html) + suffix
    return make_response(html)


if __name__ == "__main__":
    app.run(host='localhost')
