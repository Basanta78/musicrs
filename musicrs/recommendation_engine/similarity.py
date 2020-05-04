import faiss
from operator import itemgetter


def index_database_vector(dimension, database_vectors):
    """
    Index the database vector(i.e our song embeddings) using faiss
    :param dimension: dimension of the database vector
    :param database_vectors: database vector/song embeddings
    :return: index
    """

    faiss.normalize_L2(database_vectors)  # Normalize the vectors

    index = faiss.IndexFlatIP(
        dimension
    )  # Initialize index for the vector with dimension d
    index.add(database_vectors)  # Add database vector for indexing

    return index


def search(index, user_vector, k=1):
    """
    Search most similar vector from database_vector given query_vector

    :param index: index
    :param user_vector: query vectors of a user
    :param k: number of nearest neighbour vector for each query
    :return: similar sorted vector result
    """

    faiss.normalize_L2(user_vector)
    cosine, near_index = index.search(
        user_vector, k
    )  # Returns cosine similarity and index of the nearest neighbour vectors

    result_tuple = zip(cosine.flatten(), near_index.flatten())

    # Sort the result in descending order so the most similar is always the first
    similar_vector_index_sorted = []
    for x in result_tuple:
        similar_vector_index_sorted.append(x)
    # similar_vector_index_sorted.sort(key=operator.itemgetter(0), reverse=True)
    return similar_vector_index_sorted


def get_max_similarity(data_list):
    """
    Get max similar value
    :param data_list: data list to check: list of tuples
    :return: max value tuple
    """
    index = 0
    res = max(data_list, key=itemgetter(index))
    return res
