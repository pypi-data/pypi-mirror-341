"""Functions for constructing preprocessing pipelines for genomics data.

This module contains functions for building preprocessing pipelines that combine
multiple processing steps for single-cell genomics data, particularly for
RNA-seq and ATAC-seq data integration.
"""

import logging
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import scipy.sparse as sp
from anndata import AnnData
from beartype import beartype

from stormi.preprocessing._filtering import (
    filter_genes,
    filter_motif_scores,
    filter_regions,
)
from stormi.preprocessing._motifs import compute_in_silico_chipseq, compute_motif_scores

logger = logging.getLogger(__name__)


@beartype
def make_multiomic_dataset(
    adata_rna: AnnData,
    adata_atac: AnnData,
    motif_scores: pd.DataFrame = None,
    species: str = "mouse",
    genome_assembly: str = "mm10",
    motif_database: str = "cisbp",
    motif_dir: Path = None,
    output_dir: Path = None,
    hvg_flavor: str = "highly_variable",
    hvg_fraction: float = 0.1,
    hvg_key: str = None,
    protein_coding_only: bool = True,
    filter_mt_genes: bool = True,
    min_cells_per_peak: int = 10,
    peak_score_percentile: float = 90,
    score_thresh_mode: str = "score",
    promoter_only: bool = False,
    tf_chip_binary: bool = False,
    max_genes_per_peak: int = None,
    min_peaks_per_gene: int = 1,
    motif_score_percentile: float = 0,
) -> Tuple[AnnData, AnnData]:
    """Create a multiomics dataset from RNA-seq and ATAC-seq data.

    Integrates RNA-seq and ATAC-seq data by filtering genes and peaks, computing
    motif scores, and generating in-silico ChIP-seq signals.

    Args:
        adata_rna: AnnData object containing RNA data, with cells as rows, genes as columns.
        adata_atac: AnnData object containing ATAC data, with cells as rows, peaks as columns.
        motif_scores: DataFrame with motif scores, or None to compute them.
        species: Species name, e.g., "mouse", "human". Default is "mouse".
        genome_assembly: Genome assembly, e.g., "mm10", "hg38". Default is "mm10".
        motif_database: Motif database to use, e.g., "cisbp". Default is "cisbp".
        motif_dir: Directory containing motif files. Required if motif_scores is None.
        output_dir: Directory to save output files. Required if motif_scores is None.
        hvg_flavor: Method for HVG selection, one of "highly_variable" or "TF_HVG".
            Default is "highly_variable".
        hvg_fraction: Fraction of genes to select as highly variable. Default is 0.1.
        hvg_key: Key in adata_rna.var to store HVG boolean. Default is None (inferred).
        protein_coding_only: Whether to filter for protein-coding genes. Default is True.
        filter_mt_genes: Whether to filter out mitochondrial genes. Default is True.
        min_cells_per_peak: Minimum number of cells a peak must be detected in.
            Default is 10.
        peak_score_percentile: Percentile threshold for peak scores. Default is 90.
        score_thresh_mode: How to calculate peak scores, one of "score" or "std".
            Default is "score".
        promoter_only: Whether to keep only promoter regions. Default is False.
        tf_chip_binary: Whether to binarize the ChIP-seq data. Default is False.
        max_genes_per_peak: Maximum number of genes to associate with each peak.
            Default is None (no limit).
        min_peaks_per_gene: Minimum number of peaks a gene must have. Default is 1.
        motif_score_percentile: Minimum percentile for motif scores. Default is 0.

    Returns:
        Tuple of (filtered_adata_rna, filtered_adata_atac) with integrated data.
    """
    logger.info("Creating multiomics dataset...")

    # 1. Filter RNA genes
    adata_rna = filter_genes(
        adata_rna,
        protein_coding_only=protein_coding_only,
        filter_mt_genes=filter_mt_genes,
        hvg_flavor=hvg_flavor,
        hvg_fraction=hvg_fraction,
        hvg_key=hvg_key,
    )

    # 2. Filter ATAC peaks
    adata_atac = filter_regions(
        adata_atac,
        min_cells=min_cells_per_peak,
        score_percentile=peak_score_percentile,
        score_mode=score_thresh_mode,
        promoter_only=promoter_only,
    )

    # 3. Compute motif scores if not provided
    if motif_scores is None:
        if motif_dir is None or output_dir is None:
            raise ValueError(
                "motif_dir and output_dir must be provided if motif_scores is None"
            )

        logger.info("Computing motif scores...")
        # Extract peaks from adata_atac
        peaks = pd.DataFrame(index=adata_atac.var_names)
        peaks["name"] = peaks.index
        # Parse peak coordinates (format: chr:start-end)
        peaks[["chr", "coords"]] = peaks.index.str.split(":", expand=True)
        peaks[["start", "end"]] = peaks["coords"].str.split("-", expand=True)
        peaks = peaks[["chr", "start", "end", "name"]]
        peaks = peaks.reset_index(drop=True)

        # Convert start/end to integers
        peaks["start"] = peaks["start"].astype(int)
        peaks["end"] = peaks["end"].astype(int)

        # Compute motif scores
        motif_scores = compute_motif_scores(
            motif_dir=motif_dir,
            output_dir=output_dir,
            species=species,
            motif_database=motif_database,
            genome_assembly=genome_assembly,
            bed_peaks=peaks,
        )

    # 4. Filter motif scores to only include genes and peaks in our filtered data
    motif_scores = filter_motif_scores(
        motif_scores=motif_scores,
        adata_rna=adata_rna,
        adata_atac=adata_atac,
    )

    # 5. Compute in-silico ChIP-seq signals
    adata_rna_filtered, adata_atac_filtered = compute_in_silico_chipseq(
        adata_rna=adata_rna,
        adata_atac=adata_atac,
        motif_scores=motif_scores,
        motif_score_min_percentile=motif_score_percentile,
        max_genes_per_peak=max_genes_per_peak,
        min_peaks_per_gene=min_peaks_per_gene,
        binary_mode=tf_chip_binary,
    )

    logger.info(
        f"Created multiomics dataset with {adata_rna_filtered.shape[1]} genes and "
        f"{adata_atac_filtered.shape[1]} peaks"
    )

    return adata_rna_filtered, adata_atac_filtered


