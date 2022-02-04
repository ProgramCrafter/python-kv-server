from parsers.nodes import SyntaxNodeSwitcher, SyntaxNode
from parsers.nodes import templates, consts

DOCUMENT = '''
<html%s>
<head><meta charset="utf-8"></head>
<body>%s</body>
</html>
'''.replace('\n', '')

ROCYONERY = '''
<div style="background-color:#fdd;width:100%;height:60px;line-height:60px;text-align:center;">
Создано с помощью дешаблонизатора от Rocyonery, Inc.
</div>
'''.replace('\n', '')

TITLE_STYLE = '''
width: 100%;
height: 60px;
line-height: 60px;
font-size: 20px;
text-align: center;
'''.replace('\n', '')

SUBTITLE_STYLE = '''
width: 100%;
font-size: 16px;
text-align: center;
'''.replace('\n', '')

class Document(SyntaxNode):
  def __str__(self):
    children_s = ''.join(str(c) for c in self.children)
    args_s = ''.join(' %s="%s"' % tuple(a) for a in self.kw.items())
    return DOCUMENT % (args_s, children_s)

class Rocyonery(SyntaxNode):
  def __str__(self):
    return ROCYONERY

class Fullwidth(SyntaxNode):
  def __init__(self, syntax_block, parent=None):
    SyntaxNode.__init__(self, syntax_block, parent)
    
    self.s = 'div'
    self.kw['style'] = self.kw.get('style', '') + 'width:100%;'

class Title(SyntaxNode):
  def __init__(self, syntax_block, parent=None):
    SyntaxNode.__init__(self, syntax_block, parent)
    
    self.s = 'div'
    self.kw['style'] = self.kw.get('style', '') + TITLE_STYLE

class Subtitle(SyntaxNode):
  def __init__(self, syntax_block, parent=None):
    SyntaxNode.__init__(self, syntax_block, parent)
    
    self.s = 'div'
    self.kw['style'] = self.kw.get('style', '') + SUBTITLE_STYLE

class SmartColumns(Fullwidth):
  def __init__(self, syntax_block, parent=None):
    self.cw = 'calc(100%% / %d - 6px)' % len(syntax_block.children)
    
    Fullwidth.__init__(self, syntax_block, parent)

class Column(SyntaxNode):
  def __init__(self, syntax_block, parent=None):
    SyntaxNode.__init__(self, syntax_block, parent)
    
    self.s = 'div'
    self.kw['style'] = self.kw.get('style', '') + 'width:%s;display:inline-block;vertical-align:top;margin:3px;' % parent.cw

def style_affector(key):
  def apply(node, r):
    node.kw['style'] = node.kw.get('style', '') + '%s:%s;' % (key, r)
  
  return apply

def style_static_affector( new_values):
  def apply(node, r):
    node.kw['style'] = node.kw.get('style', '') + new_values
  
  return apply

def gradient(node, r):
  style_affector('background')(node, 'linear-gradient(%s)' % r)

def single_line(node, r):
  h0 = node.kw['style'].find('height:')
  h1 = node.kw['style'].find(';', h0 + 1)
  
  node.kw['style'] = node.kw['style'] + 'line-' + node.kw['style'][h0:h1+1]

def set_template(node, r):
  l, r = r.split(' ', 1)
  consts[l] = r

def register():
  templates['!Document:'] = Document
  templates['!Fullwidth:'] = Fullwidth
  templates['!Rocyonery:'] = Rocyonery
  templates['!SmartColumns:'] = SmartColumns
  templates['!Column:'] = Column
  templates['!Title:'] = Title
  templates['!Subtitle:'] = Subtitle
  
  templates['@Back_fill'] = style_affector('background-color')
  templates['@Back_grad'] = gradient
  templates['@Height'] = style_affector('height')
  templates['@LHeight'] = style_affector('line-height')
  templates['@Width'] = style_affector('width')
  templates['@Text_size'] = style_affector('font-size')
  templates['@Text_type'] = style_affector('font-family')
  
  templates['@Centred'] = style_static_affector('text-align:center;')
  templates['@Single_line'] = single_line
  
  templates['@Set'] = set_template
