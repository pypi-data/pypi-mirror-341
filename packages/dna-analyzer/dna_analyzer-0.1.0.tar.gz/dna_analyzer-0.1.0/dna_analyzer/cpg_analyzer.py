# dna_analyzer/cpg_analyzer.py
from typing import List, Tuple
import numpy as np

class CpGAnalyzer:
    """Class for analyzing CpG islands in DNA sequences."""
    
    def __init__(self, sequence: str):
        """Initialize with a DNA sequence."""
        self.sequence = sequence.upper()
    
    def find_cpg_islands(self, 
                        min_length: int = 200,
                        min_gc_content: float = 0.5,
                        min_obs_exp_ratio: float = 0.6) -> List[Tuple[int, int]]:
        """
        Find CpG islands in the sequence based on criteria:
        - Minimum length
        - Minimum GC content
        - Minimum observed/expected CpG ratio
        
        Returns list of tuples with start and end positions of CpG islands.
        """
        islands = []
        for i in range(len(self.sequence) - min_length + 1):
            for j in range(i + min_length, len(self.sequence) + 1):
                region = self.sequence[i:j]
                if (self._calculate_gc_content(region) >= min_gc_content and
                    self._calculate_cpg_ratio(region) >= min_obs_exp_ratio):
                    islands.append((i, j))
        
        # Merge overlapping islands
        return self._merge_overlapping_regions(islands)
    
    def _calculate_gc_content(self, sequence: str) -> float:
        """Calculate GC content of a sequence."""
        gc_count = sequence.count('G') + sequence.count('C')
        return gc_count / len(sequence) if len(sequence) > 0 else 0
    
    def _calculate_cpg_ratio(self, sequence: str) -> float:
        """Calculate observed/expected CpG ratio."""
        # Count CpG dinucleotides
        cpg_count = sequence.count('CG')
        
        # Calculate expected CpG count
        c_freq = sequence.count('C') / len(sequence)
        g_freq = sequence.count('G') / len(sequence)
        expected_cpg = c_freq * g_freq * (len(sequence) - 1)
        
        return cpg_count / expected_cpg if expected_cpg > 0 else 0
    
    def _merge_overlapping_regions(self, regions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Merge overlapping regions into continuous regions."""
        if not regions:
            return []
            
        regions.sort(key=lambda x: x[0])
        merged = [regions[0]]
        
        for current in regions[1:]:
            previous = merged[-1]
            if current[0] <= previous[1]:
                merged[-1] = (previous[0], max(previous[1], current[1]))
            else:
                merged.append(current)
                
        return merged