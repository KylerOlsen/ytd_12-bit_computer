# YTD 12-bit Computer
*Yeahbut, aka Kyler Olsen*

**NOTICE: Most of this document is unfinished.**

It is a custom computer and instruction set architecture. It also has its own
assembly language with assembler written in Python. Custom high level language
coming soon!

## ISA

## Assembly Language

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
- Platform: ytd 12-bit computer,
ytd 12-bit emulator (from *pytd12dk*, multi-platform)
- License: *Tentatively MIT*
- Filename extension: `.ytd12c`
- Compiler Implementations: `pytd12dk` (Python),
`ytd12nc` (*bootstrapped compiler*)

### Lexical

#### Directives

Directives start with `#` and end at the end of a line.
They are used to give additional instructions to the compiler.

#### Comments

Comments can either be single-line comments or multi-line comments.

Single-line comments start with `//` and end at the end of a line.

Multi-line comments start with `/*` and end with `*/`.

**pytd12dk implementation detail**: Comments and their content are ultimately
ignored by the lexer after they are tokenized. There are no comments in the
output of the lexer.

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
`expression` enclosed in parentheses (`(` and `)`), then a list enclosed in
curly braces (`{` and `}`) of `statements`. It may then optionally be followed
by an `else block`.

#### Do Loop

A `do loop` begins with the `do` keyword, followed by a list enclosed in curly
braces (`{` and `}`) of `statements`. It is then finished
with the `while` keyword, followed by its condition, an `expression` enclosed
in parentheses (`(` and `)`). It may then optionally be followed by another list
enclosed in curly braces (`{` and `}`) of `statements` then
again optionally by an `else block`.

#### While Loop

A `while loop` begins with the `while` keyword, followed by its condition, an
`expression` enclosed in parentheses (`(` and `)`), then a list enclosed in
curly braces (`{` and `}`) of `statements`. It may then
optionally be followed by an `else block`.

#### For Loop

A `for loop` begins with the `for` keyword, followed by three expressions
enclosed in parentheses (`(` and `)`), separated by semicolons (`;`). The first
expression is a *pre-loop expression*, the second is its condition which is a
normal `expression`, and the last is its post-loop expression which is another
normal `expression`. It is ended with a list enclosed in curly braces
(`{` and `}`) of `statements`. It may then optionally be
followed by an `else block`.

##### Pre-Loop Expression

A *pre-loop expression* can be a normal `expression` or a special variable
definition. It starts its identifier, then a colon (`:`) is its `data type`,
then an equal sign (`=`) followed by an `expression`.

#### Else Block

An `else block` begins with the `else` keyword, followed by a list enclosed in
curly braces (`{` and `}`) of `statements`.

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

##### Array Subscription

An `array subscription` starts with an `identifier` followed by an `expression`
enclosed in square brackets (`[` and `]`).

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

## pytd12dk

`pytd12dk` (Python ytd 12-bit development kit) is a tool set written in Python
to assist in developing software for the ytd 12-bit computer. It includes a
compiler, assembler with linker, and emulator.

### Compiler

### Assembler

### Emulator

## ytd12nc

`ytd12nc` (ytd 12-bit native compiler) is a compiler and assembler with linker
set written in the native high-level programming language and assembly language
to compile software for the ytd 12-bit computer natively.

Currently development of `ytd12nc` has not yet started.

### Bootstrapping

In order to compile the the compiler, we need a compiler to compile it. This
process is called *bootstrapping* as it is like pulling ourselves up by our
bootstraps. This requires writing a compiler in assembly language or another
high-level programming language. In our case we are lucky to have the compiler
that is apart of `pytd12dk`.

| Compiler | *Compiler* Compiler | *Compiler Compiler* Compiler |
| --- | --- | --- |
| `pytd12dk` | `CPython` | `gcc`, `clang`, or other C compiler |
| `ytd12nc` (a) | `pytd12dk` | `CPython` |
| `ytd12nc` (b) | `ytd12nc` (a) | `pytd12dk` |
| `ytd12nc` (c) | `ytd12nc` (b) | `ytd12nc` (a) |
| `ytd12nc` (d) | `ytd12nc` (c) | `ytd12nc` (b) |
