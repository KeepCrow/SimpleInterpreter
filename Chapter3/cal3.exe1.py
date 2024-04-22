"""
绘制一个仅识别乘除法的语法图，例如"7 * 4 / 2 * 3"
修改源代码，使其符合你绘制的语法图
"""


# token类型
# EOF 表示输入的结束
INTEGER, MULTIPLY, DIVIDE, EOF = 'INTEGER', 'MULTIPLY', 'DIVIDE', 'EOF'

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """token对象的字符串表达
        例如：
            Token(INTEGER, 3)
            Token(MULTIPLY, '*')
        """
        return f'Token({self.type}, {self.value})'

    def __repr__(self):
        return self.__str__()
    
class Interpreter:
    def __init__(self, text:str):
        self.text = text
        self.pos = 0
        self.cur_char = self.text[self.pos]
        self.cur_token = self.get_next_token()
    
    def advance(self):
        self.pos += 1
        self.cur_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.cur_char and self.cur_char.isspace():
            self.advance()

    def integer(self) -> int:
        res = 0
        while self.cur_char and self.cur_char.isdigit():
            res = res * 10 + int(self.cur_char)
            self.advance()
        return res

    # 从字符串中获取下一个token
    def get_next_token(self) -> Token:
        while self.cur_char:
            if self.cur_char.isspace():
                self.skip_whitespace()
                continue

            if self.cur_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.cur_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')
            
            if self.cur_char == '/':
                self.advance()
                return Token(DIVIDE, '/')

        return Token(EOF, None)

    def error(self):
        raise Exception('解释器遇到了错误，请检查输入是否符合语法')

    def eat(self, expect_type):
        if self.cur_token.type == expect_type:
            self.cur_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        token = self.cur_token
        self.eat(INTEGER)
        return token.value

    def is_finished(self) -> bool:
        return self.cur_token.value == None

    def expr(self):
        res = self.term()
        while not self.is_finished():
            if self.cur_token.value == '*':
                self.eat(MULTIPLY)
                res *= self.term()
            else:
                self.eat(DIVIDE)
                res /= self.term()
        return res

def main():
    while True:
        try:
            text = input('cal> ')
        except EOFError:
            break
        if not text:
            continue

        interpreter = Interpreter(text)
        print(interpreter.expr())

if __name__=="__main__":
    main()