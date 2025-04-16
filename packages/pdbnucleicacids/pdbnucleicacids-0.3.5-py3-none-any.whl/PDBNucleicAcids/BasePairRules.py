"""Classes with rules for proper base pairing."""

import warnings

# from Bio.PDB.vectors import calc_dihedral
# from Bio.PDB.Polypeptide import is_nucleic
from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom

# absolute imports
from PDBNucleicAcids.Geometry import angle_between_planes, plane_separation


class BasePairRules:
    """
    Base class for base-pairing rules.

    It contains only methods in common to most pairing rules, but doesn't
    contain any parameter.

    """

    def __init__(self):
        self.accepted_nucleotides = []

    def atoms_from_base_ring(self, base: Residue) -> tuple[Atom] | None:
        """Get atoms from the ring of a base."""
        return None

    def atom_from_central_hbond(self, base) -> Atom | None:
        """Get central H-bond atom of a base."""
        atoms = self.atoms_from_base_ring(base)
        if atoms:
            return atoms[0]
        else:
            return None

    def distance(self, base1, base2) -> float | None:
        """Compute distance between central H-bond atoms of two bases."""
        atom1 = self.atom_from_central_hbond(base1)
        atom2 = self.atom_from_central_hbond(base2)
        if atom1 is not None and atom2 is not None:
            return atom1 - atom2
        else:
            return None

    def angle_between_bases(
        self, base1: Residue, base2: Residue
    ) -> float | None:
        """Compute angle between between planes of two bases."""
        atom_list1 = self.atoms_from_base_ring(base1)
        atom_list2 = self.atoms_from_base_ring(base2)
        if atom_list1 is None or atom_list2 is None:
            return None
        plane1 = [atom.coord for atom in atom_list1]
        plane2 = [atom.coord for atom in atom_list2]
        return angle_between_planes(plane1, plane2)

    def stagger(self, base1: Residue, base2: Residue) -> float | None:
        """Compute vertical stagger between between planes of two bases."""
        atom_list1 = self.atoms_from_base_ring(base1)
        atom_list2 = self.atoms_from_base_ring(base2)
        if atom_list1 is None or atom_list2 is None:
            return None
        plane1 = [atom.coord for atom in atom_list1]
        plane2 = [atom.coord for atom in atom_list2]
        return plane_separation(plane1, plane2)

    # def dihedrals(self, base1, base2) -> float:
    #     atom1, atom2, atom3 = self.atoms_from_base_ring(base1)
    #     atom4, atom5, atom6 = self.atoms_from_base_ring(base2)

    #     v1, v2, v3, v4, v5, v6 = (
    #         atom1.get_vector(),
    #         atom2.get_vector(),
    #         atom3.get_vector(),
    #         atom4.get_vector(),
    #         atom5.get_vector(),
    #         atom6.get_vector(),
    #     )
    #     dihedral1 = calc_dihedral(v1, v2, v3, v4)
    #     dihedral2 = calc_dihedral(v1, v5, v6, v4)

    #     return (dihedral1, dihedral2)

    # methods to check validity

    def is_different_residue(self, base1: Residue, base2: Residue) -> bool:
        """Check if two bases are distinct bases."""
        return base1 != base2

    def is_complementary(self, base1: Residue, base2: Residue) -> bool:
        """Check if two bases are complementary."""
        pair: tuple[str] = (base1.get_resname(), base2.get_resname())
        return pair in self.complementary_pairs

    def is_from_different_chain(self, base1: Residue, base2: Residue) -> bool:
        """Check if two bases are from distinct chains."""
        return base1.parent != base2.parent

    def is_valid_distance(self, base1: Residue, base2: Residue) -> bool:
        """Check validity of distance between central two bases."""
        dist = self.distance(base1, base2)
        if dist is not None:
            return dist <= self.max_distance
        else:
            return False

    def is_valid_angle(self, base1: Residue, base2: Residue) -> bool:
        """Check validity of angle between between planes of the bases."""
        angle = self.angle_between_bases(base1, base2)
        if angle is not None:
            return angle <= self.max_angle or angle >= 180 - self.max_angle
        else:
            False

    def is_valid_stagger(self, base1: Residue, base2: Residue) -> bool:
        """Check validity of stagger between between planes of the bases."""
        stagger = self.stagger(base1, base2)
        if stagger is not None:
            return stagger <= self.max_stagger
        else:
            False

    def is_candidate(self, base1: Residue, base2: Residue) -> bool:
        """
        Check if (base1, base2) is a likely base pair.

        Use all the constraint methods to infer if base2 is likely to be
        paired with base1.
        """
        # if not is_nucleic(base1, standard=False):
        #     return False
        # elif not is_nucleic(base2, standard=False):
        #     return False
        # elif not is_nucleic(base1, standard=True):
        #     return False
        # elif not is_nucleic(base2, standard=True):
        #     return False
        if base1.get_resname() not in self.accepted_nucleotides:
            # TODO add warning
            # TODO explore the is_nucleic(non_standard)
            # and maybe check if it needs updating
            return False
        elif base1.get_resname() not in self.accepted_nucleotides:
            return False
        elif not self.is_different_residue(base1, base2):
            return False
        elif not self.is_complementary(base1, base2):
            return False
        # TODO are not connected instead of different chains
        # elif not self.is_from_different_chain(base1, base2):
        #     return False
        elif not self.is_valid_distance(base1, base2):
            return False
        elif not self.is_valid_angle(base1, base2):
            return False
        elif not self.is_valid_stagger(base1, base2):
            return False
        else:
            return True


