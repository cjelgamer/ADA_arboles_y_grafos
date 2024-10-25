import heapq
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import ttk

class GrafoDirigido:
    def __init__(self):
        self.grafo = {}
    
    def agregar_arista(self, origen, destino, distancia):
        if origen not in self.grafo:
            self.grafo[origen] = []
        if destino not in self.grafo:
            self.grafo[destino] = []
        # Agregar la conexión en ambas direcciones para hacerla bidireccional
        self.grafo[origen].append((destino, distancia))
        self.grafo[destino].append((origen, distancia))  # Conexión de vuelta
    
    def dijkstra(self, inicio):
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[inicio] = 0
        prioridad = [(0, inicio)]
        camino = {nodo: None for nodo in self.grafo}

        while prioridad:
            distancia_actual, nodo_actual = heapq.heappop(prioridad)

            if distancia_actual > distancias[nodo_actual]:
                continue

            for vecino, peso in self.grafo[nodo_actual]:
                distancia = distancia_actual + peso

                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    camino[vecino] = nodo_actual
                    heapq.heappush(prioridad, (distancia, vecino))
        
        return distancias, camino
    
    def encontrar_ruta(self, inicio, destino, camino):
        ruta = []
        nodo_actual = destino
        while nodo_actual is not None:
            ruta.append(nodo_actual)
            nodo_actual = camino[nodo_actual]
        ruta.reverse()
        return ruta

# Función para mostrar los resultados en la interfaz gráfica
def mostrar_resultados():
    # Obtener la ciudad de origen y destino seleccionadas
    origen = origen_combobox.get()
    destino = destino_combobox.get()
    
    # Algoritmo de Dijkstra desde la ciudad de origen seleccionada
    distancias, camino = grafo.dijkstra(origen)

    # Obtener la ruta más corta desde la ciudad de origen hasta la de destino
    ruta_mas_corta = grafo.encontrar_ruta(origen, destino, camino)

    if len(ruta_mas_corta) == 1:  # Si no se encontró ruta, mostrar mensaje de error
        ruta_text.set(f"No se encontró una ruta válida de {origen} a {destino}.")
    else:
        # Mostrar los resultados en la interfaz
        distancias_text.set(f"Distancias desde {origen}:\n{distancias}")
        ruta_text.set(f"Ruta más corta de {origen} a {destino}:\n{' -> '.join(ruta_mas_corta)}")
    
        # Graficar el grafo y la ruta más corta
        G = nx.DiGraph()

        # Añadir las aristas al grafo para visualización
        G.add_weighted_edges_from([
            ('Lima', 'Ica', 300), 
            ('Lima', 'Trujillo', 556), 
            ('Ica', 'Arequipa', 706), 
            ('Arequipa', 'Cusco', 509), 
            ('Cusco', 'Juliaca', 344), 
            ('Juliaca', 'Puno', 45), 
            ('Cusco', 'Puno', 387),
            ('Lima', 'Huancayo', 200),    
            ('Huancayo', 'Ica', 300),     
            ('Huancayo', 'Cusco', 650),
            ('Trujillo', 'Piura', 350),
            ('Piura', 'Chiclayo', 210),
            ('Trujillo', 'Chiclayo', 210),
            ('Arequipa', 'Tacna', 380),
            ('Tacna', 'Cusco', 600),
            ('Lima', 'Tarapoto', 860),
            ('Tarapoto', 'Chiclayo', 850)
        ])

        # Definir posiciones específicas para las ciudades
        pos = {
            'Lima': (0, 0),
            'Trujillo': (-2, 2),
            'Ica': (0, -2),
            'Arequipa': (2, -4),
            'Cusco': (4, -6),
            'Puno': (6, -9),
            'Juliaca': (6, -8),
            'Piura': (-3, 4),
            'Chiclayo': (-2, 3),
            'Tacna': (3, -10),
            'Huancayo': (1, -3),
            'Tarapoto': (-1, 5)
        }

        # Dibujar el grafo con posiciones fijas
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold', arrows=True)

        # Dibujar las etiquetas de peso de las aristas
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # Resaltar la ruta más corta
        path_edges = list(zip(ruta_mas_corta, ruta_mas_corta[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

        plt.title(f"Grafo de Ciudades de Perú - Ruta de {origen} a {destino} en rojo")
        plt.show()

# Crear el grafo con las ciudades de Perú
grafo = GrafoDirigido()
grafo.agregar_arista('Lima', 'Ica', 300)
grafo.agregar_arista('Lima', 'Trujillo', 556)
grafo.agregar_arista('Ica', 'Arequipa', 706)
grafo.agregar_arista('Arequipa', 'Cusco', 509)
grafo.agregar_arista('Cusco', 'Juliaca', 344)
grafo.agregar_arista('Juliaca', 'Puno', 45)
grafo.agregar_arista('Cusco', 'Puno', 387)
grafo.agregar_arista('Lima', 'Huancayo', 200)
grafo.agregar_arista('Huancayo', 'Ica', 300)
grafo.agregar_arista('Huancayo', 'Cusco', 650)
grafo.agregar_arista('Trujillo', 'Piura', 350)
grafo.agregar_arista('Piura', 'Chiclayo', 210)
grafo.agregar_arista('Trujillo', 'Chiclayo', 210)
grafo.agregar_arista('Arequipa', 'Tacna', 380)
grafo.agregar_arista('Tacna', 'Cusco', 600)
grafo.agregar_arista('Lima', 'Tarapoto', 860)
grafo.agregar_arista('Tarapoto', 'Chiclayo', 850)

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Ruta más corta en Ciudades de Perú")
root.geometry("500x350")

# Variables para mostrar los resultados
distancias_text = tk.StringVar()
ruta_text = tk.StringVar()

# Menús desplegables para seleccionar origen y destino
ciudades = ['Lima', 'Ica', 'Trujillo', 'Arequipa', 'Cusco', 'Puno', 'Juliaca', 'Huancayo', 'Piura', 'Chiclayo', 'Tacna', 'Tarapoto']
origen_combobox = ttk.Combobox(root, values=ciudades, state="readonly")
origen_combobox.set("Selecciona origen")
origen_combobox.pack(pady=5)

destino_combobox = ttk.Combobox(root, values=ciudades, state="readonly")
destino_combobox.set("Selecciona destino")
destino_combobox.pack(pady=5)

# Etiquetas para mostrar la información
ttk.Label(root, textvariable=distancias_text, wraplength=400).pack(pady=10)
ttk.Label(root, textvariable=ruta_text, wraplength=400).pack(pady=10)

# Botón para calcular y mostrar resultados
ttk.Button(root, text="Calcular Ruta", command=mostrar_resultados).pack(pady=20)

# Iniciar la interfaz gráfica
root.mainloop()
