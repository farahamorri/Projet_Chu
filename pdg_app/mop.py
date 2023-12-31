## Méthodes d'Optimisation du Planning ##

import numpy as np
import random as rd


#Variables globales pour l'exemple

nombre_de_jours = 20
nombre_medecins = 20
nombre_de_services=5
liste_med_s1 = [1,2,3,4,5]
liste_med_s2 = [4,5,6,7,8]
liste_med_s3 = [1,7,8,9,10]
liste_med_s4 = [11,12,13,14,15]
liste_med_s5 = [16,17,18,19,20]
liste_services = [liste_med_s1, liste_med_s2, liste_med_s3, liste_med_s4, liste_med_s5]
liste_medecins = np.arange(1, nombre_medecins + 1)

#remplissage aléatoire des dispo
def generate_liste_disponibilites():
    liste_disponibilites=np.zeros((2*nombre_de_services,nombre_de_jours,nombre_medecins))
    for i in range (2*nombre_de_services):
        for j in range (nombre_de_jours):
            for k in range (nombre_medecins):
                if (k+1) in liste_services[int(i/2)]:
                    r=rd.randint(0,1)
                    liste_disponibilites[i][j][k]=r
                else:
                    liste_disponibilites[i][j][k]=-1
                
    for m in range (10):
        i,j,l=rd.randint(0,2*nombre_de_services-1),rd.randint(0,nombre_de_jours-1),rd.randint(0,nombre_medecins-1)
        liste_disponibilites[i][j][l]=-1
    return liste_disponibilites

# Fonction qui prend en entrée un tableau et un indice de colonne et qui renvoie 
# True si toutes les valeurs de cette colonne sont différentes
def colonne_differentes(tableau, indice_colonne):
    colonne = tableau[:, indice_colonne]
    return np.unique(colonne).size == colonne.size

#idem sur tout le tableau
def colonnes_differentes(tableau):
    (i,j) = np.shape(tableau)
    
    # Parcours de chaque colonne
    for colonne in tableau.T:
        if np.unique(colonne).size != colonne.size:
            return False

    return True
    
##ancienne version avec liste initiale aléatoire:

# def generate_solution():
#     # initialiser un tableau de nb_services*2 lignes et 28 colonnes
#     solution = np.zeros((2*nombre_de_services, nombre_de_jours), dtype=int)
#     # remplissage du jour 1
#     P = False
#     while not P :
#         
#         for i in range (nombre_de_services) :
#             liste_med = liste_services[i]
#             solution[2*i][0] =  np.random.choice(liste_med)
#             solution[2*i +1][0] =  np.random.choice(np.setdiff1d(liste_med, [solution[2*i][0]] ))
#             
#         # Pour éviter la superposition de 2 listes de gardes
#         if colonne_differentes(solution,0) :
#             P=True 
#         
#     
#     # remplissage simultanné des services à partir du jour 2 
#     # la seule contrainte dure : on enchaîde pas 2 permanances à l'hopital
#     for j in range (1, nombre_de_jours) :
#         
#         Q = False
#         while not Q :
#             for i in range (nombre_de_services) :
#                 liste_med = liste_services[i]
#                 solution[2*i][j] =  np.random.choice(np.setdiff1d(liste_med, [solution[2*k][j-1] for k in range (nombre_de_services)]))
#                 solution[2*i +1][j] =  np.random.choice(np.setdiff1d(liste_med, [solution[2*i][j]] ))
#             
#             # Pour éviter la superposition de 2 listes de gardes
#             if colonne_differentes(solution,j) :
#                 Q=True 
#      
#             
#     return solution

# def generate_valid_solution(liste_disponibilites):
#     while True:
#         solution = generate_solution()
#         if est_valide(solution,liste_disponibilites):
#             return solution
    
    
##nouvelle version:


def generate_solution_v2(liste_disponibilites):
    liste_med_dispo=[]
    solution = np.zeros((2*nombre_de_services, nombre_de_jours), dtype=int)
#remplissage premier jour
    for i in range (nombre_de_services):
        liste_med_dispo=[]
        #garde
        liste_med=np.copy(liste_services[i])
        for k in range (len(liste_services[i])):
            x=liste_services[i][k]
            if (liste_disponibilites[2*i][0][x-1]==-1) or (x in np.transpose(solution)[0]):
                liste_med=np.delete(liste_med,np.where(liste_med==x))
        liste_med_dispo.append(liste_med)
        med=np.random.choice(liste_med)
        solution[2*i][0]=med
        #astreinte
        liste_med=np.copy(liste_services[i])
        for k in range (len(liste_services[i])):
            x=liste_services[i][k]
            if (liste_disponibilites[2*i+1][0][x-1]==-1) or (x in np.transpose(solution)[0]):
                liste_med=np.delete(liste_med,np.where(liste_med==x))
        liste_med_dispo.append(liste_med)
        med=np.random.choice(liste_med)
        solution[2*i+1][0]=med
