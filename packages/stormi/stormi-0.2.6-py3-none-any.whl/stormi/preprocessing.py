from __future__ import annotations

import logging
import math
import shutil
import subprocess
import warnings
from pathlib import Path
from typing import List, Optional, Tuple, Union

import jax.numpy as jnp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyranges as pr
import scanpy as sc
import scanpy.external as sce
import scipy.sparse as sp
from anndata import AnnData
from beartype import beartype
from gtfparse import read_gtf
from pybiomart import Server
from scipy.sparse import csr_matrix
from scvi.model import MULTIVI, SCVI
from sklearn.preprocessing import MinMaxScaler
from tangermeme.io import extract_loci, read_meme
from tangermeme.tools.fimo import fimo
from tqdm import tqdm

logger = logging.getLogger(__name__)


def compute_pca_complexity(
    adata: AnnData, variance_threshold: float = 0.9, n_comps: int = 50
) -> int:
    """
    Computes a simple measure of dataset complexity: the number of principal components
    required to explain at least `variance_threshold` of the variance.

    If PCA has not yet been computed, this function runs sc.pp.pca on the adata.
    """
    if "pca" not in adata.uns:
        sc.pp.pca(adata, n_comps=n_comps)
    variance_ratio = adata.uns["pca"]["variance_ratio"]
    cum_var = np.cumsum(variance_ratio)
    complexity = int(np.searchsorted(cum_var, variance_threshold)) + 1
    return complexity


def default_n_latent(n_obs: int, complexity: int) -> int:
    """
    Computes a default latent dimension.
    Base is 20 + 10 * log10(n_obs/1e3) and then adjusted upward by 0.5 * complexity.
    Capped at 150.
    """
    base = 20 + 10 * math.log10(n_obs / 1000)
    return int(max(20, min(150, base + 0.5 * complexity)))


def default_n_hidden(n_obs: int, complexity: int) -> int:
    """
    Computes a default number of hidden units per layer.
    Base is 256 + 64 * log10(n_obs/1e3) and then adjusted upward by 8 * complexity.
    Capped at 1024.
    """
    base = 256 + 64 * math.log10(n_obs / 1000)
    return int(max(256, min(1024, base + 8 * complexity)))


def default_n_layers(n_obs: int, complexity: int) -> int:
    """
    Returns a default number of layers.
    For fewer than 1e5 cells, use 2 layers if complexity < 20, else 3.
    For larger datasets, use 3 layers if complexity < 30, else 4.
    """
    if n_obs < 1e5:
        return 2 if complexity < 20 else 3
    else:
        return 3 if complexity < 30 else 4


def default_epochs(n_obs: int, complexity: int) -> int:
    """
    Computes a default number of training epochs.
    Base increases with n_obs and is scaled by the complexity.
    For 1e4 cells with moderate complexity, ~600 epochs are used.
    The final number is increased by a factor (1 + complexity/50)
    to ensure higher iterations for more complex datasets.
    """
    base = 600 + 200 * math.log10(n_obs / 10000)
    return int(max(400, base * (1 + complexity / 50)))


def run_scvi(
    adata_rna: AnnData,
    adata_atac: Optional[AnnData] = None,
    latent_key: str = "X_scVI",
    n_hidden: Optional[int] = None,
    n_latent: Optional[int] = None,
    n_layers: Optional[int] = None,
    dropout_rate: Optional[float] = None,
    max_epochs: Optional[int] = None,
    save_model_path: Optional[str] = None,
    variance_threshold: float = 0.9,
    n_comps: int = 50,
    **kwargs,
) -> Union[AnnData, Tuple[AnnData, AnnData]]:
    """
    Runs scVI (if only RNA is provided) or multiVI (if both RNA and ATAC are provided)
    on the input AnnData object(s). Hyperparameters are chosen automatically based on the
    number of cells and a measure of dataset complexity (computed via PCA) unless explicitly
    provided by the user.

    The latent representation is stored in .obsm under the key `latent_key` (default "X_scVI").
    Optionally, the trained model is saved to a user-defined directory.

    Parameters
    ----------
    adata_rna : AnnData
        AnnData object with RNA counts.
    adata_atac : Optional[AnnData]
        AnnData object with ATAC counts. Must have the same cells (and order) as adata_rna.
    latent_key : str, default: "X_scVI"
        Key to store the latent representation in .obsm.
    n_hidden : Optional[int]
        Number of hidden units per layer. Defaults to an automatic choice.
    n_latent : Optional[int]
        Dimensionality of the latent space. Defaults to an automatic choice.
    n_layers : Optional[int]
        Number of hidden layers. Defaults to an automatic choice.
    dropout_rate : Optional[float]
        Dropout rate. Defaults to 0.1.
    max_epochs : Optional[int]
        Maximum number of training epochs. Defaults to an automatic choice.
    save_model_path : Optional[str]
        Directory to save the trained model. If None, the model is not saved.
    variance_threshold : float, default: 0.9
        Fraction of variance that PCA must explain to define dataset complexity.
    n_comps : int, default: 50
        Maximum number of PCA components to compute for complexity estimation.
    **kwargs
        Additional keyword arguments passed to the model constructor.

    Returns
    -------
    Union[AnnData, Tuple[AnnData, AnnData]]:
        If only RNA is provided, returns the updated adata_rna.
        If ATAC is provided, returns a tuple (adata_rna, adata_atac)
        with the latent representation added.
    """
    n_obs = adata_rna.n_obs
    # Compute a simple complexity measure: #PCs needed to reach variance_threshold
    complexity = compute_pca_complexity(
        adata_rna, variance_threshold=variance_threshold, n_comps=n_comps
    )

    # Set defaults if parameters are not provided.
    if n_hidden is None:
        n_hidden = default_n_hidden(n_obs, complexity)
    if n_latent is None:
        n_latent = default_n_latent(n_obs, complexity)
    if n_layers is None:
        n_layers = default_n_layers(n_obs, complexity)
    if dropout_rate is None:
        dropout_rate = 0.1
    if max_epochs is None:
        max_epochs = default_epochs(n_obs, complexity)

    # Print out chosen hyperparameters
    print("Chosen Hyperparameters:")
    print(f"  - Number of hidden units per layer: {n_hidden}")
    print(f"  - Latent space dimensionality: {n_latent}")
    print(f"  - Number of layers: {n_layers}")
    print(f"  - Dropout rate: {dropout_rate}")
    print(f"  - Maximum training epochs: {max_epochs}")

    # ------------------------ RNA only: SCVI ------------------------
    if adata_atac is None:
        # 1) Set up Anndata specifically for SCVI
        SCVI.setup_anndata(adata_rna)

        # 2) Create and train the SCVI model
        model = SCVI(
            adata=adata_rna,
            n_hidden=n_hidden,
            n_layers=n_layers,
            n_latent=n_latent,
            dropout_rate=dropout_rate,
            **kwargs,
        )
        model.train(max_epochs=max_epochs)

        # 3) Store latent representation
        latent = model.get_latent_representation()
        adata_rna.obsm[latent_key] = latent

        # 4) Save model if path provided
        if save_model_path is not None:
            model.save(save_model_path, overwrite=True)

        return adata_rna

    # --------------------- RNA + ATAC: MULTIVI ----------------------
    else:
        # Ensure consistent cell order
        if not (adata_rna.obs_names == adata_atac.obs_names).all():
            raise ValueError(
                "RNA and ATAC AnnData objects must have the same obs_names in the same order."
            )

        # 1) Create a joint object by copying RNA and storing ATAC in obsm
        adata_joint = adata_rna.copy()
        adata_joint.obsm["X_atac"] = adata_atac.X

        # 2) Set up Anndata specifically for MULTIVI
        MULTIVI.setup_anndata(adata_joint)

        # 3) Create and train the MULTIVI model
        model = MULTIVI(
            adata_joint,
            n_hidden=n_hidden,
            n_layers=n_layers,
            n_latent=n_latent,
            dropout_rate=dropout_rate,
            **kwargs,
        )
        model.train(max_epochs=max_epochs)

        # 4) Store latent representation in both objects
        latent = model.get_latent_representation()
        adata_rna.obsm[latent_key] = latent
        adata_atac.obsm[latent_key] = latent

        # 5) Save model if path provided
        if save_model_path is not None:
            model.save(save_model_path, overwrite=True)

        return adata_rna, adata_atac


