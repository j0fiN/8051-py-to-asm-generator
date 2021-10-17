# File to store register value
#
#

class Register:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.r0 = 0
        self.r1 = 0
        self.r2 = 0
        self.r3 = 0
        self.r4 = 0
        self.r5 = 0
        self.r6 = 0
        self.r7 = 0
    
    def move(self, register, val):
        if register not in self.__dict__.keys():
            raise Exception("Register not available")
        setattr(self, register, hex(val))

    def clear(self, register):
        if register not in self.__dict__.keys():
            raise Exception("Register not available")
        setattr(self, register, 0)


reg = Register()
reg.move("a", 255)
print(reg.a)   