class WatsonCrickBasePairRules(BasePairRules):
    """
    Rules for Watson-Crick base pairs for both RNA and DNA.

    Parameters
    ----------
    max_distance : float | int, optional
        Maximum distance between nucleotide bases, in Armstrong.
        The default is 3.5.
    max_angle : float | int, optional
        Maximum angle between the planes of the bases, in degrees.
        The default is 65.
    max_stagger : float | int, optional
        Maximum vertical distance between the planes of the bases, in degrees.
        The default is 2.5.

    """

    def __init__(
        self,
        max_distance: float | int = 4,
        max_angle: float | int = 65,
        max_stagger: float | int = 2.5,
        # dihedral_range: tuple[int, float] = (90, 150),
    ):
        super().__init__()

        # parameters taken from
        # http://forum.x3dna.org/faqs/
        # how-to-fix-missing-(superfluous)-base-pairs-identified-by-find_pair/
        self.max_distance = max_distance
        self.max_angle = max_angle
        self.max_stagger = max_stagger
        # self.dihedral_angle_range = dihedral_range

        self.complementary_pairs: list[tuple[str]] = [
            ("DA", "DT"),
            ("DT", "DA"),
            ("DG", "DC"),
            ("DC", "DG"),
            ("A", "T"),
            ("T", "A"),
            ("G", "C"),
            ("C", "G"),
            ("DA", "T"),
            ("T", "DA"),
            ("DG", "C"),
            ("C", "DG"),
            ("A", "DT"),
            ("DT", "A"),
            ("G", "DC"),
            ("DC", "G"),
        ]
        self.purines: list[str] = ["DA", "DG", "A", "G"]
        self.pyrimidines: list[str] = ["DT", "DC", "T", "C"]
        self.accepted_nucleotides: list[str] = self.purines + self.pyrimidines

    def atoms_from_base_ring(self, base: Residue) -> tuple[Atom] | None:
        """Get atoms from the ring of a base."""
        if base.get_resname() in self.purines:
            if base.has_id("N1") and base.has_id("C2") and base.has_id("C6"):
                atoms: tuple[Atom] = (base["N1"], base["C2"], base["C6"])
            else:
                # nucleotide is without base atoms
                # it only has the backbone (sugar phosphate) or part of it
                atoms = None
        elif base.get_resname() in self.pyrimidines:
            if base.has_id("N3") and base.has_id("C2") and base.has_id("C4"):
                atoms: tuple[Atom] = (base["N3"], base["C2"], base["C4"])
            else:
                # nucleotide is without base atoms
                # it only has the backbone (sugar phosphate) or part of it
                atoms = None
        else:  # Hetero-residue?
            warnings.warn(
                f"{base.full_id} is not recognized as purine nor pyrimidine."
            )
            atoms = None
        return atoms


class dsDNAWatsonCrickBasePairRules(WatsonCrickBasePairRules):
    """
    Rules for Watson-Crick base pairs in double-strand DNA.

    Parameters
    ----------
    max_distance : float | int, optional
        Maximum distance between nucleotide bases, in Armstrong.
        The default is 4.
    max_angle : float | int, optional
        Maximum angle between the planes of the bases, in degrees.
        The default is 65.
    max_stagger : float | int, optional
        Maximum vertical distance between the planes of the bases, in degrees.
        The default is 2.5.

    """

    def __init__(
        self,
        max_distance: float | int = 4,
        max_angle: float | int = 65,
        max_stagger: float | int = 2.5,
    ):
        super().__init__(max_distance, max_angle, max_stagger)

        self.complementary_pairs: list[tuple[str]] = [
            ("DA", "DT"),
            ("DT", "DA"),
            ("DG", "DC"),
            ("DC", "DG"),
        ]

        self.purines: list[str] = ["DA", "DG"]
        self.pyrimidines: list[str] = ["DT", "DC"]
        self.accepted_nucleotides: list[str] = self.purines + self.pyrimidines