@beartype
def compute_metacells(
    adata_rna: "AnnData",
    adata_atac: Optional["AnnData"] = None,
    latent_key: str = "X_scVI",
    invariant_keys: List[str] = [],
    merge_categorical_keys: List[str] = [],
    numerical_keys: List[str] = [],
    n_neighbors: int = 10,
    resolution: int = 50,
    verbose: bool = True,
    merge_umap: bool = True,
    umap_key: Optional[str] = None,
) -> Union["AnnData", Tuple["AnnData", "AnnData"]]:
    """
    Computes metacells by clustering cells in a latent space and merging counts and metadata.
    If ATAC data is provided, both RNA and ATAC metacells are computed and returned.
    Otherwise, only RNA metacells are computed.

    All .var and .uns fields are copied from the original objects.

    Args:
        adata_rna (AnnData): AnnData object with RNA counts.
        adata_atac (Optional[AnnData]): AnnData object with ATAC counts (optional).
        latent_key (str): Name of latent space key in .obsm of adata_rna.
        invariant_keys (List[str], optional): List of categorical keys in adata_rna.obs that must be homogeneous
            within a metacell.
        merge_categorical_keys (List[str], optional): List of categorical keys in adata_rna.obs that can be merged.
        numerical_keys (List[str], optional): List of numerical keys in adata_rna.obs to be averaged in each metacell.
        n_neighbors (int, optional): Number of nearest neighbors for the cell–cell graph.
        resolution (int, optional): Resolution parameter for Leiden clustering.
        verbose (bool, optional): Whether to print progress and diagnostic plots.
        merge_umap (bool, optional): Whether to merge UMAP coordinates for metacells.
        umap_key (Optional[str], optional): Key for UMAP embedding in adata_rna.obsm.

    Returns:
        Union[AnnData, Tuple[AnnData, AnnData]]:
            - If adata_atac is None: returns the merged RNA AnnData object.
            - Otherwise: returns a tuple (rna_metacell, atac_metacell).
    """

    # Ensure RNA data is in sparse format and add total counts.
    if not isinstance(adata_rna.X, csr_matrix):
        adata_rna.X = csr_matrix(adata_rna.X)
    adata_rna.obs["RNA counts"] = np.array(adata_rna.X.sum(axis=1)).ravel()

    # Process ATAC data if provided.
    if adata_atac is not None:
        if len(adata_rna.obs_names) != len(adata_atac.obs_names):
            raise ValueError("RNA and ATAC data do not have the same number of cells.")
        if not (adata_rna.obs_names == adata_atac.obs_names).all():
            raise ValueError(
                "RNA and ATAC data do not contain the same cells in obs_names."
            )
        if not isinstance(adata_atac.X, csr_matrix):
            adata_atac.X = csr_matrix(adata_atac.X)
        adata_atac = adata_atac[adata_rna.obs_names, :]
        adata_atac.obs["ATAC counts"] = np.array(adata_atac.X.sum(axis=1)).ravel()

    # --- CLUSTERING STEP on RNA ---
    if verbose:
        print("Computing neighbors and running Leiden clustering on RNA data...")
    sc.pp.neighbors(adata_rna, use_rep=latent_key, n_neighbors=n_neighbors)
    sc.tl.leiden(adata_rna, key_added="leiden", resolution=resolution)

    # Define metacell labels.
    if invariant_keys:
        combined = adata_rna.obs[invariant_keys].astype(str).agg("_".join, axis=1)
        adata_rna.obs["metacell"] = adata_rna.obs["leiden"].astype(str) + "_" + combined
    else:
        adata_rna.obs["metacell"] = adata_rna.obs["leiden"]

    if adata_atac is not None:
        adata_atac.obs["metacell"] = adata_rna.obs["metacell"]
    cluster_key = "metacell"

    if verbose:
        counts = adata_rna.obs[cluster_key].value_counts()
        print("Total number of cells:", adata_rna.n_obs)
        print("Total number of metacells:", len(counts))
        print(
            "Cells per metacell -- min: {}, mean: {:.1f}, max: {}".format(
                counts.min(), counts.mean(), counts.max()
            )
        )
        plt.hist(counts, bins=10)
        plt.xlabel("Cells per metacell")
        plt.ylabel("Number of metacells")
        plt.show()

    # --- MERGE FUNCTIONS ---
    @beartype
    def merge_RNA(
        adata_rna: "AnnData",
        cluster_key: str,
        invariant_keys: List[str],
        merge_categorical_keys: List[str],
        numerical_keys: List[str],
        verbose: bool = True,
    ) -> "AnnData":
        if verbose:
            print("Merging RNA counts...")
        clusters = np.unique(adata_rna.obs[cluster_key])
        merged_X_list = []
        n_cells_list = []
        merged_annots = {
            key: []
            for key in (invariant_keys + merge_categorical_keys + numerical_keys)
        }

        for c in clusters:
            idx = adata_rna.obs[cluster_key] == c
            X_sum = np.array(adata_rna.X[idx, :].sum(axis=0)).ravel()
            merged_X_list.append(X_sum)
            n_cells = int(idx.sum())
            n_cells_list.append(n_cells)

            for key in invariant_keys:
                unique_vals = adata_rna.obs.loc[idx, key].unique()
                if len(unique_vals) != 1:
                    raise ValueError(
                        f"Metacell {c} is not homogeneous for invariant key '{key}'. Found: {unique_vals}"
                    )
                merged_annots[key].append(unique_vals[0])
            for key in merge_categorical_keys:
                mode_val = adata_rna.obs.loc[idx, key].mode()[0]
                merged_annots[key].append(mode_val)
            for key in numerical_keys:
                avg_val = adata_rna.obs.loc[idx, key].mean()
                merged_annots[key].append(avg_val)

        merged_X = np.vstack(merged_X_list)
        adata_meta = sc.AnnData(X=merged_X)
        adata_meta.var = adata_rna.var.copy()
        # Copy the unstructured data
        adata_meta.uns = adata_rna.uns.copy() if hasattr(adata_rna, "uns") else {}

        meta_obs = pd.DataFrame(index=clusters)
        meta_obs["n_cells"] = n_cells_list
        for key in invariant_keys + merge_categorical_keys + numerical_keys:
            meta_obs[key] = merged_annots[key]
        meta_obs["RNA counts"] = merged_X.sum(axis=1)
        adata_meta.obs = meta_obs

        # Merge additional layers if present.
        for layer in ["unspliced", "spliced"]:
            if layer in adata_rna.layers:
                layer_list = []
                for c in clusters:
                    idx = adata_rna.obs[cluster_key] == c
                    layer_sum = np.array(
                        adata_rna.layers[layer][idx, :].sum(axis=0)
                    ).ravel()
                    layer_list.append(layer_sum)
                merged_layer = np.vstack(layer_list)
                adata_meta.layers[layer] = csr_matrix(merged_layer, dtype=np.uint16)

        if verbose:
            print(
                "Mean RNA counts per cell before:", np.mean(adata_rna.obs["RNA counts"])
            )
            print(
                "Mean RNA counts per metacell after:",
                np.mean(adata_meta.obs["RNA counts"]),
            )
            plt.hist(
                adata_rna.obs["RNA counts"], bins=10, label="Single cells", alpha=0.5
            )
            plt.hist(
                adata_meta.obs["RNA counts"], bins=20, label="Metacells", alpha=0.5
            )
            plt.xlabel("Total RNA Counts")
            plt.ylabel("Frequency")
            plt.legend()
            plt.show()
        return adata_meta

    @beartype
    def merge_UMAP(
        adata_rna: "AnnData",
        adata_meta: "AnnData",
        cluster_key: str,
        umap_key: str = "X_umap",
        verbose: bool = True,
    ) -> "AnnData":
        if verbose:
            print("Merging UMAP coordinates...")
        clusters = np.unique(adata_rna.obs[cluster_key])
        umap_list = []
        for c in clusters:
            idx = adata_rna.obs[cluster_key] == c
            coord = np.mean(adata_rna.obsm[umap_key][idx, :], axis=0)
            umap_list.append(coord)
        adata_meta.obsm[umap_key] = np.vstack(umap_list)
        return adata_meta

    @beartype
    def merge_ATAC(
        adata_atac: "AnnData",
        cluster_key: str,
        invariant_keys: List[str],
        merge_categorical_keys: List[str],
        numerical_keys: List[str],
        verbose: bool = True,
    ) -> "AnnData":
        if verbose:
            print("Merging ATAC counts...")
        clusters = np.unique(adata_atac.obs[cluster_key])
        merged_X_list = []
        n_cells_list = []
        merged_annots = {
            key: []
            for key in (invariant_keys + merge_categorical_keys + numerical_keys)
        }

        for c in clusters:
            idx = adata_atac.obs[cluster_key] == c
            X_sum = np.array(adata_atac.X[idx, :].sum(axis=0)).ravel()
            merged_X_list.append(X_sum)
            n_cells = int(idx.sum())
            n_cells_list.append(n_cells)
            for key in invariant_keys:
                unique_vals = adata_atac.obs.loc[idx, key].unique()
                if len(unique_vals) != 1:
                    raise ValueError(
                        f"Metacell {c} is not homogeneous for invariant key '{key}'. Found: {unique_vals}"
                    )
                merged_annots[key].append(unique_vals[0])
            for key in merge_categorical_keys:
                mode_val = adata_atac.obs.loc[idx, key].mode()[0]
                merged_annots[key].append(mode_val)
            for key in numerical_keys:
                avg_val = adata_atac.obs.loc[idx, key].mean()
                merged_annots[key].append(avg_val)

        merged_X = np.vstack(merged_X_list)
        adata_meta = sc.AnnData(X=merged_X)
        adata_meta.var = adata_atac.var.copy()
        # Copy over unstructured data
        adata_meta.uns = adata_atac.uns.copy() if hasattr(adata_atac, "uns") else {}

        meta_obs = pd.DataFrame(index=clusters)
        meta_obs["n_cells"] = n_cells_list
        for key in invariant_keys + merge_categorical_keys + numerical_keys:
            meta_obs[key] = merged_annots[key]
        meta_obs["ATAC counts"] = merged_X.sum(axis=1)
        adata_meta.obs = meta_obs

        if verbose:
            print(
                "Mean ATAC counts per cell before:",
                np.mean(adata_atac.obs["ATAC counts"]),
            )
            print(
                "Mean ATAC counts per metacell after:",
                np.mean(adata_meta.obs["ATAC counts"]),
            )
            plt.hist(
                adata_atac.obs["ATAC counts"], bins=10, label="Single cells", alpha=0.5
            )
            plt.hist(
                adata_meta.obs["ATAC counts"], bins=20, label="Metacells", alpha=0.5
            )
            plt.xlabel("Total ATAC Counts")
            plt.ylabel("Frequency")
            plt.legend()
            plt.show()
        return adata_meta

    # --- MERGE RNA METACELLS ---
    adata_meta_rna = merge_RNA(
        adata_rna,
        cluster_key=cluster_key,
        invariant_keys=invariant_keys,
        merge_categorical_keys=merge_categorical_keys,
        numerical_keys=numerical_keys,
        verbose=verbose,
    )

    if merge_umap:
        if not umap_key or umap_key not in adata_rna.obsm:
            if verbose:
                warnings.warn(
                    "UMAP embedding not found; computing with sc.tl.umap()...",
                    UserWarning,
                )
            sc.tl.umap(adata_rna)
            umap_key = "X_umap"
        adata_meta_rna = merge_UMAP(
            adata_rna,
            adata_meta_rna,
            cluster_key=cluster_key,
            umap_key=umap_key,
            verbose=verbose,
        )

    # --- MERGE ATAC METACELLS if provided ---
    if adata_atac is not None:
        adata_meta_atac = merge_ATAC(
            adata_atac,
            cluster_key=cluster_key,
            invariant_keys=invariant_keys,
            merge_categorical_keys=merge_categorical_keys,
            numerical_keys=numerical_keys,
            verbose=verbose,
        )
        # Optionally copy ATAC counts into the RNA metacell object.
        adata_meta_rna.obs["ATAC counts"] = adata_meta_atac.obs["ATAC counts"]
        if verbose:
            print("Metacell construction complete for both RNA and ATAC data.")
        return adata_meta_rna, adata_meta_atac
    else:
        if verbose:
            print("Metacell construction complete for RNA data only.")
        return adata_meta_rna


