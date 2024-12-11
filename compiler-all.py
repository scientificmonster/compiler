import tkinter as tk
from tkinter import Text, Listbox, Button, Label, Scrollbar
class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value
    def __str__(self):
        return f"({self.type}, {self.value})"
# 标识符类
class triple:
    def __init__(self, name):
        # int $abc$ = 123
        self.name = name # $abc$
        self.type_ = None # int
        self.value = None # 123
    def __str__(self):
        return f"{self.name}, {self.type_}, {self.value}"

    def getValueAsInt(self):
        if self.type_ != 'int':
            return -1
        if self.value == '':
            return -1
        try:
            return int(self.value)
        except ValueError:
            return -1

    def getValueAsBool(self):
        if self.type_ != 'bool':
            return False
        if self.value == '':
            return False
        if self.value == 'true':
            return True
        return False
    def getValueAsString(self):
        if self.type_ != 'string':
            return -1
        if self.value == '':
            return -1
        return str(self.value)
#标识符列表类
class IdentifierTable:
    def __init__(self):
        # 列表里面存放标识符triple
        self.idenTable = []
    # 查询标识符列表中是否有name的标识符,查重cc,(有重则返回重复,无则None)
    def cc(self, name):
        for triple in self.idenTable:
            if triple.name == name:
                return triple
        return None
    # 为标识符列表增加新的标识符add(name)
    def add(self, name):
        # 标识符已经存在则不需要添加
        if self.cc(name) is not None:
            return False
        # 不存在的化就用name添加进去
        self.idenTable.append(triple(name))
        return True
    # 根据name更新标识符列表中的type
    def upType(self, name, type_):
        t = self.cc(name)
        if t is None:
            return False
        # if t.type_ != "":
        #     return False
        t.type_ = type_
        # print(f"{t.name}的type被更新为{type_}")
        # return True
    # 根据name更新表舒服列表中对应的value
    def upValue(self, name, value):
        triple = self.cc(name)
        if triple is None:
            return False
        # if triple.value != "":
        #     return False
        triple.value = value
        # return True
        # print(f"{triple.name}的value被更新为{value}")
    # 打印标识符列表

    def dump(self, list_box):
        # list_box.append("| \t name | \t type | \t value |")
        # for triple in self.table:
        #     list_box.append(f"|{triple}|")
        print("| \t name | \t type | \t value |")
        for triple in self.idenTable:
            print(f"|{triple}|")

# 用于表达式的临时变量表格
class TempVariableTable:
    def __init__(self):
        self.tmpTable = []
    # 每次调用返回一个未使用过名称的临时变量triple
    def createTemp(self):
        temp = triple(f"T{len(self.tmpTable)}")
        self.tmpTable.append(temp)
        print(f"新创建了一个临时变量{temp.name}")
        return temp
class TAC:
    def __init__(self, op, oprand1, oprand2, result):
        self.op = op
        self.oprand1 = oprand1
        self.oprand2 = oprand2
        self.result = result
    def __str__(self):
        return f"({self.op}, {self.oprand1}, {self.oprand2}, {self.result})"
class tacTable:
    def __init__(self):
        self.tacTable = []
    @property
    def NXQ(self):
        return len(self.tacTable)

    def generate(self, op, oprand1, oprand2, result):
        tmpTAC = TAC(op, oprand1, oprand2, result)
        # print(tmpTAC)
        # print(type(tmpTAC))
        self.tacTable.append(tmpTAC)
        # print(TAC)

    def backpatch(self, index, result):
        if index >= len(self.tacTable):
            return
        self.tacTable[index].result = result

    def dump(self):
        for i, tac in enumerate(self.tacTable):
            print(f"({i}){tac}")
