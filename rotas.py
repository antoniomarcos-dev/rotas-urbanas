# import heapq
# import requests
# import folium 

# # 1. Coordenadas (Latitude, Longitude) de locais reais em Ceres - GO
# locais = {
#     "Universidade": (-15.31047062446175, -49.615864422226814), # Uni Campus Ceres
#     "Bombeiros": (-15.309473774430527, -49.617271477898875),
#     "Policia": (-15.310070237506816, -49.619834719645006),
#     "Orb": (-15.310475696229641, -49.59614865990047),

# }

# # 2. Conexões do grafo (De onde -> Para onde)
# grafo_conexoes = {
#     "Universidade": ["Bombeiros", "Policia"],
#     "Bombeiros": ["Orb", "Policia"],
#     "Policia": ["Orb"],
#     "Orb": []
# }

# # 3. Puxa a distância e a geometria da rota pelas ruas (API OSRM)
# def pegar_rota_osrm(coord1, coord2):
#     url = f"http://router.project-osrm.org/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}?overview=full&geometries=geojson"
#     resposta = requests.get(url).json()
#     rota = resposta["routes"][0]
#     dist_km = rota["distance"] / 1000.0
    
#     # Folium precisa de [latitude, longitude], OSRM devolve [longitude, latitude]
#     coords_rua = [(lat, lon) for lon, lat in rota["geometry"]["coordinates"]]
#     return dist_km, coords_rua

# # 4. Construindo o Grafo
# grafo = {}
# rotas_para_pitar = [] # Guardaremos as coordenadas das ruas aqui

# for origem, destinos in grafo_conexoes.items():
#     grafo[origem] = []
#     for destino in destinos:
#         dist, coords_rua = pegar_rota_osrm(locais[origem], locais[destino])
#         grafo[origem].append((destino, dist))
#         rotas_para_pitar.append(coords_rua)

# # 5. Algoritmo Dijkstra Enxuto com Caminhos
# def dijkstra(grafo, inicio):
#     distancias = {no: float('inf') for no in locais}
#     caminhos = {no: [] for no in locais} # Rastreador de rota
    
#     distancias[inicio] = 0
#     caminhos[inicio] = [inicio]
#     fila = [(0, inicio)]

#     while fila:
#         dist_atual, vertice = heapq.heappop(fila)
        
#         if dist_atual > distancias[vertice]: 
#             continue

#         for vizinho, peso in grafo[vertice]:
#             nova_dist = dist_atual + peso
            
#             if nova_dist < distancias[vizinho]:
#                 distancias[vizinho] = nova_dist
#                 caminhos[vizinho] = caminhos[vertice] + [vizinho] # Registra por onde passou
#                 heapq.heappush(fila, (nova_dist, vizinho))

#     return distancias, caminhos

# # ========== TUDO NOVO ABAIXO DESTA LINHA ==========

# # 6. Gerando o Mapa Mágico Pelas Ruas! 🗺️
# def gerar_mapa(locais, rotas_para_pitar):
#     # Cria o centro do Mapa bem em cima da UEG de Ceres
#     mapa_ceres = folium.Map(location=locais["Universidade"], zoom_start=15)

#     # Coloca os Alfinetes (Marcadores) de cada local
#     for nome_local, coordenada in locais.items():
#         cor_icone = "green" if nome_local == "Universidade" else "blue"
#         folium.Marker(
#             location=coordenada, 
#             popup=nome_local, # O texto quando clica em cima
#             icon=folium.Icon(color=cor_icone)
#         ).add_to(mapa_ceres)

#     # Desenha as linhas que acompanham examente a geometria das ruas!
#     for coords_rua in rotas_para_pitar:
#         folium.PolyLine(coords_rua, color="red", weight=4, opacity=0.8).add_to(mapa_ceres)

#     # Salva tudo em uma página da web
#     mapa_ceres.save("Mapa_de_Rotas_Ceres.html")
#     print("\n✅ Sucesso! Abra o arquivo 'Mapa_de_Rotas_Ceres.html' no seu navegador para ver o mapa mágico seguindo as ruas!")

# # 7. Execução final
# menores_distancias, caminhos = dijkstra(grafo, "Universidade")
# print("🗺️ Menores distâncias de carro partindo da UEG:\n")
# for local, distancia in menores_distancias.items():
#     if distancia != float('inf') and local != "Universidade":
#         rota_formatada = " ➔ ".join(caminhos[local])
#         print(f"📍 {local}: {distancia:.2f} km")
#         print(f"   🛤️ Trajeto: {rota_formatada}\n")

# # Chama a função nova de gerar o mapa:
# gerar_mapa(locais, rotas_para_pitar)


import osmnx as ox
import networkx as nx
import folium

print("Baixando mapa de Ceres...")

# 1. Baixa o grafo real das ruas
G = ox.graph_from_place("Ceres, Goias, Brazil", network_type="drive")

# 2. Locais reais
locais = {
    "Universidade": (-15.310527768649527, -49.615869418078375),
    "Bombeiros": (-15.309443574756077, -49.61718842326959),
    "Policia": (-15.310115278311116, -49.619819693191786),
    "Orb": (-15.310388854207115, -49.596106926321326)
}

# 3. Conexões do grafo
grafo_conexoes = {
    "Universidade": ["Bombeiros", "Policia"],
    "Bombeiros": ["Orb", "Policia"],
    "Policia": ["Orb"],
    "Orb": []
}

# 4. Encontrar nós mais próximos no grafo real
nos = {}
for nome, coord in locais.items():
    no = ox.distance.nearest_nodes(G, coord[1], coord[0])
    nos[nome] = no

# 5. Criar mapa
mapa = folium.Map(location=locais["Universidade"], zoom_start=14)

# adicionar marcadores
for nome, coord in locais.items():

    cor = "green" if nome == "Universidade" else "blue"

    folium.Marker(
        coord,
        popup=nome,
        icon=folium.Icon(color=cor)
    ).add_to(mapa)

print("\nCalculando rotas...\n")

cores = ["red","blue","green","purple","orange","black"]

i = 0

# 6. Gerar todas as rotas do grafo
for origem, destinos in grafo_conexoes.items():

    for destino in destinos:

        print(f"Rota: {origem} -> {destino}")

        rota = nx.shortest_path(
            G,
            nos[origem],
            nos[destino],
            weight="length"
        )

        # calcular distância total
        distancia = nx.shortest_path_length(
            G,
            nos[origem],
            nos[destino],
            weight="length"
        )

        distancia_km = distancia / 1000

        print(f"Distância: {distancia_km:.2f} km\n")

        # coordenadas da rota
        coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in rota]

        # desenhar rota
        folium.PolyLine(
            coords,
            color=cores[i % len(cores)],
            weight=5,
            opacity=0.8,
            popup=f"{origem} → {destino} ({distancia_km:.2f} km)"
        ).add_to(mapa)

        i += 1

# 7. salvar mapa
mapa.save("Mapa_Rotas_Ceres.html")

print("Mapa criado com sucesso!")
print("Abra o arquivo: Mapa_Rotas_Ceres.html")