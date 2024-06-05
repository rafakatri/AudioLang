# AudioLang

## Linguagem feita para a disciplina de Lógica da Computação

### Descrição

* Edite arquivos de áudio MP3 

* Faça cortes e misture áudios diferentes

* Casos de uso: soundboard, cortes de áudio

## Guia de Instalação

* Dependências: ffmpeg e pydub

```
pip install pydub
sudo apt update && sudo apt upgrade
sudo apt install ffmpeg
```

## Guia de uso

* Execute o arquivo main.py do diretório "compiler" com o path do programa a ser executado
  
* Programas de exemplo usam a extensão .au mas qualquer extensão funciona

* No momento, apenas arquivos .mp3 funcionam na linguagem como fontes de áudio

```
python main.py ./programa.au
```  

## Features de áudio

* play: tocar o áudio
  
* output: realiza download do áudio

* Operações de soma entre áudios combinam os dois

* multiplicação de áudio por inteiros fazem o áudio repetir 

* audio from x to y: retorna trecho do audio de x até y milisegundos

* audio rcut x: retorna trecho de áudio do início até x milisegundos

* audio lcut x: retorna trecho de áudio de x milisegundos até o final

* audio1 insert audio2 at x: insere o audio2 dentro de audio1 no instante de x milisegundos (atalho para audio1 rcut x  + audio2 + audio lcut x)

### Para resolver dúvidas consulte os programas de exemplo


## EBNF

```
block = {statement};

statement = ('\n'|assignment|print|while|if|output|play|varDeclaration);

varDeclaration = ('source', identifier, (('=', expression)|)|'int', identifier, (('=', bool_exp)|)), ';';

assignment = identifier, '=', (bool_exp|expression), ';';

print = 'print', '(', bool_exp, ')', ';';

output = 'output', '(', identifier, ',', string, ')',';';

play = 'play', expression, ';';

while = 'while', '(', bool_exp, ')', '{', {statement}, '}', ';';

if = 'if', '(', bool_exp, ')', '{', {statement}, '}', (|'else', '{', {statement}, '}'), ';';

bool_exp = bool_term, { ( 'or' ) , bool_term };

bool_term = rel_exp, { ( 'and' ) , rel_exp };

rel_exp = expression, { ( '==' | '>'|'<' ) , expression };

expression = term, { ( '+' | '-' ) , term };

term = { factor, ( '*' | '/' ) }, factor;

factor = number | string | identifier | ('+'| '-'|'not'), factor | ('(', expression, ')')| ('read', '(', ')')|identifier_operations ;

identifier = (letter | '_'), {letter | digit | '_'};

identifier_operations = identifier, {('from', expression, 'to', expression)| ('rcut', expression)| ('lcut', expression)| ('insert', identifier, 'at', expression)};

letter = 'a' | '...' | 'Z';

number = digit, { digit };

digit = '0' | '1' | '...' | '9';

string = '"', { character }, '"';

character = letter | digit | special_character;

special_character = '!' | '@' | '#' | '$' | '%' | '^' | '&' | '*' | '(' | ')' | '-' | '_' | '+' | '=' | '[' | ']' | '{' | '}' | '|' | ':' | ';' | '<' | ',' | '.' | '>' | '?' | '/' | '`' | '~';
```
