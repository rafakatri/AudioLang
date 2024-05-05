%{
#include <stdio.h>
#include <stdlib.h>
extern int yylex();
void yyerror(char *s);
%}

%token PRINT OUTPUT PLAY WHILE IF ELSE EQ GE LE GT LT PLUS MINUS MUL DIV OR AND LPAREN RPAREN READ FROM TO RCUT LCUT INSERT AT IDENTIFIER NUMBER STRING SPECIAL_CHAR

%%

program:
    block
    ;

block:
    statement
    ;

statement:
    assignment
    | print
    | output
    | play
    | varDeclaration
    | while
    | if
    ;

varDeclaration:
    'source' IDENTIFIER ('=' expression)?
    | 'int' IDENTIFIER ('=' bool_exp)?
    ;

assignment:
    IDENTIFIER '=' (bool_exp | expression)
    ;

print:
    'print' '(' bool_exp ')' ';'
    ;

output:
    'output' '(' IDENTIFIER ',' STRING ')' ';'
    ;

play:
    'play' expression
    ;

while:
    'while' '(' bool_exp ')' '{' block '}' ';'
    ;

if:
    'if' '(' bool_exp ')' '{' block '}' ('else' '{' block '}')? ';'
    ;

bool_exp:
    bool_term ('or' bool_term)*
    ;

bool_term:
    rel_exp ('and' rel_exp)*
    ;

rel_exp:
    expression ('==' | '>' | '<') expression
    ;

expression:
    term ('+' | '-') term*
    ;

term:
    factor ('*' | '/') factor*
    ;

factor:
    number
    | string
    | IDENTIFIER
    | ('+' | '-' | 'not') factor
    | '(' expression ')'
    | READ '(' ')'
    | identifier_operations
    ;

identifier_operations:
    IDENTIFIER ('from' expression 'to' expression)?
    | IDENTIFIER ('rcut' expression)?
    | IDENTIFIER ('lcut' expression)?
    | IDENTIFIER ('insert' IDENTIFIER 'at' expression)?
    ;

%%

void yyerror(char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    yyparse();
    return 0;
}
