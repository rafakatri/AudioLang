%union {
    int ival;
    char *sval;
}

%{
#include <stdio.h>
#include <stdlib.h>
extern int yylex();
void yyerror(char *s);
extern char* yytext;
extern int yylineno;
%}

%token PRINT OUTPUT PLAY WHILE IF ELSE EQ GT LT PLUS MINUS MUL DIV OR AND LPAREN RPAREN READ FROM TO RCUT LCUT INSERT AT IDENTIFIER NUMBER STRING END WHITESPACE COMMA SOURCE INT ASSIGN


%%

program:
    block
    ;

block:
    /* Empty rule to allow for zero tests */
    |block statement
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
    SOURCE IDENTIFIER ASSIGN expression END
    | INT IDENTIFIER ASSIGN bool_exp END
    | SOURCE IDENTIFIER END
    | INT IDENTIFIER END
    ;

assignment:
    IDENTIFIER ASSIGN expression END
    ;

print:
    PRINT LPAREN expression RPAREN END
    ;

output:
    OUTPUT LPAREN IDENTIFIER COMMA STRING RPAREN END
    ;

play:
    PLAY expression END
    ;

while:
    WHILE LPAREN bool_exp RPAREN '{' block '}' END
    ;

if:
    IF LPAREN bool_exp RPAREN '{' block '}' ELSE '{' block '}' END
    | IF LPAREN bool_exp RPAREN '{' block '}' END
    ;

bool_exp:
    bool_term OR bool_term
    | bool_term
    ;

bool_term:
    rel_exp AND rel_exp
    | rel_exp
    ;

rel_exp:
    expression EQ expression
    | expression GT expression
    | expression LT expression
    ;

expression:
    term PLUS term
    | term MINUS term
    | term
    ;

term:
    factor MUL factor
    | factor DIV factor
    | factor
    ;

factor:
    NUMBER
    | STRING
    | IDENTIFIER
    | PLUS factor
    | MINUS factor
    | "not" factor
    | LPAREN expression RPAREN
    | READ LPAREN RPAREN
    | identifier_operations
    ;

identifier_operations:
    IDENTIFIER FROM expression TO expression
    | IDENTIFIER RCUT expression
    | IDENTIFIER LCUT expression
    | IDENTIFIER INSERT IDENTIFIER AT expression
    ;

%%

void yyerror(char *s) {
    fprintf(stderr, "Error: %s at line %d near '%s'\n", s, yylineno, yytext);
}

int main() {
    yyparse();
    return 0;
}