@beartype
def convert_to_dense(layer):
    """
    Convert a sparse matrix to a dense numpy array.

    Args:
        layer: Input array or sparse matrix.

    Returns:
        Dense numpy array.
    """
    if sp.issparse(layer):
        return layer.toarray()
    else:
        return layer


@beartype
def filter_genes(
    adata_rna: AnnData,
    tf_list: List[str],
    n_top_genes: int = 1000,
    count_threshold: Optional[int] = None,
) -> AnnData:
    """
    Filters genes in the AnnData object by selecting the most variable genes
    and optionally including transcription factors (TFs) above a count threshold.

    Parameters:
    - adata_rna: AnnData object containing gene expression data.
    - tf_list: List of transcription factors to consider.
    - n_top_genes: Number of most variable genes to retain (default: 1000).
    - count_threshold: Optionally add all TFs above this total count threshold. If set to None,
      no additional TFs are added.

    Returns:
    - Filtered AnnData object.
    """
    # Step 1: Filter to the most variable genes
    sc.pp.highly_variable_genes(adata_rna, n_top_genes=n_top_genes)
    highly_variable_genes = set(adata_rna.var[adata_rna.var["highly_variable"]].index)

    # Step 2: Optionally filter TFs based on total counts
    if count_threshold is not None:
        tf_in_adata = [tf for tf in tf_list if tf in adata_rna.var_names]
        tf_with_counts = [
            tf
            for tf in tf_in_adata
            if np.sum(
                adata_rna[:, tf].layers["spliced"]
                + adata_rna[:, tf].layers["unspliced"]
            )
            >= count_threshold
        ]
        highly_variable_genes = highly_variable_genes.union(tf_with_counts)

    # Step 3: Subset the AnnData object
    final_genes = list(set(highly_variable_genes) & set(adata_rna.var_names))
    return adata_rna[:, final_genes]


