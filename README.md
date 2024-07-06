# YTD 12-bit Computer
*Kyler Olsen*

**NOTICE: This project is still a *work in progress*.**

It is a custom computer and instruction set architecture. It also has its own
assembly language with assembler written in Python. Custom high level language
currently in development.

The purpose of this project is for me to practice creating an ISA and a compiler and assembler tool chain for the platform. I also plan to possibly build a redstone computer in Minecraft that implements this ISA.

## ISA

*See file `docs/12-bit ISA.html`*

## Assembly Language

### Registers

- `ZR`: Zero Register
- `PC`: Program Counter
- `SP`: Stack Pointer
- `MP`: Memory Pointer
- `D0`: Data 0
- `D1`: Data 1
- `D2`: Data 2
- `D3`: Data 3

### Zero Operand Instructions

- `NOP`
- `HLT`
- `BNZ`
- `BNA`
- `BNP`
- `BNN`

### One Operand Instructions

- `GLA` *`Destination Register`*
- `GET` *`Destination Register`*
- `LOD` *`Destination Register`*
- `STR` *`Source Register`*
- `POP` *`Destination Register`*
- `PSH` *`Source Register`*
- `LIU` *`Immediate Value (Integer)`*
- `LDI` *`Immediate Value (Integer)`*
- `LDI` :*`Label`*
- `LIL` *`Immediate Value (Integer)`*

### Two Operand Instructions

- `LSH` *`Destination Register`* *`Source Register`*
- `RSH` *`Destination Register`* *`Source Register`*
- `INC` *`Destination Register`* *`Source Register`*
- `DEC` *`Destination Register`* *`Source Register`*

### Three Operand Instructions

- `AND` *`Destination Register`* *`Source Register A`* *`Source Register B`*
- `OR` *`Destination Register`* *`Source Register A`* *`Source Register B`*
- `SUB` *`Destination Register`* *`Source Register A`* *`Source Register B`*
- `XOR` *`Destination Register`* *`Source Register A`* *`Source Register B`*
- `NOR` *`Destination Register`* *`Source Register A`* *`Source Register B`*
- `NAD` *`Destination Register`* *`Source Register A`* *`Source Register B`*
- `ADD` *`Destination Register`* *`Source Register A`* *`Source Register B`*

### Labels

*`Label`*:

### Memory Location

.*`Integer`*

### Example

```
; Yeahbut - Feb 2024
; Fibonacci

.0x0
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
```

## High Level Language
*WIP*

About
- Paradigm: Multi-Paradigm: Procedural (Imperative), Structured
- Designer: Kyler Olsen
- Created: Mar 2024
- Typing Discipline: Static, Weak, Manifest
- Platform: ytd 12-bit computer,
ytd 12-bit emulator (from *pytd12dk*, multi-platform)
- License: MIT
- Filename extension: `.ytd12c`
- Compiler Implementations: `pytd12dk` (Python),
`ytd12nc` (*native compiler*)

**Note:** The following sections define the language and may not be as well
suited for learning the language.

### Lexical

#### Directives

Directives start with `#` and end at the end of a line.
They are used to give additional instructions to the compiler.

#### Comments

Comments can either be single-line comments or multi-line comments.

Single-line comments start with `//` and end at the end of a line.

Multi-line comments start with `/*` and end with `*/`.

**pytd12dk implementation detail**: Comments and their content are ignored by
the lexer after they are tokenized. There are no comments in the output of
the lexer.

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
for         break       continue    let
unsigned    int         fixed       float
True        False       None
```

#### Literals

Number Literals

```
number ::=  decinteger | bininteger | octinteger | hexinteger | pointfloat | exponentfloat
decinteger ::=  nonzerodigit (["_"] digit)* | "0"+ (["_"] "0")*
bininteger ::=  "0" ("b" | "B") (["_"] bindigit)+
octinteger ::=  "0" ("o" | "O") (["_"] octdigit)+
hexinteger ::=  "0" ("x" | "X") (["_"] hexdigit)+
nonzerodigit ::=  "1"..."9"
digit ::=  "0"..."9"
bindigit ::=  "0" | "1"
octdigit ::=  "0"..."7"
hexdigit ::=  digit | "a"..."f" | "A"..."F"
pointfloat    ::=  ([digitpart] fraction) | (digitpart ".")
exponentfloat ::=  (digitpart | pointfloat) exponent
digitpart     ::=  digit (["_"] digit)*
fraction      ::=  "." digitpart
exponent      ::=  ("e" | "E") ["+" | "-"] digitpart
```

Character Literals

Character Literals must be on one line and begin and end with `'`. They can only
have one printable ascii character or escape code.

String Literals

