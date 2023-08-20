#avec l'aide de @j-m-l https://forum.arduino.cc/t/python-3-tkinter/1156315/4
import pickle
from pathlib import Path
import tkinter as tk
from collections import defaultdict
from tkinter import messagebox



class Sudoku(tk.Tk):
    def __init__(self):
        self.labels={}
        self.interdits={}
        self.memligne = -1
        self.memcolonne = -1
        self.ancienne_ligne = 0
        self.ancienne_colonne = 0
        self.nom_fichier= "facile 1"
        super().__init__()
        self.create_menu_bar()
        self.grille = self.creation_grille()
        self.creer_widgets_grille()

    def creation_grille(self):
        
        mon_chemin = Path(f"{self.nom_fichier}")
        with mon_chemin.open('rb') as fichier:
            grille = pickle.load(fichier)
        
        return grille  

    def creer_widgets_grille(self):
        self.label_interdits()
        #création de la grille du Sudoku
        for row in range(9):
            for col in range(9):
                self.label = tk.Label(
                    self,text=self.grille[row][col], width=4, bg = "white", highlightthickness=1,
                    highlightbackground='#000000',font=("arial", 32)
                )
                self.label.configure(fg = 'chocolate') if self.grille[row][col]== "." else self.label.configure(fg = 'black')
                pad_y = (0, 0) if (row + 1) % 3 != 0 or row == 8 else (0, 5)
                pad_x = (0, 0) if (col + 1) % 3 != 0 or col == 8 else (0, 5)
        
                self.label.grid(row=row, column=col, ipadx=5, ipady=5, padx=pad_x, pady=pad_y)
                self.labels[(row,col)] = self.label
                self.label.bind("<Button-1>", lambda event, ligne=row , col=col : self.position(ligne,col))
                
        #Création ligne de labels cachés
        for col in range(9):                  
            self.label2 = tk.Label(
                self,text = " " , width=4, bg = "beige", highlightthickness=1,
                highlightbackground='beige',font=("arial", 32), fg = 'beige'
                )
            pad_y = (0, 0) if (row + 1) % 3 != 0 or row == 8 else (0, 5)
            pad_x = (0, 0) if (col + 1) % 3 != 0 or col == 8 else (0, 5)
            
            self.label2.grid(row=10, column=col, ipadx=5, ipady=5, padx=pad_x, pady=pad_y)
            #self.label2.grid_forget()
            
        #Création des labels : Chiffres
        x = 1
        for col in range(9):                  
            self.label3 = tk.Label(
                self,text = x , width=4, bg = 'bisque1', highlightthickness=1,
                highlightbackground='#000000',font=("arial", 32), fg = 'blue', borderwidth= 2, relief ="raised" 
                )

            pad_y = (0, 0) if (row + 1) % 3 != 0 or row == 8 else (0, 5)
            pad_x = (0, 0) if (col + 1) % 3 != 0 or col == 8 else (0, 5)
            
            self.label3.grid(row=11, column=col, ipadx=5, ipady=5, padx=pad_x, pady=pad_y)
            self.label3.bind("<Button-1>", lambda event, col=col : self.chiffre(col))
            x+=1

        #Création du label : Supprimer
        self.label4 = tk.Label(
                self,text = 'SUP' , width=4, bg = "bisque1", highlightthickness=1,
                highlightbackground='#000000',font=("arial", 20), fg = 'red', borderwidth= 2, relief ="raised" 
                )
        self.label4.grid(row=12, column=4, ipadx=5, ipady=5, padx=0, pady=10)
        self.label4.bind("<Button-1>", self.sup)
        
    #Création barre de menu
    def create_menu_bar(self):
        self.menu_bar = tk.Menu(self)
        
        self.menu_file = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fichier", menu=self.menu_file)
        self.sub1= tk.Menu(self.menu_bar, tearoff=0)
        self.sub2= tk.Menu(self.menu_bar, tearoff=0)
        self.menu_file.add_cascade(label="Facile", menu=self.sub1)
        self.menu_file.add_cascade(label="Moyen", menu=self.sub2)
        self.sub1.add_command(label="Facile 1", command= lambda  fichier="facile 1" : self.ouvrir(fichier))
        self.sub1.add_command(label="Facile 2", command= lambda  fichier="facile 2" : self.ouvrir(fichier))
        self.sub1.add_command(label="Facile 3", command= lambda  fichier="facile 3" : self.ouvrir(fichier))
        self.sub1.add_command(label="Facile 4", command= lambda  fichier="facile 4" : self.ouvrir(fichier))
        self.sub1.add_command(label="Facile 5", command= lambda  fichier="facile 5" : self.ouvrir(fichier))
        self.sub1.add_command(label="Facile 6", command= lambda  fichier="facile 6" : self.ouvrir(fichier))
        self.sub1.add_command(label="Facile 7", command= lambda  fichier="facile 7" : self.ouvrir(fichier))
        self.sub2.add_command(label="Moyen 1", command= lambda  fichier="Moyen 1" : self.ouvrir(fichier))
        self.sub2.add_command(label="Moyen 2", command= lambda  fichier="Moyen 2" : self.ouvrir(fichier))
        self.sub2.add_command(label="Moyen 3", command= lambda  fichier="Moyen 3" : self.ouvrir(fichier))
        self.sub2.add_command(label="Moyen 4", command= lambda  fichier="Moyen 4" : self.ouvrir(fichier))
        self.sub2.add_command(label="Moyen 5", command= lambda  fichier="Moyen 5" : self.ouvrir(fichier))
        self.sub2.add_command(label="Moyen 6", command= lambda  fichier="Moyen 6" : self.ouvrir(fichier))
        self.sub2.add_command(label="Moyen 7", command= lambda  fichier="Moyen 7" : self.ouvrir(fichier))
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Quitter", command=self.destroy)
        self.config(menu=self.menu_bar)
        
                
    def ouvrir(self,fichier):
        for children in jeu.winfo_children():
            children.destroy()
        self.nom_fichier = fichier
        jeu.title(f"SUDOKU de philippe86220 - jeu : {jeu.nom_fichier}")
        self.create_menu_bar()
        self.grille = self.creation_grille()
        self.creer_widgets_grille()
        
    def label_interdits(self):
        for row in range(9):
            for col in range(9):
                current_val = self.grille[row][col]
                if current_val != '.':
                    self.interdits[row,col] = 'interdit'
                else:
                    self.interdits[row,col] = 'ok'

    def position(self, ligne, col):
         self.labels[(self.ancienne_ligne,self.ancienne_colonne)]['bg']= 'white'
         self.memligne = ligne
         self. memcolonne = col
         self.labels[(ligne,col)]['bg']= 'aquamarine'
         self.ancienne_ligne = ligne
         self.ancienne_colonne = col

    def chiffre (self, col):
        if self.memligne != -1 and self. memcolonne != -1:
            
            val = col + 1
            if self.grille[self.memligne][self. memcolonne] != ".":
                messagebox.showinfo("Erreur", f"Un chiffre se trouve déjà en ligne {self.memligne +  1} colonne {self. memcolonne +1}")
                self.labels[(self.memligne,self.memcolonne)]['bg']= 'white'
            else:
                self.grille[self.memligne][self.memcolonne] = val
                self.labels[(self.memligne,self.memcolonne)]['text']= col + 1
                self.labels[(self.memligne,self.memcolonne)]['bg']= 'white'
                
                if not self.test_doublon():
                    messagebox.showinfo("Erreur", f"le chiffre {val} ne peut pas être placé ici (existe déjà sur un axe horizontal, vertical ou dans le groupe de 9 chiffres !) !")
                    self.grille[self.memligne][self. memcolonne] = "."
                    self.labels[(self.memligne,self.memcolonne)]['text']= "."
                    
            
            self.test_fin()
        else:
            messagebox.showinfo("Erreur", "Veuillez selectionner une case !")
        self.memligne = -1
        self. memcolonne = -1
        
    def test_doublon (self):
        test = defaultdict(int)
        for i in range (len(self.grille)):
            for j in range (len(self.grille)):
                current_val = self.grille[i][j]
                if (current_val != "."): 
                    test[f"{str(current_val)}  dans ligne :   {str(i)}"] +=1
                    test[f"{str(current_val)}  dans col :  {str(j)}"] +=1
                    test[f"{str(current_val)}  dans Box : {str(i//3)} {str(j//3)}"] +=1
                    if test[f"{str(current_val)}  dans ligne :   {str(i)}"]>1 or test[f"{str(current_val)}  dans col :  {str(j)}"]>1 or test[f"{str(current_val)}  dans Box : {str(i//3)} {str(j//3)}"] > 1:
                        return False        
        return True
    
    def test_fin (self):
        nb_chiffre = 0
        for i in range (len(self.grille)):
            for j in range (len(self.grille)):
                current_val = self.grille[i][j]
                if str(current_val).isnumeric():
                  nb_chiffre += 1
                  #print(nb_chiffre)
                  if nb_chiffre == 81:
                      messagebox.showinfo("VOOUS AVEZ GAGNEZ", "BRAVO VOUS AVEZ REUSSI")
                      
        
    def sup(self, event):
        if self.memligne != -1 and self. memcolonne != -1:
            if self.interdits[self.memligne,self.memcolonne] != 'interdit':
                self.grille[self.memligne][self.memcolonne] = "."
                self.labels[(self.memligne,self.memcolonne)]['text']= "."  
                self.labels[(self.memligne,self.memcolonne)]['bg']= 'white'
                self.test_fin()
                self.memligne = -1
                self. memcolonne = -1
            else:
                messagebox.showinfo("Erreur", f"impossible de supprimer le chiffre {self.grille[self.memligne][self. memcolonne]} car il est prédéfini dans le jeu !")
        else:
            messagebox.showinfo("Erreur", "Veuillez selectionner une case !")
            
jeu = Sudoku()
jeu.title(f"SUDOKU de philippe86220 - jeu : {jeu.nom_fichier}")
jeu.configure(bg = 'beige')
jeu.mainloop()
