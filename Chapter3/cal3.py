# token类型
# EOF (end-of-file)表示词法分析已经结束
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        # token类型: INTEGER, PLUS, or EOF
        self.type = type
        # token取值: 非负整数, '+', '-', or None
        self.value = value

    def __str__(self):
        """token对象的字符串表达.
        例:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        # 命令行输入的字符串，例如："3 + 5", "12 - 5 + 3"
        self.text = text
        # self.pos是self.text的下标
        self.pos = 0
        # 当前正在处理的token
        self.current_token = None
        self.current_char = self.text[self.pos]

    ##########################################################
    # 词法解析器代码                                           #
    ##########################################################
    def error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        """'pos'指针前移，并为'current_char'赋值"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """返回一个从输入中获取的多位整数"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """词法解析器（别名，tokenizer）
        该函数负责将字符串分解成一个个token
        每次调用返回一个token
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()

        return Token(EOF, None)

    ##########################################################
    # 解析器/解释器代码                                        #
    ##########################################################
    def eat(self, token_type):
        # 将传入的token类型于当前的token类型进行比较，如果匹配成功，
        # 那么就"吃掉"当前的token，然后把下一个token赋值给self.current_token
        # 否则报错
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        """Return an INTEGER token value."""
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        """算术表达式解析器 / 解释器."""
	    # 将当前token设置为从输入解析出的第一个token
        self.current_token = self.get_next_token()

        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()