@beartype
def filter_regions(
    adata_atac: AnnData,
    min_cells: int = 5,
    target_sum: Union[int, float] = 1e4,
    n_top_regions: int = 10**6,
) -> AnnData:
    """
    Filter an ATAC-seq AnnData object to retain the most important regions through a
    series of preprocessing steps. The procedure includes filtering regions by the
    minimum number of cells in which they are detected, normalizing and log-transforming
    the data to compute variability, and finally subsetting to the top variable regions.

    Parameters
    ----------
    adata_atac : AnnData
        An AnnData object containing ATAC-seq peak count data.
    min_cells : int, optional
        Minimum number of cells in which a region must be detected to be retained.
    target_sum : int or float, optional
        The target total count for normalization per cell.
    n_top_regions : int, optional
        The number of top variable regions to select. Setting this to a high value (e.g., 10**6)
        will effectively retain all regions after filtering.

    Returns
    -------
    AnnData
        The filtered AnnData object containing only the selected regions.

    Example
    -------
    >>> filtered_atac = filter_peaks(adata_atac, min_cells=5, target_sum=1e4, n_top_regions=10**6)
    >>> print(filtered_atac.shape)
    """

    # Step 1: Filter peaks that are detected in at least `min_cells` cells.
    sc.pp.filter_genes(adata_atac, min_cells=min_cells)

    # Step 2: Save the raw counts.
    adata_atac.layers["raw_counts"] = adata_atac.X.copy()

    # Step 3: Normalize total counts per cell.
    sc.pp.normalize_total(adata_atac, target_sum=target_sum)

    # Step 4: Log-transform the data.
    sc.pp.log1p(adata_atac)

    # Step 5: Identify highly variable peaks and subset the AnnData object.
    sc.pp.highly_variable_genes(adata_atac, n_top_genes=n_top_regions, subset=True)

    # Step 6: Restore the original raw counts and remove the temporary layer.
    adata_atac.X = adata_atac.layers["raw_counts"]
    del adata_atac.layers["raw_counts"]

    return adata_atac


@beartype
def filter_motif_scores(
    motif_scores: pd.DataFrame,
    adata_rna: AnnData,
    adata_atac: AnnData,
    rna_col: str,
    atac_col: str,
) -> pd.DataFrame:
    """
    Filter the motif_scores DataFrame based on the variable names in the provided AnnData objects.

    The function performs two filtering steps:
      1. Keeps only those rows in `motif_scores` where the value in the column specified by
         `rna_col` exists in `adata_rna.var_names`.
      2. From the resulting DataFrame, keeps only those rows where the value in the column
         specified by `atac_col` exists in `adata_atac.var_names`.

    Parameters
    ----------
    motif_scores : pd.DataFrame
        DataFrame containing motif scores. Must include at least the columns defined by `rna_col`
        and `atac_col`.
    adata_rna : AnnData
        An AnnData object containing RNA data. Its `var_names` are used to filter the column
        specified by `rna_col` in `motif_scores`.
    adata_atac : AnnData
        An AnnData object containing ATAC data. Its `var_names` are used to filter the column
        specified by `atac_col` in `motif_scores`.
    rna_col : str
        The column name in `motif_scores` corresponding to RNA gene names.
    atac_col : str
        The column name in `motif_scores` corresponding to ATAC peak identifiers.

    Returns
    -------
    pd.DataFrame
        The filtered motif_scores DataFrame containing only rows where:
          - The value in `rna_col` is present in `adata_rna.var_names`, and
          - The value in `atac_col` is present in `adata_atac.var_names`.

    Example
    -------
    >>> filtered_scores = filter_motif_scores(motif_scores, adata_rna, adata_atac)
    >>> print(filtered_scores.shape)
    """
    # Filter based on RNA variable names.
    subset_rna = [g in adata_rna.var_names for g in motif_scores[rna_col]]
    filtered_scores = motif_scores.loc[subset_rna, :]

    # Filter based on ATAC variable names.
    subset_atac = [m in adata_atac.var_names for m in filtered_scores[atac_col]]
    filtered_scores = filtered_scores.loc[subset_atac, :]

    return filtered_scores


def extract_region_tf_pairs(
    dataframe, adata_atac, adata_rna, region_col="peak_name", tf_col="Motif_name"
):
    """
    Extract non-zero region-TF pairs.

    Args:
        dataframe: A pandas DataFrame containing region-TF metadata.
        adata_atac: AnnData object for ATAC data (regions/peaks).
        adata_rna: AnnData object for RNA data (genes/TFs).
        region_col: Column name for region (peak) identifiers in the DataFrame.
        tf_col: Column name for TF (gene) names in the DataFrame.

    Returns:
        region_tf_pairs: A JAX numpy array of region-TF pairs.
    """
    # Collect region-TF pairs as tuples
    region_tf_pairs = []
    for _, row in dataframe.iterrows():
        region_name = row[region_col]
        tf_name = row[tf_col]

        # Check existence in AnnData objects
        if region_name in adata_atac.var_names and tf_name in adata_rna.var_names:
            region_idx = adata_atac.var_names.get_loc(region_name)
            tf_idx = adata_rna.var_names.get_loc(tf_name)
            region_tf_pairs.append((region_idx, tf_idx))

    # Convert to jax array
    region_tf_pairs = jnp.array(region_tf_pairs, dtype=np.int32)

    return region_tf_pairs


def build_gene_tss_dict(adata_rna, dataset_name="mmusculus_gene_ensembl"):
    """
    Query Ensembl Biomart for chromosome, start, end, strand, and external_gene_name,
    then build a dictionary: gene_name -> (chrom, TSS).

    Args:
        adata_rna: an AnnData object with gene names in `adata_rna.var_names`
        dataset_name: typically "mmusculus_gene_ensembl" for mouse.

    Returns:
        gene_dict: {gene_name: (chrom, tss)}
                   where 'chrom' is a string (e.g., '1', '2', 'X')
                         'tss'   is an integer
    """
    # 1) Connect to Ensembl via pybiomart
    server = Server(host="http://www.ensembl.org")
    dataset = server.marts["ENSEMBL_MART_ENSEMBL"].datasets[dataset_name]

    # 2) Query for genes
    df = dataset.query(
        attributes=[
            "chromosome_name",  # might return 'Chromosome/scaffold name'
            "start_position",  # might return 'Gene start (bp)'
            "end_position",  # might return 'Gene end (bp)'
            "strand",  # might return 'Strand'
            "external_gene_name",  # might return 'Gene name'
        ]
    )

    rename_dict = {}
    for col in df.columns:
        c_lower = col.lower()
        if "chromosome" in c_lower:
            rename_dict[col] = "chromosome_name"
        elif "start" in c_lower:
            rename_dict[col] = "start_position"
        elif "end" in c_lower:
            rename_dict[col] = "end_position"
        elif "strand" in c_lower:
            rename_dict[col] = "strand"
        elif "gene name" in c_lower or "external_gene_name" in c_lower:
            rename_dict[col] = "external_gene_name"

    df.rename(columns=rename_dict, inplace=True)

    # 4) Convert to a dictionary: gene_name -> (chrom, tss)
    #    TSS depends on the strand
    gene_dict = {}
    rna_gene_set = set(adata_rna.var_names)

    for row in df.itertuples(index=False):
        chrom = str(row.chromosome_name)
        start = int(row.start_position)
        end = int(row.end_position)
        strand = int(row.strand)  # 1 or -1 for Ensembl
        gname = str(row.external_gene_name)

        # Skip if gene not in adata_rna
        if gname not in rna_gene_set:
            continue

        # Optional: skip weird contigs
        if not chrom.isdigit() and chrom not in ["X", "Y"]:
            continue

        # TSS depends on strand
        tss = start if strand == 1 else end

        # If multiple lines appear for the same gene, you can decide how to handle them
        if gname not in gene_dict:
            gene_dict[gname] = (chrom, tss)

    return gene_dict


def parse_region_name(region_str):
    """
    Parse region like 'chr1:1000-2000' => (chrom, start, end).
    If your naming scheme is different, adapt accordingly.
    """
    region_str = region_str.replace("chr", "")  # remove "chr" if present
    chrom, coords = region_str.split(":")
    start, end = coords.split("-")
    start, end = int(start), int(end)
    return chrom, start, end


def build_pyranges_for_regions(adata_atac):
    """
    Convert each region in adata_atac.var_names into a PyRanges object
    with columns: Chromosome, Start, End, region_idx.
    """
    rows = []
    for region_idx, region_str in enumerate(adata_atac.var_names):
        chrom, start, end = parse_region_name(region_str)
        rows.append([chrom, start, end, region_idx])
    df_regions = pd.DataFrame(
        rows, columns=["Chromosome", "Start", "End", "region_idx"]
    )
    return pr.PyRanges(df_regions)


