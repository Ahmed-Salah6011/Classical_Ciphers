import numpy as np
from tkinter import filedialog
import os

alpha='abcdefghijklmnopqrstuvwxyz'

letter_to_num={alpha[v]:v for v in range(len(alpha))}
num_to_letter={v:alpha[v] for v in range(len(alpha))}

path=os.path.dirname(os.path.realpath(__file__))

def cesar_cipher(file , key):
    f= open(file,'r')
    # ind=file.rfind("\\")
    # folder_path= file[:ind+1]
    out = open(os.path.join(path,"cesar_cipher.txt"),'w')
    lines= f.read()
    lines=lines.lower().splitlines()
    for line in lines:
        for char in line:
            if char == " ":
                continue
            ###algo
            new=num_to_letter[(letter_to_num[char]+key)%26]
            ####

            out.write(new)
        
        out.write("\n")


def vigenere_cipher(file,key,mode=True):
    key=key.lower()
    f= open(file,'r')
    # ind=file.rfind("\\")
    # folder_path= file[:ind+1]
    out = open(os.path.join(path,"vigenere_cipher.txt"),'w')
    lines= f.read()
    lines=lines.lower().splitlines()
    for line in lines:
        k_ptr=0 #to iterate over the new key (it will either iterate over key or plaintext in auto mode)
        e_flag=0 #to know if the key is ended and we started taking from plain text or not
        for char in line:
            if char == " ":
                continue
            ###algo
            if mode: #autokey
                if k_ptr==len(key) and e_flag==0:
                    k_ptr=0
                    e_flag=1
                if e_flag==0:
                    new=num_to_letter[(letter_to_num[char]+letter_to_num[key[k_ptr]]) %26]
                    k_ptr+=1
                if e_flag==1:
                    new=num_to_letter[(letter_to_num[char]+letter_to_num[line[k_ptr]]) %26]
                    k_ptr+=1
            
            else: #repeating
                if k_ptr==len(key):
                    k_ptr=0

                new=num_to_letter[(letter_to_num[char]+letter_to_num[key[k_ptr]]) %26]
                k_ptr+=1
            #####
            out.write(new)
        
        out.write("\n")



def vernam_cipher(file,key):
    key=key.lower()
    f= open(file,'r')
    # ind=file.rfind("\\")
    # folder_path= file[:ind+1]
    out = open(os.path.join(path,"vernam_cipher.txt"),'w')
    lines= f.read()
    lines=lines.lower().splitlines()
    for line in lines:
        if len(key) != len(line):
            print("can't encrypt this line, key length not equal plaintext length")
            continue
        k_ptr=0 #to iterate over the key
        for char in line:
            if char == " ":
                continue
            ###algo
            new =num_to_letter[(letter_to_num[char]+ letter_to_num[key[k_ptr]]) %26]
            k_ptr+=1
            #####
            out.write(new)
        
        out.write("\n")

def hill_cipher(file,key):
    key=np.array(key)
    num_letters=key.shape[0]
    f= open(file,'r')
    # ind=file.rfind("\\")
    # folder_path= file[:ind+1]
    out = open(os.path.join(path,"hill_cipher.txt"),'w')
    lines= f.read()
    lines=lines.lower().splitlines()
    for line in lines:
        g=[]
        groups=[]
        #first divide line into groups of num_letters
        for char in line:
            if char == " ":
                continue
            g.append(letter_to_num[char])
            if len(g)== num_letters:
                groups.append(list(g))
                g.clear()
        
        if len(g) == num_letters-1: #misiing letter in the last
            g.append(letter_to_num["x"])
            groups.append(list(g))
        elif  len(g) == num_letters-2:  #misiing two letters in the last
            g.append(letter_to_num["x"])
            g.append(letter_to_num["x"])
            groups.append(list(g))

        ################
        
        #second iterate over groups to encrypt each one
        for group in groups:
            group= np.array(group)
            out_g = np.dot(key,group) %26##encrypt
            for n in out_g:
                out.write(num_to_letter[n])


        
        out.write("\n")


