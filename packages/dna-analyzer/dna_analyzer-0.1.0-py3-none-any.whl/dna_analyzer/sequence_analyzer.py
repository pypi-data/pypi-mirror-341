# dna_analyzer/sequence_analyzer.py
import numpy as np
from collections import Counter
from typing import Dict, List, Tuple

class SequenceAnalyzer:
    """Class for analyzing DNA sequences."""
    
    def __init__(self, sequence: str):
        """Initialize with a DNA sequence."""
        self.sequence = sequence.upper()
        self._validate_sequence()
    
    def _validate_sequence(self) -> None:
        """Validate that the sequence contains only valid nucleotides."""
        valid_nucleotides = set('ATCG')
        if not set(self.sequence).issubset(valid_nucleotides):
            raise ValueError("Sequence contains invalid nucleotides")
    
    def nucleotide_frequency(self) -> Dict[str, float]:
        """Calculate the frequency of each nucleotide in the sequence."""
        counts = Counter(self.sequence)
        total = len(self.sequence)
        return {base: count/total for base, count in counts.items()}
    
    def gc_content(self) -> float:
        """Calculate the GC content of the sequence."""
        gc_count = self.sequence.count('G') + self.sequence.count('C')
        return gc_count / len(self.sequence) if len(self.sequence) > 0 else 0
    
    def find_motif(self, motif: str) -> List[int]:
        """Find all occurrences of a motif in the sequence."""
        positions = []
        for i in range(len(self.sequence) - len(motif) + 1):
            if self.sequence[i:i+len(motif)] == motif:
                positions.append(i)
        return positions