# YTD 12-bit Computer
*Yeahbut, aka Kyler Olsen*

It is a custom computer and instruction set architecture. It also has its own
assembly language with assembler written in Python. Custom high level language
coming soon!

## ISA
*WIP*

## Assembly Language
*WIP*

### Registers

- `ZR`
- `PC`
- `SP`
- `MP`
- `D0`
- `D1`
- `D2`
- `D3`

### Zero Operand Instructions

- `NOP`
- `HLT`
- `BNZ`
- `BNA`
- `BNP`
- `BNN`

### One Operand Instructions

- `GLA` `Destination Register`
- `GET` `Destination Register`
- `LOD` `Destination Register`
- `STR` `Source Register`
- `POP` `Destination Register`
- `PSH` `Source Register`
- `LIU` `Immediate Value`
- `LDI` `Immediate Value`
- `LDI` :`Label`
- `LIL` `Immediate Value`

### Two Operand Instructions

- `LSH` `Destination Register` `Source Register`
- `RSH` `Destination Register` `Source Register`
- `INC` `Destination Register` `Source Register`
- `DEC` `Destination Register` `Source Register`

### Three Operand Instructions

- `AND` `Destination Register` `Source Register A` `Source Register B`
- `OR` `Destination Register` `Source Register A` `Source Register B`
- `SUB` `Destination Register` `Source Register A` `Source Register B`
- `XOR` `Destination Register` `Source Register A` `Source Register B`
- `NOR` `Destination Register` `Source Register A` `Source Register B`
- `NAD` `Destination Register` `Source Register A` `Source Register B`
- `ADD` `Destination Register` `Source Register A` `Source Register B`

## High Level Language
*WIP*

About
- Paradigm: Multi-Paradigm: Procedural (Imperative), Structured
- Designer: Kyler Olsen
- Created: *Future*
- Typing Discipline: ~~Typeless~~ Static, Weak
- Platform: ytd 12-bit computer, ytd 12-bit emulator (multi-platform)
- License: *Tentatively MIT*
- Filename extension: `.ytd12c`

### Lexical

#### Directives

Directives start with `#` and end at the end of a line.
They are used to give additional instructions to the compiler.

#### Comments

Comments can either be single-line comments or multi-line comments.

Single-line comments start with `//` and end at the end of a line.

Multi-line comments start with `/*` and end with `*/`.


#### Identifiers

Can be up to 15 characters in length, and are case sensitive.
They cannot be a keyword.

```
Identifier ::= ID_Start ID_Continue*
ID_Start ::= <Any latin alphabet ligature or an underscore: "A"-"Z", "a"-"z", "_">
ID_Continue ::= ID_Start | <Any decimal ligature: "0"-"9">
```

#### Keywords

```
struct      fn          enum        static
if          else        do          while
for         pub         let         break
continue    True        False       None
unsigned    int         fixed       float
```

#### Literals

Number Literals

String Literals

#### Punctuation

```
++      --      @       $       +       -
*       /       %       ~       &       |
^       <<      >>      =       +=      -=
*=      /=      %=      &=      |=      ^=
<<=     >>=     !       &&      ||      ==
!=      <       <=      >       >=      ?
{       }       [       ]       (       )
.       ->      ,       ;       :
```

### Syntax

#### Operator Operand Counts

- Unitary: `++`, `--`, `@`, `$`
- Binary: `[ ]`, `+`, `-`, `*`, `/`, `%`, `~`, `&`, `|`, `^`, `<<`, `>>`, `=`,
`+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`, `!`, `&&`, `||`,
`==`, `!=`, `<`, `<=`, `>`, `>=`
- Ternary: `? :`

#### Operator Precedence

- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`
- Ternary Operator: `? :`
- Equality and order testing: `==`, `!=`, `<`, `<=`, `>`, `>=`
- Boolean logic: `!`, `&&`, `||`
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Bitwise: `~`, `&`, `|`, `^`, `<<`, `>>`
- Increment and decrement: `++`, `--`
- Reference and dereference: `@`, `$`, `[ ]`

### Semantics

### Scratch Area

#### Keywords

- Types: `unsigned`, `int`, `fixed`, `float`
- Structural: `if`, `else`, `do`, `while`, `for`, `break`, `continue`
- Constants: `True`, `False`, `None`
- Other: `struct`, `fn`, `enum`, `static`, `pub`, `let`

#### Delimiters

```
.       ->      ,       (       )
{       }       [       ]       ;
:
```
