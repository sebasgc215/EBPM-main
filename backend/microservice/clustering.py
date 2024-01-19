from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.cluster import KMeans
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import silhouette_samples
import matplotlib.pyplot as plt

def combine_text_information(story):
    name = story['name']
    purpose = story.get('purpose', '')
    dependencies = ' '.join(dep['name'] for dep in story.get('dependencies', []))
    combined_text = f"{name} {purpose} {dependencies}"
    return combined_text


def cluster_user_stories(user_stories, variance_threshold=0.95):

    # Combina información de nombre, propósito y dependencias en un solo texto
    combined_texts = [combine_text_information(story) for story in user_stories]
    
    # Etiqueta documentos para el entrenamiento de Doc2Vec
    tagged_documents = []
    for text, story in zip(combined_texts, user_stories):
        dependencies_text = ' '.join(dep['name'] for dep in story.get('dependencies', []))
        combined_text_with_dependencies = f"{text} {dependencies_text}"
        tagged_documents.append(TaggedDocument(combined_text_with_dependencies.split(), [story['id']]))

    # Entrenar modelo de Doc2Vec
    model = Doc2Vec(tagged_documents, vector_size=100, window=2, min_count=1, epochs=100)

    # Calcular vectores de historias considerando las dependencias
    story_vectors = [model.infer_vector(text.split()) for text in combined_texts]

    # Determinar la dimensión máxima de los vectores de historias
    max_dim = max(story_vector.shape[0] for story_vector in story_vectors)

    # Rellenar los vectores de historias con ceros para asegurar dimensiones consistentes
    padded_story_vectors = [np.pad(story_vector, (0, max_dim - story_vector.shape[0])) for story_vector in story_vectors]

    # Convertir vectores de historias a un array
    story_vectors_array = np.array(padded_story_vectors)

    # Normalizar los datos
    scaler = StandardScaler()
    scaled_story_vectors_array = scaler.fit_transform(story_vectors_array)

    # Ajustar el número de componentes principales en PCA automáticamente
    pca = PCA()
    reduced_data = pca.fit_transform(scaled_story_vectors_array)

    # Encontrar el número de componentes que alcanzan el umbral de varianza explicada
    cumulative_variance_ratio = np.cumsum(pca.explained_variance_ratio_)
    num_components = np.argmax(cumulative_variance_ratio >= variance_threshold) + 1

    # Reajustar PCA con el número final de componentes
    pca = PCA(n_components=num_components)
    reduced_data = pca.fit_transform(scaled_story_vectors_array)

    # Encontrar el número óptimo de clústeres usando k-means
    optimal_k_silhouette = find_optimal_k(reduced_data)
    kmeans = KMeans(n_clusters=optimal_k_silhouette, random_state=0)
    kmeans.fit(scaled_story_vectors_array)
    cluster_labels = kmeans.labels_

    # Crear diccionario de clústeres
    clusters = {i: [] for i in range(optimal_k_silhouette)}
    for i, (story_vector, story) in enumerate(zip(padded_story_vectors, user_stories)):
        clusters[cluster_labels[i]].append((story['id'], story['name'], int(story['points']),
                                        story['dependencies'], story['priority'], story['actor'], story['purpose']))


    return clusters

# Resto del código sigue igual

def find_optimal_k(data):
    if len(data) == 0:
        raise ValueError("La matriz de entrada 'data' está vacía")

    n_samples = len(data)
    silhouette_scores = []

    for k in range(2, n_samples):
        kmeans = KMeans(n_clusters=k)
        cluster_labels = kmeans.fit_predict(data)
        silhouette_values = silhouette_samples(data, cluster_labels)
        avg_silhouette = silhouette_values.mean()
        silhouette_scores.append(avg_silhouette)

    optimal_k = np.argmax(silhouette_scores) + 2

    plt.plot(range(2, n_samples), silhouette_scores, marker='o')
    plt.xlabel('Número de clústeres (k)')
    plt.ylabel('Puntaje Silhouette promedio')
    plt.title('Selección de k utilizando Silhouette')
    plt.show()

    return optimal_k

