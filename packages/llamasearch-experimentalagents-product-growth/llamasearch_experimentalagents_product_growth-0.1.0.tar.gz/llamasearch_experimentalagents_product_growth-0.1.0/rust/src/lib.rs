use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::Python;
use pyo3::types::{PyDict, PyList};
use ndarray::{Array1, Array2, Axis};
use rayon::prelude::*;
use std::time::Instant;
use anyhow::{Result, anyhow};
use thiserror::Error;

/// Errors that can occur in the Rust extension
#[derive(Error, Debug)]
pub enum LlamaSearchError {
    #[error("Invalid input dimensions: {0}")]
    InvalidDimensions(String),
    
    #[error("Computation error: {0}")]
    ComputationError(String),
    
    #[error("Empty input data")]
    EmptyInput,
}

/// Compute cosine similarity between a query vector and a matrix of document vectors
/// 
/// Args:
///     query: A 1D array representing the query vector
///     docs: A 2D array where each row is a document vector
/// 
/// Returns:
///     A 1D array of cosine similarity scores
#[pyfunction]
fn cosine_similarity(py: Python<'_>, query: Vec<f32>, docs: Vec<Vec<f32>>) -> PyResult<Vec<f32>> {
    if docs.is_empty() {
        return Err(LlamaSearchError::EmptyInput.into());
    }
    
    let query_len = query.len();
    if docs.iter().any(|doc| doc.len() != query_len) {
        return Err(LlamaSearchError::InvalidDimensions(
            "All document vectors must have the same dimension as the query vector".to_string()
        ).into());
    }
    
    // Convert query to ndarray
    let query_array = Array1::from_vec(query);
    let query_norm = query_array.dot(&query_array).sqrt();
    
    if query_norm == 0.0 {
        return Err(LlamaSearchError::ComputationError(
            "Query vector has zero norm".to_string()
        ).into());
    }
    
    // Calculate similarities in parallel
    let results: Vec<f32> = docs.par_iter().map(|doc| {
        let doc_array = Array1::from_vec(doc.clone());
        let doc_norm = doc_array.dot(&doc_array).sqrt();
        
        if doc_norm == 0.0 {
            return 0.0;
        }
        
        let dot_product = query_array.dot(&doc_array);
        dot_product / (query_norm * doc_norm)
    }).collect();
    
    Ok(results)
}

