# cosine_utils.pyx

import numpy as np
cimport numpy as np

def cosine_similarity_percentage(np.ndarray[np.float32_t, ndim=1] vec1, np.ndarray[np.float32_t, ndim=1] vec2):
    """
    Compute cosine similarity between two vectors and return as a percentage.

    Args:
        vec1 (np.ndarray): First input vector.
        vec2 (np.ndarray): Second input vector.

    Returns:
        float: Cosine similarity as a percentage.
    """
    cdef float dot_product, norm1, norm2
    cdef int i, n = vec1.shape[0]
    
    # Compute dot product
    dot_product = 0.0
    for i in range(n):
        dot_product += vec1[i] * vec2[i]
    
    # Compute norms (L2 norms)
    norm1 = 0.0
    norm2 = 0.0
    for i in range(n):
        norm1 += vec1[i] * vec1[i]
        norm2 += vec2[i] * vec2[i]
    
    # Calculate cosine similarity
    similarity = dot_product / (np.sqrt(norm1) * np.sqrt(norm2) + 1e-10)  # Add epsilon to avoid division by zero
    
    return similarity * 100  # Convert to percentage