def build_pyranges_for_genes(adata_rna, gene_dict):
    """
    For each gene in adata_rna, if it's in gene_dict, create a PyRanges interval
    at [tss, tss+1]. Columns: Chromosome, Start, End, gene_idx.
    """
    rows = []
    for gene_idx, gene_name in enumerate(adata_rna.var_names):
        if gene_name not in gene_dict:
            continue
        chrom, tss = gene_dict[gene_name]
        rows.append([chrom, tss, tss + 1, gene_idx])
    df_genes = pd.DataFrame(rows, columns=["Chromosome", "Start", "End", "gene_idx"])
    return pr.PyRanges(df_genes)


def build_region_gene_pairs(
    adata_atac, adata_rna, distance1=5_000, distance2=500_000, species="mouse"
):
    """
    Build a jax array of shape (N, 3): [region_idx, gene_idx, weight].

    Rules:
      - If distance < 5 kb => weight = 1.0
      - Else if distance < 200 kb => weight = 0
      - Otherwise, exclude the pair
      - Exclusive logic: If a region is within 5 kb of ANY gene => only keep 1.0 pairs
    """

    # 1) Build gene TSS dict (using pybiomart)
    if species == "mouse":
        dsname = "mmusculus_gene_ensembl"
    elif species == "human":
        dsname = "hsapiens_gene_ensembl"
    gene_dict = build_gene_tss_dict(adata_rna, dataset_name=dsname)

    # 2) Convert to PyRanges
    gr_regions = build_pyranges_for_regions(adata_atac)
    gr_genes = build_pyranges_for_genes(adata_rna, gene_dict)

    # 3) Expand the gene intervals by ±distance2 => up to 200 kb
    gr_genes_expanded = gr_genes.slack(distance2)

    # 4) Join region intervals with expanded gene intervals => all pairs < 200 kb
    joined = gr_regions.join(gr_genes_expanded)
    df_joined = joined.df

    region_start_col = "Start"
    region_end_col = "End"
    gene_start_col = "Start_b"
    gene_end_col = "End_b"

    if "Start_a" in df_joined.columns:
        region_start_col = "Start_a"
        region_end_col = "End_a"
    if "Start_b" not in df_joined.columns:
        # Possibly "Start" is for genes, "Start_a" for regions
        # We'll guess the columns by checking region_idx vs gene_idx
        if "Start_a" in df_joined.columns and "gene_idx" in df_joined.columns:
            # Then "Start_a", "End_a" might be region, so "Start_b", "End_b" is gene
            # But if we don't see "Start_b", it might be "Start"
            pass
        else:
            # or handle more systematically
            pass

    # 5) Compute distances
    region_mid = (df_joined[region_start_col] + df_joined[region_end_col]) // 2
    gene_tss = (df_joined[gene_start_col] + df_joined[gene_end_col]) // 2
    distance = (region_mid - gene_tss).abs()

    # 6) Assign raw weight
    #    We'll skip rows >= distance2 (200 kb)
    valid_mask = distance < distance2
    df_valid = df_joined[valid_mask].copy()

    # Mark rows < 5 kb => 1.0
    raw_weight = np.full(len(df_valid), 0)
    mask1 = distance[valid_mask] < distance1
    raw_weight[mask1] = 1

    df_valid["weight"] = raw_weight

    # 7) Enforce the exclusive logic:
    #    If a region has any 1.0 link, discard that region's 0 links)
    out_list = []
    grouped = df_valid.groupby("region_idx", sort=False)
    for _, subdf in grouped:
        if (subdf["weight"] == 1.0).any():
            # keep only the 1.0 rows
            keep_rows = subdf[subdf["weight"] == 1.0]
        else:
            # keep 0
            keep_rows = subdf
        out_list.append(keep_rows)

    df_final = pd.concat(out_list, ignore_index=True)

    # 8) Extract columns => [region_idx, gene_idx, weight]
    out_array = df_final[["region_idx", "gene_idx", "weight"]].to_numpy(
        dtype=np.float32
    )

    # Convert to JAX array
    region_gene_pairs = jnp.array(out_array)

    return region_gene_pairs


def construct_region_tf_gene_triplets(region_tf_pairs, region_gene_pairs):
    """
    Constructs all unique (region, tf, gene) combinations based on existing pairs.

    Args:
        region_tf_pairs: JAX array of shape (num_pairs, 2) with [region_idx, tf_idx]
        region_gene_pairs: JAX array of shape (num_rg_pairs, 3) with [region_idx, gene_idx, score]

    Returns:
        region_tf_gene_triplets: JAX array of shape (P, 3) with [region_idx, tf_idx, gene_idx]
    """
    # Convert JAX arrays to NumPy arrays for preprocessing
    region_tf_pairs_np = np.array(region_tf_pairs)
    region_gene_pairs_np = np.array(region_gene_pairs)

    region_to_tfs = {}
    for pair in region_tf_pairs_np:
        region, tf = pair
        region = int(region)  # Convert to Python int
        tf = int(tf)  # Convert to Python int
        region_to_tfs.setdefault(region, []).append(tf)

    region_to_genes = {}
    for pair in region_gene_pairs_np:
        region, gene = pair[:2]  # Ignore the third column
        region = int(region)  # Convert to Python int
        gene = int(gene)  # Convert to Python int
        region_to_genes.setdefault(region, []).append(gene)

    # Now, create all (region, tf, gene) triplets where tf and gene share the same region
    region_tf_gene_triplets = []
    for region in region_to_tfs:
        tfs = region_to_tfs[region]
        genes = region_to_genes.get(region, [])
        for tf in tfs:
            for gene in genes:
                region_tf_gene_triplets.append([region, tf, gene])

    # Convert the list to a NumPy array and then to a JAX array
    region_tf_gene_triplets_np = np.array(region_tf_gene_triplets, dtype=int)
    region_tf_gene_triplets_jax = jnp.array(region_tf_gene_triplets_np)

    return region_tf_gene_triplets_jax


def rhg_to_rh_indexing(region_tf_gene_triplets, region_tf_pairs):
    """
    Map each [R, H, G] triplet in region_tf_gene_triplets to an index in region_tf_pairs [R, H].

    Args:
        region_tf_gene_triplets: numpy array of shape (num_rtg_triplets, 3) with [region_idx, tf_idx, gene_idx].
        region_tf_pairs: numpy array of shape (num_rt_pairs, 2) with [region_idx, tf_idx].

    Returns:
        rhg_indices: numpy array of shape (num_rtg_triplets,) mapping each triplet to index in region_tf_pairs.
    """

    # Make sure everything is np.array
    region_tf_gene_triplets_np = np.array(region_tf_gene_triplets)
    region_tf_pairs_np = np.array(region_tf_pairs)

    # Tranfsorm region-TF pairs from each array (region_idx:tf_idx, e.g. 1:3000)
    rhg_rh = (
        region_tf_gene_triplets_np[:, 0].astype(str)
        + ":"
        + region_tf_gene_triplets_np[:, 1].astype(str)
    )
    rh_rh = (
        region_tf_pairs_np[:, 0].astype(str)
        + ":"
        + region_tf_pairs_np[:, 1].astype(str)
    )

    # Make region-TF-pairs a lookup dictionary
    rh_map = {val: idx for idx, val in enumerate(rh_rh)}

    # Get indices inside region-gene-pairs (rh) for every element in region-tf-gene-triplets (rhg)
    rhg_indices = np.array([rh_map.get(x, -1) for x in rhg_rh])

    # Raise error if -1 is present
    if (rhg_indices == -1).any():
        raise ValueError(
            "Unmapped entries in region_tf_pairs. Not present in region_tf_gene_triplets."
        )

    return rhg_indices


@beartype
def create_dir_if_not_exists(directory: Path) -> None:
    """
    Create the directory if it does not exist.
    """
    if not directory.exists():
        logger.info(f"Creating directory: {directory}")
        directory.mkdir(parents=True, exist_ok=True)


