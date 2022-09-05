import sys
from webbrowser import Opera

class Token():
    def __init__(self, type, valeur, position):
        self.type = type
        self.valeur = valeur
        self.position = position

    def __repr__(self):
        return (f"Type : {self.type}, Valeur : {self.valeur}, Ligne : {self.position}")

class Node:
    def __init__(self, type, valeur, ligne, children = None):
        self.type = type
        self.valeur = valeur
        self.ligne = ligne
        if children == None:
            self.children = []
        else:
            self.children = children

    
    def add_child(self, child):
        self.children.append(child)

class Operation:
    def __init__(self, prio, noeud, AG):
        self.prio = prio
        self.noeud = noeud
        self.AG = AG

# Le compilo
## Lecture de fichier
src = sys.argv[1]
dest = sys.argv[2]
position = 0
ligne = 0

with open(src) as file:
    string = file.readlines()
    string = "".join(string)

## Analyse linguistique
def next():
    global string
    global position
    global ligne

    global courant
    global precedant

    if position >= len(string):
        token = Token("EOS", None, ligne)
        precedant = courant
        courant = token

        print(courant)
        return
    
    char =  string[position]
    token = None

    if char == '\n':
        ligne+=1
        position+=1
        return next()
    elif char == ' ' or char == '\t' or char == '\r':
        position+=1
        return next()
    
    if char == '(':
        position += 1
        token = Token("po", None, ligne)
    elif char == ')':
        position += 1
        token = Token("pf", None, ligne)
    elif char == '{':
        position += 1
        token = Token("ao", None, ligne)
    elif char == '}':
        position += 1
        token = Token("af", None, ligne)
    elif char == '[':
        position += 1
        token = Token("co", None, ligne)
    elif char == ']':
        position += 1
        token = Token("cf", None, ligne)
    elif char == '+':
        position += 1
        token = Token("add", None, ligne)
    elif char == '-':
        position += 1
        token = Token("sub", None, ligne)
    elif char == '*':
        position += 1
        token = Token("star", None, ligne)
    elif char == '/':
        position += 1
        token = Token("div", None, ligne)
    elif char == '%':
        position += 1
        token = Token("mod", None, ligne)
    elif char == '&':
        if string[position+1] == '&':
            position+=2
            token = Token("and", None, ligne)
        else:
            position+=1
            token = Token("esper", None, ligne)
    elif char == '>':
        ## TODO
        pass
    elif char == '<':
        ## TODO
        pass
    elif char == '!':
        position+=1
        token = Token("neglog", None, ligne)

        if position < len(string):
            if string[position] == "=":
                position+=1
                token = Token("notequal", None, ligne)
    elif char == '=':
        position+=1
        token = Token("assign", None, ligne)
        if position < len(string):
            if string[position]:
                position+=1
                token = Token("equal", None, ligne)
    elif char == '|':
        position+=1
        if position < len(string):
            if string[position] == '|':
                position+=1
                token = Token("or", None, ligne)
            else:
                error()
        else:
            error()
            
    elif char == ';':
        position += 1
        token = Token("pvirg", None, ligne)
    elif char == ',':
        position += 1
        token = Token("virg", None, ligne)
    else:
        # MOTS CLES
        if ord('z') >= ord(char.lower()) >= ord('a'):
            s = "" + char
            position+=1
            if position < len(string):
                char = string[position]
                while ord('z') >= ord(char.lower())  >= ord('a'):
                    s+= char
                    position+=1
                    if position < len(string):
                        char=string[position]
                    else:
                        break
                if s == "return":
                    token = Token("return", None, ligne)
                elif s == "if":
                    token = Token("if", None, ligne)
                elif s == "else":
                    token = Token("else", None, ligne)
                elif s == "for":
                    token = Token("for", None, ligne)
                elif s == "while":
                    token = Token("while", None, ligne)
                elif s == "do":
                    token = Token("do", None, ligne)
                elif s == "int":
                    token = Token("int", None, ligne)
                elif s == "break":
                    token = Token("break", None, ligne)
                elif s == "continue":
                    token = Token("continue", None, ligne)
                else:
                    token = Token("var", s, ligne)           
            else:
                token = Token("var", s, ligne)
                
        elif char.isdigit():
            s = "" + char
            position+=1
            if position < len(string):
                char = string[position]
                while char.isdigit():
                    s+= char
                    position+=1
                    if position < len(string):
                        char=string[position]
                    else:
                        break
                token = Token("const", s, ligne)
            else:
                token = Token("const", s, None)
    
    ## Verif Erreurs
    if token == None:
        error()

    ## Return
    precedant = courant
    courant = token

    print(courant)

