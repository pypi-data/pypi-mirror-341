# PatANN - Pattern-Aware Vector Database / ANN

## Overview
PatANN is a pattern-aware, massively parallel, distributed, and scalable vector database algorithm and framework for efficient nearest neighbor search, operating both in-memory and on-disk.

Unlike conventional algorithms, PatANN extracts and hashes patterns from vectors, and use them for initial filtering before performing expensive distance computations. During a search, PatANN first examines these pattern hashes to identify a subset of vectors that share similar patterns with the query vector. Only after this preliminary filtering does PatANN apply traditional distance metrics (Euclidean, cosine, etc.) to this smaller candidate set.

However, the actual implementation is more involved. Vectors are encoded at multiple resolutions, capturing both macro and micro patterns within the data. This multi-scale approach ensures that both broad similarities and fine details are captured. The patterns are hashed to maintain locality of reference, minimizing cross-shard communication during searches. PatANN also uses recursive patterns to mitigate the curse of dimensionality and hubness in high-dimensional data. The system dynamically selects which patterns to prioritize based on the distribution characteristics of the vector space, optimizing for the specific dataset. Additionally, PatANN employs probabilistic matching rather than exact pattern matching to achieve massive speed advantages while maintaining high recall. A detailed research paper is forthcoming.

### Performance Implications
While still in beta, this pattern-first, details-later approach results in significant performance advantages. PatANN outperforms conventional ANN libraries including HNSW, Google ScaNN, Microsoft DiskANN, and Facebook FAISS by a substantial margin, with superior recall and speed. Detailed benchmarks conducted using industry-standard ann-benchmarks are available at https://patann.dev.

By filtering candidates based on patterns before computing exact distances, PatANN drastically reduces the number of expensive distance calculations.

For disk-based operations, pattern probing allows PatANN to be more selective about which vectors to load from disk, minimizing I/O operations.

Pattern probing operations are highly parallelized, taking advantage of modern CPU architectures and distributed computing environments. Also, as dataset size increases, the efficiency gains from pattern probing become more pronounced, making PatANN particularly effective for very large-scale vector databases.

### Mathematical Foundation
The pattern probing approach is grounded in information theory and dimensionality reduction techniques. While traditional methods like locality-sensitive hashing (LSH) approximate similarity through random projections, PatANN's pattern probing uses a more structured approach that:

1. Identifies statistically significant patterns in the vector space
2. Leverages these patterns to create a hierarchical filtering system
3. Dynamically adjusts the pattern sensitivity based on the density and distribution of the vector space

This mathematically rigorous foundation ensures that PatANN maintains high recall rates while achieving substantial speedups over conventional ANN implementations.

By combining this pattern probing technique with traditional distance metrics in a tiered approach, PatANN achieves both speed and accuracy, representing a significant advancement in vector search technology.

## Platforms
- Linux
- macOS (Apple Silicon)
- Windows
- Android
- iOS

## Key Distinguishing Features
- Novel pattern-based probing technique for ANN search
- In-Memory, On-Disk and Hybrid Index
- Refined search, filtering and pagination algorithm
- Unlimited scalability without pre-specified capacity
- Dynamic sharding to load balance across servers
- Cloud (in-progress) and Serverless
- SIMD-Accelerated for both x86_64 (SSE*, AVX2, AVX-512), and ARM (NEON, SVE) Platforms
- OS-optimized I/O--huge (Linux), large (Windows), and super (macOS) 
- NUMA-aware architecture

## Status
**Beta Version**: Currently in Beta. Not for production use yet.

## Contributions
We are seeking help to:

- Run additional datasets. So far, all tested datasets (including self-generated) exhibit patterns that helps algorithm. We have yet to test datasets without clear patterns or with uniform distribution.
- Validate and improve the algorithm

## Contact
For support / questions, please contact: support@mesibo.com

