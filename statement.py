from dataclasses import dataclass
from typing import Tuple
@dataclass
class Statement:
    label: str = ""
    inst: str = ""
    operands: Tuple[str] = ()

    def __repr__(self):
        if len(self.operands) == 2:
            if self.label != "":
                return f"{self.label}:{self.inst} {self.operands[0]}, {self.operands[1]}"
            else:
                return f"{self.inst} {self.operands[0]}, {self.operands[1]}"
        else:
            if self.label != "":
                return f"{self.label}:{self.inst} {self.operands[0]}"
            else:
                return f"{self.inst} {self.operands[0]}"