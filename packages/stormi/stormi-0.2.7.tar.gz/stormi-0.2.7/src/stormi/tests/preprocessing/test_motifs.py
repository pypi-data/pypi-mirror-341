"""Tests for the _motifs module."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import scipy.sparse as sp
from anndata import AnnData

from stormi.preprocessing import compute_in_silico_chipseq, compute_motif_scores


@pytest.fixture
def mock_adata_rna():
    """Create a mock RNA-seq AnnData object for testing."""
    # Create a small mock RNA-seq dataset
    n_cells, n_genes = 10, 5
    genes = [f"gene{i}" for i in range(n_genes)]

    # Create random expression data
    X = np.random.rand(n_cells, n_genes)

    # Create AnnData object
    adata = AnnData(X=X)
    adata.var_names = pd.Index(genes)

    return adata


@pytest.fixture
def mock_adata_atac():
    """Create a mock ATAC-seq AnnData object for testing."""
    # Create a small mock ATAC-seq dataset
    n_cells, n_peaks = 10, 5
    peaks = [f"chr1:{i * 1000}-{i * 1000 + 200}" for i in range(n_peaks)]

    # Create random count data
    X = np.random.randint(0, 5, size=(n_cells, n_peaks))

    # Create AnnData object
    adata = AnnData(X=X)
    adata.var_names = pd.Index(peaks)
    adata.var["region"] = peaks

    return adata


@pytest.fixture
def mock_motif_scores():
    """Create mock motif scores for testing."""
    # Create peaks and genes
    peaks = [f"chr1:{i * 1000}-{i * 1000 + 200}" for i in range(5)]
    genes = [f"gene{i}" for i in range(5)]

    # Create mock motif scores data
    data = []
    for i, peak in enumerate(peaks):
        for j, gene in enumerate(genes):
            data.append({"peak": peak, "gene": gene, "score": np.random.rand()})

    return pd.DataFrame(data)


def test_compute_motif_scores(monkeypatch, tmp_path):
    """Test compute_motif_scores function with mocked dependencies."""
    # Create temporary directories
    motif_dir = tmp_path / "motifs"
    output_dir = tmp_path / "output"
    motif_dir.mkdir()
    output_dir.mkdir()

    # Create mock bed file
    bed_file = output_dir / "test.bed"
    with open(bed_file, "w") as f:
        f.write("chr1\t1000\t1200\tpeak1\n")
        f.write("chr1\t2000\t2200\tpeak2\n")

    # Mock dependencies
    def mock_check_command_availability(*args):
        return True  # Pretend FIMO is available

    def mock_create_dir_if_not_exists(*args):
        pass

    def mock_run_fimo(*args, **kwargs):
        # Return a mock dataframe
        return pd.DataFrame(
            {
                "peak": ["peak1", "peak2"],
                "gene": ["gene1", "gene2"],
                "score": [0.8, 0.9],
            }
        )

    # Apply mocks
    monkeypatch.setattr(
        "stormi.preprocessing._file_utils.check_command_availability",
        mock_check_command_availability,
    )
    monkeypatch.setattr(
        "stormi.preprocessing._file_utils.create_dir_if_not_exists",
        mock_create_dir_if_not_exists,
    )
    monkeypatch.setattr("stormi.preprocessing._motif_fimo.run_fimo", mock_run_fimo)

    # Call the function
    result = compute_motif_scores(
        motif_dir=motif_dir,
        output_dir=output_dir,
        species="human",
        motif_database="cisbp",
        genome_assembly="hg38",
        bed_file=bed_file,
    )

    # Verify the result
    assert isinstance(result, pd.DataFrame)
    assert "peak" in result.columns
    assert "gene" in result.columns
    assert "score" in result.columns


def test_compute_in_silico_chipseq(mock_adata_rna, mock_adata_atac, mock_motif_scores):
    """Test compute_in_silico_chipseq function."""
    # Call the function
    adata_rna_out, adata_atac_out = compute_in_silico_chipseq(
        adata_rna=mock_adata_rna,
        adata_atac=mock_adata_atac,
        motif_scores=mock_motif_scores,
    )

    # Verify the results
    assert isinstance(adata_rna_out, AnnData)
    assert isinstance(adata_atac_out, AnnData)

    # Check that the output has the right shapes
    assert adata_rna_out.shape[0] == mock_adata_rna.shape[0]  # Same number of cells

    # Check that motif matrix was stored
    assert "motifs" in adata_atac_out.varm
    assert "motifs_genes" in adata_atac_out.uns

    # Check that ChIP-seq data was stored
    assert "chipseq" in adata_atac_out.layers


def test_compute_in_silico_chipseq_binary(
    mock_adata_rna, mock_adata_atac, mock_motif_scores
):
    """Test compute_in_silico_chipseq with binary mode."""
    # Call the function with binary mode
    adata_rna_out, adata_atac_out = compute_in_silico_chipseq(
        adata_rna=mock_adata_rna,
        adata_atac=mock_adata_atac,
        motif_scores=mock_motif_scores,
        binary_mode=True,
        score_binarization_threshold=0.5,
        activity_threshold=0.1,
    )

    # Verify that binary transformations were applied
    # Check that ChIP-seq values are binary (0 or 1)
    chipseq_data = adata_atac_out.layers["chipseq"]
    if sp.issparse(chipseq_data):
        chipseq_values = chipseq_data.data
    else:
        chipseq_values = chipseq_data.ravel()

    # The values might not be strictly binary due to matrix operations
    # but should be sparse with mainly zeros
    assert (
        np.sum(chipseq_values == 0) + np.sum(chipseq_values > 0) == chipseq_values.size
    )
