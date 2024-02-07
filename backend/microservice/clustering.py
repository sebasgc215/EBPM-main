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
    combined_text = f"{name} {purpose}"
    return combined_text


def cluster_user_stories(user_stories):

    # Combina información de nombre, propósito y dependencias en un solo texto
    combined_texts = [combine_text_information(story) for story in user_stories]
    
    # Etiqueta documentos para el entrenamiento de Doc2Vec
    tagged_documents = []
    for text, story in zip(combined_texts, user_stories):
        tagged_documents.append(TaggedDocument(text.split(), [story['id']]))

    # Entrenar modelo de Doc2Vec
    model = Doc2Vec(tagged_documents, vector_size=100, window=2, min_count=1, epochs=100)

    # Calcular vectores de historias considerando las dependencias
    #story_vectors = [model.infer_vector(text.split()) for text in combined_texts]
    story_vectors = []
    for story in user_stories:
        story_vector = model.infer_vector(story['name'].split())
        dependency_vectors = [model.infer_vector(dep['name'].split()) for dep in story.get('dependencies', [])]
        if dependency_vectors:
            max_dim = max(story_vector.shape[0] for story_vector in dependency_vectors)
            dependency_vectors = [np.pad(dep_vector, (0, max_dim - dep_vector.shape[0])) for dep_vector in dependency_vectors]
            avg_dependency_vector = np.mean(dependency_vectors, axis=0)
            story_vector = np.concatenate((story_vector, avg_dependency_vector))
        story_vectors.append(story_vector)

    # Determinar la dimensión máxima de los vectores de historias
    max_dim = max(story_vector.shape[0] for story_vector in story_vectors)

    # Rellenar los vectores de historias con ceros para asegurar dimensiones consistentes
    padded_story_vectors = [np.pad(story_vector, (0, max_dim - story_vector.shape[0])) for story_vector in story_vectors]

    # Convertir vectores de historias a un array
    story_vectors_array = np.array(padded_story_vectors)

    # Normalizar los datos
    #scaler = StandardScaler()
    #scaled_story_vectors_array = scaler.fit_transform(story_vectors_array)

    # Ajustar el número de componentes principales en PCA automáticamente
    #pca = PCA()
    #reduced_data = pca.fit_transform(scaled_story_vectors_array)

    # Encontrar el número de componentes que alcanzan el umbral de varianza explicada
    #cumulative_variance_ratio = np.cumsum(pca.explained_variance_ratio_)
    #num_components = np.argmax(cumulative_variance_ratio >= variance_threshold) + 1

    # Reajustar PCA con el número final de componentes
    #pca = PCA(n_components=num_components)
    #reduced_data = pca.fit_transform(scaled_story_vectors_array)

    # Encontrar el número óptimo de clústeres usando k-means
    #optimal_k_silhouette = find_optimal_k(reduced_data)
    optimal_k_silhouette = find_optimal_k(story_vectors_array)
    kmeans = KMeans(n_clusters=optimal_k_silhouette, random_state=42)
    #kmeans.fit(scaled_story_vectors_array)
    kmeans.fit(story_vectors_array)
    cluster_labels = kmeans.labels_

    # Crear diccionario de clústeres
    clusters = {i: [] for i in range(optimal_k_silhouette)}
    for i, (story_vector, story) in enumerate(zip(padded_story_vectors, user_stories)):
        clusters[cluster_labels[i]].append((story['id'], story['name'], int(story['points']),
                                        story['dependencies'], story['priority'], story['actor'], story['purpose']))


    return clusters



def find_optimal_k(data):
    range_clusters=(2, 10)
    if len(data) == 0:
        raise ValueError("La matriz de entrada 'data' está vacía")

    silhouette_scores = []

    for k in range(*range_clusters):
        kmeans = KMeans(n_clusters=k)
        cluster_labels = kmeans.fit_predict(data)
        silhouette_values = silhouette_samples(data, cluster_labels)
        avg_silhouette = silhouette_values.mean()
        silhouette_scores.append(avg_silhouette)

    optimal_k = range_clusters[0] + np.argmax(silhouette_scores)

    plt.plot(range(*range_clusters), silhouette_scores, marker='o')
    plt.xlabel('Número de clústeres (k)')
    plt.ylabel('Puntaje Silhouette promedio')
    plt.title('Selección de k utilizando Silhouette')
    plt.show()

    return optimal_k

