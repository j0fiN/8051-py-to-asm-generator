
from asm import ASM_8051


with open('test.py', 'r') as f:
    st = f.read()

script = ASM_8051(st)

script.generate(case='upper')