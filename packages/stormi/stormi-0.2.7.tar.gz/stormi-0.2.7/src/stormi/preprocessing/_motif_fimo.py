"""Functions for running FIMO motif scanner.

This module contains functions for running the Find Individual Motif Occurrences (FIMO)
tool from the tangermeme package to scan for transcription factor motifs in genomic regions.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from beartype import beartype
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

logger = logging.getLogger(__name__)


@beartype
def run_fimo(
    motif_path: Path,
    genome_assembly: str,
    bed_file: Path,
    output_dir: Path,
    window_size: int = 0,
    threshold: float = 1e-3,
    species: str = "mouse",
) -> pd.DataFrame:
    """Run FIMO to scan for motifs in genomic regions.

    Uses tangermeme.tools.fimo to scan for motifs in genomic regions defined in a BED file.

    Args:
        motif_path: Path to the MEME format motif file.
        genome_assembly: Genome assembly name (e.g., "mm10", "hg38").
        bed_file: Path to BED file with genomic regions.
        output_dir: Directory to save output files.
        window_size: Size of window around peaks to scan for motifs.
        threshold: P-value threshold for motif matching.
        species: Species name (e.g., "mouse", "human").

    Returns:
        DataFrame with motif scores for each region and each motif.
    """
    from tangermeme.io import extract_loci, read_meme
    from tangermeme.tools.fimo import fimo

    logger.info(f"Running FIMO motif scanner with {motif_path} on {bed_file}")

    # Read the BED file
    loci = pd.read_csv(bed_file, sep="\t", header=None)
    loci.columns = ["chr", "start", "end", "peak_name"]
    n_peaks = len(loci)

    # Get the path to the genome FASTA file
    fasta_file = output_dir.parent / "Prepared" / f"{species}_{genome_assembly}.fa"

    # Read the motif file and identify TF names
    pwms = read_meme(motif_path)
    selected_keys = []
    selected_tfs = []

    # Find TFs in the motif file
    for key in pwms.keys():
        # Example parse: "MOTIF something Tbx5_..."
        tf_name = key.split(" ")[1].split("_")[0].strip("()").strip()
        selected_keys.append(key)
        selected_tfs.append(tf_name)

    df_map = pd.DataFrame({"key": selected_keys, "TF": selected_tfs}).drop_duplicates(
        "TF"
    )
    pwms_sub = {row.key: pwms[row.key] for _, row in df_map.iterrows()}
    key_to_tf = dict(zip(df_map["key"], df_map["TF"]))

    logger.info(f"Found {len(pwms_sub)} motifs for {len(set(selected_tfs))} TFs")

    # Extract sequences
    logger.info(
        f"Extracting sequences from {fasta_file} with window_size={window_size}"
    )
    X = extract_loci(loci, str(fasta_file), in_window=window_size).float()

    # Run FIMO
    hits_list = fimo(pwms_sub, X, threshold=threshold)

    all_tf_cols = sorted(list(set(key_to_tf.values())))
    peak_motif_scores = []

    for k in tqdm(range(len(hits_list)), desc="Processing motif hits"):
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

    # Scale the scores
    scaler = MinMaxScaler()
    motif_scores = scaler.fit_transform(peak_motif_scores.values)

    # Create final dataframe with peak names as index
    df_motif = pd.DataFrame(
        motif_scores, columns=peak_motif_scores.columns, index=loci["peak_name"].values
    )

    logger.info(f"Finished computing motif scores: {df_motif.shape}")
    return df_motif
