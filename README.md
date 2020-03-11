# CS 3210 Principles of Programming Languages
Devon DeJohn, Spring 2020

### Parser

A lexical analyzer and bottom-up parser for a 'C-lite' language.

The grammar in EBNF:

```
<program>           →   int main ( ) { <declaration>+ <statement>+ }
<declaration>       →   <type> <identifier> [ [ <int_literal> ] ] { , <identifier> [ [ <int_literal> ] ] } ;
<statement>         →   <assignment> | <if> | <while> | { <statement>+ }
<assignment>        →   <identifier> [ [ <expression> ] ] = <expression> ;
<if>                →   if ( <expression> ) <statement> [ else <statement> ]
<while>             →   while ( <expression> ) <statement> 
<expression>        →   <conjunction> { || <conjunction> } 
<conjunction>       →   <equality> { && <equality> }
<equality>          →   <relation> [ <eq_neq_op> <relation> ]
<eq_neq_op>         →   == | != 
<relation>          →   <addition> [ <rel_op> <addition> ]
<rel_op>            →   < | <= | > | >=
<addition>          →   <term> { <add_sub_op> <term> }
<add_sub_op>        →   + | -
<term>              →   <factor> { <mul_div_op> <factor> }
<mul_div_op>        →   * | / 
<factor>            →   <identifier> [ [ <expression> ] ] | <literal> | ( <expression> ) 
<type>              →   int | bool | float | char 
<identifier>        →   <letter> { <letter> | <digit> }
<letter>            →   a | b | … | z | A | B | … | Z 
<digit>             →   0 | 1 | … | 9
<literal>           →   <int_literal> | <bool_literal> | <float_literal> | <char_literal> 
<int_literal>       →   <digit> { <digit> } 
<bool_literal>      →   true | false 
<float_literal>     →   <int_literal> . <int_literal>
<char_literal>      →   ' <letter> '
```

Translated into SLR table-ready productions:

```
P -> int main ( ) { D S }

D -> T D'
D -> T D' D

D' -> id D*
D' -> id [ LIT ] D*

D* -> , D'
D* -> ;

S -> S'
S -> S' S

S' -> ASS
S' -> IF
S' -> WL
S' -> { S }

ASS -> id = EXP ;
ASS -> id [ EXP ] = EXP ;

IF -> if ( EXP ) S
IF -> if ( EXP ) S [ else S ]

WL -> while ( EXP ) S

EXP -> C
EXP -> C || EXP

C -> Q
C -> Q && C

Q -> R
Q -> R QOP R

QOP -> ==
QOP -> !=

R -> ADD
R -> ADD ROP ADD

ROP -> <
ROP -> <=
ROP -> >
ROP -> >=

ADD -> TERM
ADD -> TERM AOP ADD

AOP -> +
AOP -> -

TERM -> FAC
TERM -> FAC MOP TERM

MOP -> *
MOP -> /

FAC -> id
FAC -> id [ EXP ]
FAC -> LIT
FAC -> ( EXP )

T -> int
T -> bool
T -> float
T -> char

LIT -> z
LIT -> b
LIT -> f
LIT -> c
```
