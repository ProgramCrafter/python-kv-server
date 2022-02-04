# from parsers.templates import templates, consts
templates = {}
consts = {}

class ISyntaxNode:
  def __init__(self, block): pass
  def __str__(self):         pass

class SyntaxTextNode(ISyntaxNode): # basically equivalent to str()
  def __init__(self, line):
    self.s = line
  
  def __str__(self):
    return self.s

class SyntaxNode(ISyntaxNode):
  def __init__(self, syntax_block, parent=None):
    self.children = []
    self.parent = parent
    self.kw = {}
    
    self.s = syntax_block.s[:-1]
    
    for child_block in syntax_block.children:
      child_s = child_block.s
      
      if not child_s:
        continue
      elif ':' not in child_s[:-1]:
        self.children.append(SyntaxNodeSwitcher(child_block, self))
      else:
        l, r = child_s.split(':', 1)
        
        r = r.strip()
        for c, v in consts.items():
          r = r.replace(c, v)
        
        if l in templates:
          templates[l](self, r)
        else:
          self.kw[l] = r
  
  def __str__(self):
    children_s = ''.join(str(c) for c in self.children)
    args_s = ''.join(' %s="%s"' % tuple(a) for a in self.kw.items())
    return '<%s%s>%s</%s>' % (self.s, args_s, children_s, self.s)
  
  def __repr__(self):
    return 'Node.%s%s%s' % (self.s, self.children, self.kw)

def SyntaxNodeSwitcher(syntax_block, parent=None):
  s = syntax_block.s
  
  if s in templates:
    return templates[s](syntax_block, parent)
  elif ':' not in s:
    return SyntaxTextNode(s)
  else:
    return SyntaxNode(syntax_block, parent)

class PySyntaxParser:
  def parse(self, blocks):
    import parsers.templates
    parsers.templates.register()
    
    return SyntaxNodeSwitcher(blocks.lines_stack[1])
