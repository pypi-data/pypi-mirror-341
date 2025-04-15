import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from anndata import AnnData

from stormi.preprocessing import check_command_availability, preprocessing_pipeline


# Dummy AnnData fixture with minimal RNA and ATAC data.
@pytest.fixture
def dummy_anndata():
    # ---- Create dummy RNA AnnData object ----

    # 10 cells and 10 genes
    cell_ids = [
        "cell_1",
        "cell_2",
        "cell_3",
        "cell_4",
        "cell_5",
        "cell_6",
        "cell_7",
        "cell_8",
        "cell_9",
        "cell_10",
    ]

    gene_names = [
        "TF1",
        "TF2",
        "Gene3",
        "Gene4",
        "Gene5",
        "Gene6",
        "Gene7",
        "Gene8",
        "Gene9",
        "Gene10",
    ]

    rna_data = np.random.rand(10, 10)
    rna_obs = pd.DataFrame(index=cell_ids)
    rna_var = pd.DataFrame(index=gene_names)
    adata_rna = AnnData(X=rna_data, obs=rna_obs, var=rna_var)

    # ---- Create dummy ATAC AnnData object ----

    peak_names = [
        "chr1:110-290",
        "chr1:310-390",
        "chr1:3000-3100",
        "chr1:4000-4100",
        "chr1:5000-5100",
        "chr1:6000-6100",
        "chr1:7000-7100",
        "chr1:8000-8100",
        "chr1:9000-9100",
        "chr1:10000-10100",
    ]

    atac_data = np.random.randint(0, 5, size=(10, 10))
    atac_obs = pd.DataFrame(index=cell_ids)
    atac_var = pd.DataFrame(index=peak_names)
    adata_atac = AnnData(X=atac_data, obs=atac_obs, var=atac_var)

    return adata_rna, adata_atac


# Fixture to set up dummy file structure and dummy files.
@pytest.fixture
def dummy_files(tmp_path):
    # Create a main directory
    main_dir = tmp_path / "main_dir"
    main_dir.mkdir()
    # Create subdirectories as expected by the pipeline.
    prepared_dir = main_dir / "Prepared"
    prepared_dir.mkdir()
    generated_dir = main_dir / "Generated"
    generated_dir.mkdir()

    # Create a dummy GTF file (with one line sufficient for gene filtering)

    gtf_lines = [
        'chr1\tDummySource\tgene\t100\t1500\t.\t+\t.\tgene_id "TF1"; gene_name "TF1"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t2000\t2500\t.\t+\t.\tgene_id "TF2"; gene_name "TF2"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t3000\t3500\t.\t+\t.\tgene_id "Gene3"; gene_name "mt-Gene3"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t4000\t4500\t.\t+\t.\tgene_id "Gene4"; gene_name "Gene4"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t5000\t5500\t.\t+\t.\tgene_id "Gene5"; gene_name "Gene5"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t6000\t6500\t.\t+\t.\tgene_id "Gene6"; gene_name "Gene6"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t7000\t7500\t.\t+\t.\tgene_id "Gene7"; gene_name "Gene7"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t8000\t8500\t.\t+\t.\tgene_id "Gene8"; gene_name "Gene8"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t9000\t9500\t.\t+\t.\tgene_id "Gene9"; gene_name "Gene9"; gene_type "protein_coding";',
        'chr1\tDummySource\tgene\t10000\t10500\t.\t+\t.\tgene_id "Gene10"; gene_name "Gene10"; gene_type "non_prot_coding";',
    ]

    gtf_file = prepared_dir / "mouse_annotation.gtf"
    gtf_file.write_text("\n".join(gtf_lines))

    # Create a dummy motif file with one motif.
    meme_file = prepared_dir / "cisbp_mouse.meme"
    # The line below will yield tf_name "TF1" (parts[2] is "TF1")
    motif_data = (
        "MOTIF dummy TF1\n\n"
        "letter-probability matrix: alength= 4 w= 10 nsites= 1 E= 0\n"
        "  0.220377        0.335405        0.102037        0.342181\n"
        "  0.111784        0.193750        0.669524        0.024942\n"
        "  0.009553        0.989147        0.000370        0.000929\n"
        "  0.000437        0.891193        0.000324        0.108046\n"
        "  0.046223        0.377462        0.191229        0.385087\n"
        "  0.132612        0.336106        0.329451        0.201830\n"
        "  0.430307        0.248265        0.229178        0.092250\n"
        "  0.301624        0.024759        0.651437        0.022180\n"
        "  0.055101        0.000431        0.943092        0.001376\n"
        "  0.095237        0.349453        0.435445        0.119865\n\n"
        "URL http://dummy-url.com/TF1\n\n"
        "MOTIF dummy TF2\n\n"
        "letter-probability matrix: alength= 4 w= 10 nsites= 1 E= 0\n"
        "  0.000019        0.999823        0.000038        0.000120\n"
        "  0.000091        0.899183        0.000093        0.100634\n"
        "  0.023042        0.234469        0.177208        0.565281\n"
        "  0.107618        0.390953        0.394882        0.106547\n"
        "  0.537857        0.155647        0.286458        0.020037\n"
        "  0.051649        0.000023        0.948115        0.000213\n"
        "  0.000014        0.000011        0.999930        0.000045\n"
        "  0.000011        0.667311        0.331377        0.001301\n"
        "  0.201422        0.246017        0.349115        0.203446\n"
        "  0.598826        0.108307        0.129667        0.163199\n\n"
        "URL http://dummy-url.com/TF2\n"
    )
    meme_file.write_text(motif_data)

    # Create a dummy FASTA file.
    fasta_file = prepared_dir / "mouse_mm10.fa"
    sequence = "ATC" * 600
    with open(fasta_file, "w") as f:
        f.write(">chr1\n")
        for i in range(0, 600, 53):
            f.write(sequence[i : i + 53] + "\n")

    # Create a dummy chrom.sizes file for mouse_mm10
    chrom_sizes_file = prepared_dir / "mouse_mm10.chrom.sizes"
    chrom_sizes_file.write_text("chr1\t1000000\nchr2\t2000000\n")

    return main_dir


