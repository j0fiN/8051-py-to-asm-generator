# lexer for ASM script generater
#
# Jofin F Archbald
from statement import Statement
class ASM_8051:
    def __init__(self, script):
        self.source_code: str = ""
        self.script: str = script
        self.stack = []

    def clean_operands(self, a, b):
        a = a.strip()
        b = b.strip()
        return a, b
    


    def scan_statements(self, line):
        if '=' in line:
            try:
                a, b = line.split('=')
            except Exception:
                print('only one operator and two operands')
            
            a, b = self.clean_operands(a, b)

            if ':' in a:
                return self.colon_functions(a, b)

            if b == a:
                raise Exception("Cannot move values to the same register")
            if a[0] == 'r' and b[0] == 'r':
                raise Exception("Cannot move values from within Rn registers")

            if b == '0':
                return [Statement(inst = 'clr', operands=(a,))]

            if b[0].isdigit():
                return [Statement(inst = 'mov', operands=(a, '#'+b))]
            elif b[0] == '*':
                if b[1] == 'r':
                    if b[2] not in '01':
                        raise Exception("Only registers R0 and R1 are allowed")
                    else:
                        return [Statement(inst = 'mov', operands=(a, '@'+b[1:]))]
                else:
                    return [Statement(inst = 'mov', operands=(a, b[1:]))]
            return [Statement(inst = 'mov', operands=(a, b))]
            
        elif '+' in line:
            try:
                a, b = line.split('+')
            except Exception:
                print('only one operator and two operands')
            a, b = self.clean_operands(a, b)
            if a != 'a':
                raise Exception("ADD is only valid if result is stored in Acc")

            return [Statement(inst = 'add', operands=(a, b)),
                    Statement(inst = 'jnc', operands=('no_carry',)),
                    Statement(inst = 'inc', operands=('r7',)),
                    Statement(label="no_carry"),
                    ]
    
    def colon_functions(self, a, b):
        command, arguments = a.split(':')
        self.clean_operands(command, arguments)
        if command == 'delay':
            return self.delay_snippet(arguments, b)
        elif command == 'timer':
            return self.timer_snippet(arguments, b)
        



    def delay_snippet(self, init, register):
        # single loop DJNZ
        if  int(init) < 255:
            self.stack.append([Statement(label='delay', inst = 'mov', operands=(register, "#"+init.strip())),
                                Statement(label='loop', inst = 'djnz', operands=(register, 'loop')),
                                Statement(inst = 'ret')])
            return [
                Statement(inst='acall', operands=('delay',))
            ]
        elif int(init) > 255 and int(init) < 65025:
            init_2 = str(int(round(int(init) / 255)))

            register_2 = int(register[-1]) + 1
            if register_2 > 7:
                register_2 = 'r0'
            else:
                register_2 = 'r' + str(register_2)
            self.stack.append([
                Statement(label='delay', inst = 'mov', operands=(register, "#"+"255")),
                Statement(label='outer_loop', inst = 'mov', operands=(register_2, '#'+init_2)),
                Statement(label='inner_loop', inst = 'djnz', operands=(register_2, 'inner_loop')),
                Statement(inst = 'djnz', operands=(register, 'outer_loop')),
                Statement(inst = 'ret')
            ])
            return [
                Statement(inst='acall', operands=('delay',))
            ]
        else:
            raise Exception("init value larger than 65025 in delay cannot be processed.")

        


    def timer_snippet(self, a, b):...


    def generate(self, case='lower'):
        st = "org 0000h\n"
        self.script = self.script.strip()
        lines = self.script.split('\n')
        for line in lines:
            if line == "":
                st += '\n'
                continue
            for statements in self.scan_statements(line):
                st += str(statements) + '\n'
        while self.stack:
            statements = self.stack.pop()
            for statement in statements:
                st += str(statement) + '\n'
        st += 'END\n'
        if case == 'upper':
            st = st.upper()
        
        with open('file.ASM', 'w') as f:
            f.write(st)