@beartype
def pipeline_setup_multiview(
    samples: Dict[str, AnnData],
    hvg_fraction: float = 0.1,
    hvg_flavor: str = "highly_variable",
    gene_key: str = "gene_symbol",
    gene_renamer_func: Callable = None,
) -> Dict[str, AnnData]:
    """Set up multiple AnnData views filtering genes and renaming based on gene symbols.

    Args:
        samples: Dictionary mapping sample names to AnnData objects.
        hvg_fraction: Fraction of genes to select as highly variable. Default is 0.1.
        hvg_flavor: Method for HVG selection. Default is "highly_variable".
        gene_key: Key in adata.var containing gene symbols. Default is "gene_symbol".
        gene_renamer_func: Function to rename genes, taking gene names as input. Default is None.

    Returns:
        Dictionary mapping sample names to processed AnnData objects.
    """
    logger.info(f"Setting up multiview pipeline for {len(samples)} samples")
    processed_samples = {}

    for name, adata in samples.items():
        # Make a copy to avoid modifying the original
        adata_copy = adata.copy()

        # Rename genes if needed
        if gene_key in adata_copy.var and gene_key != "index":
            # Extract gene symbols as new index
            gene_symbols = adata_copy.var[gene_key].values

            # Apply renamer function if provided
            if gene_renamer_func is not None:
                gene_symbols = np.array([gene_renamer_func(g) for g in gene_symbols])

            # Set new index
            adata_copy.var.index = gene_symbols

        # Filter genes
        adata_filtered = filter_genes(
            adata_copy,
            protein_coding_only=True,
            filter_mt_genes=True,
            hvg_flavor=hvg_flavor,
            hvg_fraction=hvg_fraction,
        )

        processed_samples[name] = adata_filtered
        logger.info(
            f"Processed sample {name}: {adata_filtered.shape[0]} cells, {adata_filtered.shape[1]} genes"
        )

    return processed_samples