class compiler:
    def __init__(self, source_program):
        self.source_program = source_program
        self.pointer = 0
        # token 列表仅用作输出时使用,并非多遍扫描
        self.tokens = []

        self.parse_idx = 0
        self.current_token = Token("null", 'null')
        self.parse_list = []

        self.idenTable = IdentifierTable()
        self.tmpTable = TempVariableTable()
        self.tacTable = tacTable()
    #############################################################################################
    # 以下为词法分析
    def next_input(self):
        tmp_word = ""
        state = 0
        while self.pointer < len(self.source_program):
            symbol = self.source_program[self.pointer]
            # if symbol == '#':
            #     if tmp_word != "" :
            #         print(tmp_word)
            #         print(type(tmp_word))
            if symbol == ' ':
                self.pointer += 1
                continue
            if state == 0:
                if symbol == '$':
                    state = 100
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                if symbol == '"':
                    state = 300
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif '0' <= symbol <= '9':
                    state = 200
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == ';':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("分号", tmp_word)
                elif symbol == 'i':
                    state = 400
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == 's':
                    state = 500
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == 'b':
                    state = 600
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == ',':
                    # state = 700
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("逗号", tmp_word)
                elif symbol == ':':
                    # state = 2200
                    tmp_word += symbol
                    self.pointer += 1
                    if self.pointer < len(self.source_program) and self.source_program[self.pointer] == '=':
                        tmp_word += self.source_program[self.pointer]
                        self.pointer += 1
                        return Token("赋值号", tmp_word)
                    return Token("冒号", tmp_word)
                elif symbol == 'o':
                    state = 900
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == 'a':
                    state = 1000
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == 'n':
                    state = 1100
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == 't':
                    state = 1200
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == 'f':
                    state = 1300
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == 'e':
                    state = 1800
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == 'w':
                    state = 1900
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == '(':
                    # state = 1400
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("左括号", tmp_word)
                elif symbol == ')':
                    # state = 1500
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("右括号", tmp_word)
                elif symbol == '<':
                    tmp_word += symbol
                    self.pointer += 1
                    if self.pointer < len(self.source_program) and self.source_program[self.pointer] == '=':
                        tmp_word += self.source_program[self.pointer]
                        self.pointer += 1
                        return Token("关系", tmp_word)
                    return Token("关系", tmp_word)
                elif symbol == '>':
                    tmp_word += symbol
                    self.pointer += 1
                    if self.pointer < len(self.source_program) and self.source_program[self.pointer] == '=':
                        tmp_word += self.source_program[self.pointer]
                        self.pointer += 1
                        return Token("关系", tmp_word)
                    return Token("关系", tmp_word)
                elif symbol == '=':
                    state = 1620
                    tmp_word += symbol
                    self.pointer += 1
                    if self.source_program[self.pointer]=='=':
                        self.pointer += 1
                        tmp_word += '='
                        return Token("关系", tmp_word)

                elif symbol == '+' or symbol == '-':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("加法", tmp_word)
                elif symbol == '*' or symbol == '/' or symbol == '%':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("乘法", tmp_word)
                elif symbol == '{':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("begin", tmp_word)
                elif symbol == '}':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("end", tmp_word)
                elif symbol == '#':
                    self.pointer += 1
                    return Token("#", "#")
                else:
                    self.pointer += 1
                    return Token("Error", f"未知符号 '{symbol}'")
            if state == 100:  # 标识符
                if 'a' <= symbol <= 'z':
                    state = 101
                    tmp_word += symbol
                    self.pointer += 1
                    if self.source_program[self.pointer] == '$':
                        self.pointer += 1
                        tmp_word += "$"
                        return Token("标识符", tmp_word)
                    continue
            if state == 101:
                if 'a' <= symbol <= 'z' or '0' <= symbol <= '9':
                    state = 101
                    tmp_word += symbol
                    self.pointer += 1
                    if self.source_program[self.pointer] == '$':
                        self.pointer += 1
                        tmp_word += "$"
                        return Token("标识符", tmp_word)
                    continue
                else:
                    return Token("Error", f"标识符中包含非法字符 '{symbol}'")
            if state == 300:  # 字符串状态
                if symbol == '"':  # 处理空字符串
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("字符串", tmp_word)
                elif 'a' <= symbol <= 'z' or '0' <= symbol <= '9' or symbol == ' ':
                    state = 300
                    tmp_word += symbol
                    self.pointer += 1
                    if self.source_program[self.pointer] == '"':
                        self.pointer += 1
                        tmp_word += '"'
                        return Token("字符串", tmp_word)
                    continue
                else:
                    return Token("Error", f"字符串中包含非法字符 '{symbol}'")
            if state == 200:  # Number state
                # if symbol.isdigit():
                if '0' <= symbol <= '9':
                    state = 200
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                else:
                    return Token("整数", tmp_word)
            if state == 400:
                if symbol == 'n':
                    state = 401
                    tmp_word += symbol
                    self.pointer += 1
                    continue
                elif symbol == 'f':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("if", tmp_word)
            if state == 401:
                if symbol == 't':
                    # state = 402
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("变量说明", tmp_word)
            if state == 500:
                if symbol == 't':
                    state = 501
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 501:
                if symbol == 'r':
                    state = 502
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 502:
                if symbol == 'i':
                    state = 503
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 503:
                if symbol == 'n':
                    state = 504
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 504:
                if symbol == 'g':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("变量说明", tmp_word)
            if state == 600:
                if symbol == 'o':
                    state = 601
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 601:
                if symbol == 'o':
                    state = 602
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 602:
                if symbol == 'l':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("变量说明", tmp_word)
            if state == 900:
                if symbol == 'r':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("or", tmp_word)
            if state == 1000:
                if symbol == 'n':
                    state = 1001
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1001:
                if symbol == 'd':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("and", tmp_word)
            if state == 1100:
                if symbol == 'o':
                    state = 1101
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1101:
                if symbol == 't':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("not", tmp_word)
            if state == 1200:
                if symbol == 'r':
                    state = 1201
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1201:
                if symbol == 'u':
                    state = 1202
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1202:
                if symbol == 'e':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("true", tmp_word)

            if state == 1300:
                if symbol == 'a':
                    state = 1301
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1301:
                if symbol == 'l':
                    state = 1302
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1302:
                if symbol == 's':
                    state = 1303
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1303:
                if symbol == 'e':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("false", tmp_word)
            if state == 1800:
                if symbol == 'l':
                    state = 1801
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1801:
                if symbol == 's':
                    state = 1802
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1802:
                if symbol == 'e':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("else", tmp_word)
            if state == 1900:
                if symbol == 'h':
                    state = 1901
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1901:
                if symbol == 'i':
                    state = 1902
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1902:
                if symbol == 'l':
                    state = 1903
                    tmp_word += symbol
                    self.pointer += 1
                    continue
            if state == 1903:
                if symbol == 'e':
                    tmp_word += symbol
                    self.pointer += 1
                    return Token("while", tmp_word)
            else:
                return Token("Error", f"未知符号 '{symbol}'")
    def run_lexer(self):
        self.pointer = 0
        self.tokens = []
        while True:
            self.current_token = self.next_input()
            self.tokens.append(self.current_token)
            if self.current_token.type == "#":
                # self.tokens.append(Token("#", "#"))
                break
        return self.tokens
    #############################################################################################
    # 以下为语法分析
    # 这是一遍扫描的程序调用
    def run_parse_one(self):
        self.pointer = 0
        # self.tokens = []
        while True:
            self.current_token = self.next_input()
            # self.tokens.append(self.current_token)
            self.parse_program()
            if self.current_token.type == "#":
                # self.tokens.append(Token("#", "#"))
                break
        return self.parse_list
    def match(self, expected_token):
        if self.current_token.type != expected_token:
            print(f"匹配失败：expect'{expected_token}',got'{self.current_token.type}'")
            self.parse_list.append(f"匹配失败：expect'{expected_token}',got'{self.current_token.type}'")
            return False
        # print(f"匹配成功：{self.current_token}")
        self.parse_list.append(f"匹配成功：{self.current_token}")
        # self.parse_idx += 1
        # self.current_token = self.tokens[self.parse_idx]
        # print(self.current_token)
        self.current_token = self.next_input()
        return True
    def parse_program(self):
        self.parse_list.append('推导:<程序> → <变量说明部分> <语句部分>')
        self.parse_declareSec()
        self.parse_stateSec()
        print('语法分析结束')

    #############################################################################################
    #变量说明部分
    def parse_declareSec(self):

        self.parse_list.append('推导:<变量说明部分> → <变量说明语句> 分号 A')
        self.parse_declareState()
        self.match("分号")
        self.parseA()
    def parseA(self):

        self.parse_list.append('选择产生式:A → <变量说明语句> 分号 A | ε')
        if self.current_token.type == "变量说明":

            self.parse_list.append('推导:A → <变量说明语句> 分号 A')
            self.parse_declareState()
            self.match("分号")
            self.parseA()
        elif self.current_token.type == "标识符" or self.current_token.type == "if" or self.current_token.type == "while":

            self.parse_list.append('推导:A → ε')
            return
    def parse_declareState(self):

        self.parse_list.append('推导:<变量说明语句> → 变量说明 <标识符列表>')
        # 传参获得变量说明
        type_ = self.current_token.value

        self.match("变量说明")
        self.parse_varlist(type_)
    def parse_varlist(self, type_):

        # 获得标识符列表的name
        name = self.current_token.value
        print('推导:<标识符列表> → 标识符 B')
        self.parse_list.append('推导:<标识符列表> → 标识符 B')
        self.match("标识符")

        # 更新标识符表(name,type_)
        self.idenTable.add(name)
        # add后就更新type
        self.idenTable.upType(name, type_)
        for i in self.idenTable.idenTable:
            print(i)
        self.tacTable.generate(op="declare", oprand1=type_, oprand2='null', result=f"{name}.type")
        self.parseB(type_)
    def parseB(self, type_):
        # print('选择产生式:B → 逗号 标识符 B | ε')
        self.parse_list.append('选择产生式:B → 逗号 标识符 B | ε')
        if self.current_token.type == '逗号':
            # print('推导:B → 逗号 标识符 B')
            self.parse_list.append('推导:B → 逗号 标识符 B')
            self.match('逗号')
            name = self.current_token.value
            self.match("标识符")
            self.idenTable.add(name)
            self.idenTable.upType(name, type_)
            self.tacTable.generate(op="declare", oprand1=type_, oprand2=None, result=f"{name}.type")

            self.parseB(type_)
        elif self.current_token.type == "分号":
            # print('推导:B → ε')
            self.parse_list.append('推导:B → ε')
    ############################################################################################################
    def parse_stateSec(self):
        print('推导:<语句部分> → <语句> C')
        self.parse_list.append('推导:<语句部分> → <语句> C')
        self.parse_state()
        self.parseC()
    def parseC(self):
        print('选择产生式:C → 分号 <语句> C | ε')
        self.parse_list.append('选择产生式:C → 分号 <语句> C | ε')
        if self.current_token.type == "分号":
            self.match("分号")
            print('推导:C → 分号 <语句> C')
            self.parse_list.append('推导:C → <语句> C')
            self.parse_state()
            self.parseC()
        elif self.current_token.type == "#" or self.current_token.type == "end":
            print('推导:C → ε')
            self.parse_list.append('推导:C → ε')
    def parse_state(self):
        print("选择产生式:<语句> → <赋值语句>|<条件语句>|<循环语句>")
        self.parse_list.append("选择产生式:<语句> → <赋值语句>|<条件语句>|<循环语句>")
        if self.current_token.type == "标识符":
            print("推导:<语句> → <赋值语句>")
            self.parse_list.append("推导:<语句> → <赋值语句>")
            self.parse_assignState()
        elif self.current_token.type == "if":
            print("推导:<语句> → <条件语句>")
            self.parse_list.append("推导:<语句> → <条件语句>")
            self.parse_condState()
        elif self.current_token.type == "while":
            print("推导:<语句> → <循环语句>")
            self.parse_list.append("推导:<语句> → <循环语句>")
            self.parse_loopState()
    ###################################################################################################
    # 赋值+表达式

    def parse_assignState(self):
        print('推导:<赋值语句> → 标识符 赋值号 <表达式>')
        self.parse_list.append('推导:<赋值语句> → 标识符 赋值号 <表达式>')
        # 记录下标识符名字
        name = self.current_token.value
        # print(name)
        self.match("标识符")
        self.match("赋值号")

        exp = self.parse_exp()
        # print(exp)
        # exp是一个临时变量其name是我创建的临时变量
        # self.idenTable.upValue(name, exp.value)
        self.tacTable.generate(op="assign", oprand1=exp.name, oprand2="null", result=name)
        self.tacTable.dump()
        # print(self.tacTable.tacTable[len(self.tacTable.tacTable)])
    def parse_exp(self):
        # print("推导:<表达式> → < conjunction > D")
        # self.parse_list.append("推导:<表达式> → < conjunction > D")
        print('推导:<表达式> → < inversion > E D')
        self.parse_list.append('推导:<表达式> → < inversion > E D')
        # self.tacTable.dump()
        # E1 = self.parse_inversion()
        # E = self.parseD(E1)
        E1 = self.parse_inversion()
        E2 = self.parseE(E1)
        E = self.parseD(E2)
        return E
    def parseD(self, E1):
        # print("选择产生式:D → or < conjunction > D | ε")
        # self.parse_list.append("选择产生式:D → or < conjunction > D | ε")
        print(E1)
        print('选择产生式:D → or < inversion > E D | ε')
        self.parse_list.append('选择产生式:D → or < inversion > E D | ε')
        if self.current_token.type == "or":
            # print("推导:D → or < conjunction > D")
            print("推导:D → or < inversion > E D")
            self.parse_list.append("推导:D → or < inversion > E D")
            self.match("or")
            E2 = self.parse_inversion()
            # 进行or运算
            T = self.tmpTable.createTemp()
            T.type_ = "bool"
            # 进行or运算,获得T正确的值
            T.value = "true"
            self.tacTable.generate(op="or", oprand1=E1.name, oprand2=E2.name, result=T.name)
            self.tacTable.dump()
            tmp = self.parseE(T)
            t2 = self.parseD(tmp)
            ###################################
            return t2
        elif self.current_token.type == "分号" or self.current_token.type == "#" or self.current_token.type == "end":
            print("推导:D → ε")
            self.parse_list.append("推导:D → ε")
            return E1
        return E1
    def parseE(self, E1):
        print(E1)
        print("选择产生式:E → and < inversion > E | ε")
        self.parse_list.append("选择产生式:E → and < inversion > E | ε")
        if self.current_token.type == "and":
            print("推导:E → and < inversion > E")
            self.parse_list.append("推导:E → and < inversion > E")
            self.match("and")
            E2 = self.parse_inversion()
            # 进行and运算
            T = self.tmpTable.createTemp()
            T.type_ = "bool"
            T.value = "true"
            self.tacTable.generate(op="and", oprand1=E1.name, oprand2=E2.name, result=T.name)
            self.tacTable.dump()
            a = self.parseE(T)
            return a
            ################################################
            # return self.parseE(T)
        elif self.current_token.type == "or" or self.current_token.type == "分号" or self.current_token.type == "#" or self.current_token.type == "end":
            print("推导:E → ε")
            self.parse_list.append("推导:E → ε")
            return E1
        return E1
    def parse_inversion(self):
        print("选择产生式:< inversion > → not < inversion > | <关系表达式>")
        self.parse_list.append("选择产生式:< inversion > → not < inversion > | <关系表达式>")
        if self.current_token.type == "not":
            print("推导:< inversion > → not < inversion >")
            self.parse_list.append("推导:< inversion > → not < inversion >")
            self.match("not")
            E1 = self.parse_inversion()
            print(E1.name)
            # 创建临时变量
            T = self.tmpTable.createTemp()
            print(T.name)
            T.type_ = "bool"
            # 根据E1进行not运算,获得T正确的值
            if E1 == None:
                return None
            if E1.value == "true":
                T.value = "false"
            else:
                T.value = "true"
            self.tacTable.generate(op="not", oprand1=E1.name, oprand2="null", result=T.name)
            self.tacTable.dump()
            return T

        elif self.current_token.type == "标识符" or self.current_token.type == "true" or self.current_token.type == "false" or self.current_token.type == "字符串" or self.current_token.type == "整数" or self.current_token.type == "左括号":
            print("推导:< inversion > → <关系表达式>")
            self.parse_list.append("推导:< inversion > → <关系表达式>")
            # print("1111111111111111111111111111111111111111")
            return self.parse_rel()
        return None
    def parse_rel(self):
        print("推导:<关系表达式> → <算术表达式> F")
        self.parse_list.append("推导:<关系表达式> → <算术表达式> F")
        E1 = self.parse_math()
        # 可能有问题
        E = self.parseF(E1)
        return E
    def parseF(self, E1):
        print(E1)
        print("选择产生式:F → 关系 <算术表达式> F | ε")
        self.parse_list.append("选择产生式:F → 关系 <算术表达式> F | ε")
        if self.current_token.type == "关系":
            print("推导:F → 关系 <算术表达式> F")
            self.parse_list.append("推导:F → 关系 <算术表达式> F")
            op = self.current_token.value
            self.match("关系")
            E2 = self.parse_math()
            T = self.tmpTable.createTemp()
            T.type_ = "bool"
            # 根据E1和E2进行关系运算,获得T正确的值
            T.value = "true"
            if op == "<":
                op = "lt"
            elif op == ">":
                op = "gt"
            elif op == "<>":
                op = "noteq"
            elif op == "<=":
                op = "lte"
            elif op == ">=":
                op = "gte"
            elif op == "==":
                op = "eq"
            self.tacTable.generate(op=op, oprand1=E1.name, oprand2=E2.name, result=T.name)
            self.tacTable.dump()
            # self.parseF(T)
            a = self.parseF(T)
            # 这边有问题
            return a
        elif self.current_token.type == "or" or self.current_token.type == "and" or self.current_token.type == "分号" or self.current_token.type == "#" or self.current_token.type == "end":
            print("推导:F → ε")
            self.parse_list.append("推导:F → ε")
            return E1
        return E1
    def parse_math(self):
        print("推导:<算术表达式> → <term> G")
        self.parse_list.append("推导:<算术表达式> → <term> G")
        E1 = self.parse_term()
        E = self.parseG(E1)
        return E
    def parseG(self, E1):
        print(E1)# None
        # print("G得到了值T1")
        print("选择产生式:G → 加法 <term> G | ε")
        self.parse_list.append("选择产生式:G → 加法 <term> G | ε")
        if self.current_token.type == "加法":
            print("推导:G → 加法 <term> G")
            op = self.current_token.value
            self.parse_list.append("推导:G → 加法 <term> G")
            self.match("加法")
            E2 = self.parse_term()
            # parse_term()->
            T = self.tmpTable.createTemp()
            if op == "+":
                op = "add"
            elif op == "-":
                op = "sub"
            self.tacTable.generate(op=op, oprand1=E1.name, oprand2=E2.name, result=T.name)
            self.tacTable.dump()
            a = self.parseG(T)
            return a
        elif self.current_token.type == "关系" or self.current_token.type == "or" or self.current_token.type == "and" or self.current_token.type == "分号" or self.current_token.type == "#" or self.current_token.type == "end":
            print("推导:G → ε")
            self.parse_list.append("推导:G → ε")
            return E1
        return E1
    def parse_term(self):
        print("推导:<term> → <factor> H")
        self.parse_list.append("推导:<term> → <factor> H")
        E1 = self.parse_factor()#parse_factor应该传过来,但是这里的E1是空的
        print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
        print(E1)#这是None
        E = self.parseH(E1)#下传到parseH
        return E
    def parseH(self,E1):
        print(E1)#这里参数没有传递过来E1有问题,None
        print(self.current_token.type)# 关系
        print("选择产生式:H → 乘法 <factor> H | ε")
        self.parse_list.append("选择产生式:H → 乘法 <factor> H | ε")
        # print('7777777777777777777')
        if self.current_token.type == "乘法":
            op = self.current_token.value
            # print(op)
            print("推导:H → 乘法 <factor> H")
            self.parse_list.append("推导:H → 乘法 <factor> H")
            self.match("乘法")
            E2 = self.parse_factor()
            T = self.tmpTable.createTemp()
            print(E2.name)
            print(T)#此处验证T2已经可以正确产生,E1的参数传递出了问题
            print(E1)#打印为None
            # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            T.type_ = "int"
            T.value = "1"
            if op == "*":
                op = "mul"
            elif op == "/":
                op = "div"
            elif op == "%":
                op = "mod"
            print(op)
            self.tacTable.generate(op=op, oprand1=E1.name, oprand2=E2.name, result=T.name)
            self.tacTable.dump()

            a = self.parseH(T)
            return a

        elif self.current_token.type == "关系" or self.current_token.type == "加法" or self.current_token.type == "or" or self.current_token.type == "and" or self.current_token.type == "分号" or self.current_token.type == "#" or self.current_token.type == "end":
            print("推导:H → ε")
            self.parse_list.append("推导:H → ε")
            print("当H推导空时E1为以下情况")
            print(E1)
            return E1

        return E1
    def parse_factor(self):
        print("选择产生式:<factor> → 标识符 | true | false | 字符串 | 整数 | 左括号 <表达式> 右括号")
        self.parse_list.append("选择产生式:<factor> → 标识符 | true | false | 字符串 | 整数 | 左括号 <表达式> 右括号")
        print('555555555555')
        print(self.current_token.type)#关系
        if self.current_token.type == "标识符":
            print("推导:<factor> → 标识符")
            name = self.current_token.value
            # print('66666666666666666666666666')
            self.parse_list.append("推导:<factor> → 标识符")
            self.match("标识符")
            print(self.idenTable.cc(name))
            return self.idenTable.cc(name)#此处参数传递有问题,未能成功传递到+右操作数
        elif self.current_token.type == "true":
            print("推导:<factor> → true")
            self.parse_list.append("推导:<factor> → true")
            self.match("true")
            t = triple("true")
            t.type_ = "bool"
            t.value = "true"
            return t
        elif self.current_token.type == "false":
            print("推导:<factor> → false")
            self.parse_list.append("推导:<factor> → false")
            self.match("false")
            t = triple("false")
            t.type_ = "bool"
            t.value = "false"
            return t
        elif self.current_token.type == "字符串":
            print("推导:<factor> → 字符串")
            value = self.current_token.value
            self.parse_list.append("推导:<factor> → 字符串")
            self.match("字符串")
            t = triple(value)
            t.type_ = "string"
            t.value = value
            # print(t)
            return t
        elif self.current_token.type == "整数":
            print('整数')
            print("推导:<factor> → 整数")
            value = self.current_token.value
            self.parse_list.append("推导:<factor> → 整数")
            self.match("整数")
            t = triple(value)
            t.type_ = "bool"
            t.value = value
            return t
        elif self.current_token.type == "左括号":
            print("推导:<factor> → 左括号 <表达式> 右括号")
            self.parse_list.append("推导:<factor> → 左括号 <表达式> 右括号")
            self.match("左括号")
            exp = self.parse_exp()

            self.match("右括号")
            print(exp)
            return exp

        t = triple(self.current_token.value)
        return t

    def parse_condState(self):
        print("推导:<条件语句> → if 左括号 <表达式> 右括号 <嵌套语句> else <嵌套语句>")
        self.parse_list.append("推导:<条件语句> → if 左括号 <表达式> 右括号 <嵌套语句> else <嵌套语句>")
        self.match("if")
        self.match("左括号")
        T = self.parse_exp()
        self.tacTable.generate(op="jnz", oprand1=T.name, oprand2='null', result=str(self.tacTable.NXQ+2))
        falseIndex = self.tacTable.NXQ
        self.tacTable.generate(op="jump", oprand1='null', oprand2='null', result='0')
        self.match("右括号")
        self.parse_nestState()
        exitIndex = self.tacTable.NXQ
        self.tacTable.generate(op="jump", oprand1='null', oprand2='null', result='0')
        self.tacTable.backpatch(falseIndex, str(self.tacTable.NXQ+2))
        self.match("else")
        self.parse_nestState()

        self.tacTable.backpatch(exitIndex, str(self.tacTable.NXQ+2))


    def parse_loopState(self):
        print("推导:<循环语句> → while 左括号 <表达式> 右括号 冒号 <嵌套语句>")
        self.parse_list.append("推导:<循环语句> → while 左括号 <表达式> 右括号 冒号 <嵌套语句>")
        self.match("while")
        self.match("左括号")
        T = self.parse_exp()
        self.tacTable.generate(op="jnz", oprand1=T.name, oprand2='null', result=str(self.tacTable.NXQ + 2))
        index = self.tacTable.NXQ
        self.tacTable.generate(op="jump", oprand1='null', oprand2='null', result='0')
        self.match("右括号")
        self.match("冒号")
        self.parse_nestState()
        self.tacTable.generate(op="jump", oprand1='null', oprand2='null', result='0')
        self.tacTable.backpatch(index, str(self.tacTable.NXQ + 2))
    def parse_nestState(self):
        print("选择产生式:<嵌套语句> → <语句> 分号 | <复合语句>")
        self.parse_list.append("选择产生式:<嵌套语句> → <语句> 分号 | <复合语句>")
        if self.current_token.type == "标识符" or self.current_token.type == "if" or self.current_token.type == "while":
            self.parse_state()
            self.match("分号")
            print("推导:<嵌套语句> → <语句> 分号")
            self.parse_list.append("推导:<嵌套语句> → <语句> 分号")
        elif self.current_token.type == "begin":
            print("推导:<嵌套语句> → <复合语句>")
            self.parse_list.append("推导:<嵌套语句> → <复合语句>")
            self.parse_compState()
    def parse_compState(self):
        print("推导:<复合语句> → begin <语句部分> end")
        self.parse_list.append("推导:<复合语句> → begin <语句部分> end")
        self.match("begin")
        self.parse_stateSec()
        self.match("end")


