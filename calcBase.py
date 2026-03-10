from genereTreeGraphviz2 import printTreeGraph

 
reserved={
        'print':'PRINT',
        'if':'IF',
        'while':'WHILE'
        }
 
tokens = [ 'NUMBER','MINUS', 'PLUS','TIMES','DIVIDE', 'LPAREN',
          'RPAREN', 'OR', 'AND', 'SEMI', 'EGAL', 'NAME', 'INF', 'SUP',
          'EGALEGAL','INFEG', 'LACC', 'RACC']+ list(reserved.values())
 
t_PLUS = r'\+' 
t_MINUS = r'-' 
t_TIMES = r'\*' 
t_DIVIDE = r'/' 
t_LPAREN = r'\(' 
t_RPAREN = r'\)' 
t_OR = r'\|'
t_AND = r'\&'
t_SEMI = r';'
t_EGAL = r'\='
#t_NAME = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_INF = r'\<'
t_SUP = r'>'
t_INFEG = r'\<\='
t_EGALEGAL = r'\=\='
t_LACC = r'{'
t_RACC = r'}'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t
 
def t_NUMBER(t): 
    r'\d+' 
    t.value = int(t.value) 
    return t
 
t_ignore = " \t"
 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 
import ply.lex as lex
lex.lex()
names={}

def evalInst(t) :

    print('evalInst de ', t)
    if t == 'empty' : return    

    assert type(t) is tuple 
    if t[0] == 'bloc' : 
        evalInst(t[1])
        evalInst(t[2])
    if t[0] == 'print' : print('CALC> ', evalExpr(t[1]))
    if t[0] == 'assign' : names[t[1]] = evalExpr(t[2])
    if t[0] == 'if' :
        if evalExpr(t[1]) : evalInst(t[2])
    if t[0] == 'while' :
        while evalExpr(t[1]) : evalInst(t[2])

def evalExpr(t) : #renvoie un int
    print('evalExpr de ', t)
    if type(t) is int : return t
    if type(t) is tuple :
        if t[0] == '+' : return evalExpr(t[1])+evalExpr(t[2])
        if t[0] == '*' : return eval(t[1])*eval(t[2])

precedence = ( 
        ('left','OR' ), 
        ('left','AND'), 
        ('nonassoc', 'INF', 'INFEG', 'EGALEGAL', 'SUP'), 
        ('left','PLUS', 'MINUS' ), 
        ('left','TIMES', 'DIVIDE'), 
        )

def p_start(p):
    'start : bloc'
    print(p[1])
    printTreeGraph(p[1])
    evalInst(p[1])
 
def p_bloc(p):
    '''bloc : bloc statement SEMI
    | statement SEMI'''
    if len(p)==4  : 
        p[0] = ('bloc', p[1], p[2])
    else : 
        p[0] = ('bloc', 'empty', p[1])

def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN LACC bloc RACC'
    p[0] = ('if', p[3], p[6])

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LACC bloc RACC'
    p[0] = ('while', p[3], p[6])


def p_statement_expr(p): 
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = ('print', p[3])
    #print(p[3]) 
 
def p_statement_assign(p):
    'statement : NAME EGAL expression'
    #names[p[1]]=p[3]
    #print(p[1], 'a été modifié')
    p[0] = ('assign', p[1], p[3])
 
def p_expression_binop_inf(p): 
    'expression : expression INF expression' 
    p[0] = p[1] < p[3] 
 
def p_expression_binop_infEGAL(p): 
    'expression : expression INFEG expression' 
    p[0] = p[1] <= p[3]
 
def p_expression_binop_sup(p): 
    'expression : expression SUP expression' 
    p[0] = p[1] > p[3] 
 
def p_expression_binop_egal(p): 
    'expression : expression EGALEGAL expression' 
    p[0] = p[1] == p[3] 
 
def p_expression_binop_and(p): 
    'expression : expression AND expression' 
    p[0] = p[1] and p[3] 
 
def p_expression_binop_or(p): 
    'expression : expression OR expression' 
    p[0] = p[1] or p[3]
 
def p_expression_binop_plus(p): 
    'expression : expression PLUS expression' 
    #p[0] = p[1] + p[3] 
    p[0] = ('+', p[1], p[3])
 
def p_expression_binop_times(p): 
    'expression : expression TIMES expression' 
    #p[0] = p[1] * p[3] 
    p[0] = ('*', p[1], p[3])
 
def p_expression_binop_divide_and_minus(p): 
    '''expression : expression MINUS expression 
     | expression DIVIDE expression''' 
    if p[2] == '-': p[0] = p[1] - p[3] 
    else : p[0] = p[1] / p[3] 
 
def p_expression_group(p): 
    'expression : LPAREN expression RPAREN' 
    p[0] = p[2] 
 
def p_expression_number(p): 
    'expression : NUMBER' 
    p[0] = p[1] 
 
def p_expression_name(p): 
    'expression : NAME' 
    #p[0] = names[p[1]]
    p[0] = p[1]
 
def p_error(p):    print("Syntax error in input!")
 
import ply.yacc as yacc
yacc.yacc()
s = 'if(1<2){print(5+5);};print(5+5);'
yacc.parse(s)