from re import M
import sys
from tkinter import N
from webbrowser import Opera

class Token:
    def __init__(self, type, valeur, position):
        self.type = type
        self.valeur = valeur
        self.position = position

    def __repr__(self):
        return (f"Type : {self.type}, Valeur : {self.valeur}, Ligne : {self.position}")

class Node:
    def __init__(self, type, valeur, ligne, adr = None, children = None):
        self.type = type
        self.valeur = valeur
        self.ligne = ligne
        self.adr = adr

        if children == None:
            self.children = []
        else:
            self.children = children

    def __repr__(self) -> str:
        return f"Type : {self.type}, Valeur : {self.valeur}, Ligne : {self.ligne}, Adresse : {self.adr}, Enfants :" + "".join([n.type for n in self.children])
    
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
        if string[position+1] == "=":
            position+=2
            token = Token("sup_equal", None, ligne)
        else:
            position+=1
            token = Token("sup", None, ligne)
    elif char == '<':
        if string[position+1] == "=":
            position+=2
            token = Token("inf_equal", None, ligne)
        else:
            position+=1
            token = Token("inf", None, ligne)
    elif char == '!':
        if string[position+1] == "=":
            position+=2
            token = Token("notequal", None, ligne)
        else:
            position+=1
            token = Token("neglog", None, ligne)
    elif char == '=':

        if string[position+1] ==  '=':
            position+=2
            token = Token("equal", None, ligne)
        else:
            position+=1
            token = Token("affect", None, ligne)
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
        if ord('z') >= ord(char.lower()) >= ord('a') or char == "_":
            s = "" + char
            position+=1
            if position < len(string):
                char = string[position]
                while ord('z') >= ord(char.lower())  >= ord('a') or char.isdigit() or char == "_":
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
                elif s == "send":
                    token = Token("send", None, ligne)
                elif s == "recv":
                    token = Token("recv", None, ligne)
                else:
                    token = Token("ident", s, ligne)           
            else:
                token = Token("ident", s, ligne)
                
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

def AS():
    # G (le plus général, englobe les fonctions et plein de trucs qu'on utilise pas)
    # F (une fonction)
    # I (une instruction)
    # E (une expression)
    # P (pour prefixe)
    # S (pour suffixe)
    # A (pour Atome)
    return G()

def G():
    return F()

def F():
    accept('int')
    accept('ident')
    
    N = Node("nd_func", precedant.valeur, precedant.position)
    N.add_child(Node("nd_decl", None, precedant.position))

    accept("po")

    if check("int"):
        accept("ident")
        N.children[0].add_child(Node("nd_arg", precedant.valeur, precedant.position))

        while check('virg'):
            accept("int")
            accept("ident")
            N.children[0].add_child(Node("nd_arg", precedant.valeur, precedant.position))

    accept("pf")
    instr = I()

    N.add_child(instr)

    return N

def I(): 
    # check if
    if check('if'):
        accept('po')
        test = E()
        accept('pf')
        then = I()
        N = Node('nd_cond', None, precedant.position)
        N.add_child(test)
        N.add_child(then)
        if check('else'):
            else_ = I()
            N.add_child(else_)
        return N
    elif check('ao'):
        N = Node('nd_block', None, precedant.position)
        while not check('af'):
            N.add_child(I())
        return N
    elif check('int'):
        decl = Node("nd_decl", None, precedant.position)
        while check("star"):    # On se debarasse des etoiles
            pass
        accept("ident")
        decl.add_child(Node("nd_var", precedant.valeur, precedant.position))
        while not check('pvirg'):
            accept('virg')
            while check("star"): # On se debarasse des etoiles
                pass
            accept('ident')
            decl.add_child(Node("nd_var", precedant.valeur, precedant.position))
        return decl
    elif check('while'):
        accept('po')
        test = E()
        accept('pf')
        instr = I()
        l = Node('nd_loop', None, precedant.position)
        cond = Node('nd_cond', None, precedant.position)
        cond.add_child(test)
        cond.add_child(instr)
        cond.add_child(Node('nd_break', None, precedant.position))
        l.add_child(cond)
        return l
    elif check('do'):
        instr = I()
        accept('while')
        accept('po')
        test = E()
        accept('pf')
        accept('pvirg')

        l = Node('nd_loop', None, precedant.position)
        l.add_child(instr)
        cond = Node('nd_cond', None, precedant.position)
        not_ = Node('nd_neglog', None, precedant.position)
        not_.add_child(test)
        cond.add_child(not_)
        cond.add_child(Node('nd_break', None, precedant.position))

        return l
    elif check('for'):
        accept('po')
        init = E()
        accept('pvirg')
        test = E()
        accept('pvirg')
        next = E()
        accept('po')

        instr = I()

        seq = Node('nd_seq', None, precedant.position)
        seq.add_child(init)
        l = Node('nd_loop', None, precedant.position)
        seq.add_child(l)

        l.add_child(instr)
        l.add_child(next)
        
        cond = Node('nd_cond', None, precedant.position)

        not_ = Node('nd_neglog', None, precedant.position)
        not_.add_child(test)
        cond.add_child(not_)
        cond.add_child(Node('nd_break', None, precedant.position))
        
        l.add_child(cond)

        return l
    elif check("return"):
        N = Node("nd_return", None, precedant.position)
        N.add_child(E())
        accept("pvirg")
        return N
    elif check("send"):
        sendNode = Node("nd_send", None, precedant.position)
        sendNode.add_child(E())
        accept("pvirg")
        return sendNode
    else:
        N = Node('nd_drop', None, courant.position)
        N.add_child(E())
        accept('pvirg')
        return N

