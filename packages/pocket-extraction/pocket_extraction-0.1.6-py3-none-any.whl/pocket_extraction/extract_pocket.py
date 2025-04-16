import numpy as np
from typing import Optional
from pathlib import Path
from Bio import PDB
from .data_utils import load_structure, save_structure, process_output_path
from .selection import PocketSelect
from .logger import logger, setup_logger
from .arguments import get_pocket_parser

def get_ligand_coords(ligand_file: str, quiet: bool = False) -> np.ndarray:
    """Extract coordinates from ligand structure file."""
    path = Path(ligand_file)
    suffix = path.suffix.lower()
    
    try:
        if suffix == ".pdb":
            struct = PDB.PDBParser(QUIET=quiet).get_structure("ligand", str(path))
        elif suffix in (".cif", ".mmcif"):
            struct = PDB.MMCIFParser(QUIET=quiet).get_structure("ligand", str(path))
        else:
            raise ValueError(f"Unsupported ligand format: {suffix}")
            
        return np.array([atom.coord for atom in struct.get_atoms()])
    except Exception as e:
        logger.error(f"Failed to process {path}: {str(e)}")
        raise

def extract_pocket(
    pdb_file: str,
    output_path: str,
    ligand_coords: Optional[np.ndarray] = None,
    ligand_center: Optional[np.ndarray] = None,
    radius: float = 10.0,
    ext: Optional[str] = None,
    quiet: bool = False
) -> str:
    """Extract pocket around specified ligand coordinates."""
    if radius <= 0:
        raise ValueError("Radius must be positive")
    
    output_path = process_output_path(output_path, "pocket", ext)
    
    try:
        structure = load_structure(pdb_file, quiet)
        selector = PocketSelect(
            radius=radius,
            ligand_coords=ligand_coords,
            ligand_center=ligand_center,
            quiet=quiet
        )
        
        save_structure(output_path, structure, selector, quiet)
        return output_path
    except Exception as e:
        logger.exception(f"Pocket extraction failed for {pdb_file}: {(e)}")
        raise

def main():
    parser = get_pocket_parser()
    
    args = parser.parse_args()
    
    try:
        # Configure logging
        setup_logger(
            quiet=args.quiet,
            debug=args.debug,
            logfile=args.logfile
        )
        
        # Process ligand coordinates
        ligand_coords = None
        if args.ligand_file:
            ligand_coords = get_ligand_coords(args.ligand_file, args.quiet)
        
        # Perform extraction
        output = extract_pocket(
            pdb_file=args.pdb_file,
            output_path=args.output,
            ligand_coords=ligand_coords,
            ligand_center=args.ligand_center,
            radius=args.radius,
            ext=args.ext,
            quiet=args.quiet
        )
        
        if not args.quiet:
            logger.info(f"Pocket saved to: {output}")
            
    except Exception as e:
        logger.exception("Fatal error")
        exit(1)

if __name__ == "__main__":
    main()
    