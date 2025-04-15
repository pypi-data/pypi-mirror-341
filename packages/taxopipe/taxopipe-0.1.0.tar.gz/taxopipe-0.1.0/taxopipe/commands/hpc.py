#!/usr/bin/env python3
"""
HPC command module for TaxoPipe
"""
import os
import sys
import click
import logging
import tempfile
import shutil
from pathlib import Path
from taxopipe.utils.ssh import SSHClient
from taxopipe.utils.config import Config
from taxopipe.utils.workflow import SnakemakeWorkflow
from taxopipe.commands.hpc_impl import create_directories, upload_raw_files, setup_reference_databases

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.command(name="hpc")
@click.option('-r', '--raw-files', required=True, multiple=True, 
              help='Raw FASTQ files to process (use multiple -r flags for multiple files)')
@click.option('-o', '--output-dir', required=True, 
              help='Output directory on the HPC system')
@click.option('--kraken-db', required=True, 
              help='Path to Kraken2 database on the HPC system')
@click.option('--corn-db', required=True, 
              help='Path to corn genome database for host removal')
@click.option('--host', help='HPC hostname')
@click.option('--username', help='HPC username')
@click.option('--identity-file', help='Path to SSH identity file (private key)')
@click.option('--password-auth', is_flag=True, help='Use password authentication instead of key-based')
@click.option('--partition', default='normal', help='HPC partition/queue to use')
@click.option('--threads', default=16, help='Number of threads to request')
@click.option('--memory', default='200GB', help='Memory to request')
@click.option('--time', default='48:00:00', help='Time limit for the job')
@click.option('--no-download-db', is_flag=True, help='Skip downloading reference databases')
@click.option('--no-upload-data', is_flag=True, help='Skip uploading raw data files (use if files are already on HPC)')
@click.option('--dry-run', is_flag=True, help='Show what would be done without actually connecting to HPC')
def hpc_command(raw_files, output_dir, kraken_db, corn_db, host, username, 
                identity_file, password_auth, partition, threads, memory, time, no_download_db, no_upload_data, dry_run):
    """Run taxonomic profiling workflow on an HPC system.
    
    This command connects to an HPC system, uploads raw data files (if not already present),
    sets up the necessary environment, and submits a Snakemake workflow for taxonomic profiling.
    
    The workflow includes quality control, host removal, taxonomic classification, and abundance estimation.
    Results will be available in the specified output directory on the HPC system.
    
    Use the --no-upload-data flag if your raw data files are already on the HPC system to avoid re-uploading.
    Use the --no-download-db flag if reference databases are already set up on the HPC system.
    """
    try:
        # Initialize configuration
        config = Config(
            raw_files=raw_files,
            output_dir=output_dir,
            kraken_db=kraken_db,
            corn_db=corn_db,
            host=host,
            username=username,
            identity_file=identity_file,
            password_auth=password_auth,
            partition=partition,
            threads=threads,
            memory=memory,
            time=time,
            no_download_db=no_download_db,
            no_upload_data=no_upload_data
        )
        
        # If dry-run, just print what would be done
        if dry_run:
            logger.info("DRY RUN: Would connect to HPC system")
            logger.info(f"DRY RUN: Would use host: {config.host}")
            logger.info(f"DRY RUN: Would use username: {config.username}")
            if config.password_auth:
                logger.info(f"DRY RUN: Would use password authentication")
            elif config.identity_file:
                logger.info(f"DRY RUN: Would use identity file: {config.identity_file}")
            else:
                logger.info(f"DRY RUN: Would use default SSH keys")
            logger.info(f"DRY RUN: Would create directories on HPC")
            if not no_upload_data:
                logger.info(f"DRY RUN: Would upload {len(raw_files)} raw files to HPC")
            else:
                logger.info(f"DRY RUN: Would skip uploading raw files (--no-upload-data specified)")
            if not no_download_db:
                logger.info("DRY RUN: Would set up reference databases")
            logger.info("DRY RUN: Would configure and submit workflow")
            logger.info(f"DRY RUN: Output would be available at: {output_dir}")
            return
            
        # Connect to HPC
        logger.info(f"Connecting to HPC system: {config.host}")
        try:
            ssh = SSHClient(config.host, config.username, config.identity_file, config.password_auth)
        except Exception as e:
            logger.error(f"Failed to connect to HPC system: {str(e)}")
            logger.error("Please check your SSH configuration or use --dry-run to test without connecting.")
            sys.exit(1)
        
        # Create directories on HPC
        logger.info(f"Creating directories on HPC")
        create_directories(ssh, config)
        
        # Upload raw files if not skipped
        if not no_upload_data:
            logger.info(f"Uploading {len(raw_files)} raw files to HPC")
            upload_raw_files(ssh, config)
        else:
            logger.info("Skipping raw file upload (--no-upload-data specified)")
        
        # Download reference databases if needed
        if not no_download_db:
            logger.info("Setting up reference databases")
            setup_reference_databases(ssh, config)
        
        # Configure and submit workflow
        logger.info("Configuring and submitting workflow")
        workflow = SnakemakeWorkflow(ssh, config)
        job_id = workflow.submit()
        
        logger.info(f"Workflow submitted with job ID: {job_id}")
        logger.info(f"Output will be available at: {output_dir}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

def create_directories(ssh, config):
    """Create necessary directories on the HPC system."""
    # Implementation will be in a separate file
    pass

def upload_raw_files(ssh, config):
    """Upload raw FASTQ files to the HPC system."""
    # Implementation will be in a separate file
    pass

def setup_reference_databases(ssh, config):
    """Download and set up reference databases on the HPC system."""
    # Implementation will be in a separate file
    pass