@beartype
def download_file(url: str, out_path: Path) -> None:
    """
    Download a file from `url` to `out_path` using wget.

    Parameters
    ----------
    url : str
        The URL to download from
    out_path : Path
        The local file path to save the downloaded file
    """
    if out_path.exists():
        logger.info(f"File already exists: {out_path}. Skipping download.")
        return
    cmd = f"wget --no-verbose -O {out_path} {url}"
    logger.info(f"Downloading {url} -> {out_path}")
    subprocess.run(cmd, shell=True, check=True)


@beartype
def unzip_gz(file_path: Path, remove_input: bool = False) -> None:
    """
    Gzip-decompress a file. If remove_input=True, deletes the original .gz file.

    Parameters
    ----------
    file_path : Path
    remove_input : bool
    """
    cmd = f"gzip -d {file_path}"
    logger.info(f"Decompressing {file_path}")
    subprocess.run(cmd, shell=True, check=True)
    if remove_input:
        gz_file = file_path
        if gz_file.exists():
            gz_file.unlink()


@beartype
def resolve_genome_urls(
    species: str,
    assembly: str,
    gtf_url: Optional[str],
    chrom_sizes_url: Optional[str],
    fasta_url: Optional[str],
) -> tuple[str, str, str]:
    """
    Decide which URLs to use for GTF, chrom.sizes, and FASTA based on:
    1) species & assembly (e.g. "mouse", "mm10" or "human", "hg38")
    2) user overrides in config

    Returns
    -------
    (final_gtf_url, final_chrom_sizes_url, final_fasta_url)

    If the user didn't provide a URL and we know a default for that assembly, we use it.
    Otherwise, raise an error if we can't guess a default.
    """
    # If user provided them in config, we override. If not, we set defaults for known combos.
    final_gtf_url = gtf_url
    final_chrom_sizes_url = chrom_sizes_url
    final_fasta_url = fasta_url

    # Known defaults for mouse mm10
    if species.lower() == "mouse" and assembly.lower() == "mm10":
        if final_gtf_url is None:
            final_gtf_url = (
                "https://ftp.ebi.ac.uk/pub/databases/gencode/"
                "Gencode_mouse/release_M18/gencode.vM18.basic.annotation.gtf.gz"
            )
        if final_chrom_sizes_url is None:
            final_chrom_sizes_url = "https://hgdownload.cse.ucsc.edu/goldenpath/mm10/bigZips/mm10.chrom.sizes"
        if final_fasta_url is None:
            final_fasta_url = (
                "https://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/mm10.fa.gz"
            )

    # Known defaults for human hg38
    elif species.lower() == "human" and assembly.lower() == "hg38":
        if final_gtf_url is None:
            final_gtf_url = (
                "https://ftp.ebi.ac.uk/pub/databases/gencode/"
                "Gencode_human/release_47/gencode.v47.primary_assembly.basic.annotation.gtf.gz"
            )
        if final_chrom_sizes_url is None:
            final_chrom_sizes_url = "https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/hg38.chrom.sizes"
        if final_fasta_url is None:
            final_fasta_url = (
                "https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/hg38.fa.gz"
            )

    else:
        # Unknown assembly => user must provide or raise an error if any is None
        if (
            final_gtf_url is None
            or final_chrom_sizes_url is None
            or final_fasta_url is None
        ):
            raise ValueError(
                f"Unknown assembly '{assembly}' for species='{species}'. "
                "Please provide gtf_url, chrom_sizes_url, and fasta_url in config."
            )

    return (final_gtf_url, final_chrom_sizes_url, final_fasta_url)


@beartype
def download_genome_references(
    genome_dir: Path,
    species: str,
    assembly: str,
    gtf_url: Optional[str] = None,
    chrom_sizes_url: Optional[str] = None,
    fasta_url: Optional[str] = None,
) -> None:
    """
    Download GTF, chromosome sizes, and FASTA for the specified species & assembly
    if not already present locally. If any URL is not provided, attempt to
    use known defaults for recognized combos (e.g. mouse/mm10, human/hg38).
    Otherwise, user must supply them in config.

    Parameters
    ----------
    genome_dir : Path
    species : str
    assembly : str
    gtf_url : str | None
    chrom_sizes_url : str | None
    fasta_url : str | None
    """
    genome_dir.mkdir(parents=True, exist_ok=True)

    # 1) Resolve the final URLs based on species/assembly + user overrides
    final_gtf_url, final_chrom_sizes_url, final_fasta_url = resolve_genome_urls(
        species, assembly, gtf_url, chrom_sizes_url, fasta_url
    )
    logger.info(
        f"Using genome references for species='{species}', assembly='{assembly}'.\n"
        f"GTF: {final_gtf_url}\n"
        f"Chrom.sizes: {final_chrom_sizes_url}\n"
        f"FASTA: {final_fasta_url}"
    )

    # Decide on local filenames
    gtf_gz = genome_dir / f"{species}_annotation.gtf.gz"
    gtf_final = genome_dir / f"{species}_annotation.gtf"
    chrom_sizes_path = genome_dir / f"{species}_{assembly}.chrom.sizes"
    fasta_gz = genome_dir / f"{species}_{assembly}.fa.gz"
    fasta_final = genome_dir / f"{species}_{assembly}.fa"

    # 2) GTF
    if not gtf_final.exists():
        download_file(final_gtf_url, gtf_gz)
        unzip_gz(gtf_gz, remove_input=True)

    # 3) chrom sizes
    if not chrom_sizes_path.exists():
        download_file(final_chrom_sizes_url, chrom_sizes_path)

    # 4) FASTA
    if not fasta_final.exists():
        download_file(final_fasta_url, fasta_gz)
        unzip_gz(fasta_gz, remove_input=True)

    logger.info(f"Reference files are ready in {genome_dir}")


@beartype
def func_mitochondrial_genes(data_rna: AnnData) -> AnnData:
    orig_num_genes = data_rna.shape[1]
    data_rna.var["mt"] = [gene.lower().startswith("mt-") for gene in data_rna.var_names]
    keep_mask = ~data_rna.var["mt"]
    data_rna = data_rna[:, keep_mask].copy()
    dropped = orig_num_genes - data_rna.shape[1]

    logger.info(f"Removed {dropped} mitochondrial genes with prefix= mt-")
    return data_rna


@beartype
def func_protein_coding_genes(data_rna: AnnData, gtf_df: pd.DataFrame) -> AnnData:
    # Remove non-protein coding genes based on annotation
    df_protein_coding = gtf_df[gtf_df["gene_type"] == "protein_coding"]
    pc_genes = set(df_protein_coding["gene_name"].unique())
    rna_genes = set(data_rna.var_names)
    keep_genes = sorted(list(pc_genes & rna_genes))
    data_rna = data_rna[:, keep_genes].copy()
    logger.info(f"Filtered to protein-coding genes: {data_rna.shape[1]} genes left.")
    return data_rna