String Literals must be on one line and begin and end with `"`. They can have a
unspecified number of printable ascii characters and escape codes.

Escape Codes

| Code | Meaning |
| -- | -- |
| `\0` | Null Character |
| `\a` | Alert (Beep, Bell) |
| `\b` | Backspace |
| `\e` | Escape Character |
| `\f` | Formfeed Page Break* |
| `\n` | Line Feed |
| `\r` | Return Carriage |
| `\t` | Horizontal Tab |
| `\v` | Vertical Tab* |
| `\\` | Backslash |
| `\'` | Single Quotation Mark (In char literals) |
| `\"` | Double Quotation Mark (In str literals) |

#### Punctuation

```
++      --      @       $       +       -
*       /       %       ~       &       |
^       <<      >>      =       +=      -=
*=      /=      %=      &=      |=      ^=
<<=     >>=     !       &&      ||      ^^
==      !=      <       <=      >       >=
{       }       [       ]       (       )
?       .       ->      ,       ;       :
```

### Syntax

The syntactical structure starts with a `File` at the root.

#### File

A `File` can contain any number of the following elements:
- `directive`
- `struct`
- `enum`
- `function`

#### Directive

Just a `directive`.

**pytd12dk implementation detail**: Their content is stored here for later when
directive compilation occurs.

#### struct

A `struct` begins with the `struct` keyword. It then has its `identifier`
followed by a comma (`,`) separated list enclosed in curly braces (`{` and `}`)
of *structure members*.

##### Structure Member

A *structure member* begins with its `identifier`, which may optionally be
preceded with the `static` keyword. After a colon (`:`) is its `data type`. It
may then optionally be followed by an equal sign (`=`) and a `literal`.

#### enum

A `enum` begins with the `enum` keyword. It then has its `identifier` followed
by a comma (`,`) separated list enclosed in curly braces (`{` and `}`) of
*enum members*.

##### Enum Member

An *enum member* begins with its `identifier`. It can then optionally be
followed by an equal sign (`=`) and a `number literal`.

#### Function

A `function` begins with the `fn` keyword. It then has its `identifier` followed
by a comma (`,`) separated list enclosed in parentheses (`(` and `)`) of
*function parameters*. After that is an arrow (`->`) followed by a `data type`
denoting the function's return type. After that is a list enclosed in curly
braces (`{` and `}`) of `statements`.

##### Function Parameter

A *function parameter* begins with its `identifier`, followed by a colon (`:`)
and its `data type`. It may then optionally be followed by an equal sign (`=`)
and a `literal`.

#### If Statement

An `if statement` begins with the `if` keyword, followed by its condition, an
`expression` enclosed in parentheses (`(` and `)`), then a single `statement`
or a list enclosed in curly braces (`{` and `}`) of `statements`. It may then
optionally be followed by an `else block`.

#### Do Loop

A `do loop` begins with the `do` keyword, followed by a single `statement` or a
list enclosed in curly braces (`{` and `}`) of `statements`. It is then followed
with the `while` keyword, then by its condition, an `expression` enclosed in
parentheses (`(` and `)`). It is then followed by a single `statement` or
another list enclosed in curly braces (`{` and `}`) of `statements`. Finally
the `do loop` may optionally be followed by an `else block`.

#### While Loop

A `while loop` begins with the `while` keyword, followed by its condition, an
`expression` enclosed in parentheses (`(` and `)`), then a single `statement`
or a list enclosed in curly braces (`{` and `}`) of `statements`. It may then
optionally be followed by an `else block`.

#### For Loop

A `for loop` begins with the `for` keyword, followed by three expressions
enclosed in parentheses (`(` and `)`), separated by semicolons (`;`). The
first expression is a *pre-loop expression*, the second is its condition which
is a normal `expression`, and the last is its post-loop expression which is
another normal `expression`. It is ended with a single `statement` or a list
enclosed in curly braces (`{` and `}`) of `statements`. It may then optionally
be followed by an `else block`.

##### Pre-Loop Expression

A *pre-loop expression* can be a normal `expression` or a special variable
definition. It starts its identifier, then a colon (`:`) is its `data type`,
then an equal sign (`=`) followed by an `expression`.

#### Else Block

An `else block` begins with the `else` keyword, followed by a single
`statement` or a list enclosed in curly braces (`{` and `}`) of `statements`.

#### Let Statement

A `let statement` begins with the `let` keyword, which may optionally be
preceded with the `static` keyword. It then has  its `identifier`, followed by
a colon (`:`) and its `data type`. It may then optionally be followed by an
equal sign (`=`) and an `expression`. It must then be finished with a semicolon
(`;`).

#### Expressions



##### Unary Expression

A `unary expression` is made up of one `expression` and one `unary operator`.
The operator may come before or after the expression.

