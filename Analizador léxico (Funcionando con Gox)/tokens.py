from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    # Palabras Reservadas
    CONST = "const"
    VAR = "var"
    PRINT = "print"
    RETURN = "return"
    BREAK = "break"
    CONTINUE = "continue"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    FUNC = "func"
    IMPORT = "import"
    TRUE = "true"
    FALSE = "false"
    
    # Identificadores
    ID = "id"
    
    # Literales
    INTEGER = "integer"
    FLOAT = "float"
    CHAR = "char"
    
    # Operadores
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    LT = '<'
    LE = '<='
    GT = '>'
    GE = '>='
    EQ = '=='
    NE = '!='
    LAND = '&&'
    LOR = '||'
    GROW = '^'
    
    # Simbolos Miscelaneos
    ASSIGN = '='           
    SEMI = ';'
    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'
    COMMA = ','
    DEREF = '`'
    
    def __str__(self) -> str:
        return self.name
    
@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    lineno: int = 0  # Para reportar errores

    def __repr__(self) -> str:
        return f'{self.token_type}("{self.lexeme}")'