/// Perform K-means clustering on a matrix of vectors
/// 
/// Args:
///     vectors: A 2D array where each row is a vector to cluster
///     k: Number of clusters
///     max_iterations: Maximum number of iterations (default: 100)
///     tolerance: Convergence tolerance (default: 1e-4)
/// 
/// Returns:
///     A tuple of (cluster_labels, centroids)
#[pyfunction]
fn kmeans_clustering(
    py: Python<'_>, 
    vectors: Vec<Vec<f32>>, 
    k: usize,
    max_iterations: Option<usize>,
    tolerance: Option<f32>
) -> PyResult<(Vec<usize>, Vec<Vec<f32>>)> {
    if vectors.is_empty() {
        return Err(LlamaSearchError::EmptyInput.into());
    }
    
    if k == 0 || k > vectors.len() {
        return Err(LlamaSearchError::InvalidDimensions(
            format!("Invalid k: {}, must be between 1 and {}", k, vectors.len())
        ).into());
    }
    
    let max_iterations = max_iterations.unwrap_or(100);
    let tolerance = tolerance.unwrap_or(1e-4);
    
    // Convert input to ndarray
    let n_samples = vectors.len();
    let n_features = vectors[0].len();
    
    // Check that all vectors have the same dimensions
    if vectors.iter().any(|v| v.len() != n_features) {
        return Err(LlamaSearchError::InvalidDimensions(
            "All vectors must have the same dimension".to_string()
        ).into());
    }
    
    // Flatten vectors into a single array and convert to Array2
    let data_flat: Vec<f32> = vectors.iter().flat_map(|v| v.iter().cloned()).collect();
    let data = Array2::from_shape_vec((n_samples, n_features), data_flat)?;
    
    // Initialize centroids by selecting k random samples
    let mut rng = rand::thread_rng();
    let mut indices: Vec<usize> = (0..n_samples).collect();
    indices.shuffle(&mut rng);
    let centroid_indices = &indices[0..k];
    
    let mut centroids = Array2::zeros((k, n_features));
    for (i, &idx) in centroid_indices.iter().enumerate() {
        centroids.row_mut(i).assign(&data.row(idx));
    }
    
    let mut labels = vec![0; n_samples];
    let mut old_inertia = f32::INFINITY;
    
    // Main K-means loop
    for iteration in 0..max_iterations {
        // Assign samples to nearest centroid
        for (i, sample) in data.outer_iter().enumerate() {
            let mut min_dist = f32::INFINITY;
            let mut min_idx = 0;
            
            for (j, centroid) in centroids.outer_iter().enumerate() {
                let dist: f32 = sample
                    .iter()
                    .zip(centroid.iter())
                    .map(|(&a, &b)| (a - b).powi(2))
                    .sum();
                
                if dist < min_dist {
                    min_dist = dist;
                    min_idx = j;
                }
            }
            
            labels[i] = min_idx;
        }
        
        // Update centroids
        let mut new_centroids = Array2::zeros((k, n_features));
        let mut counts = vec![0; k];
        
        for (i, sample) in data.outer_iter().enumerate() {
            let cluster = labels[i];
            counts[cluster] += 1;
            
            for (j, &value) in sample.iter().enumerate() {
                new_centroids[[cluster, j]] += value;
            }
        }
        
        // Normalize by cluster size
        for i in 0..k {
            if counts[i] > 0 {
                for j in 0..n_features {
                    new_centroids[[i, j]] /= counts[i] as f32;
                }
            }
        }
        
        // Calculate inertia (sum of squared distances to closest centroid)
        let inertia: f32 = data
            .outer_iter()
            .enumerate()
            .map(|(i, sample)| {
                let cluster = labels[i];
                sample
                    .iter()
                    .zip(new_centroids.row(cluster).iter())
                    .map(|(&a, &b)| (a - b).powi(2))
                    .sum::<f32>()
            })
            .sum();
        
        // Check for convergence
        let inertia_change = (old_inertia - inertia).abs();
        if inertia_change < tolerance {
            break;
        }
        
        old_inertia = inertia;
        centroids = new_centroids;
    }
    
    // Convert centroids back to Vec<Vec<f32>>
    let centroids_vec: Vec<Vec<f32>> = centroids
        .outer_iter()
        .map(|row| row.iter().cloned().collect())
        .collect();
    
    Ok((labels, centroids_vec))
}

/// Extract keyword embeddings from text
/// 
/// Args:
///     texts: A list of text strings
///     top_n: Number of keywords to extract per text
/// 
/// Returns:
///     A list of extracted keywords for each text
#[pyfunction]
fn extract_keywords(py: Python<'_>, texts: Vec<String>, top_n: Option<usize>) -> PyResult<Vec<Vec<String>>> {
    let top_n = top_n.unwrap_or(5);
    
    // Simple keyword extraction based on term frequency
    // In a real implementation, this would use a more sophisticated algorithm
    
    // For each text, split into words, count frequencies, and return top N
    let results: Vec<Vec<String>> = texts
        .par_iter()
        .map(|text| {
            // Normalize text: lowercase and remove punctuation
            let normalized = text
                .to_lowercase()
                .chars()
                .map(|c| if c.is_alphanumeric() || c.is_whitespace() { c } else { ' ' })
                .collect::<String>();
            
            // Split into words
            let words: Vec<&str> = normalized
                .split_whitespace()
                .collect();
            
            // Count word frequencies
            let mut word_counts: std::collections::HashMap<&str, usize> = std::collections::HashMap::new();
            for word in &words {
                *word_counts.entry(word).or_insert(0) += 1;
            }
            
            // Filter out stop words (simplified list)
            let stop_words = ["the", "a", "an", "and", "or", "but", "is", "are", "was", "were", 
                             "in", "on", "at", "to", "for", "with", "by", "of", "this", "that"];
            
            for stop_word in &stop_words {
                word_counts.remove(stop_word);
            }
            
            // Sort by frequency and take top N
            let mut word_counts_vec: Vec<(&str, usize)> = word_counts.into_iter().collect();
            word_counts_vec.sort_by(|a, b| b.1.cmp(&a.1));
            
            word_counts_vec
                .iter()
                .take(top_n)
                .map(|(word, _)| word.to_string())
                .collect()
        })
        .collect();
    
    Ok(results)
}