##### Binary Expression

A `binary expression` is made up of one `expression`, then one
`binary operator`, then another `expression`.

##### Ternary Expression

A `ternary expression` is made up of one `expression` which is the condition,
then a question mark (`?`) followed by two `expression`s separated by a colon
(`:`).

##### Function Call

A `function call` starts with an `identifier` followed by a comma (`,`)
separated list enclosed in parentheses (`(` and `)`) of *function arguments*.

###### Function Argument

A *function argument* is an `expression` that may optionally be preceded by an
`identifier` which is immediately followed by an equal sign (`=`).

##### Enclosed Expression

An `enclosed expression` is simply an `expression` enclosed in parentheses
(`(` and `)`).

##### Operator

Here are all operators and their types and names in order of operator precedence.

| Operator | Type | Name |
| -- | -- | -- |
| `@` | Unary (Prefix) | Address of *Operator* |
| `$` | Unary (Prefix) | Dereference *Operator* |
| `~` | Unary (Prefix) | Bitwise NOT *Operator* |
| `--` | Unary (Postfix) | Postfix Decrement *Operator* |
| `++` | Unary (Postfix) | Postfix Increment *Operator* |
| `--` | Unary (Prefix) | Prefix Decrement *Operator* |
| `++` | Unary (Prefix) | Prefix Increment *Operator* |
| `-` | Unary (Prefix) | Negate *Operator* |
| `!` | Unary (Prefix) | Boolean NOT *Operator* |
| `.` | Binary | Member of *Operator* |
| `>>` | Binary | Right Shift *Operator* |
| `<<` | Binary | Left Shift *Operator* |
| `^` | Binary | Bitwise XOR *Operator* |
| `\|` | Binary | Bitwise OR *Operator* |
| `&` | Binary | Bitwise AND *Operator* |
| `%` | Binary | Modulus *Operator* |
| `/` | Binary | Division *Operator* |
| `*` | Binary | Multiplication *Operator* |
| `-` | Binary | Subtraction *Operator* |
| `+` | Binary | Addition *Operator* |
| `>=` | Binary | Greater or Equal to Than *Operator* |
| `>` | Binary | Greater Than *Operator* |
| `<=` | Binary | Less or Equal to Than *Operator* |
| `<` | Binary | Less Than *Operator* |
| `!=` | Binary | Inequality Comparison *Operator* |
| `==` | Binary | Equality Comparison *Operator* |
| `^^` | Binary | Boolean XOR *Operator* |
| `\|\|` | Binary | Boolean OR *Operator* |
| `&&` | Binary | Boolean AND *Operator* |
| `?` `:` | Ternary | Ternary Conditional *Operator* |
| `>>=` | Binary | Right Shift Assignment *Operator* |
| `<<=` | Binary | Left Shift Assignment *Operator* |
| `^=` | Binary | Bitwise XOR Assignment *Operator* |
| `\|=` | Binary | Bitwise OR Assignment *Operator* |
| `&=` | Binary | Bitwise AND Assignment *Operator* |
| `%=` | Binary | Modulus Assignment *Operator* |
| `/=` | Binary | Division Assignment *Operator* |
| `*=` | Binary | Multiplication Assignment *Operator* |
| `-=` | Binary | Subtraction Assignment *Operator* |
| `+=` | Binary | Addition Assignment *Operator* |
| `=` | Binary | Assignment *Operator* |

#### Literal

A `literal` is just simply the content of the literal. There are three types of
literals:

- Number Literal
- Character Literal
- String Literal

#### Identifier

A `identifier` is just simply the name of the identifier.

#### Data Type

A `data type` is made up of an `identifier` or `default data type`, and may
optionally be preceded by an at symbol (`@`).

##### Default Data Types

There are four default data types represented by the following keywords:

- `unsigned`
- `int`
- `fixed`
- `float`

#### Statement

A `statement` is made up of an `expression` followed by a semicolon (`;`), a
`let statement`, a `loop statement`, or a `nestable code block`.

##### Nestable Code Block

There are four `nestable code block`s:

- `if statement`
- `do loop`
- `while loop`
- `for loop`

##### Loop Statement

A `loop statement` are either the keyword `continue` or `break` followed by a
semicolon (`;`).

### Semantics

<!-- **NOTICE: This section describes the plan on how the semantical analyzer will be
implemented in the `pytd12dk` implementation.** -->

<!-- First the semantical analyzer converts the syntax tree into an instruction list. -->

### Directive Compilation

Currently directives are ignored by the compiler. In future versions of the
language, directives will be used.

## pytd12dk

`pytd12dk` (Python ytd 12-bit development kit) is a tool set written in Python
to assist in developing software for the ytd 12-bit computer. It includes a
compiler, assembler with linker, and emulator.

