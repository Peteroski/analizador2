import unittest
from scanner import Scanner
from tokens import Token, TokenType

class TestScanner(unittest.TestCase):
    
    def test_single_tokens(self):
        tests = [
            ('(', TokenType.LPAREN),
            (')', TokenType.RPAREN),
            ('{', TokenType.LBRACE),
            ('}', TokenType.RBRACE),
            ('+', TokenType.PLUS),
            ('-', TokenType.MINUS),
            ('*', TokenType.TIMES),
            ('/', TokenType.DIVIDE),
            ('<', TokenType.LT),
            ('<=', TokenType.LE),
            ('>', TokenType.GT),
            ('>=', TokenType.GE),
            ('==', TokenType.EQ),
            ('=', TokenType.ASSIGN),
            (';', TokenType.SEMI),
            (',', TokenType.COMMA),
            ('`', TokenType.DEREF),
            ('!=', TokenType.NE),
            ('&&', TokenType.LAND),
            ('||', TokenType.LOR),
            ('^', TokenType.GROW)
        ]
        
        for text, expected_type in tests:
            with self.subTest(text=text):
                scanner = Scanner(text)
                token = scanner.scan()
                self.assertEqual(token.token_type, expected_type)
                self.assertEqual(token.lexeme, text)
    
    def test_keywords(self):
        tests = [
            ('true', TokenType.TRUE),
            ('false', TokenType.FALSE),
            ('const', TokenType.CONST),
            ('var', TokenType.VAR),
            ('print', TokenType.PRINT),
            ('return', TokenType.RETURN),
            ('break', TokenType.BREAK),
            ('continue', TokenType.CONTINUE),
            ('if', TokenType.IF),
            ('else', TokenType.ELSE),
            ('while', TokenType.WHILE),
            ('func', TokenType.FUNC),
            ('import', TokenType.IMPORT)
        ]
        
        for text, expected_type in tests:
            with self.subTest(text=text):
                scanner = Scanner(text)
                token = scanner.scan()
                self.assertEqual(token.token_type, expected_type)
                self.assertEqual(token.lexeme, text)
    
    def test_whitespace(self):
        scanner = Scanner('  \t\n  +  ')
        token = scanner.scan()
        self.assertEqual(token.token_type, TokenType.PLUS)
        self.assertEqual(token.lexeme, '+')
    
    def test_invalid_character(self):
        scanner = Scanner('@')
        with self.assertRaises(Exception) as context:
            scanner.scan()
        self.assertTrue('Caracter ilegal' in str(context.exception))
    
    def test_scan_all(self):
        scanner = Scanner('if (true) { return 1; }')
        tokens = scanner.scanAll()
        expected = [
            'IF("if")',
            'LPAREN("(")',
            'TRUE("true")',
            'RPAREN(")")',
            'LBRACE("{")',
            'RETURN("return")',
            'INTEGER("1")',
            'SEMI(";")',
            'RBRACE("}")'
        ]
        self.assertEqual(tokens, expected)

    
    def test_identifiers(self):
        tests = [
            ('x', TokenType.ID),
            ('var1', TokenType.ID),
            ('_test', TokenType.ID),
            ('a1b2c3', TokenType.ID)
        ]
        
        for text, expected_type in tests:
            with self.subTest(text=text):
                scanner = Scanner(text)
                token = scanner.scan()
                self.assertEqual(token.token_type, expected_type)
                self.assertEqual(token.lexeme, text)
    
    def test_numbers(self):
        tests = [
            ('123', TokenType.INTEGER),
            ('123.456', TokenType.FLOAT),
            ('123.', TokenType.FLOAT),
            ('.456', TokenType.FLOAT)
        ]
        
        for text, expected_type in tests:
            with self.subTest(text=text):
                scanner = Scanner(text)
                token = scanner.scan()
                self.assertEqual(token.token_type, expected_type)
                self.assertEqual(token.lexeme, text)
    
    def test_chars(self):
        tests = [
            ("'a'", TokenType.CHAR),
            ("'\\n'", TokenType.CHAR),
            ("'\\x41'", TokenType.CHAR),
            ("'\\''", TokenType.CHAR)
        ]
        
        for text, expected_type in tests:
            with self.subTest(text=text):
                scanner = Scanner(text)
                token = scanner.scan()
                self.assertEqual(token.token_type, expected_type)
                self.assertEqual(token.lexeme, text[1:-1])
    
    def test_comments(self):
        scanner = Scanner('// comentario\n+')
        token = scanner.scan()
        self.assertEqual(token.token_type, TokenType.PLUS)
        
        scanner = Scanner('/* comentario */+')
        token = scanner.scan()
        self.assertEqual(token.token_type, TokenType.PLUS)
    
    def test_error_handling(self):
        # Test illegal character with exact error message
        with self.assertRaises(Exception) as context:
            scanner = Scanner('@')
            scanner.scan()
        self.assertEqual(str(context.exception), "Caracter ilegal '@' en linea 1")
        
        # Test unterminated character with exact error message
        with self.assertRaises(Exception) as context:
            scanner = Scanner("'a")
            scanner.scan()
        self.assertEqual(str(context.exception), "Caracter no terminado en linea 1")
        
        # Test unterminated character on line 2 with exact error message
        with self.assertRaises(Exception) as context:
            scanner = Scanner("\n'a")
            scanner.scan()
        self.assertEqual(str(context.exception), "Caracter no terminado en linea 2")
        
        # Test unterminated comment with exact error message
        with self.assertRaises(Exception) as context:
            scanner = Scanner('/* comentario no terminado')
            scanner.scanAll()
        self.assertEqual(str(context.exception), "Comentario no terminado en linea 1")
        
        # Test unterminated comment spanning multiple lines with exact error message
        with self.assertRaises(Exception) as context:
            scanner = Scanner('/* comentario\nno terminado')
            scanner.scanAll()
        self.assertEqual(str(context.exception), "Comentario no terminado en linea 2")
        
        # Test invalid escape sequence
        with self.assertRaises(Exception) as context:
            scanner = Scanner("'\\z'")
            scanner.scan()
        self.assertEqual(str(context.exception), "Caracter de escape desconocido en linea 1")
        
        # Test incomplete hex character
        with self.assertRaises(Exception) as context:
            scanner = Scanner("'\\x1'")
            scanner.scan()
        self.assertEqual(str(context.exception), "Caracter hexadecimal incompleto en linea 1")



if __name__ == '__main__':
    unittest.main()
