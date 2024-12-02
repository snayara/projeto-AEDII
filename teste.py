import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def busca_forca_bruta(text, pattern):
    m = len(pattern)
    n = len(text)

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            return i  # Padrão encontrado
    return -1  # Não encontrado


def busca_boyer_moore(text, pattern):
    # Função de busca Boyer-Moore para localizar padrão no texto
    m = len(pattern)
    n = len(text)

    # Construir a tabela de deslocamento para "bad character"
    bad_char_shift = {}
    for i in range(m - 1):
        bad_char_shift[pattern[i]] = m - i - 1

    # Inicializar o deslocamento
    shift = 0
    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            # Padrão encontrado
            return shift
        else:
            # Deslocamento baseado no caractere ruim
            bad_char = text[shift + j]
            shift += bad_char_shift.get(bad_char, m)
    return -1  # Não encontrado


def detecta_plagio(doc1, doc2, tipo, frase_length=2):
    palavras1 = doc1.split()
    palavras2 = doc2.split()
    
    total_frases = 0
    matching_frases = 0

    for i in range(len(palavras1) - frase_length + 1):
        frase = ' '.join(palavras1[i:i + frase_length])
        total_frases += 1

        if tipo == 'forca bruta':
            # Verificar se a frase existe no doc2 usando Força Bruta
            if busca_forca_bruta(' '.join(palavras2), frase) != -1:
                matching_frases += 1  # Contador de frases coincidentes
        else:
            # Verificar se a frase existe no doc2 usando Boyer-Moore
            if busca_boyer_moore(' '.join(palavras2), frase) != -1:
                matching_frases += 1  # Contador de frases coincidentes

    # Calcular porcentagem de plágio
    percentual_plagio = (matching_frases / total_frases) * 100 if total_frases > 0 else 0
    return percentual_plagio, matching_frases, total_frases


# Exemplo de uso com dois documentos
# Caso 1: a com a1
# Caso 2: a com a2  
# Caso 3: b com b1
# Caso 4: b com b2
doc1_path = 'docs/texto-b.txt'
doc2_path = 'docs/texto-b2.txt'
with open(doc1_path, 'r') as file:
    doc1 = file.read()
with open(doc2_path, 'r') as file:
    doc2 = file.read()

#Força bruta
start_fb = time.time()
percentual_plagio, matching_frases, total_frases = detecta_plagio(doc1, doc2, 'forca bruta', frase_length=2)
end_fb = time.time()
print(f"Porcentagem de plágio FROÇA BRUTA: {percentual_plagio:.2f}%")
print(f"Frases coincidentes: {matching_frases} de {total_frases}")
print(f"Tempo de execução {(end_fb-start_fb) * 10**3}ms")

#Boyer Moore
start_bm = time.time()
percentual_plagio, matching_frases, total_frases = detecta_plagio(doc1, doc2, 'boyer moore', frase_length=3)
end_bm = time.time()
print(f"Porcentagem de plágio BOYER MOORE: {percentual_plagio:.2f}%")
print(f"Frases coincidentes: {matching_frases} de {total_frases}")
print(f"Tempo de execução {(end_bm-start_bm) * 10**3}ms")

# Plotar gráfico
labels = ['Força Bruta', 'Boyer-Moore']
times = [end_fb-start_fb, end_bm-start_bm]
plt.bar(labels, times)
plt.ylabel('Tempo de execução (ms)')
plt.title('Tempo de execução dos algoritmos')
plt.show()