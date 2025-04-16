"""
Module for handling MSA files and mapping original residue numbers.
"""

from Bio import AlignIO

def build_residue_maps(alignment):
    """
    For each sequence, build a list mapping each aligned column to 
    the original residue number. Non-gap characters increment the residue number.
    Gaps receive None.
    """
    residue_maps = []
    for record in alignment:
        current_residue = 0
        col_map = []
        for char in record.seq:
            if char != '-':
                current_residue += 1
                col_map.append(current_residue)
            else:
                col_map.append(None)
        residue_maps.append({'header': record.id, 'map': col_map})
    return residue_maps

def build_msa_columns(alignment):
    """
    Builds a list where each element represents a column of the MSA.
    Each column is a list of dictionaries containing:
      - 'header': the sequence ID
      - 'residue': the aligned residue or gap
      - 'residue_id': the actual residue number (None if gap)
    """
    residue_maps = build_residue_maps(alignment)
    num_columns = alignment.get_alignment_length()
    columns = []
    for col in range(num_columns):
        col_data = []
        for i, record in enumerate(alignment):
            col_data.append({
                'header': record.id,
                'residue': record.seq[col],
                'residue_id': residue_maps[i]['map'][col]
            })
        columns.append(col_data)
    return columns

# Optional simple test when running the module as a script.
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python msa.py <alignment_file.fasta>")
        sys.exit(1)
    alignment_file = sys.argv[1]
    alignment = AlignIO.read(alignment_file, "fasta")
    msa_columns = build_msa_columns(alignment)
    
    # Print first 5 columns for demonstration.
    for i, col in enumerate(msa_columns[:5]):
        print(f"Column {i + 1}:")
        for entry in col:
            print(entry)
        print("-" * 40)

