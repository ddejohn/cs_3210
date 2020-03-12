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
# program
P -> int main ( ) { D S }

# type
T -> int
T -> bool
T -> float
T -> char

# declaration
D -> T D^
D -> T D^ D
D^ -> id D*
D^ -> id [ L ] D*
D* -> , D^
D* -> ;

# statement
S -> S^
S -> S^ S
S^ -> A
S^ -> I
S^ -> W
S^ -> { S }

# assignment
A -> id = X ;
A -> id [ X ] = X ;

# if
I -> if ( X ) S
I -> if ( X ) S [ else S ]

# while
W -> while ( X ) S

# expression
X -> C
X -> C || X

# compound
C -> Q
C -> Q && C

# equality
Q -> R
Q -> R Q* R

Q* -> ==
Q* -> !=

# relation
R -> P
R -> P R* P
R* -> <
R* -> <=
R* -> >
R* -> >=

# plus (addition)
P -> M
P -> M P* P
P* -> +
P* -> -

# term
M -> F
M -> F M* M
M* -> *
M* -> /

# factor
F -> id
F -> id [ X ]
F -> L
F -> ( X )

# literal
L -> z
L -> b
L -> f
L -> c
```
