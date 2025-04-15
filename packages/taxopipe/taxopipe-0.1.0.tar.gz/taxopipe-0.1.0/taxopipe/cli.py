#!/usr/bin/env python3
"""
TaxoPipe: A package for running taxonomic profiling workflows on HPC systems
"""
import os
import sys
import click
from taxopipe.commands.hpc import hpc_command
from taxopipe.commands.status import status_command
from taxopipe.commands.download import download_command
from taxopipe.commands.get_abundance_fixed import get_abundance_command
from taxopipe.commands.download_abundance import download_abundance_command


@click.group()
def main():
    """TaxoPipe: Run taxonomic profiling workflows on HPC systems."""
    pass


# Add commands
main.add_command(hpc_command)
main.add_command(status_command)
main.add_command(download_command)
main.add_command(get_abundance_command)
main.add_command(download_abundance_command)


if __name__ == "__main__":
    main()