def create_matrix(key):
    matrix= np.zeros((5,5),dtype='str')
    alph = {alpha[v]:1 for v in range(len(alpha)) if alpha[v] !='j'}
    k_ptr=0
    for row_ind in range(len(matrix)):
        for col_ind in range(len(matrix[row_ind])):
            if k_ptr != len(key):
                if alph[key[k_ptr]]==0:
                    k_ptr+=1

                matrix[row_ind][col_ind] = key[k_ptr]
                alph[key[k_ptr]] = 0
                k_ptr+=1
            else:
                for letter,flag in alph.items():
                    if flag==1:
                        matrix[row_ind][col_ind] = letter
                        alph[letter]=0
                        break
    
    return matrix

def find_group_indices(matrix,group):
    first=group[0]
    second=group[1]

    first_row=0
    first_col=0
    second_row=0
    second_col=0
    
    flag=0
    for row_ind in range(len(matrix)):
        if flag==2:
                break
        for col_ind in range(len(matrix[row_ind])):
            if flag==2:
                break


            if matrix[row_ind][col_ind] == first:
                first_row=row_ind
                first_col=col_ind
                flag+=1
            elif matrix[row_ind][col_ind] == second:
                second_row=row_ind
                second_col=col_ind
                flag+=1
    
    return first_row,first_col,second_row,second_col
            
        



def playfair_cipher(file,key):
    key=key.lower().replace("j","i")
    f= open(file,'r')
    # ind=file.rfind("\\")
    # folder_path= file[:ind+1]
    out = open(os.path.join(path,"playfair_cipher.txt"),'w')
    lines= f.read()
    lines=lines.lower().splitlines()
    matrix= create_matrix(key)

    for line in lines:
        line= line.replace("j","i")
        g=[]
        groups=[]
        first_flag=0
        #first divide line into groups of 2
        for char in line:
            if char == " ":
                continue
            if first_flag==0:
                g.append(char)
                first_flag=1
            else:
                if char == g[0]:
                    g.append("x")
                    groups.append(list(g))
                    g.clear()

                    ##add repeated letter to new group
                    g.append(char)
                    first_flag=1

                else:
                    g.append(char)
                    groups.append(list(g))
                    g.clear()
                    first_flag=0
        
        if len(g) == 2-1: #misiing letter in the last
            g.append("x")
            groups.append(list(g))

        ################
        
        #second iterate over groups to encrypt each one
        for group in groups:
            nf_row=0
            nf_col=0
            ns_row=0
            ns_col=0
            f_row,f_col,s_row,s_col = find_group_indices(matrix,group)
            if f_row == s_row:
                #shift right rows
                nf_row = (f_row+1)%5
                ns_row = (s_row+1)%5
                #keep cols
                nf_col=f_col
                ns_col=s_col

            elif f_col == s_col:
                #shift down cols
                nf_col = (f_col+1)%5
                ns_col = (s_col+1)%5
                #keep rows
                nf_row=f_row
                ns_row=s_row

            else:
                nf_row= f_row
                nf_col= s_col

                ns_row= s_row
                ns_col= f_col
            


            ###write to file
            out.write(matrix[nf_row][nf_col])
            out.write(matrix[ns_row][ns_col])

    ###############################
        out.write("\n")








if __name__ == "__main__":
    cesar_key=None
    vigenere_key=None
    mode=None
    vernam_key=None
    hill_key=None
    playfair_key=None

    print("Choose Plaintext File")
    file_path = filedialog.askopenfile().buffer.name
    print("Now Enter the key for each cipher:")
    cesar_key=int(input("Cesar Key: "))
    vigenere_key = input("Vigenere Key: ")
    mode=int(input("Vigenere Mode (0 or 1): "))
    vernam_key= input("Vernam Key: ")
    playfair_key = input("Playfair Key: ")
    dim = int(input("Enter Hill Cipher Key first dimension: "))
    hill_key = np.zeros((dim,dim), dtype="int")
    h_k=[]
    while(len(h_k)!= dim*dim):
        h_k = input("Hill Key (fill rows first then columns in one line with spaces) : ").split()
        if len(h_k)!= dim*dim:
            print("Error , Please enter the key again!")
    i=0
    for r in range(dim):
        for c in range(dim):
            hill_key[r][c]= int(h_k[i])
            i+=1
    

    cesar_cipher(file_path,cesar_key)
    vigenere_cipher(file_path,vigenere_key,mode)
    vernam_cipher(file_path,vernam_key)
    playfair_cipher(file_path,playfair_key)
    hill_cipher(file_path,hill_key)