/// Calculate sentiment scores for a list of texts
/// 
/// Args:
///     texts: A list of text strings
///     positive_words: A list of positive sentiment words
///     negative_words: A list of negative sentiment words
/// 
/// Returns:
///     A list of sentiment scores between -1.0 and 1.0
#[pyfunction]
fn calculate_sentiment(
    py: Python<'_>, 
    texts: Vec<String>, 
    positive_words: Option<Vec<String>>, 
    negative_words: Option<Vec<String>>
) -> PyResult<Vec<f32>> {
    // Default sentiment lexicons if not provided
    let pos_words = positive_words.unwrap_or_else(|| vec![
        "good", "great", "excellent", "amazing", "love", "best", "helpful",
        "nice", "fantastic", "awesome", "wonderful", "happy", "impressed",
        "like", "positive", "easy", "perfect", "recommend", "fast", "beautiful"
    ].iter().map(|&s| s.to_string()).collect());
    
    let neg_words = negative_words.unwrap_or_else(|| vec![
        "bad", "poor", "terrible", "worst", "hate", "difficult", "issue",
        "problem", "slow", "disappointed", "frustrating", "annoying", "bug",
        "expensive", "negative", "confusing", "error", "broken", "hard", "wrong"
    ].iter().map(|&s| s.to_string()).collect());
    
    // Calculate sentiment scores
    let sentiments: Vec<f32> = texts
        .par_iter()
        .map(|text| {
            let text_lower = text.to_lowercase();
            let words: Vec<&str> = text_lower.split_whitespace().collect();
            
            let mut positive_count = 0;
            let mut negative_count = 0;
            
            for word in words {
                // Check if word contains a positive or negative term
                // (allows for partial matching, e.g. "helpful" matches in "unhelpful")
                if pos_words.iter().any(|pos| word.contains(pos)) {
                    positive_count += 1;
                }
                
                if neg_words.iter().any(|neg| word.contains(neg)) {
                    negative_count += 1;
                }
            }
            
            let total = positive_count + negative_count;
            if total > 0 {
                (positive_count as f32 - negative_count as f32) / total as f32
            } else {
                0.0 // Neutral if no sentiment words
            }
        })
        .collect();
    
    Ok(sentiments)
}

/// Benchmark different implementations of vector operations
/// 
/// Args:
///     vector_size: Size of test vectors
///     num_vectors: Number of vectors to process
///     num_iterations: Number of iterations for the benchmark
/// 
/// Returns:
///     A dictionary with benchmark results
#[pyfunction]
fn benchmark_vector_ops(
    py: Python<'_>,
    vector_size: usize,
    num_vectors: usize,
    num_iterations: usize
) -> PyResult<PyObject> {
    // Generate random test data
    let mut rng = rand::thread_rng();
    
    // Create query vector
    let query: Vec<f32> = (0..vector_size)
        .map(|_| rng.gen::<f32>())
        .collect();
    
    // Create document vectors
    let docs: Vec<Vec<f32>> = (0..num_vectors)
        .map(|_| (0..vector_size).map(|_| rng.gen::<f32>()).collect())
        .collect();
    
    // Run benchmarks
    let start = Instant::now();
    for _ in 0..num_iterations {
        let _ = cosine_similarity(py, query.clone(), docs.clone())?;
    }
    let cosine_sim_time = start.elapsed().as_micros() as f64 / (num_iterations as f64 * 1000.0); // ms
    
    // Create result dictionary
    let results = PyDict::new(py);
    results.set_item("rust_cosine_similarity_ms", cosine_sim_time)?;
    results.set_item("vector_size", vector_size)?;
    results.set_item("num_vectors", num_vectors)?;
    
    Ok(results.into())
}

