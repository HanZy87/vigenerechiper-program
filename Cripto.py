import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

def vigenere_encrypt(plaintext, key):
    key = key.upper()
    key_length = len(key)
    plaintext = plaintext.upper()
    encrypted = ''
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            key_char = key[i % key_length]
            encrypted += chr(((ord(plaintext[i]) - 65) + (ord(key_char) - 65)) % 26 + 65)
        else:
            encrypted += plaintext[i]
    return encrypted

def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    key_length = len(key)
    ciphertext = ciphertext.upper()
    decrypted = ''
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            key_char = key[i % key_length]
            decrypted += chr(((ord(ciphertext[i]) - 65) - (ord(key_char) - 65)) % 26 + 65)
        else:
            decrypted += ciphertext[i]
    return decrypted


def create_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    used_chars = set()
    for char in key:
        if char not in used_chars and char.isalpha():
            used_chars.add(char)
            matrix.append(char)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ123456789":
        if char not in used_chars:
            used_chars.add(char)
            matrix.append(char)
    return [matrix[i:i + 5] for i in range(0, 25, 5)]


def playfair_encrypt(plaintext, key):
    matrix = create_playfair_matrix(key)
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
    if len(plaintext) % 2 != 0:
        plaintext += 'X'
    ciphertext = ''
    for i in range(0, len(plaintext), 2):
        char1, char2 = plaintext[i], plaintext[i + 1]
        row1, col1 = find_position(char1, matrix)
        row2, col2 = find_position(char2, matrix)
        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]
    return ciphertext


def playfair_decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    ciphertext = ciphertext.upper().replace(" ", "")
    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        char1, char2 = ciphertext[i], ciphertext[i + 1]
        row1, col1 = find_position(char1, matrix)
        row2, col2 = find_position(char2, matrix)
        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]
    return plaintext


def find_position(char, matrix):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col


def hill_encrypt(plaintext, key):
    n = len(key)
    plaintext = plaintext.upper().replace(" ", "")
    while len(plaintext) % n != 0:
        plaintext += 'X'
    plaintext_vector = [ord(char) - 65 for char in plaintext]
    plaintext_matrix = np.array(plaintext_vector).reshape(-1, n)
    key_matrix = np.array(key)
    ciphertext_matrix = (np.dot(plaintext_matrix, key_matrix) % 26).astype(int)
    ciphertext = ''.join([chr(num + 65) for num in ciphertext_matrix.flatten()])
    return ciphertext


def hill_decrypt(ciphertext, key):
    n = len(key)
    ciphertext = ciphertext.upper().replace(" ", "")
    ciphertext_vector = [ord(char) - 65 for char in ciphertext]
    ciphertext_matrix = np.array(ciphertext_vector).reshape(-1, n)
    key_matrix = np.array(key)
    key_inverse = np.linalg.inv(key_matrix).astype(float)
    determinant = int(round(np.linalg.det(key_matrix)))
    adjugate_matrix = np.round(key_inverse * determinant).astype(int) % 26
    plaintext_matrix = (np.dot(ciphertext_matrix, adjugate_matrix) % 26).astype(int)
    plaintext = ''.join([chr(num + 65) for num in plaintext_matrix.flatten()])
    return plaintext


def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            plaintext_input.delete(1.0, tk.END)
            plaintext_input.insert(tk.END, file.read())


def validate_key(key):
    if len(key) < 12:
        messagebox.showerror("Error", "Kunci harus minimal 12 karakter.")
        return False
    return True


root = tk.Tk()
root.title("Program Kriptografi")


tk.Label(root, text="Masukkan Plainteks:").pack()
plaintext_input = tk.Text(root, height=5, width=50)
plaintext_input.pack()


upload_button = tk.Button(root, text="Unggah File", command=upload_file)
upload_button.pack()


tk.Label(root, text="Masukkan Kunci:").pack()
key_input = tk.Entry(root, show="*")
key_input.pack()


tk.Label(root, text="Pilih Algoritma:").pack()
algorithm = tk.StringVar(value="Vigenere")
tk.Radiobutton(root, text="Vigenere", variable=algorithm, value="Vigenere").pack()
tk.Radiobutton(root, text="Playfair", variable=algorithm, value="Playfair").pack()
tk.Radiobutton(root, text="Hill", variable=algorithm, value="Hill").pack()


encrypt_button = tk.Button(root, text="Enkripsi", command=lambda: encrypt_action())
decrypt_button = tk.Button(root, text="Dekripsi", command=lambda: decrypt_action())
encrypt_button.pack()
decrypt_button.pack()


def encrypt_action():
    plaintext = plaintext_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    if validate_key(key):
        selected_algorithm = algorithm.get()
        if selected_algorithm == "Vigenere":
            ciphertext = vigenere_encrypt(plaintext, key)
        elif selected_algorithm == "Playfair":
            ciphertext = playfair_encrypt(plaintext, key)
        elif selected_algorithm == "Hill":
            key_matrix = [[3, 3], [2, 5]]  
            ciphertext = hill_encrypt(plaintext, key_matrix)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, ciphertext)


def decrypt_action():
    ciphertext = plaintext_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    if validate_key(key):
        selected_algorithm = algorithm.get()
        if selected_algorithm == "Vigenere":
            decrypted_text = vigenere_decrypt(ciphertext, key)
        elif selected_algorithm == "Playfair":
            decrypted_text = playfair_decrypt(ciphertext, key)
        elif selected_algorithm == "Hill":
            key_matrix = [[3, 3], [2, 5]] 
            decrypted_text = hill_decrypt(ciphertext, key_matrix)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, decrypted_text)


tk.Label(root, text="Hasil:").pack()
result_text = tk.Text(root, height=5, width=50)
result_text.pack()

root.mainloop()
