from genereTreeGraphviz2 import printTreeGraph

 
reserved={
        'print':'PRINT',
        'if':'IF',
        'else':'ELSE',
        'while':'WHILE',
        'for':'FOR',
        #'def' : 'DEF',
        #'call' : 'CALL',
        'fonctionValue' : 'FONCTIONVALUE',
        'return' : 'RETURN'
        }
 
tokens = [ 'NUMBER','MINUS', 'PLUS','TIMES','DIVIDE', 'LPAREN',
          'RPAREN', 'OR', 'AND', 'SEMI', 'EGAL', 'NAME', 'INF', 'SUP',
          'EGALEGAL','INFEG', 'LACC', 'RACC', 'PLUSEGAL', 'PLUSPLUS','COLON', 'STRING', 'LBRACK', 'RBRACK']+ list(reserved.values())
 
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
t_PLUSEGAL = r'\+='
t_PLUSPLUS = r'\+\+'
#t_NAME = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_INF = r'\<'
t_SUP = r'>'
t_INFEG = r'\<\='
t_EGALEGAL = r'\=\='
t_LACC = r'{'
t_RACC = r'}'
t_COLON = r','
t_LBRACK = r'\[' 
t_RBRACK = r'\]'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t
 
def t_NUMBER(t): 
    r'\d+' 
    t.value = int(t.value) 
    return t

def t_COMMENTAIRE(t):
    r'\#.*'

def t_STRING(t):
    r'\"[^\"]*\"' #Recherche d'une chaine entre " "
    t.value = t.value[1:-1] #Supp les guillemets
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
fonctions={}

def evalInst(t) :

    print('evalInst de ', t)
    if t == 'empty' : return    

    assert type(t) is tuple 
    if t[0] == 'bloc' :                                     #Bloc
        evalInst(t[1])
        evalInst(t[2])
    if t[0] == 'print' : print('CALC> ', evalExpr(t[1]))    #Print
    #if t[0] == 'call' : fonctions = evalExpr(t[2])
    if t[0] == 'assign' : names[t[1]] = evalExpr(t[2])      #Assign
    if t[0] == 'if' :                                       #If
        if evalExpr(t[1]) : evalInst(t[2])
    if t[0] == 'else':                                      #Else
        if evalExpr(t[1]) : evalInst(t[2])
        else: 
            evalInst(t[3]) 
    if t[0] == 'while' :                                    #While
        while evalExpr(t[1]) : evalInst(t[2])
    if t[0] == 'for' :                                      #For
        evalInst(t[1])
        while evalExpr(t[2]) :
            evalInst(t[4])
            evalInst(t[3])
    if t[0] == 'def' :
        fonctions[t[1]] = (t[2], t[3], t[4]) #stockage de la fonction dans un dictionnaire 
    if t[0] == 'call':
        #evalExpr(t)
        print('CALC>', evalExpr(t))
    if t[0] == 'return' :
        names['_return_value'] = evalExpr(t[1]) #permet de stckoer la valeur dans une variable pour l'utiliser apres
    if t[0] == 'init_tab' :
        nomTab = t[1]
        taille = evalExpr(t[2])
        valeurInit = evalExpr(t[3])
        names[nomTab] = [valeurInit] * taille 
    if t[0] == 'assign_tab' :
        nomTab = t[1]
        index = evalExpr(t[2])
        valeur = evalExpr(t[3])
        names[nomTab][index] = valeur


def evalExpr(t) : #renvoie un int
    print('evalExpr de ', t)
    if type(t) is int : return t
    if type(t) is str : return names.get(t, 0)
    if type(t) is tuple :
        if t[0] == '+' : return evalExpr(t[1])+evalExpr(t[2])           #Addition
        if t[0] == '*' : return evalExpr(t[1])*evalExpr(t[2])           #Multiplication
        if t[0] == '-' : return evalExpr(t[1])-evalExpr(t[2])           #Soustraction
        if t[0] == '/' : return evalExpr(t[1])/evalExpr(t[2])           #Division
        if t[0] == '<' : return evalExpr(t[1]) < evalExpr(t[2])         #Inférieur à 
        if t[0] == '<=' : return evalExpr(t[1]) <= evalExpr(t[2])       #Inférieur ou égal à
        if t[0] == '>' : return evalExpr(t[1]) > evalExpr(t[2])         #Supérieur à
        if t[0] == '==' : return evalExpr(t[1]) == evalExpr(t[2])       #Égal à 
        if t[0] == 'and' : return evalExpr(t[1]) and evalExpr(t[2])     #Et
        if t[0] == 'or' : return evalExpr(t[1]) or evalExpr(t[2])       #Ou
        if t[0] == 'call' :    
            nom_fonction = t[1]
            if nom_fonction in fonctions :
                param1, param2, bloc = fonctions[nom_fonction]

                #val1 = evalExpr(t[2]) #calcul des paramètres
                #val2 = evalExpr(t[3])

                names[param1] = evalExpr(t[2]) 
                names[param2] = evalExpr(t[3])

                #names['_return_value'] = None #initialisation de la variable de retour
                names[nom_fonction] = None

                evalInst(bloc) 

                #return names['_return_value'] 
                return names[nom_fonction]
        if t[0] == 'access_tab' :
            nomTab = t[1]
            index = evalExpr(t[2])
            return names[nomTab][index]

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
    'statement : IF LPAREN expression RPAREN LACC bloc RACC' #IF
    p[0] = ('if', p[3], p[6])
    
