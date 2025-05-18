#!/usr/bin/env python3
"""
RNA-seq Analysis Pipeline for RNAlytics

This script performs differential expression analysis and pathway enrichment
on RNA-seq data comparing CsA and VOC treatments against controls.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import scanpy as sc
import anndata as ad
from scipy import stats
from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt
import seaborn as sns

class RNASeqAnalyzer:
    def __init__(self, raw_dir: Path, processed_dir: Path):
        """Initialize the RNA-seq analyzer."""
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.treatments = ['CsA', 'VOC']
        
    def load_data(self, treatment: str) -> ad.AnnData:
        """Load raw counts data for a specific treatment."""
        counts_file = self.raw_dir / f"{treatment}_counts.csv"
        metadata_file = self.raw_dir / f"{treatment}_metadata.csv"
        
        # Load counts and metadata
        counts = pd.read_csv(counts_file, index_col=0)
        metadata = pd.read_csv(metadata_file, index_col=0)
        
        # Create AnnData object
        adata = ad.AnnData(X=counts.T, obs=metadata)
        return adata
    
    def preprocess_data(self, adata: ad.AnnData) -> ad.AnnData:
        """Preprocess the data: normalize, filter, etc."""
        sc.pp.normalize_total(adata, target_sum=1e6)  # CPM normalization
        sc.pp.log1p(adata)  # Log transformation
        
        # Filter low-expressed genes
        sc.pp.filter_genes(adata, min_cells=5)
        
        return adata
    
    def differential_expression(self, adata: ad.AnnData, treatment: str) -> pd.DataFrame:
        """Perform differential expression analysis."""
        results = []
        
        for gene in adata.var_names:
            treated = adata[adata.obs['condition'] == treatment, gene].X.flatten()
            control = adata[adata.obs['condition'] == 'control', gene].X.flatten()
            
            # Perform t-test
            t_stat, p_val = stats.ttest_ind(treated, control)
            log2fc = np.mean(treated) - np.mean(control)
            
            results.append({
                'gene': gene,
                'log2FoldChange': log2fc,
                'pvalue': p_val,
                'treatment': treatment
            })
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        
        # Multiple testing correction
        results_df['padj'] = multipletests(results_df['pvalue'], method='fdr_bh')[1]
        
        return results_df
    
    def plot_volcano(self, deg_results: pd.DataFrame, treatment: str):
        """Generate volcano plot."""
        plt.figure(figsize=(10, 8))
        
        # Define significant genes
        significant = deg_results['padj'] < 0.05
        
        # Plot
        plt.scatter(deg_results.loc[~significant, 'log2FoldChange'],
                   -np.log10(deg_results.loc[~significant, 'padj']),
                   alpha=0.5, color='gray', label='Not significant')
        
        plt.scatter(deg_results.loc[significant, 'log2FoldChange'],
                   -np.log10(deg_results.loc[significant, 'padj']),
                   alpha=0.7, color='red', label='Significant')
        
        plt.xlabel('log2 Fold Change')
        plt.ylabel('-log10(adjusted p-value)')
        plt.title(f'Volcano Plot: {treatment} vs Control')
        plt.legend()
        
        # Save plot
        plt.savefig(self.processed_dir / f"volcano_{treatment}.png")
        plt.close()
    
    def run_analysis(self):
        """Run the complete analysis pipeline."""
        for treatment in self.treatments:
            print(f"Processing {treatment}...")
            
            # Load and preprocess data
            adata = self.load_data(treatment)
            adata = self.preprocess_data(adata)
            
            # Perform differential expression
            deg_results = self.differential_expression(adata, treatment)
            
            # Save results
            deg_results.to_csv(self.processed_dir / f"deg_{treatment}.csv")
            
            # Generate plots
            self.plot_volcano(deg_results, treatment)
            
            print(f"Completed analysis for {treatment}")

if __name__ == "__main__":
    # Set up directories
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(exist_ok=True)
    
    # Initialize and run analysis
    analyzer = RNASeqAnalyzer(raw_dir, processed_dir)
    analyzer.run_analysis() 