**NOTICE: `pytd12dk` requires Python version 3.12 (or higher).**

### Compiler

The first part of the tool kit is the compiler. It is currently unfinished and
can not yet produce an executable.

Running the following command we can get the arguments for the
compiler `python -m pytd12dk cm -h`:

```
usage: __main__.py cm [-h] [-t TOKEN_FILE] [-x SYNTAX_FILE] input_file

positional arguments:
  input_file

options:
  -h, --help            show this help message and exit
  -t TOKEN_FILE, --token_file TOKEN_FILE
  -x SYNTAX_FILE, --syntax_file SYNTAX_FILE
```

The only required positional argument is `input_file`. This is the source
code file to be compiled.

The optional argument `--token_file` is a text file output which contains debug
information from the output of the lexer. It is a list of the tokens parsed from
the source file and their lexical types.

The optional argument `--syntax_file` is a text file output which contains debug
information from the output of the syntactical analyzer. It is a text
representation of the syntax tree.

Additional optional arguments for semantical debug info, object file, and
executable file will be added.

### Assembler

The second part of the tool kit is the assembler. Included with the assembler is
a simple linker.

Running the following command we can get the arguments for the
compiler `python -m pytd12dk am -h`:

```
usage: __main__.py am [-h] [-o OUTPUT_FILE] [-l LABELS_FILE] [-x HEX_FILE] input_file

positional arguments:
  input_file

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
  -l LABELS_FILE, --labels_file LABELS_FILE
  -x HEX_FILE, --hex_file HEX_FILE
```

The only required positional argument is `input_file`. This is the assembly
code file to be assembled.

The optional argument `--labels_file` is a text file output which contains a
list of the labels found and their address locations in the executable.

The optional argument `--hex_file` is a text file output which contains the
generated machine code in hexadecimal representation.

The optional argument `--output_file` is a binary file output which contains the
generated machine code which can directly be executed by the emulator.

### Emulator

The second part of the tool kit is the assembler. Included with the assembler is
a simple linker.

Running the following command we can get the arguments for the
compiler `python -m pytd12dk em -h`:

```
usage: __main__.py em [-h] [-m {tty}] [-v] [-s] [-c CLOCK] rom_file

positional arguments:
  rom_file

options:
  -h, --help            show this help message and exit
  -m {tty}, --machine {tty}
  -v, --verbose
  -s, --step
  -c CLOCK, --clock CLOCK
```

The only required positional argument is `rom_file`. This is the executable
binary generated by the assembler or compiler.

The optional argument `--machine` allows for the selection of a pre-configured
virtual machine. Later in the section [Pre-configured VMs](#pre-configured-vms)
are a list of included machine(s). The default selection is `tty`.

The optional argument `--verbose` turns on printing the current program address,
the value at the address, the interpreted instruction, and each register and
their current values every clock cycle.

The optional argument `--step` turns on waiting for user input between each
clock cycle. This disables any set or default value of the option `--clock`,
making it essentially zero.

The optional argument `--clock` sets the time between each clock cycle in
thousandths of a second. The default value is `100` (one tenth of a second).

#### Pre-configured VMs.

Here are the pre-configured virtual machine(s) included with `pytd12dk`.

##### tty

The machine `tty` includes a tty IO device.

- Writing to address `0x7FD` outputs a signed integer.

- Writing to address `0x7FE` outputs an unsigned integer.

- Writing to address `0x7FF` outputs an ASCII/UTF-8 character.

<!-- - Reading from address `0x7FD` inputs a signed integer. -->

<!-- - Reading from address `0x7FE` inputs an unsigned integer. -->

- Reading from address `0x7FF` inputs an ASCII/UTF-8 character.

### Assembly Example

Included in the repo is an `examples` directory. Inside there is the
file `test1.s`. It contains a simple assembly program to calculate and output
the fibonacci sequence.

```
; Kyler Olsen - Feb 2024
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
```

We can assemble and link it using the following command. **Notice: Python 3.12
or higher is required for `pytd12dk`.**

```
python3 -m pytd12dk am examples/test1.s -o bin/a.out
```

We can then execute the binary using the included emulator. We should see the
fibonacci sequence printed to the console. We can use `ctrl` + `c` to exit the
emulator.

```
python3 -m pytd12dk em bin/a.out
```

Also inside the `examples` directory there is a Hello World program in the
file `test2.s`.

## ytd12nc

`ytd12nc` (ytd 12-bit native compiler) is a compiler and assembler with linker
written in the native high-level programming language and assembly language
to compile software for the ytd 12-bit computer natively.

Currently development of `ytd12nc` has not yet started.
