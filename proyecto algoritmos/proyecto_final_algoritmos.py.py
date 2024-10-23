import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

class CalculadoraMatricesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto de Julio Adán")
        self.root.state('zoomed')  # Maximizar la ventana
        self.root.configure(bg="lightblue")

        # Título dentro de la ventana
        self.label_titulo = tk.Label(root, text="Proyecto de Julio Adán", bg="lightblue", font=("Arial", 40, "bold"))
        self.label_titulo.grid(row=0, columnspan=5, pady=50)

        # Etiqueta y entrada para el tamaño de la matriz
        self.label_n = tk.Label(root, text="Ingrese el tamaño de la matriz (n x n):", bg="lightblue", font=("Arial", 25, "bold"))
        self.label_n.grid(row=1, column=0, padx=10, pady=10)

        self.entry_n = tk.Entry(root, font=("Arial", 27))
        self.entry_n.grid(row=1, column=1, padx=10, pady=10)

        # Botón para establecer el tamaño de la matriz
        self.btn_establecer_tamano = tk.Button(root, text="Establecer Tamaño", font=("Arial", 25), bg="pink", command=self.crear_entradas_matriz)
        self.btn_establecer_tamano.grid(row=1, column=2, padx=10, pady=10)

        self.entradas_matriz = []  # Lista para almacenar las entradas de la matriz
        self.entradas_independientes = []  # Lista para almacenar los términos independientes

        # Asociar Enter al botón de establecer tamaño
        root.bind('<Return>', lambda event: self.crear_entradas_matriz())

    # Crear las entradas para la matriz y los términos independientes
    def crear_entradas_matriz(self):
        try:
            n = int(self.entry_n.get())  # Obtener el tamaño de la matriz
            if n > 5 or n < 1:
                raise ValueError("El tamaño de la matriz debe estar entre 1 y 5")
            self.limpiar_entradas_matriz()

            # Crear campos de entrada para la matriz
            for i in range(n):
                fila_entradas = []
                for j in range(n):
                    entrada = tk.Entry(self.root, width=5, font=("Arial", 12))
                    entrada.grid(row=i+3, column=j, padx=5, pady=5)
                    fila_entradas.append(entrada)
                self.entradas_matriz.append(fila_entradas)

            # Generar y mostrar términos independientes automáticamente
            self.generar_terminos_independientes(n)

            # Crear botones para los métodos
            self.btn_gauss_jordan = tk.Button(self.root, text="Gauss-Jordan", font=("Arial", 25), bg="lightgreen", command=self.resolver_gauss_jordan)
            self.btn_gauss_jordan.grid(row=n+4, column=0, padx=10, pady=30, columnspan=2)

            self.btn_cramer = tk.Button(self.root, text="Regla de Cramer", font=("Arial", 25), bg="lightgreen", command=self.resolver_cramer)
            self.btn_cramer.grid(row=n+4, column=1, padx=10, pady=30, columnspan=2)

            self.btn_multiplicar = tk.Button(self.root, text="Multiplicar Matrices", font=("Arial", 25), bg="lightgreen", command=self.multiplicar_matrices)
            self.btn_multiplicar.grid(row=n+5, column=0, padx=10, pady=20, columnspan=2)

            self.btn_inversa = tk.Button(self.root, text="Matriz Inversa", font=("Arial", 25), bg="lightgreen", command=self.calcular_inversa)
            self.btn_inversa.grid(row=n+5, column=1, padx=10, pady=20, columnspan=2)

            # Asociar Enter a los botones de métodos
            self.root.bind('<Return>', lambda event: self.resolver_gauss_jordan())

        except ValueError as ve:
            messagebox.showerror("Error de Entrada", f"Entrada no válida: {ve}")

    # Generar términos independientes automáticamente
    def generar_terminos_independientes(self, n):
        self.entradas_independientes.clear()  # Limpiar las entradas anteriores
        for i in range(n):
            # Generar un término independiente aleatorio entre 1 y 10
            valor_independiente = random.randint(1, 10)
            label_independiente = tk.Label(self.root, text=f"{valor_independiente}", font=("Arial", 12, "bold"), bg="lightyellow", width=5)
            label_independiente.grid(row=i+3, column=n+1, padx=5, pady=5)
            self.entradas_independientes.append(valor_independiente)  # Guardar el valor generado

    # Limpiar las entradas anteriores
    def limpiar_entradas_matriz(self):
        for fila in self.entradas_matriz:
            for entrada in fila:
                entrada.grid_forget()
        self.entradas_matriz = []

        # Limpiar los términos independientes
        for label in self.entradas_independientes:
            if isinstance(label, tk.Label):
                label.grid_forget()
        self.entradas_independientes = []

    # Obtener la matriz ingresada por el usuario
    def obtener_matriz(self):
        try:
            n = len(self.entradas_matriz)
            matriz = []
            for fila_entradas in self.entradas_matriz:
                fila = [float(entrada.get()) for entrada in fila_entradas]
                matriz.append(fila)
            return np.array(matriz)  # Convertir a matriz de NumPy
        #si un valor no es numero o la casilla esta vasia arrojara este error 
        except ValueError:
            messagebox.showerror("Error de Entrada", "Todos los valores de la matriz deben ser números")
            return None

    # Resolver usando Gauss-Jordan
    def resolver_gauss_jordan(self):
        matriz = self.obtener_matriz()
        if matriz is not None:
            try:
                resultado = np.linalg.inv(matriz)
                self.mostrar_resultado(resultado, "Gauss-Jordan")