#remplissage de la suite à partir du premier jour
    for j in range (1,nombre_de_jours):
        for i in range(nombre_de_services):
            #garde
            liste_med=np.copy(liste_services[i])
            for k in range (len(liste_services[i])):
                x=liste_services[i][k]
                if (liste_disponibilites[2*i][j][x-1]==-1) or (x in np.transpose(solution)[j]):
                    liste_med=np.delete(liste_med,np.where(liste_med==x))
                for l in range (nombre_de_services):
                    if solution[2*l][j-1]==x:
                        liste_med=np.delete(liste_med,np.where(liste_med==x))
            liste_med_dispo.append(liste_med)
            med=np.random.choice(liste_med)
            solution[2*i][j]=med
            #astreinte
            liste_med=np.copy(liste_services[i])
            for k in range (len(liste_services[i])):
                x=liste_services[i][k]
                if (liste_disponibilites[2*i+1][j][x-1]==-1) or (x in np.transpose(solution)[j]):
                    liste_med=np.delete(liste_med,np.where(liste_med==x))
            liste_med_dispo.append(liste_med)
            med=np.random.choice(liste_med)
            solution[2*i+1][j]=med
    return [solution,liste_med_dispo]

def est_valide(solution,liste_disponibilites):
    #verif qu'un medecin n'enchaine pas deux gardes
    for i in range (nombre_de_services):
        for j in range (1,nombre_de_jours):
            if solution[2*i][j]==solution[2*i][j-1]:
                return False
    
    # finalement on vérifie les indisponibilités des médecins
    
    for i in range(nombre_de_services):       
        for j in range (nombre_de_jours):
            if liste_disponibilites[2*i][j][solution[2*i][j]-1]==-1:
                return False
            elif liste_disponibilites[2*i+1][j][solution[2*i+1][j]-1]==-1:
                return False
    
    #verif qu'un medecin est affecté à une seule tache par jour 
    for i in range (nombre_de_jours):
        if len(np.unique(np.transpose(solution)[i]))!=len(np.transpose(solution)[i]):
            return False
    
    return True



def evaluate_solution(solution,liste_disponibilites):
    #Limites de validité des critères
    a=3
    p=0.5
    L=True
    #N=liste des nombres de gardes/astreintes pour chaque médecin
    #k=liste de l'insatisfaction de chaque médecin (k[i]=nb de fois que le médecin i a une tâche sur une indisponibilité noté 0)
    N=np.zeros(nombre_medecins)
    k=np.zeros(nombre_medecins)
    
    #on remplit les listes N et k 
    for i in range(nombre_de_services):
        for j in range(nombre_de_jours):
            med = solution[2*i][j]
            N[med-1]+=1
            if liste_disponibilites[2*i][j][med-1] == 0 :
                k[med-1]+=1
            med = solution[2*i+1][j]
            N[med-1]+=1
            if liste_disponibilites[2*i+1][j][med-1] == 0 :
                k[med-1]+=0.5
    K=k/N  ##attention au cas ou il existe i tq N[i]=0 ! (mais dans ce cas : exception ou planning non valable!)
    Nmoy=sum(N)/nombre_medecins
    M=sum(K)/nombre_medecins
    
    #Critères de validité du planning
    for i in range(nombre_medecins):
        if np.abs(N[i]-Nmoy)>a or np.abs(M-K[i])>p:
            L='false'
    return [M,L]


def mouvement():
    s = np.random.randint(0,2*nombre_de_services )
    j = np.random.randint(0, nombre_de_jours)
    med=np.random.choice(liste_services[int(s/2)])
    return [s,j,med]
    
    
def mouvement_v2(best_solution,liste_med_dispo):
    s = np.random.randint(0,2*nombre_de_services )
    j = np.random.randint(0, nombre_de_jours)
    med=best_solution[s][j]
    liste_med=np.delete(liste_med_dispo[j*s],np.where(med))
    if len(liste_med)!=0:
        med=np.random.choice(liste_med)
        return [s,j,med]
    else :
        return 0


def changement_solution(best_solution,best_score,liste_disponibilites,liste_tabou,mouv):
    new_solution = np.copy(best_solution)
    new_solution[mouv[0]][mouv[1]] = mouv[2]
    M,L=evaluate_solution(new_solution,liste_disponibilites)[0],evaluate_solution(new_solution,liste_disponibilites)[1]
    if L=='false':
        liste_tabou.append(mouv)
    elif not est_valide(new_solution,liste_disponibilites):
        liste_tabou.append(mouv)
    else:
        if M<best_score :
            best_solution=new_solution
            best_score=M
            print (best_score)
            liste_tabou=[]
    return [best_solution, best_score]

def recherche_tabou (nombre_iterations) :
    liste_disponibilites=generate_liste_disponibilites()
    print(liste_disponibilites)
    sol= generate_solution_v2(liste_disponibilites)
    best_solution,liste_med_dispo= sol[0],sol[1]
    best_score = evaluate_solution(best_solution,liste_disponibilites)[0]
    print (best_score)
    liste_tabou=[]
    for k in range (nombre_iterations) :
        mouv=mouvement()
        #mouv=mouvement_v2(best_solution,liste_med_dispo)
        if mouv not in liste_tabou and mouv!=0:
            L=changement_solution(best_solution,best_score,liste_disponibilites,liste_tabou,mouv)
            best_solution,best_score=L[0],L[1]
    return best_solution