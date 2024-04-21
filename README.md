# AudioLang

## Linguagem feita para a disciplina de Lógica da Computação

### Descrição

* Edite arquivos de áudio, como MP3 e WAV

* Faça cortes e misture áudios diferentes

### EBNF

```
block = {statement};

statement = ('\n'|assignment|print|while|if);

assignment = identifier, '=', expression, ';';

print = 'print', '(', expression, ')', ';';

output = 'output', '(', identifier, ',', string, ')',';';

while = 'while', '(', bool_exp, ')', '{', {statement}, '}', ';';

if = 'if', '(', bool_exp, ')', '{', {statement}, '}', (|'else', '{', {statement}, '}'), ';';

bool_exp = bool_term, { ( 'or' ) , bool_term };

bool_term = rel_exp, { ( 'and' ) , rel_exp };

rel_exp = expression, { ( '+' | '-' ) , expression };

expression = term, { ( '+' | '-' ) , term };

term = { factor, ( '*' | '/' ) }, factor;

factor = number | string | identifier | ('+'| '-'|'not'), factor | ('(', expression, ')')| ('read', '(', ')') | array_access ;

array_access = identifier, '[', expression, ']';

identifier = letter, {(letter | digit | '_')};

letter = 'a' | '...' | 'Z';

number = digit, { digit };

digit = '0' | '1' | '...' | '9';

string = '"', { character }, '"';

character = letter | digit | special_character;

special_character = '!' | '@' | '...';
```