def p_statement_else(p):
    'statement : IF LPAREN expression RPAREN LACC bloc RACC ELSE LACC bloc RACC' #ELSE
    p[0] = ('else', p[3], p[6], p[10])

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LACC bloc RACC' #WHILE
    p[0] = ('while', p[3], p[6])
    
def p_statement_for(p):
    'statement : FOR LPAREN statement SEMI expression SEMI statement RPAREN LACC bloc RACC' #FOR
    p[0] = ('for', p[3], p[5], p[7], p[10])

def p_statement_plus_egal(p):
    'statement : NAME PLUSEGAL expression'          #+=
    p[0] = ('assign', p[1], ('+', p[1], p[3]))

def p_statement_plus_plus(p):
    'statement : NAME PLUSPLUS'                     #++  
    p[0] = ('assign', p[1], ('+', p[1], 1))
    
#def p_statement_def_fonction(p):
 #   'statement : DEF NAME LPAREN expression RPAREN'
  #  p[0] = p[2] + p[3]
    
#def p_statement_call_fonction(p):
#    'statement : CALL NAME'

def p_statement_retrun(p):
    'statement : RETURN expression'
    p[0] = ('return', p[2]) 

def p_statement_def_fonction_explicite(p):
    'statement : FONCTIONVALUE NAME LPAREN NAME COLON NAME RPAREN LACC bloc RACC'
    p[0] = ('def', p[2], p[4], p[6], p[9])

def p_expression_call_fonction_explicite(p):
    'expression : NAME LPAREN expression COLON expression RPAREN'
    p[0] = ('call', p[1], p[3], p[5])

def p_statement_expr_seul(p):  #Permet de continuer ou avoir une expr 
    'statement : expression SEMI'
    p[0] = p[1]
    
    
def p_statement_init_tab(p): #Initialisation de la tab
    'statement : NAME LBRACK RBRACK EGAL LBRACK expression SEMI expression RBRACK'
    p[0] = ('init_tab', p[1], p[6], p[8])

def p_statement_assign_tab(p): #Modif de la tab
    'statement : NAME LBRACK expression RBRACK EGAL expression'
    p[0] = ('assign_tab', p[1], p[3], p[6])

def p_expression_tab_access(p): #Lecture de la tab
    'expression : NAME LBRACK expression RBRACK'
    p[0] = ('access_tab', p[1], p[3])

def p_statement_expr(p): 
    'statement : PRINT LPAREN expression RPAREN' #Print Expression
    p[0] = ('print', p[3])
    #print(p[3]) 
 
def p_statement_assign(p):
    'statement : NAME EGAL expression' #Assign
    #names[p[1]]=p[3]
    #print(p[1], 'a été modifié')
    p[0] = ('assign', p[1], p[3])
 
def p_expression_binop_inf(p): 
    'expression : expression INF expression' #Inférieur à
    #p[0] = p[1] < p[3]
    p[0] = ('<', p[1], p[3])

def p_expression_string(p):           #Utilisation des chaînes de caractères
    'expression : STRING' 
    p[0] = p[1]
 
def p_expression_binop_infEGAL(p): 
    'expression : expression INFEG expression' #Inférieur ou égal à
    #p[0] = p[1] <= p[3]
    p[0] = ('<=', p[1], p[3])
 
def p_expression_binop_sup(p): 
    'expression : expression SUP expression' #Supérieur à
    #p[0] = p[1] > p[3] 
    p[0] = ('>', p[1], p[3]) 
 
def p_expression_binop_egal(p): 
    'expression : expression EGALEGAL expression' #Égal à
    #p[0] = p[1] == p[3] 
    p[0] = ('==', p[1], p[3]) 
 
def p_expression_binop_and(p): 
    'expression : expression AND expression' #Et
    #p[0] = p[1] and p[3] 
    p[0] = ('and', p[1], p[3])
 
def p_expression_binop_or(p): 
    'expression : expression OR expression' #Ou
    #p[0] = p[1] or p[3]
    p[0] = ('or', p[1], p[3])
 
def p_expression_binop_plus(p): 
    'expression : expression PLUS expression' #Addition
    #p[0] = p[1] + p[3] 
    p[0] = ('+', p[1], p[3])
 
def p_expression_binop_times(p): 
    'expression : expression TIMES expression' #Multiplication
    #p[0] = p[1] * p[3] 
    p[0] = ('*', p[1], p[3])
 
def p_expression_binop_divide_and_minus(p): #Division et Soustraction
    '''expression : expression MINUS expression 
     | expression DIVIDE expression''' 
    #if p[2] == '-': p[0] = p[1] - p[3] 
    #else : p[0] = p[1] / p[3] 
    if p[2] == '-': p[0] = ('-', p[1], p[3]) 
    else : p[0] = ('/', p[1], p[3])
 
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
s = 'scores[] = [3 ; 0] ;print(scores[1]) ;'

yacc.parse(s)