/// Analyze top words by topic
///
/// Args:
///     texts: List of text documents
///     topics: List of topic assignments for each document
///     num_topics: Total number of topics
///     top_n: Number of top words to extract per topic
///
/// Returns:
///     A dictionary mapping topic IDs to lists of top words
#[pyfunction]
fn analyze_topic_keywords(
    py: Python<'_>,
    texts: Vec<String>,
    topics: Vec<usize>,
    num_topics: usize,
    top_n: Option<usize>
) -> PyResult<PyObject> {
    if texts.len() != topics.len() {
        return Err(LlamaSearchError::InvalidDimensions(
            "Number of texts must match number of topic assignments".to_string()
        ).into());
    }
    
    let top_n = top_n.unwrap_or(10);
    
    // Group texts by topic
    let mut topic_texts: Vec<Vec<String>> = vec![Vec::new(); num_topics];
    for (i, &topic) in topics.iter().enumerate() {
        if topic < num_topics {
            topic_texts[topic].push(texts[i].clone());
        }
    }
    
    // Extract keywords for each topic
    let topic_keywords: Vec<Vec<String>> = topic_texts
        .par_iter()
        .map(|texts| {
            if texts.is_empty() {
                return Vec::new();
            }
            
            // Combine all texts for this topic
            let combined_text = texts.join(" ");
            
            // Extract keywords (similar to the function above)
            let normalized = combined_text
                .to_lowercase()
                .chars()
                .map(|c| if c.is_alphanumeric() || c.is_whitespace() { c } else { ' ' })
                .collect::<String>();
            
            let words: Vec<&str> = normalized.split_whitespace().collect();
            
            let mut word_counts: std::collections::HashMap<&str, usize> = std::collections::HashMap::new();
            for word in &words {
                *word_counts.entry(word).or_insert(0) += 1;
            }
            
            // Filter out stop words
            let stop_words = ["the", "a", "an", "and", "or", "but", "is", "are", "was", "were", 
                             "in", "on", "at", "to", "for", "with", "by", "of", "this", "that"];
            
            for stop_word in &stop_words {
                word_counts.remove(stop_word);
            }
            
            // Sort by frequency and take top N
            let mut word_counts_vec: Vec<(&str, usize)> = word_counts.into_iter().collect();
            word_counts_vec.sort_by(|a, b| b.1.cmp(&a.1));
            
            word_counts_vec
                .iter()
                .take(top_n)
                .map(|(word, _)| word.to_string())
                .collect()
        })
        .collect();
    
    // Convert to Python dictionary
    let result = PyDict::new(py);
    for (topic_id, keywords) in topic_keywords.iter().enumerate() {
        let py_keywords = PyList::new(py, keywords);
        result.set_item(topic_id.to_string(), py_keywords)?;
    }
    
    Ok(result.into())
}

/// Python module configuration
#[pymodule]
fn llamasearch_experimentalagents_product_growth_rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(cosine_similarity, m)?)?;
    m.add_function(wrap_pyfunction!(kmeans_clustering, m)?)?;
    m.add_function(wrap_pyfunction!(extract_keywords, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_sentiment, m)?)?;
    m.add_function(wrap_pyfunction!(benchmark_vector_ops, m)?)?;
    m.add_function(wrap_pyfunction!(analyze_topic_keywords, m)?)?;
    Ok(())
} 