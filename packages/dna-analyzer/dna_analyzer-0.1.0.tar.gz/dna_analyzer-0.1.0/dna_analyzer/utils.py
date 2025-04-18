# dna_analyzer/utils.py
def reverse_complement(sequence: str) -> str:
    """Generate the reverse complement of a DNA sequence."""
    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement_dict[base] for base in reversed(sequence.upper()))

def transcribe(sequence: str) -> str:
    """Transcribe DNA to RNA."""
    return sequence.upper().replace('T', 'U')

def translate(sequence: str) -> str:
    """
    Translate a DNA sequence to protein sequence.
    Assumes the sequence starts with a start codon.
    """
    genetic_code = {
        'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
        'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
        # ... (add complete genetic code)
    }
    
    protein = []
    for i in range(0, len(sequence)-2, 3):
        codon = sequence[i:i+3]
        if codon in genetic_code:
            protein.append(genetic_code[codon])
    
    return ''.join(protein)