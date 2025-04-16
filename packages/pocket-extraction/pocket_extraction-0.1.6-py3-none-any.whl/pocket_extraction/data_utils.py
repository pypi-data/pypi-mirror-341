import numpy as np
import os
import requests
import tempfile
from Bio import PDB
from Bio.PDB import Select
from Bio.PDB.Structure import Structure
from typing import Optional, List, Union, Set
from pathlib import Path
from .logger import logger

# Constants
RESIDUE_MAP = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
    "MSE": "M", "UNK": "X"
}

AA_RADII = {
    "A": 1.5, "C": 1.7, "D": 2.0, "E": 2.2, "F": 2.8, "G": 1.0,
    "H": 2.5, "I": 2.2, "K": 2.8, "L": 2.2, "M": 2.3, "N": 2.0,
    "P": 1.9, "Q": 2.2, "R": 3.0, "S": 1.6, "T": 1.9, "V": 2.0,
    "W": 2.8, "Y": 2.5
}

def fetch_pdb(pdb_id: str, output_dir: Optional[str] = None, ext: str = 'pdb', quiet: bool = False, retry: int = 3) -> str:
    """Fetch PDB file from RCSB database.
    
    Args:
        pdb_id: PDB ID to fetch.
        output_dir: Directory to save the file. Default is a temporary directory.
        ext: File extension (pdb or cif). Default is 'pdb'.
        quiet: Suppress output messages.
        retry: Number of retries on failure.
    Returns:
        Path to the downloaded file.
    """    
    if ext not in ('pdb', 'cif'):
        raise ValueError("Extension must be 'pdb' or 'cif'")
    
    url = f"https://files.rcsb.org/download/{pdb_id}.{ext}"
    if output_dir is None:
        output_dir = tempfile.gettempdir()
    
    output_path = os.path.join(output_dir, f"{pdb_id}.{ext}")
    
    for attempt in range(retry):
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            if not quiet:
                logger.info(f"Downloaded {url} to {output_path}")
            return output_path
        except requests.RequestException as e:
            if attempt < retry - 1:
                if not quiet:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            else:
                logger.error(f"Failed to download {url}: {e}")
                raise
    return output_path

def is_valid_pdb_id(pdb_id: str) -> bool:
    """Check if the given string is a valid PDB ID."""
    return len(pdb_id) == 4 and pdb_id.isalnum()

def get_remove_ligands() -> Set[str]:
    """Get set of ligand names to exclude from extraction."""
    exclusion_set = {
        "DMS", "ZN", "SO4", "GOL", "BTB", "EDO", "ACT", "PO4", 
        "NA", "CL", "CA", "MG", "K", "HOH", "WAT"
    }
    
    # Load additional exclusions from file if exists
    blocklist_path = Path(__file__).parent / "non-LOI-blocklist.tsv"
    if blocklist_path.exists():
        try:
            with blocklist_path.open() as f:
                exclusion_set.update(line.split("\t")[0].strip() for line in f)
        except Exception as e:
            logger.warning(f"Couldn't read blocklist: {str(e)}")
    
    return exclusion_set

def process_output_path(output_path: str, base_name: str, ext: Optional[str] = None, index: Optional[int] = None) -> str:
    """Process output path with proper extension handling.
    
    Args:
        output_path: User-specified output path (could be file or directory)
        base_name: Default base name if path is directory
        ext: User-specified extension override
        index: Counter for multi-file mode
    
    Returns:
        Full output path with proper extension
    """
    if os.path.isdir(output_path) or output_path.endswith(os.path.sep):
        # Handle directory path case
        output_dir = output_path
        filename = base_name
    else:
        output_dir, filename = os.path.split(output_path)
    
    # Split name and original extension
    name_part, orig_ext = os.path.splitext(filename)
    
    if index:
        name_part = f"{name_part}_{index}"
         
    orig_ext = orig_ext.lstrip('.').lower()  # Normalize extension
    
    # Determine final extension priority: user specified > filename extension > default pdb
    final_ext = (ext or orig_ext or 'pdb').lower()
    
    # Validate supported formats
    if final_ext not in ('pdb', 'cif'):
        raise ValueError(f"Unsupported output format: {final_ext}. Use 'pdb' or 'cif'.")
    
    # Construct final filename
    final_name = f"{name_part}.{final_ext}"
    
    # Create directory if needed
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    return os.path.join(output_dir, final_name)

def load_structure(pdb_file: str, quiet: bool = False) -> Structure:
    """Load structure from file with format autodetection."""
    if not os.path.isfile(pdb_file):
        if is_valid_pdb_id(pdb_file):
            pdb_file = fetch_pdb(pdb_file, quiet=quiet)
        else:
            raise ValueError(f"Invalid PDB ID or file: {pdb_file}")
        
    path = Path(pdb_file)
    suffix = path.suffix.lower()
    
    try:
        if suffix == ".pdb":
            return PDB.PDBParser(QUIET=quiet).get_structure("structure", str(path))
        elif suffix in (".cif", ".mmcif"):
            return PDB.MMCIFParser(QUIET=quiet).get_structure("structure", str(path))
        raise ValueError(f"Unsupported format: {suffix}")
    except Exception as e:
        logger.error(f"Failed to parse {path}: {str(e)}")
        raise

def save_structure(
    filename: Union[str, Path],
    structure: Structure,
    select: Select = Select(),
    quiet: bool = False
) -> None:
    """Save structure to file with comprehensive error handling."""
    path = Path(filename).resolve()
    suffix = path.suffix.lower()
    
    if suffix not in (".pdb", ".cif"):
        raise ValueError(f"Unsupported format '{suffix}'. Use .pdb or .cif")
    
    try:
        io = PDB.MMCIFIO() if suffix == ".cif" else PDB.PDBIO()
        io.set_structure(structure)
        
        path.parent.mkdir(parents=True, exist_ok=True)
        io.save(str(path), select=select)
        
        if not quiet:
            logger.info(f"Saved structure to {path}")
            
    except Exception as e:
        if path.exists():
            try:
                path.unlink()
                logger.warning(f"Removed corrupted output: {path}")
            except Exception as cleanup_err:
                logger.error(f"Cleanup failed: {cleanup_err}")
        
        logger.exception("Save operation failed")
        raise
    