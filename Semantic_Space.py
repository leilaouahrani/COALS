import codecs as c
import math as m
import io
import os
import sys

# entree : le dossier qui contient le corpus(les fichiers texts)
entree= sys.argv[1]

# sortie : le dossier la ou vous voulez sauvegarder votre espace semantique
sortie= sys.argv[2]


# Fonction Lecture permet de lire le corpus fichier par ficher
# Et les regroupe dans un seul fichier text qui est corpus_stemmee
def lecture(corpus):
    ALL_corpus = []
    ss = os.listdir(corpus)
    for i in ss:
        r = corpus + "//" + i
        with c.open(r, "r", encoding="utf-8")as file:
            tt = file.read()

        txt = tt.split()
        txt2 = ' '.join(w for w in txt)
        ALL_corpus.append(txt2)
    txt3 = ' '.join(i for i in ALL_corpus)
    with io.open("corpus_stemmee.txt", 'w', encoding="utf-8") as f:
        f.write(txt3)
    return txt3


def poid(txt):
    WORDS = txt.split()

    NWORDS=[]
    for i in range(len(WORDS)):
        if WORDS[i] not in NWORDS:
            NWORDS.append(WORDS[i])

    # Sauvegarder Words dans un fichier txt
    with io.open("Words.txt", 'w',encoding="utf-8") as f:
        for i in range(len(NWORDS)-1):
            f.write(NWORDS[i]+"\n")
        f.write(NWORDS[len(NWORDS)-1])		

    # Declaration de la matrice de poids -Matrice Initiale FREQ
    FREQ = [[0 for j in range(0,len(NWORDS))] for FREQ in range(0,len(NWORDS))]

    # Calcul des poids entre pair de mot en utilisant -Ramped size 4 window- ( notion de voisinage
    for i in range(len(WORDS)):

        if i < len(WORDS)-4:
            for f in range(1,5):
                FREQ[NWORDS.index(WORDS[i])][NWORDS.index(WORDS[i+f])] += (5-f)

        elif i < len(WORDS)-3:
            for f in range(1,4):
                FREQ[NWORDS.index(WORDS[i])][NWORDS.index(WORDS[i+f])] += (5-f)


        elif i < len(WORDS)-2:
            for f in range(1,3):
                FREQ[NWORDS.index(WORDS[i])][NWORDS.index(WORDS[i+f])] += (5-f)


        elif i < len(WORDS)-1:
            FREQ[NWORDS.index(WORDS[i])][NWORDS.index(WORDS[i+1])] += 4

        if i >= 4:
            for f in range(1,5):
                FREQ[NWORDS.index(WORDS[i])][NWORDS.index(WORDS[i-f])] += (5-f)

        elif i >= 3:
            for f in range(1,4):
                FREQ[NWORDS.index(WORDS[i])][NWORDS.index(WORDS[i-f])] += (5-f)


        elif i >= 2:
            for f in range(1,3):
                FREQ[NWORDS.index(WORDS[i])][NWORDS.index(WORDS[i-f])] += (5-f)

        elif i >= 1:
            FREQ[NWORDS.index(WORDS[i])][NWORDS.index(WORDS[i-1])] += 4

    # Affichage de la matrice de poids
    # print("la matrice de co-occurence")
    # for i in range(len(FREQ)) :
    # print (FREQ[i])
    return FREQ,NWORDS


def corr(FREQ,NWORDS):
    som = 0      # somme des element de la matrice de poids
    for i in range(len(NWORDS)):
        for j in range(len(NWORDS)):
            som += FREQ[i][j]

    # v contient la somme des colonne pour chaque ligne (respectivement colonne car elle est symetrique )
    v = [0 for i in range(len(FREQ))]
    for i in range(len(FREQ)):
        for j in range(len(FREQ)):
            v[i] += FREQ[i][j]

    # Calcul et affichage de la matrice de correlation
    # print("la matrice de correlation")
    for i in range(len(FREQ)):
        for j in range(len(FREQ)):
            FREQ[i][j] = round(((som * FREQ[i][j])-(v[i] * v[j])) / m.sqrt(v[i] * (som-v[i]) * v[j] * (som-v[j])),3)
        # print ( FREQ[i])

    # Normalisation de la matrice de correlation
    for i in range(len(FREQ)):
        for j in range(len(FREQ)):
            if FREQ[i][j] > 0:
                FREQ[i][j] = round(m.sqrt(FREQ[i][j]),3)
            else:
                FREQ[i][j] = 0


    # print("la matrice de correlation normalise")
    # for g in range (len(FREQ)):

        # print (FREQ[g])

    return FREQ

def save(FREQ):
    
    with io.open("%s/SemanticSpace.txt"%(sortie),"w",encoding="utf-8")as f:
        for i in range(len(FREQ)):
            for j in range(len(FREQ)):
                f.write(str(FREQ[i][j])+" ")
            f.write('\n')

#read_files = glob.glob("%s/*.txt" %(param_1))
Corpus=lecture(entree)
ES,NWORDS=poid(Corpus)
ES=corr(ES,NWORDS)

save(ES)