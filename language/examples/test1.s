; Yeahbut - Feb 2024
; Example 1 - ytd 12-bit Computer
; Fibonacci

; .0x5
main:
    ; Initialize Fibonacci values
    ldi 1
    or D0 MP ZR
    or D1 ZR ZR
    or D2 ZR ZR

loop:
    ; Output current value
    liu 0x1f
    lil 0x3D
    str D0

    ; Move values down
    or D2 D1 ZR
    or D1 D0 ZR

    ; Add last two values to get the next value
    add D0 D1 D2

    ldi :loop
    or PC MP ZR