## Analyse Synthaxique

def G():
    return F()

def F():
    return I()

def I(): 
    return E()

def E(pmin = 0):
    global courant
    
    table = {
        "add": Operation(5, "nd_add", 1),
        "sub": Operation(5, "nd_sub", 1),
        "star": Operation(6, "nd_mul", 1),
        "div": Operation(6, "nd_div", 1),
        "mod": Operation(6, "nd_mod", 1),
        "equal": Operation(3, "nd_set", 0)
    }

    A1 = P()
    while(courant.type in table):
        op = courant.type
        if table[op].prio >= pmin:
            next()
            A2 = E(table[op].prio + table[op].AG)
            A = Node(table[op].noeud, None, precedant.position)
            A.add_child(A1)
            A.add_child(A2)
            A1 = A
        else: 
            break
    return A1

def P():
    if check('sub'): 
        N = P()
        M = Node('nd_neg', None, courant.position)
        M.add_child(N)
        return M
    elif check('add'):
        return P()
    elif check('neglog'):
        N = P()
        M = Node('nd_neglog', None, courant.position)
        M.add_child(N)
        return M
    else:
        return S()

def S():
    return A()

def A():
    if check("const"):
        return Node('const', precedant.valeur, precedant.position) 
    elif check("po"):
        N = E()
        accept('pf')
        return N
    else:
        error()

def error():
    # TODO
    # Faire une fonction erreur
    print("ERROR OMG OMG OMG !!!")

def check(type):
    global courant
    global precedant

    if (courant.type == type):
        next()
        return True
    else:
        return False

def accept(type):
    if not check(type):
        error()

def AS():
    # G (le plus général, englobe les fonctions et plein de trucs qu'on utilise pas) = F *  (L'étoile signifie qu'on peut en avoir autant qu'on veut, mais on l'ignore pour l'instant)
    # F (une fonction) = I
    # I (une instruction) = E
    # E (une expression) =  P + E | P
    # P (pour prefixe)= -P | +P | !P | S
    # S (pour suffixe)= A
    # A (pour Atome) = Constante | ( E )
    return G()

## Analyse Sementique
def ASe():
    return AS()

## Generation de Code
def Gc():
    Node = ASe()
    global outtxt 
    outtxt = f".start\n{GenNode(Node)} \ndbg \nhalt"

def GenNode(Node):
    match Node.type:
        case "const":
            return f"push {Node.valeur}"
        case "nd_add":
            return f"{GenNode(Node.children[0])}\n{GenNode(Node.children[1])}\nadd"
        case "nd_sub":
            return f"{GenNode(Node.children[0])}\n{GenNode(Node.children[1])}\nsub"
        case "nd_mul":
            return f"{GenNode(Node.children[0])}\n{GenNode(Node.children[1])}\nmul"
        case "nd_div":
            return f"{GenNode(Node.children[0])}\n{GenNode(Node.children[1])}\ndiv"
        case "nd_mod":
            return f"{GenNode(Node.children[0])}\n{GenNode(Node.children[1])}\nmod"
        case "nd_equal":
            return f"{GenNode(Node.children[0])}\n{GenNode(Node.children[1])}\nERROR"
        case "nd_neg":
            return f"push 0\n{GenNode(Node.children[0])}\nsub"

# Main
courant = None
precedant = None

next()
Gc()

# Ecriture de fichier

print(outtxt)

with open("out.txt", "w") as out:
    out.write(outtxt)