def E(pmin = 0):
    global courant
    
    table = {
        "add": Operation(5, "nd_add", 1),
        "sub": Operation(5, "nd_sub", 1),
        "star": Operation(6, "nd_mul", 1),
        "div": Operation(6, "nd_div", 1),
        "mod": Operation(6, "nd_mod", 1),
        "affect": Operation(3, "nd_affect", 0),
        "equal": Operation(4, "nd_equal", 1),
        "sup": Operation(4, "nd_sup", 1),
        "sup_equal": Operation(4, "nd_sup_equal", 1),
        "inf": Operation(4, "nd_inf", 1),
        "inf_equal": Operation(4, "nd_inf_equal", 1),
        "notequal": Operation(4, "nd_not_equal", 1)
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

            if A.type == "nd_affect":
                print(f"E1 : {A1.type}, E2 : {A2.type} \n")

            A1 = A
        else: 
            break
    return A1

def P():
    if check('sub'): 
        N = P()
        M = Node('nd_neg', None, precedant.position)
        M.add_child(N)
        return M
    elif check('add'):
        return P()
    elif check('neglog'):
        N = P()
        M = Node('nd_neglog', None, precedant.position)
        M.add_child(N)
        return M
    elif check('star'):
        N = Node("nd_indir", None, precedant.position)
        N.add_child(P())
        return N
    elif check("esper"):
        N = Node("nd_adr", None, precedant.position)
        N.add_child(P())
        return N
    else:
        return S()

def S():
    r = A()
    while check('co'):
        indir = Node('nd_indir', None, precedant.position)
        indir.add_child(Node('nd_add', None, precedant.position))
        e = E()
        indir.children[0].add_child(r)
        indir.children[0].add_child(e)
        r = indir
        accept('cf')
    return r


class Symbol():
    def __init__(bashboush, ident=None, type="sym_var", adr=None):
        bashboush.ident = ident
        bashboush.type = type
        bashboush.adr = adr

    def __repr__(self) -> str:
        return f"Ident : {self.ident}, Type : {self.type}, Adr : {self.adr}\n"

def A():
    if check("const"):
        return Node('const', precedant.valeur, precedant.position) 
    elif check("po"):
        N = E()
        accept('pf')
        return N
    elif check("recv"):
        return Node("recv", None, precedant.ligne)
    elif check("ident"):
        name = precedant.valeur
        N = Node('nd_call', name, precedant.position)
        if check("po"):     # Appel de fonctions, call
            if check("pf"):
                return N
            else:
                N.add_child(E())
                while check('virg'):
                    N.add_child(E())
                accept('pf')
                return N          
        else:
            return Node('nd_var', precedant.valeur, precedant.position)
    else:
        error(f"Erreur reconnaissance Atome ici : {precedant.position}")

class CompilationException(Exception):
    pass

def error(msg = "ERROR OMG OMG OMG !!!", l=""):
    raise CompilationException(msg+f"l.{l}" if l != "" else msg)

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

## Analyse Sementique
nbvar = 0
def ASe():
    N = AS()
    global nbvar        # On choisit de ne pas mettre nbvar dans le noeud fonction, on a mis le nom à la place
    nbvar = 0
    ASeNode(N)
    return N

def ASeNode(N):
    global nbvar
    match(N.type):
        case "nd_block":
            start_block()
            for child in N.children:
                ASeNode(child)
            end_block()
        case "nd_var":
            N.adr = find(N.valeur).adr
        case "nd_decl":
            for child in N.children:
                s= declare(child)
                child.adr = s.adr
        case "nd_affect":
            if N.children[0].type != "nd_var" and N.children[0].type != "nd_indir":
                error("Affectation à un truc pas affectable.")
            for child in N.children:
                ASeNode(child)
        case "nd_func":
            s = declare(N)
            s.type = "fonction"
            start_block()
            for child in N.children:
                ASeNode(child)
            nbvar = nbvar - len(N.children[0].children)
            end_block()
        case "nd_call":
            s = find(N.valeur)
            if s.type != "fonction":
                error("Erreur : A essaye d'appeler autre chose qu'une fonction !")  
        case "nd_adr":
            if (N.children[0].type != "nd_var"):
                error("Erreur : Une variable est attendue ! l.",N.ligne)
            ASeNode(N.children[0])
        case _:
            for child in N.children:
                ASeNode(child)

pile = [{}]

def start_block():
    global pile
    pile.append({})

def end_block():
    global pile
    pile.pop()

def find(ident):
    # Faire retourner un Symbole
    global pile

    for scope in pile[::-1]:
        if ident in scope:
            return scope[ident]
    error("Erreur : Variable inconnue/pas dans le scope")

def declare(c):
    global nbvar
    global pile

    if c.valeur in pile[-1]:
        error("Variable deja déclaree")
    
    print(f"\nDeclaring {c.valeur}... Done !\n")
    s = Symbol(c.valeur, "sym_var", nbvar)
    pile[-1][c.valeur] = s
    nbvar += 1

    print(pile)
    return s


## Generation de Code
def Gc():
    global outtxt 
    global nbvar
    
    outtxt = ""

    while True:
        N = ASe()
        outtxt += GenNode(N)
        if courant.type == "EOS":
            break

    outtxt += "\n;RUNTIME\n"

    outtxt += ".adrof \nget -1\nget 0 \nsub \npush 1 \nsub \nret\n"

    outtxt += ";RUNTIME\n\n"
    outtxt += ".start\nprep main\ncall 0\ndbg \nhalt"

label = 0
label_break = 0

def GenNode(N):
    global label
    global label_break
    match N.type:
        case "const":
            return f"push {N.valeur}\n"
        case "nd_add":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}add\n"
        case "nd_sub":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}sub\n"
        case "nd_mul":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}mul\n"
        case "nd_div":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}div\n"
        case "nd_mod":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}mod\n"
        # case "nd_equal":
        #     return f"{GenNode(N.children[0])}{GenNode(N.children[1])}ERROR\n"
        case "nd_neg":
            return f"push 0\n{GenNode(N.children[0])}sub\n"
        case "nd_drop":
            return f"{GenNode(N.children[0])}drop\n"
        case "nd_block":
            return "".join([f"{GenNode(child)}" for child in N.children])
        case "nd_cond":
            if len(N.children) < 3:
                N.add_child(Node(None, None, None))
            l1 = label
            l2 = label+1
            label = label+2
            s = f"{GenNode(N.children[0])}jumpf l{l1} \n{GenNode(N.children[1])}jump l{l2} \n.l{l1} \n{GenNode(N.children[2])}.l{l2}\n"
            return s
        case "nd_break":
            return f"jump l{label_break}\n"
        case "nd_return":
            return f"{GenNode(N.children[0])}ret ; DEAD CODE FROM NOW\n"
        case "nd_send":
            return f"{GenNode(N.children[0])}send \n"
        case "nd_recv":
            return "recv \n"
        case "nd_loop":
            temp = label_break
            label_break = label
            label += 1
            l1 = label
            label += 1

            s = f".l{l1} \n"
            for child in N.children:
                s += GenNode(child)
            
            s += f"jump l{l1}\n"
            s += f".l{label_break}\n"
            label_break = temp

            return s
        case "nd_decl":
            return ""
        case "nd_var":
            # TODO : A supprimer
            if N.adr is None:
                print(f"Dict : {pile}")

            return f"get {N.adr} ; {N.valeur} \n"
        case "nd_affect":
            if N.children[0].type == "nd_indir":
                return f"{GenNode(N.children[1])}dup \n{GenNode(N.children[0].children[0])}write \n"
            return f"{GenNode(N.children[1])}dup \nset {N.children[0].adr} ; {N.children[0].valeur} \n"
        case "nd_call":
            return f"prep {N.valeur} \n" + "".join([f"{GenNode(child)}" for child in N.children]) + f"call {len(N.children)}\n"
        case "nd_func":
            return f".{N.valeur} \nresn {nbvar} \n{GenNode(N.children[1])}push 0 \nret \n\n"
        case "nd_indir":
            return f"{GenNode(N.children[0])}read \n"
        case "nd_adr":
            return f"prep adrof \npush {N.children[0].adr}\ncall 1 \n"
        case "nd_sup":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}cmpgt\n"
        case "nd_sup_equal":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}cmpge\n"
        case "nd_inf":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}cmplt\n"
        case "nd_inf_equal":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}cmple\n"
        case "nd_equal":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}cmpeq\n"
        case "nd_not_equal":
            return f"{GenNode(N.children[0])}{GenNode(N.children[1])}cmpne\n"
        case _:
            return ""


# Main
courant = None
precedant = None

next()
Gc()

# Ecriture de fichier

print(outtxt)

with open(dest, "w") as out:
    out.write(outtxt)