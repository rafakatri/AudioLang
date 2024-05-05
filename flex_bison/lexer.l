%{
#include "parser.tab.h"
extern char* yytext;
extern int yylineno;
%}

%%

[ \t\n]+                   /* Ignore whitespace */
"="                        {return ASSIGN; }
"source"                   {return SOURCE; }
"int"                      {return INT; }
","                        {return COMMA; }
"print"                    { return PRINT; }
"output"                   { return OUTPUT; }
"play"                     { return PLAY; }
"while"                    { return WHILE; }
"if"                       { return IF; }
"else"                     { return ELSE; }
"=="                        { return EQ; }
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
";"                        { return END; }
[a-zA-Z_][a-zA-Z0-9_]*      { yylval.sval = strdup(yytext); return IDENTIFIER; }
[0-9]+                     { yylval.ival = atoi(yytext); return NUMBER; }
\"[^"]*\"                 { yylval.sval = strdup(yytext+1); yylval.sval[strlen(yylval.sval)-1] = '\0'; return STRING; }
%%
