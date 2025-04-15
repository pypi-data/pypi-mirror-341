"""Functions for motif analysis in genomic data.

This module contains functions for analyzing transcription factor motifs
in genomic data, including computing motif scores and generating
in-silico ChIP-seq signals based on motif information.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import scipy.sparse as sp
from anndata import AnnData
from beartype import beartype

logger = logging.getLogger(__name__)


@beartype
def compute_motif_scores(
    motif_dir: Path,
    output_dir: Path,
    species: str,
    motif_database: str,
    genome_assembly: str,
    bed_file: Path = None,
    bed_peaks: pd.DataFrame = None,
    window_size: int = 0,
) -> pd.DataFrame:
    """Compute motif scores for genomic regions.

    Uses either FIMO or MOODS to scan motifs in given genomic regions.
    Supports providing regions as a BED file or as a DataFrame.

    Args:
        motif_dir: Directory containing motif files.
        output_dir: Directory to save output files.
        species: Species name (e.g., "mouse", "human").
        motif_database: Motif database name (e.g., "cisbp").
        genome_assembly: Genome assembly name (e.g., "mm10", "hg38").
        bed_file: Path to BED file with genomic regions. Either this or bed_peaks must be provided.
        bed_peaks: DataFrame with genomic regions in BED format. Either this or bed_file must be provided.
        window_size: Size of window around peaks to scan for motifs.

    Returns:
        DataFrame with motif scores for each region and each motif.
    """
    from stormi.preprocessing._file_utils import create_dir_if_not_exists
    from stormi.preprocessing._motif_fimo import run_fimo

    create_dir_if_not_exists(output_dir)

    # Write out the bed file if provided as a DataFrame
    if bed_file is None and bed_peaks is not None:
        bed_file = output_dir / "peaks.bed"
        bed_peaks.to_csv(bed_file, sep="\t", header=False, index=False)

    # Only one of bed_file or bed_peaks should be provided
    if bed_file is None and bed_peaks is None:
        raise ValueError("Either bed_file or bed_peaks must be provided")

    # Set correct paths
    motif_path = motif_dir / f"{motif_database}_{species}.meme"

    # Use FIMO from tangermeme
    logger.info("Using FIMO to scan motifs...")
    motif_df = run_fimo(
        motif_path=motif_path,
        genome_assembly=genome_assembly,
        bed_file=bed_file,
        output_dir=output_dir,
        window_size=window_size,
    )

    return motif_df


@beartype
def compute_in_silico_chipseq(
    adata_rna: AnnData,
    adata_atac: AnnData,
    motif_scores: pd.DataFrame,
    motif_score_min_percentile: float = 0,
    region_subset_cols: List[str] = None,
    activity_threshold: float = 0.0,
    rna_col: str = "gene",
    atac_col: str = "peak",
    score_col: str = "score",
    max_genes_per_peak: int = None,
    min_peaks_per_gene: int = 1,
    motif_key: str = "motifs",
    chipseq_key: str = "chipseq",
    binary_mode: bool = False,
    score_binarization_threshold: float = 0.25,
) -> Tuple[AnnData, AnnData]:
    """Compute in-silico ChIP-seq signals using RNA expression and ATAC-seq data.

    Integrates gene expression (RNA) and chromatin accessibility (ATAC) data to
    predict transcription factor binding, producing in-silico ChIP-seq signals.

    Args:
        adata_rna: AnnData object containing RNA data, with cells as rows, genes as columns.
        adata_atac: AnnData object containing ATAC data, with cells as rows, peaks as columns.
        motif_scores: DataFrame with motif scores for each region and each TF.
        motif_score_min_percentile: Minimum percentile of motif scores to keep. Scores below
            this percentile are set to 0. Default is 0 (no filtering).
        region_subset_cols: List of column names in motif_scores to use for subsetting.
            Default is None (no subsetting).
        activity_threshold: Minimum expression level for a TF to be considered active.
            Default is 0.0 (no filtering).
        rna_col: Column name in motif_scores containing gene names. Default is "gene".
        atac_col: Column name in motif_scores containing peak names. Default is "peak".
        score_col: Column name in motif_scores containing motif scores. Default is "score".
        max_genes_per_peak: Maximum number of genes to associate with each peak.
            Default is None (no limit).
        min_peaks_per_gene: Minimum number of peaks a gene must have to be included.
            Default is 1.
        motif_key: Key to store motif matrix in adata_atac.varm. Default is "motifs".
        chipseq_key: Key to store ChIP-seq matrix in adata_atac.layers. Default is "chipseq".
        binary_mode: Whether to binarize the motif scores. Default is False.
        score_binarization_threshold: Threshold for binarizing scores if binary_mode=True.
            Default is 0.25.

    Returns:
        Tuple of (adata_rna, adata_atac) with in-silico ChIP-seq data added.
    """
    logger.info("Computing in-silico ChIP-seq signals...")

    # 1. Filter motif scores
    final_scores = motif_scores.copy()
    if region_subset_cols is not None:
        for col_name in region_subset_cols:
            mask = final_scores[col_name].astype(bool)
            final_scores = final_scores[mask].copy()
            logger.info(
                f"Filtered motif scores by {col_name}, {len(final_scores)} rows left"
            )

    # 2. Check for genes/peaks in our data
    genes_present = [g in adata_rna.var_names for g in final_scores[rna_col]]
    peaks_present = [p in adata_atac.var_names for p in final_scores[atac_col]]

    mask = np.logical_and(genes_present, peaks_present)
    final_scores = final_scores[mask].copy()

    logger.info(
        f"After matching to data matrices: {len(final_scores)} motif score entries"
    )

    # 3. Apply score percentile filtering if requested
    if motif_score_min_percentile > 0:
        score_threshold = np.percentile(
            final_scores[score_col], motif_score_min_percentile
        )
        mask = final_scores[score_col] >= score_threshold
        final_scores = final_scores[mask].copy()
        logger.info(
            f"Filtered scores >= {score_threshold:.4f} "
            f"({motif_score_min_percentile}th percentile), "
            f"{len(final_scores)} rows left"
        )

    # 4. Limit number of genes per peak if requested
    if max_genes_per_peak is not None:
        peak_gene_counts = final_scores.groupby(atac_col).size()
        peaks_to_trim = peak_gene_counts[peak_gene_counts > max_genes_per_peak].index

        rows_to_keep = []
        for peak in peaks_to_trim:
            peak_rows = final_scores[final_scores[atac_col] == peak]
            # Sort by score and keep top max_genes_per_peak
            peak_rows = peak_rows.sort_values(score_col, ascending=False)
            rows_to_keep.append(peak_rows.iloc[:max_genes_per_peak])

        # Combine with rows for peaks that don't need trimming
        peaks_to_keep = set(final_scores[atac_col]) - set(peaks_to_trim)
        other_rows = final_scores[final_scores[atac_col].isin(peaks_to_keep)]

        if rows_to_keep:
            trimmed_rows = pd.concat(rows_to_keep)
            final_scores = pd.concat([other_rows, trimmed_rows])
        else:
            final_scores = other_rows

        logger.info(
            f"After limiting to {max_genes_per_peak} genes per peak: {len(final_scores)} rows"
        )

    # 5. Create a sparse matrix of genes x peaks with motif scores
    genes = sorted(list(set(final_scores[rna_col])))
    peaks = sorted(list(set(final_scores[atac_col])))

    gene_idx = {g: i for i, g in enumerate(genes)}
    peak_idx = {p: i for i, p in enumerate(peaks)}

    # Create sparse matrix
    motif_mat = sp.lil_matrix((len(genes), len(peaks)), dtype=np.float32)

    # Fill in the matrix with scores
    for _, row in final_scores.iterrows():
        g_idx = gene_idx[row[rna_col]]
        p_idx = peak_idx[row[atac_col]]
        score = row[score_col]
        motif_mat[g_idx, p_idx] = score

    # Convert to CSR for efficient operations
    motif_mat = motif_mat.tocsr()

    # 6. Filter genes with minimum peaks
    if min_peaks_per_gene > 0:
        gene_peak_counts = np.asarray(motif_mat.sum(axis=1)).flatten()
        genes_to_keep = np.where(gene_peak_counts >= min_peaks_per_gene)[0]
        motif_mat = motif_mat[genes_to_keep, :]
        genes = [genes[i] for i in genes_to_keep]

        logger.info(
            f"After filtering for min {min_peaks_per_gene} peaks per gene: {len(genes)} genes"
        )

    # 7. Process RNA data and create gene expression matrix
    adata_rna_subset = adata_rna[:, genes].copy()

    # 8. Create the gene x peak motif matrix for each cell
    n_cells = adata_atac.shape[0]
    n_peaks = adata_atac.shape[1]
    n_genes = len(genes)

    # Ensure atac_peaks and peaks are in the same order
    atac_peaks = list(adata_atac.var_names)
    peak_reorder = [peak_idx[p] for p in atac_peaks if p in peak_idx]

    # Reorder the motif matrix to match adata_atac.var_names
    motif_mat_reordered = sp.lil_matrix((n_genes, n_peaks), dtype=np.float32)
    for i, j in enumerate(peak_reorder):
        if j < motif_mat.shape[1]:  # Ensure j is within bounds
            motif_mat_reordered[:, i] = motif_mat[:, j]

    motif_mat_reordered = motif_mat_reordered.tocsr()

    # 9. Binarize scores if requested
    if binary_mode:
        # Binarize motif scores, and we'll also binarize ATAC
        motif_mat_reordered.data = (
            motif_mat_reordered.data >= score_binarization_threshold
        ).astype(np.float32)
        adata_atac.X = (adata_atac.X > 0).astype(np.float32)
        logger.info(
            f"Binarized motif scores with threshold {score_binarization_threshold}"
        )

    # 10. Create chip-seq matrix
    # For each cell, multiply: activity(gene) * motif_score(gene,peak) * accessibility(peak)
    gene_exp = adata_rna_subset.X.copy()  # cells x genes

    # Apply activity threshold if needed
    if activity_threshold > 0:
        # Using CSR or CSC for gene_exp
        if sp.issparse(gene_exp):
            gene_exp.data = (gene_exp.data > activity_threshold).astype(np.float32)
        else:
            gene_exp = (gene_exp > activity_threshold).astype(np.float32)

        logger.info(f"Applied TF activity threshold {activity_threshold}")

    # Save the motif matrix in adata_atac for reference
    genes_df = pd.DataFrame(index=genes)
    adata_atac.varm[motif_key] = motif_mat_reordered.T
    adata_atac.uns[f"{motif_key}_genes"] = genes_df

    # For each cell, compute cell_chip = gene_exp * motif_mat
    chipseq_mat = np.zeros((n_cells, n_peaks), dtype=np.float32)

    # Use matrix multiplication: (cells x genes) x (genes x peaks) = (cells x peaks)
    if sp.issparse(gene_exp):
        chipseq_mat = gene_exp @ motif_mat_reordered
    else:
        chipseq_mat = gene_exp @ motif_mat_reordered.toarray()

    # Element-wise multiply with ATAC accessibility
    atac_mat = adata_atac.X
    if sp.issparse(atac_mat):
        # Convert ATAC matrix to dense if necessary for element-wise multiplication
        if sp.issparse(chipseq_mat):
            chipseq_mat = chipseq_mat.multiply(atac_mat)
        else:
            # Convert dense chipseq to sparse for efficient multiplication
            chipseq_mat = sp.csr_matrix(chipseq_mat).multiply(atac_mat).toarray()
    else:
        # Both are dense
        if sp.issparse(chipseq_mat):
            chipseq_mat = chipseq_mat.toarray() * atac_mat
        else:
            chipseq_mat = chipseq_mat * atac_mat

    # Store result in layers
    adata_atac.layers[chipseq_key] = chipseq_mat

    logger.info(
        f"Computed in-silico ChIP-seq with {len(genes)} genes and {n_peaks} peaks. "
        f"Result in adata_atac.layers['{chipseq_key}']"
    )

    return adata_rna_subset, adata_atac