#si la matriz no se puede invertir aparesera el siguiente mensaje                 
            except np.linalg.LinAlgError:
                messagebox.showerror("Error", "Las matices singulares no se pueden invertir ).")

    # Resolver usando la Regla de Cramer
    def resolver_cramer(self):
        matriz = self.obtener_matriz()
        if matriz is not None:
            try:
#si el determinante es cero no se puede aplicar la regla de cramer y arrojara el siguiente mensaje
                n = len(matriz)
                det_matriz = np.linalg.det(matriz)
                if det_matriz == 0:
                    raise np.linalg.LinAlgError("Determinante es cero, no se puede aplicar la Regla de Cramer.")
                
                # Crear un array de soluciones
                soluciones = []
                for i in range(n):
                    matriz_temp = np.copy(matriz)
                    matriz_temp[:, i] = self.entradas_independientes
                    soluciones.append(np.linalg.det(matriz_temp) / det_matriz)
                
                self.mostrar_resultado(np.array(soluciones), "Regla de Cramer")
            except np.linalg.LinAlgError as e:
                messagebox.showerror("Error", str(e))

    # Multiplicar matrices
    def multiplicar_matrices(self):
        matriz = self.obtener_matriz()
        if matriz is not None:
            # Crear una segunda matriz de igual tamaño y multiplicar
            try:
                matriz2 = np.random.randint(1, 10, size=matriz.shape)  # Generar matriz aleatoria
                resultado = np.dot(matriz, matriz2)
                self.mostrar_resultado(resultado, "Multiplicación de Matrices")
            except ValueError as ve:
                messagebox.showerror("Error", f"Error en la multiplicación: {ve}")

    # Calcular la inversa de la matriz
    def calcular_inversa(self):
        matriz = self.obtener_matriz()
        if matriz is not None:
            try:
 #las matrices singulares no se pueden invertir entonces el siguiente mensaje aparesera                
                inversa = np.linalg.inv(matriz)
                self.mostrar_resultado(inversa, "Matriz Inversa")
            except np.linalg.LinAlgError:
                messagebox.showerror("Error", "La matrices singulares no se pueden invertir.")

    # Mostrar resultado en una ventana emergente color amarillo con el titulo de mi nombre 
    def mostrar_resultado(self, resultado, metodo):
        resultado_str = np.array_str(resultado)
        ventana_resultado = tk.Toplevel(self.root)
        ventana_resultado.title(f"Resultado: *Julio Adán*")
        ventana_resultado.configure(bg="yellow")
        #ventana_resultado.state('zoomed')  #lo anterior es para Maximizar la ventana
                       
        label_resultado = tk.Label(ventana_resultado, text=f"La calculadora de Julio debuelve el:\n\n Resultado ({metodo}):\n{resultado_str}", bg="yellow", font=("Arial", 14))
        label_resultado.pack(padx=20, pady=20)

# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraMatricesApp(root)
    root.mainloop()