@beartype
def preprocessing_pipeline(
    main_dir: Path,
    data_rna: AnnData,
    data_atac: AnnData,
    drop_mitochondrial_genes: bool = True,
    drop_non_protein_coding_genes: bool = True,
    HVG_Genes_TF: bool = True,
    gene_bed_intersection: bool = True,
    perform_clustering: bool = True,
    peak_selection: bool = True,
    motif_analysis: bool = True,
    chipseq_analysis: bool = True,
    species: str = "mouse",
    motif_database: str = "cisbp",
    genome_assembly: str = "mm10",
    num_tfs_hvg: int = 300,
    num_genes_hvg: int = 3000,
    window_size: int = 80000,
    resolution: int = 5,
    grouping_key: str = "leiden",
    batch_key: str = "sample",
    num_peaks: int = 50000,
    cluster_key: str = "leiden",
    promoter_col: str = "is_promoter",
    motif_match_pvalue_threshold: float = 1e-3,
    window: int = 500,
    correlation_percentile: float = 95.0,
    n_bg_peaks_for_corr: int = 5000,
) -> Optional[pd.DataFrame]:
    """
    Preprocessing Pipeline from Manu  Saraswat

    Args:
        main_dir (Path):
            Path to the main directory containing the input files and where other files will be stored/downloaded.
        data_rna (AnnData):
            Annotated RNA expression matrix containing gene expression data for each cell.
        data_atac (AnnData):
            Annotated ATAC-seq matrix containing chromatin accessibility data for each cell.
        drop_mitochondrial_genes (bool): optional
            Preprocessing step to remove all mitochondrial genes from data_rna. Default is True.
        drop_non_protein_coding_genes (bool): optional
            Preprocessing step to remove all non protein coding genes from data_rna. Default is True.
        HVG_Genes_TF (bool): optional
            Preprocessing step to select highly variable TF genes and HVG non TF genes. Default is True.
        gene_bed_intersection (bool): optional
            Preprocessing step to intersect Peaks with Genes. Default is True.
        perform_clustering (bool): optional
            Preprocessing step to perform temporary clustering on data_rna/_atac. Default is True.
        peak_selection (bool): optional
            Preprocessing step to slect TF peaks and HV Peaks across clustering. Default is True.
        motif_analysis (bool): optional
            Motif Matching can be turned off if one wants only the filter RNA/ATAC data. Default is True.
        chipseq_analysis (bool): optional
            Insilico_chiseq can be turned off if one wants only Motif matching without filtering afterwards. Default is True.
        species (str): optional
            The species being analyzed. Default is "mouse".
        motif_database (str): optional
            The database used for transcription factor motif analysis. Default is "cisbp".
        genome_assembly (str): optional
            The genome assembly version to use for the analysis. Default is "mm10".
        num_tfs_hvg (int): optional
            Number of HV TF genes to be selected. Default is 300.
        num_genes_hvg (int): optional
            Number of HV  non TF genes to be selected. Default is 3000.
        window_size (int): optional
            Window size for Gene-Peaks Intersection. Default is 80,000.
        resolution (int): optional
            Resolution parameter for clustering. Default is 5.
        grouping_key (str): optional
            Key used to define groups in the clustering process. Default is "leiden".
        batch_key (str): optional
            Metadata key used for batch correction or grouping cells by batch. Default is "sample".
        num_peaks (int): optional
            The total number of TF Peaks + HV Peaks across clustering to be selected. Default is 50,000.
        cluster_key (str): optional
            Key used to assign cluster labels to cells. Default is "leiden".
        promoter_col (str): optional
            Column name indicating whether a genomic region is a promoter. Default is "is_promoter".
        motif_match_pvalue_threshold (float): optional
            P-value threshold for motif matching algorithm. Default is 1e-3.
        window (int): optional
            Size of the window around peak centre for motif scanning. Default is 500.
        correlation_percentile (int): optional
            Percentile threshold for selecting highly correlated features. Default is 95.
        n_bg_peaks_for_corr (int): optional
            Number of background peaks used for correlation analysis. Default is 5000.


    Returns:
        insilico_chipseq.csv: pd.DataFrame containing filtered motif matches with corresponding gene and region names and motif scores.
    """
    # Import specific functions from the refactored modules
    import matplotlib.pyplot as plt
    from gtfparse import read_gtf
    from sklearn.preprocessing import MinMaxScaler
    from tangermeme.io import extract_loci, read_meme
    from tangermeme.tools.fimo import fimo
    from tqdm import tqdm

    from stormi.preprocessing._file_utils import (
        check_command_availability,
        create_dir_if_not_exists,
    )
    from stormi.preprocessing._filtering import (
        TF_HVG_selection,
        bed_file_intersection,
        func_mitochondrial_genes,
        func_protein_coding_genes,
        keep_promoters_and_select_hv_peaks,
        simple_bed_intersection,
    )
    from stormi.preprocessing._metacells import create_metacells

    # define folder structure
    genome_dir = main_dir / Path("Prepared")
    motif_dir = main_dir / Path("Prepared")
    output_dir = main_dir / Path("Generated")
    create_dir_if_not_exists(output_dir)

    # Intersection: Keeping only cells which are present in both rna and atac files
    common_idx = data_rna.obs_names.intersection(data_atac.obs_names)
    data_rna = data_rna[common_idx].copy()
    data_atac = data_atac[common_idx].copy()
    logger.info(f"Intersected cells: now RNA={data_rna.shape}, ATAC={data_atac.shape}")

    # Mitochondrial Genes: Dropping mitochondrial genes in RNA Data
    if drop_mitochondrial_genes:
        data_rna = func_mitochondrial_genes(data_rna)
    else:
        logger.info("Kept mitochondrial genes")

    # Protein Coding Genes: Dropping non-protein coding genes in RNA Data
    # Load the annotations for genes
    gtf_path = genome_dir / Path(f"{species}_annotation.gtf")
    logger.info(f"Loading GTF from {gtf_path}")
    df = read_gtf(gtf_path)
    gtf_df = pd.DataFrame(df)
    gtf_df.columns = df.columns

    if drop_non_protein_coding_genes:
        data_rna = func_protein_coding_genes(data_rna, gtf_df)
    else:
        logger.info("Kept non-protein coding genes")

    # TF + HVG selection
    if HVG_Genes_TF:
        data_rna, final_genes, final_tfs = TF_HVG_selection(
            data_rna, motif_dir, num_genes_hvg, num_tfs_hvg, species, motif_database
        )
    else:
        # Load all possible TF
        motif_path = motif_dir / f"{motif_database}_{species}.meme"
        tf_names_all = []
        with open(motif_path, "r") as f:
            for line in f:
                if line.startswith("MOTIF"):
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        tf_name = parts[2].split("_")[0].strip("()").strip()
                        tf_names_all.append(tf_name)
        tf_names_all = sorted(list(set(tf_names_all)))
        final_tfs = sorted(list(set(tf_names_all) & set(data_rna.var_names)))
        final_genes = sorted(list(set(data_rna.var_names) - set(final_tfs)))
        combined = final_genes + final_tfs
        data_rna = data_rna[:, combined].copy()
        gene_types = ["HVG"] * len(final_genes) + ["TF"] * len(final_tfs)
        data_rna.var["gene_type"] = gene_types

        logger.info("No HVG and TF were selected. All were kept.")
        logger.info(
            f"Selected {len(final_genes)} non TF Genes from {len(data_rna.var_names)} available Genes  + {len(final_tfs)} TFs from {len(tf_names_all)} available TFs."
        )

    # Gene Bed Intersection
    if gene_bed_intersection:
        data_atac = bed_file_intersection(
            genome_dir,
            output_dir,
            data_atac,
            genome_assembly,
            species,
            window_size,
            gtf_df,
            final_genes,
            final_tfs,
        )
    else:
        logger.info("No gene-window filtering was done. All peaks were kept.")

    # Temporary Clustering

    # if no batch is defined one can parse on a dummy batch
    # e.g. data_rna.obs["sample"] = ["A"] * data_rna.shape[0]
    if perform_clustering:
        data_rna.obs["sample"] = ["A"] * data_rna.shape[0]
        rna_metacell, atac_metacell = create_metacells(
            data_rna, data_atac, grouping_key, resolution, batch_key
        )
        # Copy Labels
        data_atac.obs["leiden"] = data_rna.obs["leiden"]
    else:
        logger.info("No Clustering was performed")

    # Keep promoter peaks + HV from the rest => total # = num_peaks
    if peak_selection:
        data_atac = keep_promoters_and_select_hv_peaks(
            data_atac=data_atac,
            total_n_peaks=num_peaks,
            cluster_key=cluster_key,
            promoter_col=promoter_col,
        )
        logger.info(f"Final shape after combining promoters + HV => {data_atac.shape}")
    else:
        logger.info("No peak selection was performed")

    # Creating Bed for selected peaks
    data_atac.var["chr"] = [v.split(":")[0] for v in data_atac.var_names]
    data_atac.var["start"] = [
        int(v.split(":")[1].split("-")[0]) for v in data_atac.var_names
    ]
    data_atac.var["end"] = [
        int(v.split(":")[1].split("-")[1]) for v in data_atac.var_names
    ]
    data_atac.var["peak_name"] = data_atac.var_names
    peaks_bed = output_dir / "peaks_selected.bed"
    data_atac.var[["chr", "start", "end", "peak_name"]].to_csv(
        peaks_bed, sep="\t", header=False, index=False
    )

    # Saving Processed Data
    common_cells = data_rna.obs_names.intersection(data_atac.obs_names)
    data_rna = data_rna[common_cells].copy()
    data_atac = data_atac[common_cells].copy()

    # Save
    rna_path = output_dir / Path("rna_processed.h5ad")
    atac_path = output_dir / Path("atac_processed.h5ad")
    data_rna.write_h5ad(rna_path)
    data_atac.write_h5ad(atac_path)
    logger.info(f"Saved processed RNA to {rna_path} with shape={data_rna.shape}")
    logger.info(f"Saved processed ATAC to {atac_path} with shape={data_atac.shape}")

    # Motif Matching
    if motif_analysis:
        # Loading necessary data
        motif_path = motif_dir / f"{motif_database}_{species}.meme"
        # Read .meme motif file and subset to only TFs of interest.
        logger.info(f"Reading motif file: {motif_path}")
        pwms = read_meme(motif_path)
        selected_keys = []
        selected_tfs = []
        for key in pwms.keys():
            # Example parse: "MOTIF  something Tbx5_..."
            tf_name = key.split(" ")[1].split("_")[0].strip("()").strip()
            if tf_name in final_tfs:
                selected_keys.append(key)
                selected_tfs.append(tf_name)

        df_map = pd.DataFrame(
            {"key": selected_keys, "TF": selected_tfs}
        ).drop_duplicates("TF")
        pwms_sub = {row.key: pwms[row.key] for _, row in df_map.iterrows()}
        key_to_tf = dict(zip(df_map["key"], df_map["TF"]))

        logger.info(f"Subselected {len(pwms_sub)} motifs for {len(final_tfs)} TFs.")

        df_motif = compute_motif_scores(
            bed_file=output_dir / Path("peaks_selected.bed"),
            fasta_file=genome_dir / f"{species}_{genome_assembly}.fa",
            pwms_sub=pwms_sub,
            key_to_tf=key_to_tf,
            n_peaks=data_atac.shape[1],
            window=window,
            threshold=motif_match_pvalue_threshold,
        )
    else:
        logger.info(" No motif matching was performed.")
        return

    if chipseq_analysis:
        # Insilico Chipseq

        # Filtering meta cells to new set of peaks
        atac_metacell = atac_metacell[:, data_atac.var_names].copy()
        tf_mask = rna_metacell.var["gene_type"] == "TF"
        rna_matrix = rna_metacell.X[:, tf_mask]  # shape=(n_meta, n_tfs)
        atac_matrix = atac_metacell.X  # shape=(n_meta, n_peaks)

        insilico_chipseq = compute_in_silico_chipseq(
            atac_matrix=atac_matrix,
            rna_matrix=rna_matrix,
            df_motif=df_motif,
            correlation_percentile=correlation_percentile,
            n_bg_peaks_for_corr=n_bg_peaks_for_corr,
        )
        insilico_chipseq.to_csv(output_dir / "insilico_chipseq.csv")

        return insilico_chipseq
    else:
        logger.info(" No insilico_chipseq was performed.")
        raw_motif_results = df_motif.reset_index().melt(
            id_vars="index", var_name="column", value_name="value"
        )
        raw_motif_results = raw_motif_results[raw_motif_results["value"] != 0]
        raw_motif_results.rename(
            columns={
                "index": "peak_name",
                "column": "Motif_name",
                "value": "Matching_Score",
            },
            inplace=True,
        )
    return raw_motif_results


