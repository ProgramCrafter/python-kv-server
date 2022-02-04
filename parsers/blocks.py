class SyntaxBlock:
  def __init__(self, s):
    s = s.rstrip()
    self.s = s.lstrip()
    self.padding = len(s) - len(self.s)
    self.children = []
    self.parent = None
  
  def set_parent(self, parent):
    if parent == None: return
    self.parent = parent
    parent.children.append(self)
  
  def __str__(self):
    return '%s(%d)' % (self.s, len(self.children))


class PyBlocksParser:
  def __init__(self):
    self.lines_stack = [SyntaxBlock('')]
  
  def add_line(self, line):
    line_block = SyntaxBlock(line)
    
    cur_pad = line_block.padding
    
    # print()
    # print('  Stack was [%s]' %  ', '.join(str(L) for L in self.lines_stack))
    
    while self.lines_stack[-1].padding > cur_pad:
      self.lines_stack.pop()
    
    if self.lines_stack[-1].padding == cur_pad:
      line_block.set_parent(self.lines_stack[-1].parent)
    else:
      line_block.set_parent(self.lines_stack[-1])
    
    self.lines_stack.append(line_block)
    
    # print('  Stack became [%s]' %  ', '.join(str(L) for L in self.lines_stack))
    # print('Line %s: padding %d, parent %s' % (line.strip(), cur_pad, line_block.parent))
  
  def parse(self, lines):
    for line in lines:
      if line == '[STOP]':
        print('Found line [STOP]')
        break
      
      if line.strip() and not line.startswith('#'):
        self.add_line(line)