class GUI:
    def __init__(self, root):
        # 创建主窗口
        self.root = root
        self.root.title("Compiler   计(嵌入)2202朱智荣    202221176060")
        # 设置整体布局
        self.root.geometry("600x400")

        # 输入框
        self.input_label = Label(root, text="input")
        self.input_label.grid(row=0, column=0, columnspan=4, sticky='w', padx=5)
        self.input_text = Text(root, height=7, width=50)
        self.input_text.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='ew')

        # 按钮列表
        self.btn_0 = Button(root, text="词法分析", width=15, command=self.btn_0)
        self.btn_0.grid(row=2, column=0, padx=5, pady=5)

        self.btn_1 = Button(root, text="语法分析", width=15, command=self.btn_1)
        self.btn_1.grid(row=2, column=1, padx=5, pady=5)

        self.btn_2 = Button(root, text="TAC", width=15, command=self.btn_2)
        self.btn_2.grid(row=2, column=2, padx=5, pady=5)

        self.btn_3 = Button(root, text="AST", width=15, command=self.btn_3)
        self.btn_3.grid(row=2, column=3, padx=5, pady=5)

        # 左侧列表框（输出）
        self.output_label = Label(root, text="output")
        self.output_label.grid(row=3, column=0, sticky='w', padx=5)

        self.output_frame = tk.Frame(root)  # 创建一个新框架以包含列表框和滚动条
        self.output_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.output_listbox = Listbox(self.output_frame, height=10)
        self.output_listbox.pack(side='left', fill='both', expand=True)

        self.scrollbar_output = Scrollbar(self.output_frame, orient='vertical', command=self.output_listbox.yview)
        self.scrollbar_output.pack(side='right', fill='y')

        self.output_listbox.config(yscrollcommand=self.scrollbar_output.set)

        # 右侧列表框（调试）
        self.debug_label = Label(root, text="debug")
        self.debug_label.grid(row=3, column=2, sticky='w', padx=5)

        self.debug_frame = tk.Frame(root)  # 创建一个新框架以包含列表框和滚动条
        self.debug_frame.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.debug_listbox = Listbox(self.debug_frame, height=10)
        self.debug_listbox.pack(side='left', fill='both', expand=True)

        self.scrollbar_debug = Scrollbar(self.debug_frame, orient='vertical', command=self.debug_listbox.yview)
        self.scrollbar_debug.pack(side='right', fill='y')

        self.debug_listbox.config(yscrollcommand=self.scrollbar_debug.set)

        # 调整列宽
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)

    def btn_0(self):
        # input
        source_code = self.input_text.get("1.0", tk.END).strip() + "#"
        # 对象
        print(source_code)
        lexer = compiler(source_code)
        tokens = lexer.run_lexer()
        # 清空输出列表框的内容
        self.output_listbox.delete(0, tk.END)
        self.debug_listbox.delete(0, tk.END)
        # print(tokens)
        # self
        for token in tokens:
            self.output_listbox.insert(tk.END, str(token))
        self.output_listbox.insert(tk.END, '词法分析完成!!!')
            # print(token)
    def btn_1(self):
        # input
        source_code = self.input_text.get("1.0", tk.END).strip() + "#"
        # 对象
        parser = compiler(source_code)
        parser_list = parser.run_parse_one()

        # 清空输出列表框的内容
        self.output_listbox.delete(0, tk.END)
        self.debug_listbox.delete(0, tk.END)
        for token in parser.tokens:
            self.debug_listbox.insert(tk.END, str(token))
        self.output_listbox.insert(tk.END, '词法分析完成!!!')
        # print(tokens)
        for parser in parser_list:
            self.output_listbox.insert(tk.END, str(parser))
            print(parser)

        self.output_listbox.insert(tk.END, '语法分析完成!!!')
    def btn_2(self):
        # input
        source_code = self.input_text.get("1.0", tk.END).strip() + "#"
        # 对象
        tac = compiler(source_code)
        tac.run_parse_one()
        # 清空输出列表框的内容
        self.output_listbox.delete(0, tk.END)
        self.output_listbox.insert(tk.END, '词法分析完成!!!')
        self.output_listbox.insert(tk.END, '语法分析完成!!!')
        # 清空debug列表框的内容
        self.debug_listbox.delete(0, tk.END)
        self.debug_listbox.insert(tk.END, '词法分析完成!!!')
        parser_list = compiler(source_code).run_parse_one()
        for parser in parser_list:
            self.debug_listbox.insert(tk.END, str(parser))
            print(parser)
        self.debug_listbox.insert(tk.END, '语法分析完成!!!')

        i = 0
        # 把tac表保存到outputTAC.txt文件中
        fp = open("outputTAC.txt", "w")
        for tac in tac.tacTable.tacTable:
            self.output_listbox.insert(tk.END, f"({i}){str(tac)}")
            fp.write(f"({i}){str(tac)}\n")
            i = i + 1
        self.output_listbox.insert(tk.END, 'tac完成!!!')
    def btn_3(self):
        # source_code = self.input_text.get("1.0", tk.END).strip() + "#"
        # parser = compiler(source_code)
        # parser_list = parser.run_parse()
        # 清空输出列表框的内容
        self.output_listbox.delete(0, tk.END)
        self.debug_listbox.delete(0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
    # code = 'string $mwc$; int $sq$; bool $j6$; bool $e11$;  $mwc$:="zdw"; $e11$:=true; $j6$:=false; $sq$:=738; $mwc$:=$mwc$ * 2 + ($mwc$+"") * $sq$; while($mwc$ * $sq$ + "" * $sq$<"g" * 2 + "rc" * $sq$ or $e11$ and not false):{$sq$:=($sq$+34)*$sq$+$sq$ % $sq$;$mwc$:=$mwc$ * $sq$ + "f" * $sq$}; if(not false and true / $sq$*$sq$+($sq$-37) / 44+65*$sq$>= "h" * 2 + $mwc$ * $sq$ or false*41+($sq$+97) / $sq$==($sq$-98) % 48-false){$sq$:=$e11$*16+false / $sq$ / $sq$-($sq$+45)*$sq$;$mwc$:=$mwc$ * 3 + "" * 2}else$sq$:=$sq$ / 55*$sq$-($sq$+50)*$sq$;; $e11$:=61*64==($mwc$+"") * $sq$ + $mwc$ * $sq$; $sq$:=84 / 48*$sq$-($sq$-11) % 82+true % 25+($sq$+56)'
    # source_code = code + "#"
    # test = compiler(source_code)
    # test.run_parse_one()
    # for i in test.parse_list:
    #     print(i)