# The full test that runs the entire pipeline
def test_preprocessing_pipeline_full(dummy_anndata, dummy_files):
    adata_rna, adata_atac = dummy_anndata
    main_dir = dummy_files

    # Check if bedtools is available - test will work with or without it
    has_bedtools = check_command_availability("bedtools")
    if not has_bedtools:
        print("bedtools not available - test will use fallback Python implementation")

    # Run the preprocessing pipeline
    result = preprocessing_pipeline(
        main_dir=main_dir,
        data_rna=adata_rna,
        data_atac=adata_atac,
        perform_clustering=False,
        chipseq_analysis=False,
        motif_match_pvalue_threshold=0.99,
        correlation_percentile=95.0,
    )

    # Check that the output files were created in the Generated directory.
    output_dir = main_dir / "Generated"
    rna_path = output_dir / "rna_processed.h5ad"
    atac_path = output_dir / "atac_processed.h5ad"

    # Both output files should exist regardless of bedtools availability
    assert rna_path.exists(), f"RNA processed file not found at {rna_path}"
    assert atac_path.exists(), f"ATAC processed file not found at {atac_path}"

    # Intersected peaks file should also exist whether bedtools is used or the fallback
    peaks_intersected_path = output_dir / "peaks_intersected.bed"
    assert peaks_intersected_path.exists(), (
        f"Intersected peaks file not found at {peaks_intersected_path}"
    )

    # the pipeline should return a DataFrame.
    assert isinstance(result, pd.DataFrame), (
        "Expected the pipeline to return a DataFrame from motif analysis."
    )
    # check that the DataFrame has the expected columns.
    expected_columns = {"peak_name", "Motif_name", "Matching_Score"}
    assert expected_columns.issubset(result.columns), (
        f"Result DataFrame is missing columns: {expected_columns - set(result.columns)}"
    )
    # Now check that the column data types are as expected.
    # For example, 'peak_name' and 'Motif_name' should be strings (object type) and 'Matching_Score' should be float.
    dtypes = result.dtypes
    assert dtypes["peak_name"] == object, (
        f"Expected 'peak_name' to be of type object, got {dtypes['peak_name']}"
    )
    assert dtypes["Motif_name"] == object, (
        f"Expected 'Motif_name' to be of type object, got {dtypes['Motif_name']}"
    )

    assert np.issubdtype(dtypes["Matching_Score"], float), (
        f"Expected 'Matching_Score' to be a float, got {dtypes['Matching_Score']}"
    )


def test_bedtools_availability():
    """Test that the bedtools availability check works correctly."""
    is_available = check_command_availability("bedtools")
    assert isinstance(is_available, bool), (
        "Expected a boolean result from check_command_availability"
    )