@beartype
def TF_HVG_selection(
    data_rna: AnnData,
    motif_dir: Path,
    num_genes_hvg: int,
    num_tfs_hvg: int,
    species: str,
    motif_database: str,
) -> tuple[AnnData, list[str], list[str]]:
    logger.info("Selecting HVGs and TFs...")

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

    # Computing HVG among TFs
    tf_candidates = sorted(list(set(tf_names_all) & set(data_rna.var_names)))
    data_rna_tf = data_rna[:, tf_candidates].copy()

    sc.pp.normalize_total(data_rna_tf)
    sc.pp.log1p(data_rna_tf)
    sc.pp.highly_variable_genes(data_rna_tf, n_top_genes=num_tfs_hvg, subset=True)

    selected_tfs = sorted(list(data_rna_tf.var_names))

    # Computing HVG among non-TFs
    non_tf_candidates = set(data_rna.var_names) - set(
        selected_tfs
    )  # wouldnt it need to exlude tf_candidates and not selected_tfs
    data_rna_non_tf = data_rna[:, sorted(list(non_tf_candidates))].copy()

    sc.pp.normalize_total(data_rna_non_tf)
    sc.pp.log1p(data_rna_non_tf)
    sc.pp.highly_variable_genes(data_rna_non_tf, n_top_genes=num_genes_hvg, subset=True)

    selected_non_tfs = sorted(set(data_rna_non_tf.var_names))
    selected_non_tfs = [
        g for g in selected_non_tfs if g not in selected_tfs
    ]  # isn't this line obsolete

    final_genes = selected_non_tfs
    final_tfs = selected_tfs

    combined = final_genes + final_tfs
    data_rna = data_rna[:, combined].copy()

    # Mark gene_type in .var
    gene_types = ["HVG"] * len(final_genes) + ["TF"] * len(final_tfs)
    data_rna.var["gene_type"] = gene_types

    logger.info(
        f"Selected {len(final_genes)} HVGs from {len(non_tf_candidates)} available HVGs  + {len(final_tfs)} TFs from {len(tf_candidates)} available TFs."
    )
    return data_rna, final_genes, final_tfs


@beartype
def check_command_availability(command: str) -> bool:
    """
    Check if a command is available in the system PATH.

    Parameters
    ----------
    command : str
        The command name to check

    Returns
    -------
    bool
        True if the command is available, False otherwise
    """
    return shutil.which(command) is not None


@beartype
def bed_file_intersection(
    genome_dir: Path,
    output_dir: Path,
    data_atac: AnnData,
    genome_assembly: str,
    species: str,
    window_size: int,
    gtf_df: pd.DataFrame,
    final_genes: list[str],
    final_tfs: list[str],
) -> AnnData:
    """
    1. Create Bed files for all genes and TFs
    2. Create Bed files for all peaks
    3. Create Bed files for intersection betwenn Peaks and Genes + TFs
    """
    logger.info(f"Before gene-window filtering => shape={data_atac.shape}")

    # 1 Create Bed files for all genes and TFs

    # Load chromosome data
    chrom_sizes_path = genome_dir / f"{species}_{genome_assembly}.chrom.sizes"

    # Filter for final genes & gene features
    gtf_gene = gtf_df[gtf_df["feature"] == "gene"].drop_duplicates("gene_name")
    gtf_gene = gtf_gene.set_index("gene_name")
    gtf_gene = gtf_gene.loc[sorted(set(final_genes + final_tfs) & set(gtf_gene.index))]

    # rename for clarity
    gtf_gene["chr"] = gtf_gene["seqname"]

    # If we want clamping, load chrom.sizes
    chrom_dict = {}
    if chrom_sizes_path is not None:
        chrom_sizes = pd.read_csv(
            chrom_sizes_path, sep="\t", header=None, names=["chrom", "size"]
        )
        chrom_dict = dict(zip(chrom_sizes["chrom"], chrom_sizes["size"]))

    extended_rows = []
    for gene in gtf_gene.index:
        row = gtf_gene.loc[gene]
        chr_ = row["chr"]
        start_ = row["start"]
        end_ = row["end"]
        strand_ = row["strand"] if "strand" in row else "+"

        start_extended = max(0, start_ - window_size)
        end_extended = end_ + window_size

        if chr_ in chrom_dict:
            chr_len = chrom_dict[chr_]
            if end_extended > chr_len:
                end_extended = chr_len
            # If start_extended < 0, we already clamp to 0 above

        extended_rows.append([chr_, start_extended, end_extended, gene, strand_])

    extended_genes_bed_df = pd.DataFrame(
        extended_rows, columns=["chr", "start_new", "end_new", "gene_name", "strand"]
    )

    # Save extended gene bed file
    gene_bed = output_dir / f"genes_extended_{window_size // 1000}kb.bed"
    extended_genes_bed_df.to_csv(gene_bed, sep="\t", header=False, index=False)
    logger.info(f"Created extended gene bed => {gene_bed}")

    # 2 Create Bed files for all peaks
    data_atac.var["chr"] = [x.split(":")[0] for x in data_atac.var.index]
    data_atac.var["start"] = [
        int(x.split(":")[1].split("-")[0]) for x in data_atac.var.index
    ]
    data_atac.var["end"] = [
        int(x.split(":")[1].split("-")[1]) for x in data_atac.var.index
    ]
    data_atac.var["peak_name"] = data_atac.var.index
    all_peaks_bed = output_dir / Path("peaks_all.bed")
    data_atac.var[["chr", "start", "end", "peak_name"]].to_csv(
        all_peaks_bed, sep="\t", header=False, index=False
    )

    # 3 Create Bed files for intersection between Peaks and Genes + TFs
    intersected_bed = output_dir / Path("peaks_intersected.bed")

    if check_command_availability("bedtools"):
        cmd = f"bedtools intersect -u -wa -a {all_peaks_bed} -b {gene_bed} > {intersected_bed}"
        logger.info(f"Running: {cmd}")

        try:
            subprocess.run(cmd, shell=True, check=True)

            peaks_intersected = pd.read_csv(intersected_bed, sep="\t", header=None)
            peaks_intersected.columns = ["chr", "start", "end", "peak_name"]
            windowed_set = set(peaks_intersected["peak_name"])

        except subprocess.CalledProcessError:
            logger.warning(
                "Error running bedtools. Using fallback method for intersection."
            )
            windowed_set = simple_bed_intersection(all_peaks_bed, gene_bed)
    else:
        logger.warning(
            "bedtools command not found in PATH. Using fallback Python-based intersection method. "
            "For better performance, please install bedtools (https://bedtools.readthedocs.io/)."
        )
        windowed_set = simple_bed_intersection(all_peaks_bed, gene_bed)

    # Subset data_atac to these peaks
    data_atac = data_atac[:, list(windowed_set)].copy()
    logger.info(f"After gene-window filtering => shape={data_atac.shape}")
    return data_atac


@beartype
def simple_bed_intersection(peaks_bed: Path, genes_bed: Path) -> set:
    """
    A simple Python-based implementation of `bedtools intersect` for when bedtools
    is not available. This is a fallback method that performs the intersection
    without requiring bedtools.

    Parameters
    ----------
    peaks_bed : Path
        Path to the BED file containing peaks
    genes_bed : Path
        Path to the BED file containing extended gene regions

    Returns
    -------
    set
        Set of peak names that overlap with any gene region
    """
    logger.info("Using Python-based intersection as fallback for bedtools")

    peaks = pd.read_csv(peaks_bed, sep="\t", header=None)
    peaks.columns = ["chr", "start", "end", "peak_name"]

    genes = pd.read_csv(genes_bed, sep="\t", header=None)
    genes.columns = ["chr", "start", "end", "gene_name", "strand"]

    peaks_by_chr = {chr_name: group for chr_name, group in peaks.groupby("chr")}
    genes_by_chr = {chr_name: group for chr_name, group in genes.groupby("chr")}

    overlapping_peaks = set()

    for chr_name, chr_peaks in peaks_by_chr.items():
        if chr_name not in genes_by_chr:
            continue

        chr_genes = genes_by_chr[chr_name]

        for _, peak in chr_peaks.iterrows():
            peak_start = peak["start"]
            peak_end = peak["end"]

            for _, gene in chr_genes.iterrows():
                gene_start = gene["start"]
                gene_end = gene["end"]

                if not (peak_end <= gene_start or peak_start >= gene_end):
                    overlapping_peaks.add(peak["peak_name"])
                    break

    overlapping_peaks_df = peaks[peaks["peak_name"].isin(overlapping_peaks)]
    intersected_bed = peaks_bed.parent / "peaks_intersected.bed"
    overlapping_peaks_df.to_csv(intersected_bed, sep="\t", header=False, index=False)

    logger.info(
        f"Found {len(overlapping_peaks)} peaks overlapping with extended gene regions"
    )
    return overlapping_peaks


