import sys

class Token():
    def __init__(self, type, valeur, position):
        self.type = type
        self.valeur = valeur
        self.position = position

    def __repr__(self):
        print(f"Type : {self.type}, Valeur : {self.valeur}, Position : {self.position}")


# MAIN
## Lecture de fichier
src = sys.argv[1]
dest = sys.argv[2]
position = 0
ligne = 0

with open(src) as file:
    string = file.readlines()
    string = "".join(string)

def next():
    global string
    global position
    global ligne

    char =  string[position]

    if char == '\n':
        ligne+=1
        position+=1
        return next()
    elif char == ' ' or char == '\t' or char == '\r':
        position+=1
        return next()
    elif char == '(':
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
        ##
        pass
    elif char == '>':
        ##
        pass
    elif char == '<':
        ##
        pass
    elif char == '!':
        ##
        pass
    elif char == '=':
        ##
        pass
    elif char == '|':
        ## (un seul = erreur)
        pass
    elif char == ';':
        pass
    elif char == ',':
        pass
    else:
        # MOTS CLES
        if ord('z') >= ord(char.lower()) >= ord('a'):
            ## while toussa
            ## NE PAS OUBLIER RETURN IF ETC
            pass
        elif char.isdigit():
            ## while toussa
            pass


    # Verif

## Tings
courant = None
precedant = None

n = next()
while n.type != "EOS":
    precedant = courant
    courant = n
    print(courant)
    


