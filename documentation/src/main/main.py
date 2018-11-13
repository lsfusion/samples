from flask import Flask, make_response, request
from os import path
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexer import RegexLexer, words
from pygments.style import Style
from pygments.token import *
from pygments.token import Keyword, Whitespace, Name, Comment, String, Number, Literal, Punctuation
from sys import argv


#inherited from TangoStyle (https://kite.com/docs/python/pygments.styles.tango.TangoStyle)
class LSFStyle(Style):
    background_color = "#ffffff"
    default_style = ""

    styles = {
        # No corresponding class for the following:
        #Text:                     "", # class:  ''
        Whitespace:                "underline #ffffff",      # class: 'w'
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
            (r"\b\d{4}_\d\d_\d\d(?:_\d\d:\d\d)?\b", Number.Integer), # DATE, DATETIME
            (r"\b\d\d:\d\d\b", Number.Integer),         # TIME
            (r"\b\d+\.\d*(?:D|d)?\b", Number.Float),    # NUMERIC, DOUBLE 
            (r"\b\d+(?:l|L)?\b", Number.Integer),       # INTEGER, LONG
            (r"#[0-9A-Fa-f]{6}", Number.Integer),       # COLOR        
            (words(('INTEGER', 'DOUBLE', 'LONG', 'BOOLEAN', 'DATE', 'DATETIME', 'TEXT', 'STRING', 'ISTRING', 'VARISTRING', 'VARSTRING', 'TIME', 'RICHTEXT',
                    'ABSTRACT', 'ACTION', 'ACTIVE', 'ACTIVATE', 'NEW', 'AFTER',
                    'AGGR', 'ALL', 'AND', 'APPEND', 'APPLY', 'AS', 'ASON', 'ASYNCUPDATE', 'ATTACH',
                    'ATTR', 'AUTO', 'AUTOREFRESH', 'AUTOSET', 'BACKGROUND', 'BCC', 'BEFORE', 'BODY', 'BOTTOM', 'BREAK', 'BY', 'CANCEL', 'CANONICALNAME',
                    'CASE', 'CC', 'CENTER', 'CHANGE', 'CHANGECLASS', 'CHANGEABLE', 'CHANGED', 'CHANGEKEY', 'CHANGEWYS', 'CHARSET', 'CHECK',
                    'CHECKED', 'CLASS', 'CLIENT', 'CLOSE', 'COLOR', 'COLUMNS', 'COMPLEX', 'CONCAT', 'CONFIRM', 'CONNECTION', 'CONSTRAINT',
                    'CONTAINERH', 'CONTAINERV', 'CONTEXTMENU', 'CSV', 'CSVFILE', 'CSVLINK', 'CUSTOM',
                    'CYCLES', 'DATA', 'DBF', 'DEFAULT', 'DEFAULTCOMPARE', 'DELAY', 'DELETE',
                    'DESC', 'DESIGN', 'DIALOG', 'DO', 'DOC', 'DOCKED', 'DOCX', 'DRAWROOT', 'DROP', 'DROPCHANGED', 'ECHO', 'EDIT',
                    'ELSE', 'EMAIL', 'END', 'EQUAL', 'EVAL', 'EVENTID', 'EVENTS', 'EXCELFILE', 'EXCELLINK',
                    'EXCEPTLAST', 'EXCLUSIVE', 'EXEC', 'EXPORT', 'EXTEND', 'EXTERNAL', 'FALSE', 'FIELDS', 'FILE', 'FILTER', 'FILTERGROUP',
                    'FILTERS', 'FINALLY', 'FIRST', 'FIXED', 'FOLDER', 'FOOTER', 'FOR', 'FORCE', 'FOREGROUND',
                    'FORM', 'FORMS', 'FORMULA', 'FROM', 'FULL', 'GET', 'GOAFTER', 'GRID', 'GROUP', 'GROUPCHANGE', 'HALIGN', 'HEADER',
                    'HIDE', 'HIDESCROLLBARS', 'HIDETITLE', 'HINTNOUPDATE', 'HINTTABLE', 'HORIZONTAL',
                    'HTML', 'HTMLFILE', 'HTMLLINK', 'HTTP', 'IF', 'IMAGE', 'IMAGEFILE', 'IMAGELINK', 'IMPORT', 'IMPOSSIBLE', 'IN', 'INDEX',
                    'INDEXED', 'INIT', 'INITFILTER', 'INLINE', 'INTERNAL', 'INPUT', 'IS', 'JAVA', 'JOIN',
                    'JSON', 'JSONFILE', 'JSONLINK', 'KEYPRESS', 'LAST', 'LEFT', 'LIKE', 'LINK', 'LIMIT',
                    'LIST', 'LOCAL', 'LSF', 'LOGGABLE', 'MANAGESESSION', 'MAX', 'MDB',
                    'MEMO', 'MESSAGE', 'META', 'MIN', 'MODULE', 'MOVE', 'MS', 'MULTI', 'NAGGR', 'NAME', 'NAMESPACE',
                    'NAVIGATOR', 'NESTED', 'NEW', 'NEWEXECUTOR', 'NEWSESSION', 'NEWSQL', 'NEWTHREAD', 'NO', 'NOCANCEL', 'NOESCAPE', 'NOHEADER', 'NOHINT', 'NONULL', 'NODEFAULT', 
                     'NOT', 'NOWAIT', 'NULL', 'NUMERIC', 'OBJECT',
                    'OBJECTS', 'OK', 'ON', 'OPTIMISTICASYNC', 'OR', 'ORDER', 'OVERRIDE', 'PAGESIZE',
                    'PANEL', 'PARENT', 'PARTITION', 'PASSWORD', 'PDF', 'PDFFILE', 'POST', 'RAWFILE', 'PDFLINK', 'RAWLINK', 'PERIOD', 'MATERIALIZED', 'PG', 'POSITION',
                    'PREV', 'PRINT', 'PRIORITY', 'PROPERTIES', 'PROPERTY',
                    'PROPORTION', 'PUT', 'QUERYOK', 'QUERYCLOSE', 'QUICKFILTER', 'READ', 'READONLY', 'READONLYIF', 'RECURSION', 'REFLECTION', 'REGEXP', 'REMOVE',
                    'REPORT', 'REPORTFILES', 'REQUEST', 'REQUIRE', 'RESOLVE', 'RETURN', 'RGB', 'RIGHT', 'ROOT',
                    'ROUND', 'RTF', 'SCHEDULE', 'SCROLL', 'SEEK', 'SELECTOR', 'SESSION', 'SET', 'SETCHANGED', 'SETDROPPED', 'SHOW',
                    'SHOWIF', 'SINGLE', 'SHEET', 'SPLITH', 'SPLITV', 'SQL', 'STEP', 'STRETCH', 'STRICT', 'STRUCT', 'SUBJECT',
                    'SUM', 'TAB', 'TABBED', 'TABLE', 'TAG', 'TEXTHALIGN', 'TEXTVALIGN', 'THEN', 'THREADS', 'THROW', 'TIME', 'TO', 'DRAW',
                    'TOOLBAR', 'TOP', 'TRAILING', 'TREE', 'TRUE', 'TRY', 'UNGROUP', 'VALIGN', 'VALUE',
                    'VERTICAL', 'VIEW', 'WHEN', 'WHERE', 'WHILE', 'WINDOW', 'WORDFILE', 'WORDLINK',
                    'WRITE', 'XLS', 'XLSX', 'XML', 'XMLFILE', 'XMLLINK', 'XOR', 'YES'), prefix=r'\b', suffix=r'\b'),
             Keyword),
            (r".", Text),
        ]
    }


