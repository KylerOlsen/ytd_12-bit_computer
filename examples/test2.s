; Kyler Olsen - Mar 2024
; Example 2 - ytd 12-bit Computer
; Hello World

ldi :main
or PC MP ZR

print:
    dec SP SP

    ; Output current value
    liu 0x1F
    lil 0x3F
    str D0

    ; Return
    inc SP SP
    pop MP
    inc PC MP

main:
    ; Initialize Stack Pointer
    liu 0x3F
    lil 0x3F
    or SP MP ZR

    ; 'H' (0x48)
    liu 0x1
    lil 0x08
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; 'e' (0x65)
    liu 0x1
    lil 0x25
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; 'l' (0x6c)
    liu 0x1
    lil 0x2c
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; 'l' (0x6c)
    liu 0x1
    lil 0x2c
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; 'o' (0x6f)
    liu 0x1
    lil 0x2f
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; ',' (0x2c)
    ldi 0x2c
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; ' ' (0x20)
    ldi 0x20
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; 'W' (0x57)
    liu 0x1
    lil 0x17
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; 'o' (0x6f)
    liu 0x1
    lil 0x2f
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; 'r' (0x72)
    liu 0x1
    lil 0x32
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; 'l' (0x6c)
    liu 0x1
    lil 0x2c
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; 'd' (0x64)
    liu 0x1
    lil 0x24
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; '!' (0x21)
    ldi 0x21
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    ; '\n' (0xa)
    ldi 0xa
    or D0 MP ZR
    ldi :print
    psh PC
    or PC MP ZR

    hlt