# Add supplementary compute_motif_scores and compute_in_silico_chipseq functions
# needed by preprocessing_pipeline but not included in _motifs.py
@beartype
def compute_motif_scores(
    bed_file: Path,
    fasta_file: Path,
    pwms_sub: dict,
    key_to_tf: dict,
    n_peaks: int,
    window: int,
    threshold: float,
) -> pd.DataFrame:
    """
    Extract sequences from peaks_bed, run FIMO with `pwms_sub`,
    build a motif score matrix (n_peaks x n_TFs).

    Parameters
    ----------
    peaks_bed : Path
    fasta_file : Path
    pwms_sub : dict
    key_to_tf : dict
    n_peaks : int
    window : int

    Returns
    -------
    pd.DataFrame
        shape=(n_peaks, n_TFs), index=peak_name, columns=TF)
    """
    from sklearn.preprocessing import MinMaxScaler
    from tangermeme.io import extract_loci
    from tangermeme.tools.fimo import fimo
    from tqdm import tqdm

    # actual method
    logger.info(
        f"Computing motif scores for {bed_file} (n_peaks={n_peaks}) with window={window}"
    )
    loci = pd.read_csv(bed_file, sep="\t", header=None)
    loci.columns = ["chr", "start", "end", "peak_name"]

    # Extract sequences
    X = extract_loci(loci, str(fasta_file), in_window=window).float()
    # Run FIMO
    hits_list = fimo(pwms_sub, X, threshold=threshold)

    all_tf_cols = sorted(list(set(key_to_tf.values())))

    peak_motif_scores = []

    for k in tqdm(range(len(hits_list))):
        # Group by motif_name and sequence_name, keeping the max score per group
        motif_df = (
            hits_list[k][["motif_name", "sequence_name", "score"]]
            .groupby(["motif_name", "sequence_name"])
            .max()
            .reset_index()
        )

        if motif_df.shape[0] > 0:  # Proceed if there are valid scores
            all_sequences = pd.DataFrame({"sequence_name": range(n_peaks)})

            motif_name = motif_df.motif_name.values[0]
            tf_name = key_to_tf[motif_name]

            # Merge all sequences with motif_df, filling missing values
            complete_df = all_sequences.merge(motif_df, on="sequence_name", how="left")
            complete_df["score"] = complete_df["score"].fillna(
                0
            )  # Fill NaN scores with 0

            # Ensure only the "score" column remains before renaming
            complete_df = complete_df[["sequence_name", "score"]].set_index(
                "sequence_name"
            )
            complete_df.columns = [tf_name]  # Rename the "score" column to the TF name

            # Append to the list
            peak_motif_scores.append(complete_df)

    # Concatenate all the individual dataframes into a single dataframe
    if len(peak_motif_scores) > 0:
        peak_motif_scores = pd.concat(peak_motif_scores, axis=1)
    else:
        logger.warning("No motif scores were computed. Returning an empty DataFrame.")
        peak_motif_scores = pd.DataFrame(index=range(n_peaks))

    # Handle remaining TFs not present in the scores
    remaining_tfs = set(key_to_tf.values()) - set(peak_motif_scores.columns)
    for tf in remaining_tfs:
        peak_motif_scores[tf] = 0

    # Reorder columns to match the final TF list

    final_tf_list = sorted(list(set(key_to_tf.values())))
    peak_motif_scores = peak_motif_scores[final_tf_list]

    scaler = MinMaxScaler()
    motif_scores = scaler.fit_transform(peak_motif_scores.values)

    bed_file_peak = pd.read_csv(bed_file, sep="\t", header=None)
    df_motif = pd.DataFrame(
        motif_scores, columns=peak_motif_scores.columns, index=bed_file_peak[3].values
    )

    logger.info(f"Finished computing motif scores: {df_motif.shape}")
    return df_motif


