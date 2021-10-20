# 8051-py-to-asm-generator
Assembly Language Generator for 8051 microcontroller


Work in progress :construction:


| **INSTRUCTION** | **IDENTIFIER** | **SYNTAX** | **SNIPPET** |
|------|------|------|------|
| MOV  |   =   |   reg=reg, reg=val (val != 0)   |   NO   |
|  ADD    |   +   |   a+reg, a+val   |   YES   |
|   DELAY   |   =   |   delay:'delay_1, rn, rn(optional)'   |   YES   |
|   ACALL   |   label()   |   delay_1(), timer_long()    |   NO   |