@beartype
def create_metacells(
    data_rna: AnnData,
    data_atac: AnnData,
    grouping_key: str,
    resolution: int,
    batch_key: str,
) -> tuple[AnnData, AnnData]:
    """
    1) Normalize, run PCA + harmony integration on batch_key ,
    2) cluster using leiden => store in data_rna.obs[grouping_key]
    3) Summarize expression & accessibility per cluster => metacell.

    Returns two AnnData objects: (rna_metacell, atac_metacell).

    Parameters
    ----------
    data_rna : AnnData
    data_atac : AnnData
    grouping_key : str
    resolution : float
    batch_key : str

    Returns
    -------
    (rna_metacell, atac_metacell)
    """
    logger.info(
        f"Creating metacells with resolution={resolution} (grouping key={grouping_key})."
    )
    # Keep original counts in a layer
    data_rna.layers["counts"] = data_rna.X.copy()

    # Normalize & run PCA
    sc.pp.normalize_total(data_rna)
    sc.pp.log1p(data_rna)
    sc.pp.pca(data_rna)

    # Harmony integration
    sce.pp.harmony_integrate(
        data_rna, batch_key
    )  # does that even apply to us if we only have one dataset per analysis?

    sc.pp.neighbors(data_rna, use_rep="X_pca_harmony")
    sc.tl.leiden(data_rna, resolution=resolution, key_added=grouping_key)

    # Summarize
    clusters = data_rna.obs[grouping_key].unique()
    cluster_groups = data_rna.obs.groupby(grouping_key)

    mean_rna_list = []
    mean_atac_list = []
    cluster_names = []

    for cluster_name in clusters:
        cell_idx = cluster_groups.get_group(cluster_name).index

        # RNA
        rna_vals = data_rna[cell_idx].X
        if sp.issparse(rna_vals):
            # 2) Convert to dense
            rna_vals = rna_vals.toarray()  # or atac_vals.A
        mean_rna = np.array(rna_vals.mean(axis=0)).ravel()
        mean_rna_list.append(mean_rna)

        # ATAC
        if len(set(cell_idx).intersection(data_atac.obs_names)) == 0:
            mean_atac_list.append(np.zeros(data_atac.shape[1]))
        else:
            atac_vals = data_atac[cell_idx].X

            if sp.issparse(atac_vals):
                # 2) Convert to dense
                atac_vals = atac_vals.toarray()  # or atac_vals.A
            # get fragment values from insertions
            atac_bin = (atac_vals + 1) // 2
            mean_atac = np.array(atac_bin.mean(axis=0)).ravel()
            mean_atac_list.append(mean_atac)

        cluster_names.append(cluster_name)

    # Build new AnnData
    mean_rna_arr = np.vstack(mean_rna_list)
    mean_atac_arr = np.vstack(mean_atac_list)

    obs_df = pd.DataFrame({grouping_key: cluster_names}).set_index(grouping_key)

    rna_metacell = AnnData(X=mean_rna_arr, obs=obs_df, var=data_rna.var)
    atac_metacell = AnnData(X=mean_atac_arr, obs=obs_df, var=data_atac.var)

    logger.info(
        f"Metacell shapes: RNA={rna_metacell.shape}, ATAC={atac_metacell.shape}"
    )
    return rna_metacell, atac_metacell


@beartype
def select_highly_variable_peaks_by_std(
    data_atac: AnnData, n_top_peaks: int, cluster_key: str
) -> AnnData:
    """
    A standard HV peak selection using cluster-based std across 'leiden' or another grouping.

    """
    if cluster_key not in data_atac.obs.columns:
        logger.warning(
            f"{cluster_key} not found in data_atac.obs; skipping peak selection."
        )
        return data_atac

    clusters = data_atac.obs[cluster_key].unique()
    cluster_groups = data_atac.obs.groupby(cluster_key)
    mean_list = []

    for c_label in clusters:
        idx_cells = cluster_groups.get_group(c_label).index
        mat = data_atac[idx_cells].X
        if sp.issparse(mat):
            # 2) Convert to dense
            mat = mat.toarray()  # or mat.A
        mat = (mat + 1) // 2  # get fragments
        mean_vec = mat.mean(axis=0).A1 if hasattr(mat, "A1") else mat.mean(axis=0)
        mean_list.append(mean_vec)

    cluster_matrix = np.vstack(mean_list)  # shape=(n_clusters, n_peaks)
    stdev_peaks = cluster_matrix.std(axis=0)
    data_atac.var["std_cluster"] = stdev_peaks

    if n_top_peaks < data_atac.shape[1]:
        sorted_idx = np.argsort(stdev_peaks)[::-1]
        keep_idx = sorted_idx[:n_top_peaks]
        mask = np.zeros(data_atac.shape[1], dtype=bool)
        mask[keep_idx] = True
        data_atac_sub = data_atac[:, mask].copy()
        logger.info(
            f"Selected top {n_top_peaks} variable peaks (by std across {cluster_key})."
        )
        return data_atac_sub
    else:
        logger.info("n_top_peaks >= total peaks; no filtering applied.")
        return data_atac


@beartype
def keep_promoters_and_select_hv_peaks(
    data_atac: AnnData, total_n_peaks: int, cluster_key: str, promoter_col: str
) -> AnnData:
    """
    1) Identify all promoter peaks where var[promoter_col] == True.
    2) Keep them all.
    3) For the NON-promoter peaks in data_atac, select top (num_peaks - #promoters) by std.
    4) Final set = all promoters + HV among non-promoters.
    5) If #promoters alone >= num_peaks, we keep all promoters and skip HV selection,
        possibly exceeding num_peaks.

    Returns the new subset of data_atac.
    """
    if promoter_col not in data_atac.var.columns:
        logger.warning(
            f"Column {promoter_col} not found in data_atac.var; no special promoter logic."
        )
        # fallback: just do normal HV selection
        return select_highly_variable_peaks_by_std(
            data_atac, total_n_peaks, cluster_key
        )
    else:
        # (A) Extract promoter vs non-promoter
        promoter_mask = data_atac.var[promoter_col].values == True
        promoter_peaks = data_atac.var_names[promoter_mask]
        n_promoters = len(promoter_peaks)

        logger.info(
            f"Found {n_promoters} promoter peaks. Target total is {total_n_peaks}."
        )

        if n_promoters >= total_n_peaks:
            # Just keep all promoters, ignoring user target or raise warning
            logger.warning(
                f"Promoter peaks ({n_promoters}) exceed num_peaks={total_n_peaks}. "
                "Keeping all promoters, final set might exceed user target."
            )
            data_atac_sub = data_atac[:, promoter_peaks].copy()
            return data_atac_sub
        else:
            # (B) We keep all promoters, and we can select HV among the non-promoter peaks
            n_needed = total_n_peaks - n_promoters
            logger.info(
                f"Selecting HV among non-promoters => picking {n_needed} peaks."
            )

            # Subset to non-promoters
            non_promoter_mask = ~promoter_mask
            data_atac_nonprom = data_atac[:, non_promoter_mask].copy()

            # HV selection among non-promoters for n_needed
            data_atac_nonprom_hv = select_highly_variable_peaks_by_std(
                data_atac_nonprom, n_needed, cluster_key
            )

            # Final union => promoter peaks + HV(non-promoters)
            final_promoter_set = set(promoter_peaks)
            final_nonprom_set = set(data_atac_nonprom_hv.var_names)
            final_set = list(final_promoter_set.union(final_nonprom_set))

            data_atac_sub = data_atac[:, final_set].copy()
            logger.info(
                f"Final set => {len(promoter_peaks)} promoter + "
                f"{data_atac_nonprom_hv.shape[1]} HV => total {data_atac_sub.shape[1]} peaks."
            )
            return data_atac_sub


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
    # define folder structure
    genome_dir = main_dir / Path("Prepared")
    motif_dir = main_dir / Path("Prepared")
    output_dir = main_dir / Path("Generated")

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