@beartype
def compute_in_silico_chipseq(
    df_motif: pd.DataFrame,
    atac_matrix: np.ndarray,
    rna_matrix: np.ndarray,
    correlation_percentile: float,
    n_bg_peaks_for_corr: int,
) -> pd.DataFrame:
    """
    Compute correlation between peak accessibility and TF expression,
    then combine with motif scores for an in-silico ChIP-seq embedding.

    Parameters
    ----------
    df_motif : pd.DataFrame,  shape=(n_peaks, n_tfs)
    atac_matrix : (n_metacells, n_peaks) np.ndarray
    rna_matrix : (n_metacells, n_tfs) np.ndarray
    correlation_percentile : float
        Threshold correlation_percentile for correlation significance
    n_bg_peaks_for_corr : int
        Number of peaks per motif to use as background

    Returns
    -------
    insilico_chipseq_sig
        shape=(n_peaks, n_tfs)
    """
    from sklearn.preprocessing import MinMaxScaler
    from tqdm import tqdm

    logger.info("Computing in-silico ChIP-seq correlation...")

    n_cells, n_peaks = atac_matrix.shape
    _, n_tfs = rna_matrix.shape
    if df_motif.shape != (n_peaks, n_tfs):
        logger.warning("df_motif dimension does not match (n_peaks x n_tfs).")

    # Z-score peaks & TF expression
    X = (atac_matrix - atac_matrix.mean(axis=0)) / (atac_matrix.std(axis=0) + 1e-8)
    Y = (rna_matrix - rna_matrix.mean(axis=0)) / (rna_matrix.std(axis=0) + 1e-8)

    # Pearson correlation => (n_peaks x n_tfs)
    pearson_r = (X.T @ Y) / n_cells
    pearson_r = np.nan_to_num(pearson_r)

    pearson_r_act = np.clip(pearson_r, 0, None)  # only positive
    pearson_r_rep = np.clip(pearson_r, None, 0)  # only negative

    pearson_r_act_sig = np.zeros_like(pearson_r_act)
    pearson_r_rep_sig = np.zeros_like(pearson_r_rep)

    tf_list = df_motif.columns

    # Thresholding
    for t in tqdm(range(n_tfs), desc="Thresholding correlation"):
        tf_name = tf_list[t]
        # Find background peaks with smallest motif
        scores_t = df_motif[tf_name].values
        order = np.argsort(scores_t)
        bg_idx = order[
            : min(n_bg_peaks_for_corr, n_peaks)
        ]  # top n_bg smallest motif peaks
        # Activator significance
        bg_vals_act = pearson_r_act[bg_idx, t]
        cutoff_act = np.percentile(bg_vals_act, correlation_percentile)
        # Repressor significance
        bg_vals_rep = pearson_r_rep[bg_idx, t]
        cutoff_rep = np.percentile(bg_vals_rep, 100 - correlation_percentile)

        act_vec = pearson_r_act[:, t]
        rep_vec = pearson_r_rep[:, t]
        pearson_r_act_sig[:, t] = np.where(act_vec > cutoff_act, act_vec, 0)
        pearson_r_rep_sig[:, t] = np.where(rep_vec < cutoff_rep, rep_vec, 0)

    # Combine with motif
    insilico_chipseq_act_sig = df_motif.values * pearson_r_act_sig
    insilico_chipseq_rep_sig = df_motif.values * pearson_r_rep_sig
    insilico_chipseq_sig_all = insilico_chipseq_act_sig + insilico_chipseq_rep_sig

    logger.info("Finished in-silico ChIP-seq computation.")

    peak_index_list = list(df_motif.index)
    insilico_chipseq_sig_all = pd.DataFrame(insilico_chipseq_sig_all)

    insilico_chipseq_sig_all["peak_name"] = peak_index_list
    insilico_chipseq_sig_all = insilico_chipseq_sig_all.set_index("peak_name")
    insilico_chipseq_sig_all.columns = df_motif.columns

    insilico_chipseq_sig_all = insilico_chipseq_sig_all.reset_index().melt(
        id_vars="peak_name", var_name="column", value_name="value"
    )
    insilico_chipseq_sig_all = insilico_chipseq_sig_all[
        insilico_chipseq_sig_all["value"] != 0
    ]

    insilico_chipseq_sig_all.rename(
        columns={"column": "Motif_name", "value": "Matching_Score"}, inplace=True
    )

    scaler = MinMaxScaler(feature_range=(-1, 1))
    insilico_chipseq_sig_scaled = scaler.fit_transform(
        insilico_chipseq_sig_all[["Matching_Score"]]
    )
    insilico_chipseq_sig_all["Matching_Score"] = insilico_chipseq_sig_scaled
    return insilico_chipseq_sig_all
