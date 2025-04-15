#!/usr/bin/env python3
"""
Configuration utility module for TaxoPipe
"""
import os
import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Config:
    """Configuration class for TaxoPipe."""
    
    def __init__(self, raw_files, output_dir, kraken_db, corn_db, host=None, 
                 username=None, identity_file=None, password_auth=False, partition='normal', 
                 threads=16, memory='200GB', time='48:00:00', no_download_db=False, no_upload_data=False,
                 conda_env=None):
        """
        Initialize configuration.
        
        Args:
            raw_files (list): List of raw FASTQ files
            output_dir (str): Output directory on the HPC system
            kraken_db (str): Path to Kraken2 database on the HPC system
            corn_db (str): Path to corn genome database for host removal
            host (str): HPC hostname
            username (str): HPC username
            partition (str): HPC partition/queue to use
            threads (int): Number of threads to request
            memory (str): Memory to request
            time (str): Time limit for the job
            no_download_db (bool): Skip downloading reference databases
            no_upload_data (bool): Skip uploading raw data files
            conda_env (str): Name of the conda environment to activate (if manually created)
        """
        self.raw_files = raw_files
        self.output_dir = output_dir
        self.kraken_db = kraken_db
        self.corn_db = corn_db
        self.host = host
        self.username = username
        self.identity_file = identity_file
        self.password_auth = password_auth
        self.partition = partition
        self.threads = threads
        self.memory = memory
        self.time = time
        self.no_download_db = no_download_db
        self.no_upload_data = no_upload_data
        self.conda_env = conda_env
        
        # Derived paths
        self.raw_data_dir = os.path.join(self.output_dir, "Raw_Data")
        self.preprocessed_data_dir = os.path.join(self.output_dir, "Preprocessed_Data")
        self.results_dir = os.path.join(self.output_dir, "Results")
        self.logs_dir = os.path.join(self.output_dir, "Logs")
        
        # Results subdirectories
        self.taxonomic_profiling_dir = os.path.join(self.results_dir, "Taxonomic_Profiling")
        self.kraken2_dna_dir = os.path.join(self.taxonomic_profiling_dir, "1_DNA_Kraken2")
        self.bracken_dna_dir = os.path.join(self.taxonomic_profiling_dir, "2_DNA_Bracken")
        self.bracken_to_krona_dir = os.path.join(self.taxonomic_profiling_dir, "3_DNA_Bracken_To_Krona_Python")
        self.alpha_beta_diversity_dir = os.path.join(self.taxonomic_profiling_dir, "4_DNA_Alpha_Beta_Diversity_Python")
        self.rel_abundance_matrix_dir = os.path.join(self.taxonomic_profiling_dir, "5_DNA_Relative_Abundance_Matrix_Python")
        
        # Logs subdirectories
        self.fastp_logs_dir = os.path.join(self.logs_dir, "Preprocessing", "Fastp")
        self.bowtie2_host_logs_dir = os.path.join(self.logs_dir, "Preprocessing", "Bowtie2_Host")
        self.kraken2_db_logs_dir = os.path.join(self.logs_dir, "Kraken2_DB")
        self.kraken2_dna_logs_dir = os.path.join(self.logs_dir, "Taxonomic_Profiling", "1_DNA_Kraken2")
        self.bracken_dna_logs_dir = os.path.join(self.logs_dir, "Taxonomic_Profiling", "2_DNA_Bracken")
        self.bracken_to_krona_logs_dir = os.path.join(self.logs_dir, "Taxonomic_Profiling", "3_DNA_Bracken_To_Krona_Python")
        self.alpha_beta_diversity_logs_dir = os.path.join(self.logs_dir, "Taxonomic_Profiling", "4_DNA_Alpha_Beta_Diversity_Python")
        self.rel_abundance_matrix_logs_dir = os.path.join(self.logs_dir, "Taxonomic_Profiling", "5_DNA_Relative_Abundance_Matrix_Python")
        
        # Parse samples and lanes from raw files
        self.samples, self.lanes = self._parse_samples_and_lanes()
        
        # Validate configuration
        self._validate()
    
    def _parse_samples_and_lanes(self):
        """
        Parse sample and lane information from raw file names.
        
        Returns:
            tuple: (samples, lanes)
        """
        samples = set()
        lanes = set()
        
        # Regular expression pattern for extracting sample and lane
        pattern = r'([^_/]+)_([^_/]+)_R[12]\.fastq\.gz$'
        
        for file_path in self.raw_files:
            file_name = os.path.basename(file_path)
            match = re.search(pattern, file_name)
            
            if match:
                sample, lane = match.groups()
                samples.add(sample)
                lanes.add(lane)
            else:
                logger.warning(f"Could not parse sample and lane from file: {file_name}")
        
        return sorted(list(samples)), sorted(list(lanes))
    
    def _validate(self):
        """Validate configuration."""
        # Check if raw files exist
        for file_path in self.raw_files:
            if not os.path.isfile(file_path):
                raise ValueError(f"Raw file does not exist: {file_path}")
        
        # Check if we have at least one sample
        if not self.samples:
            raise ValueError("No samples found in raw files")
        
        # Check if we have at least one lane
        if not self.lanes:
            raise ValueError("No lanes found in raw files")
        
        logger.info(f"Found {len(self.samples)} samples: {', '.join(self.samples)}")
        logger.info(f"Found {len(self.lanes)} lanes: {', '.join(self.lanes)}")
    
    def get_snakemake_config(self):
        """
        Get Snakemake configuration.
        
        Returns:
            dict: Snakemake configuration
        """
        return {
            "RAW_DATA_DIR": self.raw_data_dir,
            "PREPROCESSED_DATA_DIR": self.preprocessed_data_dir,
            "KRAKEN2_DB_DIR": self.kraken_db,
            "KRAKEN2_DNA_DIR": self.kraken2_dna_dir,
            "BRACKEN_DNA_DIR": self.bracken_dna_dir,
            "PYTHON_BRACKEN_TO_KRONA_DIR": self.bracken_to_krona_dir,
            "PYTHON_ALPHA_BETA_DIVERSITY_DIR": self.alpha_beta_diversity_dir,
            "PYTHON_RELATIVE_ABUNDANCE_MATRIX_DIR": self.rel_abundance_matrix_dir,
            "FASTP_LOGS_DIR": self.fastp_logs_dir,
            "BOWTIE2_HOST_LOGS_DIR": self.bowtie2_host_logs_dir,
            "KRAKEN2_DB_LOGS_DIR": self.kraken2_db_logs_dir,
            "KRAKEN2_DNA_LOGS_DIR": self.kraken2_dna_logs_dir,
            "BRACKEN_DNA_LOGS_DIR": self.bracken_dna_logs_dir,
            "PYTHON_BRACKEN_TO_KRONA_LOGS_DIR": self.bracken_to_krona_logs_dir,
            "PYTHON_ALPHA_BETA_DIVERSITY_LOGS_DIR": self.alpha_beta_diversity_logs_dir,
            "PYTHON_RELATIVE_ABUNDANCE_MATRIX_LOGS_DIR": self.rel_abundance_matrix_logs_dir,
            "SAMPLES": self.samples,
            "LANES": self.lanes,
            "CORN_DB": self.corn_db
        }
