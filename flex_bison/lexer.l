%{
#include "parser.tab.h"
extern int yylval;
%}

%%

[ \t\n]+                   /* Ignore whitespace */
"print"                    { return PRINT; }
"output"                   { return OUTPUT; }
"play"                     { return PLAY; }
"while"                    { return WHILE; }
"if"                       { return IF; }
"else"                     { return ELSE; }
"=="                        { return EQ; }
">="                       { return GE; }
"<="                       { return LE; }
">"                        { return GT; }
"<"                        { return LT; }
"+"                        { return PLUS; }
"-"                        { return MINUS; }
"*"                        { return MUL; }
"/"                        { return DIV; }
"or"                       { return OR; }
"and"                      { return AND; }
"("                        { return LPAREN; }
")"                        { return RPAREN; }
"read"                     { return READ; }
"from"                     { return FROM; }
"to"                       { return TO; }
"rcut"                     { return RCUT; }
"lcut"                     { return LCUT; }
"insert"                   { return INSERT; }
"at"                       { return AT; }
[a-zA-Z_][a-zA-Z0-9_]*      { yylval.sval = strdup(yytext); return IDENTIFIER; }
[0-9]+                     { yylval.ival = atoi(yytext); return NUMBER; }
\"[^"]*\"                  { yylval.sval = strdup(yytext+1, yytext+strlen(yytext)-1); return STRING; }
[@#$%^&*()-=+[]{}|:,.<>?/~`] { return SPECIAL_CHAR; }

%%