specialCommentPrefix = '//#'
defaultId = 'default'

def startFragmentComment(id):
    return specialCommentPrefix + id

def endFragmentComment(id):
    return specialCommentPrefix + id + ' end'

def filterLines(lines):
    return [line for line in lines if not line.startswith(specialCommentPrefix)]

def joinLines(lines):
    return '\n'.join(lines)

def filteredCode(lines):
    return joinLines(filterLines(lines))

def getCodeFragment(lines, blockId):
    filteredLines = 0
    lineIndex = 0
    startLine = None
    resultStartLine = 0

    for line in lines:
        if line.startswith(specialCommentPrefix):
            filteredLines += 1
            if line.strip() == endFragmentComment(blockId):
                return filteredCode(lines[startLine:lineIndex]), resultStartLine
            elif line.strip() == startFragmentComment(blockId) and startLine is None:
                startLine = lineIndex + 1
                resultStartLine = startLine - filteredLines + 1
        lineIndex += 1

    if startLine is not None:
        return filteredCode(lines[startLine:]), resultStartLine
    else:
        return None, None


#tries to get the fragment, if fails then returns entire filtered code
def extractCodeFragment(code, blockId=defaultId):
    lines = code.splitlines()
    resultCode, startLine = getCodeFragment(lines, blockId)
    if resultCode is None:
        return filteredCode(lines), 1
    else:
        return resultCode, startLine



app = Flask(__name__)

@app.route("/samphighl", methods=['GET', 'POST'])
def index():
    filesPath = argv[1]
    relPath = argv[2]
    defProjectName = argv[3]
    fileLocation = request.args.get('file', 'Test') + '.lsf'
    blockId = request.args.get('block', 'default')
    originalLines = request.args.get('original')

    fileElements = fileLocation.split("/")
    if(len(fileElements) > 1):
        projectName = fileElements[0]
        fileName = fileElements[1]
    else:
        projectName = defProjectName
        fileName = fileLocation
        
    with open(path.join(filesPath,projectName,relPath,fileName)) as file:
        code = file.read()

    fragment, startLine = extractCodeFragment(code, blockId)

    if originalLines is None:
        startLine = 1
        
    formatter = HtmlFormatter(style=LSFStyle, linenos='table', noclasses=True, linenostart=startLine)
    html = highlight(fragment, LSFLexer(), formatter)
    return make_response(html)

if __name__ == "__main__":
    app.run(host='localhost')
