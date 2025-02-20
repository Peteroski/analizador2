from tokens import Token, TokenType

class Scanner:
    def __init__(self, text) -> None:
        self.it = iter(text)
        self.curr = None
        self.lineno = 1
        self.advance()
        
    def advance(self):
        try:
            self.curr = next(self.it)
            if self.curr == '\n':
                self.lineno += 1
        except StopIteration:
            self.curr = None
    
    def scan(self):
        while self.curr is not None:
            print(self.curr)
            if self.curr in ('\n','\t', ' '):
                self.advance()
            elif self.curr == '/':
                token = self.handle_comment_or_divide()
                if token is not None:
                    return token

            elif self.curr == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.lineno)
            elif self.curr == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.lineno)
            elif self.curr == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{', self.lineno)
            elif self.curr == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}', self.lineno)
            elif self.curr == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', self.lineno)
            elif self.curr == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', self.lineno)
            elif self.curr == '*':
                self.advance()
                return Token(TokenType.TIMES, '*', self.lineno)
            elif self.curr == '<':
                self.advance()
                if self.curr == '=':
                    self.advance()
                    return Token(TokenType.LE, '<=', self.lineno)
                return Token(TokenType.LT, '<', self.lineno)
            elif self.curr == '>':
                self.advance()
                if self.curr == '=':
                    self.advance()
                    return Token(TokenType.GE, '>=', self.lineno)
                return Token(TokenType.GT, '>', self.lineno)
            elif self.curr == '=':
                self.advance()
                if self.curr == '=':
                    self.advance()
                    return Token(TokenType.EQ, '==', self.lineno)
                return Token(TokenType.ASSIGN, '=', self.lineno)
            elif self.curr == ';':
                self.advance()
                return Token(TokenType.SEMI, ';', self.lineno)
            elif self.curr == ',':
                self.advance()
                return Token(TokenType.COMMA, ',', self.lineno)
            elif self.curr == '`':
                self.advance()
                return Token(TokenType.DEREF, '`', self.lineno)
            elif self.curr == '!':
                self.advance()
                if self.curr == '=':
                    self.advance()
                    return Token(TokenType.NE, '!=', self.lineno)
                raise Exception(f'Caracter ilegal {self.curr!r} en linea {self.lineno}')
            elif self.curr == '&':
                self.advance()
                if self.curr == '&':
                    self.advance()
                    return Token(TokenType.LAND, '&&', self.lineno)
                raise Exception(f'Caracter ilegal {self.curr!r} en linea {self.lineno}')
            elif self.curr == '|':
                self.advance()
                if self.curr == '|':
                    self.advance()
                    return Token(TokenType.LOR, '||', self.lineno)
                raise Exception(f'Caracter ilegal {self.curr!r} en linea {self.lineno}')
            elif self.curr == '^':
                self.advance()
                return Token(TokenType.GROW, '^', self.lineno)
            elif self.curr == '.' or self.curr.isdigit():
                return self.handle_number()

            elif self.curr.isalpha() or self.curr == '_':
                return self.handle_identifier_or_keyword()
            elif self.curr == '\'':
                return self.handle_char()
            else:
                # raise Exception(f'Caracter ilegal {self.curr!r} en linea {self.lineno}')
                return f'Caracter ilegal {self.curr!r} en linea {self.lineno}'
        return None
    
    def handle_comment_or_divide(self):
        start_line = self.lineno
        self.advance()
        if self.curr == '/':
            # Comentario de una línea
            while self.curr is not None and self.curr != '\n':
                self.advance()
            return None
        elif self.curr == '*':


            # Comentario de múltiples líneas
            self.advance()
            while self.curr is not None:
                if self.curr == '*' and self.peek() == '/':
                    self.advance()  # Consume '*'
                    self.advance()  # Consume '/'
                    return None
                self.advance()
            raise Exception(f'Comentario no terminado en linea {self.lineno}')
        else:
            return Token(TokenType.DIVIDE, '/', self.lineno)
    
    def handle_number(self):
        num_str = ''
        is_float = False
        
        # Manejar números que comienzan con punto
        if self.curr == '.':
            is_float = True
            num_str += self.curr
            self.advance()
            
            # Parte fraccionaria
            while self.curr is not None and self.curr.isdigit():
                num_str += self.curr
                self.advance()
        else:
            # Parte entera
            while self.curr is not None and self.curr.isdigit():
                num_str += self.curr
                self.advance()
            
            # Punto decimal
            if self.curr == '.':
                is_float = True
                num_str += self.curr
                self.advance()
                
                # Parte fraccionaria
                while self.curr is not None and self.curr.isdigit():
                    num_str += self.curr
                    self.advance()

        
        if is_float:
            return Token(TokenType.FLOAT, num_str, self.lineno)
        else:
            return Token(TokenType.INTEGER, num_str, self.lineno)
    
    def handle_identifier_or_keyword(self):
        ident = ''
        while self.curr is not None and (self.curr.isalnum() or self.curr == '_'):
            ident += self.curr
            self.advance()
        
        # Verificar si es una palabra reservada
        try:
            token_type = TokenType(ident)
            return Token(token_type, ident, self.lineno)
        except ValueError:
            return Token(TokenType.ID, ident, self.lineno)
    
    def handle_char(self):
        self.advance()  # Consume la comilla inicial
        char = ''
        
        if self.curr == '\\':
            # Caracter de escape
            self.advance()
            if self.curr in ('n', 't', 'r', '\\', '\''):
                char = '\\' + self.curr
                self.advance()
            elif self.curr == 'x':
                # Caracter hexadecimal
                self.advance()
                hex_digits = ''
                for _ in range(2):
                    if self.curr is None or not self.curr.isalnum():
                        raise Exception(f'Caracter hexadecimal incompleto en linea {self.lineno}')
                    hex_digits += self.curr
                    self.advance()
                char = '\\x' + hex_digits
            else:
                raise Exception(f'Caracter de escape desconocido en linea {self.lineno}')
        else:
            # Caracter normal
            if self.curr is None or self.curr == '\'':
                raise Exception(f'Caracter no terminado en linea {self.lineno}')
            char = self.curr
            self.advance()
        
        if self.curr != '\'':
            raise Exception(f'Caracter no terminado en linea {self.lineno}')
        self.advance()  # Consume la comilla final
        
        return Token(TokenType.CHAR, char, self.lineno)
    
    def peek(self):
        try:
            next_char = next(self.it)
            self.it = iter([next_char] + list(self.it))
            return next_char
        except StopIteration:
            return None
    
    def scanAll(self):
        tokens = []
        while True:
            token = self.scan()
            if token is None:
                break
            tokens.append(token)
        # Convert tokens to string representation for comparison
        return [str(t) for t in tokens]
