from parsers.blocks import PyBlocksParser
from parsers.nodes import PySyntaxParser

import tarfile
import gzip
import os

class PyBlocksSyntaxParser:
  def parse(self, lines):
    blocks = PyBlocksParser()
    blocks.parse(lines)
    blocks.add_line('')
    
    return PySyntaxParser().parse(blocks)

try:
  file_path = __file__.rstrip('.py')
  
  parser = PyBlocksSyntaxParser()
  with open(file_path + '.kv', encoding='utf-8') as f:
    result = parser.parse(f)
  
  print('If the result seems to be incorrect, make sure you use only tabs or only spaces.')
  
  # print(result)
  # print(repr(result))
  
  with open(file_path + '-gen.html', 'w', encoding='utf-8') as f:
    f.write(str(result))
  
  with tarfile.open(file_path + '-gen.tar.gz', 'w:gz', encoding='utf-8') as f:
    f.add(file_path + '-gen.html')
  
  # os.system('start "null" "%s"' % (file_path + '-gen.html'))
except:
  __import__('traceback').print_exc()
finally:
  pass
  # input('...')
