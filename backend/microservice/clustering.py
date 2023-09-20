from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.cluster import KMeans
import numpy as np
import json
from sklearn.metrics import silhouette_score, silhouette_samples 

def cluster_text_user_stories(diagram_data):
    user_stories = json.loads(diagram_data['data']['json_user_stories'])

     # Convert user stories to tagged documents for doc2vec training
    tagged_documents = [TaggedDocument(story['name_us'].split(), [story['id_us']]) for story in user_stories]

    # Train a doc2vec model
    model = Doc2Vec(tagged_documents, vector_size=100, window=2, min_count=1, epochs=100)

    # Calculate story vectors considering dependencies
    story_vectors = []
    for story in user_stories:
        story_vector = model.infer_vector(story['name_us'].split())
        dependency_vectors = [model.infer_vector(dep.split()) for dep in story.get('dependencies', [])]
        if dependency_vectors:
            max_dim = max(story_vector.shape[0] for story_vector in dependency_vectors)
            dependency_vectors = [np.pad(dep_vector, (0, max_dim - dep_vector.shape[0])) for dep_vector in dependency_vectors]
            avg_dependency_vector = np.mean(dependency_vectors, axis=0)
            story_vector = np.concatenate((story_vector, avg_dependency_vector))
        story_vectors.append(story_vector)

    # Determine the maximum dimension of the story vectors
    max_dim = max(story_vector.shape[0] for story_vector in story_vectors)

    # Pad the story vectors with zeros to ensure consistent dimensions
    padded_story_vectors = [np.pad(story_vector, (0, max_dim - story_vector.shape[0])) for story_vector in story_vectors]

    # Convert story vectors to an array
    story_vectors_array = np.array(padded_story_vectors)

    # Cluster stories using k-means
    #num_clusters = find_optimal_k(story_vectors_array)
    optimal_k_silhouette = find_optimal_k(story_vectors_array)
    kmeans = KMeans(n_clusters=optimal_k_silhouette, random_state=0)
    kmeans.fit(story_vectors_array)
    cluster_labels = kmeans.labels_
    
    print("Optimal k: ",optimal_k_silhouette)
    # Create clusters dictionary
    clusters = {i: [] for i in range(optimal_k_silhouette)}
    for i, (story_vector, story) in enumerate(zip(padded_story_vectors, user_stories)):
        clusters[cluster_labels[i]].append((story['id_us'], story['name_us'], story['points']))

    return clusters


def cluster_user_stories(user_stories):
    # Convert user stories to tagged documents for doc2vec training
    tagged_documents = [TaggedDocument(story['name'].split(), [story['id']]) for story in user_stories]

    # Train a doc2vec model
    model = Doc2Vec(tagged_documents, vector_size=100, window=2, min_count=1, epochs=100)

    # Calculate story vectors considering dependencies
    story_vectors = []
    for story in user_stories:
        story_vector = model.infer_vector(story['name'].split())
        dependency_vectors = [model.infer_vector(dep.split()) for dep in story.get('dependencies', [])]
        if dependency_vectors:
            max_dim = max(story_vector.shape[0] for story_vector in dependency_vectors)
            dependency_vectors = [np.pad(dep_vector, (0, max_dim - dep_vector.shape[0])) for dep_vector in dependency_vectors]
            avg_dependency_vector = np.mean(dependency_vectors, axis=0)
            story_vector = np.concatenate((story_vector, avg_dependency_vector))
        story_vectors.append(story_vector)

    # Determine the maximum dimension of the story vectors
    max_dim = max(story_vector.shape[0] for story_vector in story_vectors)

    # Pad the story vectors with zeros to ensure consistent dimensions
    padded_story_vectors = [np.pad(story_vector, (0, max_dim - story_vector.shape[0])) for story_vector in story_vectors]

    # Convert story vectors to an array
    story_vectors_array = np.array(padded_story_vectors)

    # Cluster stories using k-means
    #num_clusters = find_optimal_k(story_vectors_array)
    optimal_k_silhouette = find_optimal_k(story_vectors_array)
    kmeans = KMeans(n_clusters=optimal_k_silhouette, random_state=0)
    kmeans.fit(story_vectors_array)
    cluster_labels = kmeans.labels_
    
    print("Optimal k: ",optimal_k_silhouette)
    # Create clusters dictionary
    clusters = {i: [] for i in range(optimal_k_silhouette)}
    for i, (story_vector, story) in enumerate(zip(padded_story_vectors, user_stories)):
        clusters[cluster_labels[i]].append((story['id'], story['name'], story['points']))

    return clusters

def find_optimal_k(data):
    if len(data) == 0:
        # Handle the case where the input is empty
        raise ValueError("Input array 'data' is empty")

    n_samples = len(data)
    print(n_samples)
    silhouette_scores = []

    for k in range(2, n_samples):
        kmeans = KMeans(n_clusters=k)
        cluster_labels = kmeans.fit_predict(data)
        silhouette_values = silhouette_samples(data, cluster_labels)
        avg_silhouette = silhouette_values.mean()
        silhouette_scores.append(avg_silhouette)

    # Find the index of the maximum silhouette score
    optimal_k = np.argmax(silhouette_scores) + 2

    return optimal_k