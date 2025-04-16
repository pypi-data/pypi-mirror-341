"""Nucleic Acids related classes and functions."""

import warnings

import pandas as pd
from Bio.Data.PDBData import nucleic_letters_3to1_extended
from Bio.Seq import Seq
from Bio.PDB.Polypeptide import is_nucleic
from Bio.PDB.PDBExceptions import PDBException
from Bio.PDB.NeighborSearch import NeighborSearch

from Bio.PDB.Structure import Structure
from Bio.PDB.Model import Model
from Bio.PDB.Chain import Chain
from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom

# absolute imports
from PDBNucleicAcids.BasePairRules import BasePairRules
from PDBNucleicAcids.BasePairRules import WatsonCrickBasePairRules


def search_paired_base(
    residue: Residue,
    pairing_rules: BasePairRules = WatsonCrickBasePairRules(),
    nucleic_chain_ids: list[str] | None = None,
    nucleic_atoms: list[Atom] | None = None,
) -> Residue | None:
    """
    Search in the vicinity of a given base for its paired base.

    Parameters
    ----------
    residue : Bio.PDB.Residue.Residue
        A Biopython nucleic acid residue (nucleotide) taken from a Biopython
        structure.
    pairing_rules : optional
        Class instance with rules for proper pairing.
        `PDBNucleicAcids.BasePairsRules.WatsonCrickBasePairRules`
        is the default.
    nucleic_chain_ids : list[str], optional
        List of ids for nucleic acid chains. If None they will be
        inferred using `NABuilder` class. Default is None.
    nucleic_atoms : list[Atom], optional
        List of atoms from the nucleic acid chains. If None they will be
        inferred using `nucleic_chain_ids` parameter. Default is None.

    Returns
    -------
    Bio.PDB.Residue.Residue | None
        Nucleotide that binds to the input nucleotide residue.
        None in the case there is no nucleotide paired to the input nucleotide.

    """
    # from residue get to the structure
    structure: Structure = residue.parent.parent.parent

    # in case no nucleic atoms and no nucleic chain ids were given
    # get nucleic chains using get_polymer_dataframe
    if not nucleic_atoms and not nucleic_chain_ids:
        builder = NABuilder()
        nucleic_acids = builder.build_nucleic_acids(
            structure, standard_nucleotides=False
        )
        nucleic_atoms = []
        for na in nucleic_acids:
            nucleic_atoms += na.get_atoms()

    # in case no nucleic atoms were given but
    # nucleic chain ids were given or got from get_polymer_dataframe
    # list of all nucleic atoms, compute only once
    if not nucleic_atoms and nucleic_chain_ids:
        nucleic_atoms: list[Atom] = [
            atom
            for atom in structure.get_atoms()
            if atom.parent.parent.id in nucleic_chain_ids
            and atom.parent != residue  # not from the same residue
        ]

    # if there are no nucleic atoms except from the one input residue
    # then NeighborSearch will return an error
    if len(nucleic_atoms) == 0 or nucleic_atoms is None:
        return None

    # initialize NeighborSearch class
    ns = NeighborSearch(nucleic_atoms)

    central_atom: Atom = pairing_rules.atom_from_central_hbond(residue)
    # if the input residue is not a DNA base then the central atom
    # will be None
    if central_atom is None:
        return None

    # search around the central atom of the residue
    # TODO radius as parameter
    atom_neighborhood = ns.search(center=central_atom.coord, radius=4.0)

    residue_neighborhood: list[Residue] = list(
        {atom.parent for atom in atom_neighborhood}
    )

    candidate_residues: list[Residue] = []

    for residue_neighbour in residue_neighborhood:
        if pairing_rules.is_candidate(base1=residue, base2=residue_neighbour):
            dist = pairing_rules.distance(
                base1=residue, base2=residue_neighbour
            )
            candidate_residues.append((residue_neighbour, dist))

    if len(candidate_residues) > 1:
        # If there is more than one paired residue
        # TODO maybe add a scoring function instead of simple distance
        # TODO add a warning if there is more than one candidate
        # or maybe more than one candidate with similar dist or score
        min_tuple: tuple = min(candidate_residues, key=lambda x: x[1])
        return min_tuple[0]
    elif candidate_residues:
        # only one paired nucleotide found
        return candidate_residues[0][0]
    else:
        # no paired nucleotides found
        return None


class NucleicAcid(list):
    """A nucleic acid is simply a list of nucleic L{Residue} objects."""

    def get_seq(self) -> Seq:
        """
        Return the nucleotide sequence as a Seq object.

        Returns
        -------
        Bio.Seq.Seq
            Sequence of nucleotides in a continous strand.

        """
        resname_list = [res.get_resname() for res in self]

        # add padding since nucleic_letters_3to1_extended requires three char
        # i.e. from "DT" to "DT "
        resname_list = [resname.ljust(3, " ") for resname in resname_list]

        seq = "".join(
            nucleic_letters_3to1_extended.get(resname, "X")
            for resname in resname_list
        )

        return Seq(seq)

    def get_atoms(self) -> list[Atom]:
        """Return atoms in the nucleic acid."""
        atom_list = []
        for res in self:
            atom_list += res.get_atoms()
        return atom_list

    def get_chain_id(self) -> str:
        """Return chain id of the nucleic acid."""
        return self[0].parent.id

    def get_na_type(self) -> str:
        """Return type of nucleic acid: DNA or RNA."""
        dna_counter = 0
        rna_counter = 0
        other_counter = 0
        other_list = []

        for res in self:
            if (
                is_nucleic(res, standard=False)
                and "O3'" in res
                and "O2'" not in res  # deoxy-ribose
            ):
                dna_counter += 1
            elif (
                is_nucleic(res, standard=False)
                and "O3'" in res
                and "O2'" in res
            ):
                rna_counter += 1
            else:
                other_counter += 1
                other_list.append(res.get_resname())

        if dna_counter == len(self):
            return "DNA"
        elif rna_counter == len(self):
            return "RNA"
        elif dna_counter + rna_counter == len(self):
            return "DNA-RNA hybrid"
        else:
            warnings.warn(f"Found these unknown residues: {other_list}")
            return "Unknown"

    def __repr__(self) -> str:
        """Return string representation of the nucleic acid."""
        start = self[0].get_id()[1]
        end = self[-1].get_id()[1]
        return f"<NucleicAcid chain='{self.get_chain_id()}' \
type='{self.get_na_type()}' start={start} end={end}>"


class _NABuilder:
    """Base class to extract nucleic acids.

    It checks if two consecutive residues in a chain are connected.
    The connectivity test is implemented by a subclass.

    This assumes you want both standard and non-standard nucleotides.
    """

    def __init__(self, radius: float | int) -> None:
        """
        Initialize the base class.

        Parameters
        ----------
        radius : float | int
            Maximum allowed distance between P atom and O3' atom.

        """
        self.radius = radius

    def _accept(self, residue: Residue, standard_nucleotides: bool) -> bool:
        """Check if the residue is a nucleotide (PRIVATE)."""
        if is_nucleic(residue, standard=standard_nucleotides):
            return True
        elif not standard_nucleotides and "O3'" in residue.child_dict:
            # It has an alpha carbon...
            # We probably need to update the hard coded list of
            # non-standard residues, see function is_aa for details.
            warnings.warn(
                f"Assuming residue {residue.resname} is an unknown modified \
nucleotide."
            )
            return True
        else:
            # not a standard nucleotide so skip
            return False

    def build_nucleic_acids(
        self,
        entity: Structure | Model | Chain,
        standard_nucleotides: bool = False,
    ) -> list[NucleicAcid]:
        """
        Build and return a list of NucleicAcid objects.

        Parameters
        ----------
        entity : L{Structure}, L{Model} or L{Chain}
            Double-stranded nucleic acids are searched for in this object.
        standard_nucleotides : bool, optional
            Looking for standard nucleotides. The default is True.

        Raises
        ------
        PDBException
            In case input entity is not a L{Structure}, L{Model} or L{Chain}.

        Returns
        -------
        na_list : list[NucleicAcid]
            List if all NucleicAcid found in the input entity.

        """
        level = entity.get_level()
        # Decide which entity we are dealing with
        if level == "S":
            model = entity[0]
            chain_list = model.get_list()
        elif level == "M":
            chain_list = entity.get_list()
        elif level == "C":
            chain_list = [entity]
        else:
            raise PDBException("Entity should be Structure, Model or Chain.")

        # initialize list of nucleic acids (polymers)
        na_list = []
        for chain in chain_list:
            # list of residues filtered by accepted nucleotides
            res_list = [
                res
                for res in chain
                if self._accept(res, standard_nucleotides=standard_nucleotides)
            ]

            na = None
            for prev_res in res_list:
                # look for a 5' end of the nucleic acid
                if not any(
                    [self._is_connected(res, prev_res) for res in res_list]
                ):
                    # residue is 5' end because it has no residue connected to
                    # its 5' oxygen

                    # we build the nucleic acid in 5'->3' direction
                    # initialize nucleic acid class with already the 5' end
                    na = NucleicAcid()
                    na.append(prev_res)
                    na_list.append(na)

                    # loop over all residues
                    i = 0
                    while i < len(res_list):
                        next_res = res_list[i]
                        i += 1

                        # check if previous and next residues are connected
                        if self._is_connected(prev_res, next_res):
                            na.append(next_res)

                            # update previous residue
                            prev_res = next_res

                            # restarts the while loop
                            i = 0
                    # while loop ends only when no connected next nucleotide
                    # is found
                    # it goes back to the for loop
                    # which looks for another 5' end

        return na_list


class NABuilder(_NABuilder):
    """Use P--O3' distance to find connected nucletides."""

    def __init__(self, radius: float | int = 1.9) -> None:
        """
        Initialize the class.

        Parameters
        ----------
        radius : float | int
            Maximum allowed distance between P atom and O3' atom.

        """
        _NABuilder.__init__(self, radius)

    def _is_connected(self, prev_res: Residue, next_res: Residue) -> bool:
        if not prev_res.has_id("O3'"):
            return False
        if not next_res.has_id("P"):
            return False

        o = prev_res["O3'"]
        p = next_res["P"]

        # get all disordered atom positions
        if o.is_disordered():
            o_list = o.disordered_get_list()
        else:
            o_list = [o]
        if p.is_disordered():
            p_list = p.disordered_get_list()
        else:
            p_list = [p]

        # Test all disordered atom positions if any
        # if not then just test the atom pair
        for pp in p_list:
            for oo in o_list:
                # To form a peptide bond, N and C must be
                # within radius and have the same altloc
                # identifier or one altloc blank
                p_altloc = pp.get_altloc()
                o_altloc = oo.get_altloc()
                if (
                    p_altloc == o_altloc or p_altloc == " " or o_altloc == " "
                ) and self._test_dist(pp, oo):
                    # Select the disordered atoms that
                    # are indeed bonded
                    if o.is_disordered():
                        o.disordered_select(o_altloc)
                    if p.is_disordered():
                        p.disordered_select(p_altloc)
                    return True
        return False

    def _test_dist(self, o: Atom, p: Atom) -> bool:
        """Return True if distance between atoms<radius (PRIVATE)."""
        if (o - p) < self.radius:
            return True
        else:
            return False


class BasePair:
    """Pair of nucleotides."""

    def __init__(
        self, i_res: Residue, j_res: Residue, pairing_rules: BasePairRules
    ) -> None:
        self.i_res = i_res
        self.j_res = j_res
        self.pairing_rules = pairing_rules

    def get_i_res(self) -> Residue:
        """Return i-th nucleotide."""
        return self.i_res

    def get_j_res(self) -> Residue:
        """Return j-th nucleotide."""
        return self.j_res

    def get_atoms(self) -> list[Atom]:
        """Return atoms in the nucleic acid."""
        atom_list = []
        atom_list += self.i_res.get_atoms()
        atom_list += self.j_res.get_atoms()
        return atom_list

    def check_validity(
        self, pairing_rules: None | BasePairRules = None
    ) -> bool:
        """Check for validity for base pair, using input rules."""
        if pairing_rules is None:
            pairing_rules = self.pairing_rules
        return pairing_rules.is_candidate(self.i_res, self.j_res)

    # TODO get other information: shear, stretch, buckle, propeller, opening
    def get_stagger(self, pairing_rules: None | BasePairRules = None) -> float:
        """Return stagger value from base pair."""
        if pairing_rules is None:
            pairing_rules = self.pairing_rules
        return pairing_rules.stagger(self.i_res, self.j_res)

    def __repr__(self) -> str:
        """Return string representation of base pair."""
        i_resname = self.i_res.get_resname()
        j_resname = self.j_res.get_resname()
        return f"<BasePair i_res={i_resname} j_res={j_resname}>"


class DoubleStrandNucleicAcid(list):
    """List of BasePairs."""

    def get_atoms(self) -> list[Atom]:
        """Return atoms in the double stranded nucleic acid."""
        atom_list = []
        for bp in self:
            atom_list += bp.get_atoms()
        return atom_list

    def get_i_strand(self) -> NucleicAcid:
        """Get i-th strand as NucleicAcid object."""
        na = NucleicAcid()
        for bp in self:
            na.append(bp.i_res)
        return na

    def get_j_strand(self) -> NucleicAcid:
        """Get j-th strand as NucleicAcid objects."""
        na = NucleicAcid()
        for bp in self:
            na.append(bp.j_res)
        return na

    def get_na_complex_type(self) -> str:
        """
        Return nucleic acid complex type.

        i.e. dsDNA, DNA:RNA, etc
        """
        i_type = self.get_i_strand().get_na_type()
        j_type = self.get_j_strand().get_na_type()

        if i_type == "DNA" and j_type == "DNA":
            return "dsDNA"
        elif i_type == "RNA" and j_type == "RNA":
            return "dsRNA"
        else:
            return f"{i_type}:{j_type}"

    # TODO get other information: shear, stretch, buckle, propeller, opening
    def get_stagger_values(self) -> list[float]:
        """Get stagger value for every base pair."""
        return [bp.get_stagger() for bp in self]

    def as_dataframe(self) -> pd.DataFrame:
        """
        Return dataframe with base pairs data.

        Returns
        -------
        pandas.DataFrame
            Dataframe with base pairs data in the structure.

        """
        pass
        data = []
        for bp in self:
            i_res = bp.i_res
            j_res = bp.j_res

            # info from base pair
            row: tuple[str, int] = (
                i_res.parent.id,
                i_res.id[1],
                i_res.resname,
                j_res.resname,
                j_res.id[1],
                j_res.parent.id,
            )
            data.append(row)

        # cast into dataframe
        df = pd.DataFrame(
            data,
            columns=[
                "i_chain_id",
                "i_residue_index",
                "i_residue_name",
                "j_residue_name",
                "j_residue_index",
                "j_chain_id",
            ],
        )
        return df

    def __repr__(self) -> str:
        """Return string representation of the double-stranded nucleic acid."""
        i_strand_id = self.get_i_strand().get_chain_id()
        j_strand_id = self.get_j_strand().get_chain_id()

        return f"<DoubleStrandNucleicAcid \
type='{self.get_na_complex_type()}' \
strand ids='{i_strand_id}:{j_strand_id}' \
length={len(self)}>"


class DSNABuilder:
    """Base class to extract double-stranded nucleic acids.

    This assumes you want both standard and non-standard amino acids.
    """

    def __init__(self, radius: float | int = 1.9) -> None:
        """
        Initialize the class.

        Parameters
        ----------
        radius : float | int
            Maximum allowed distance between P atom and O3' atom.

        """
        self.radius = radius

    def build_double_strands(
        self,
        entity: Structure | Model | Chain,
        pairing_rules: BasePairRules = WatsonCrickBasePairRules(),
    ) -> list[DoubleStrandNucleicAcid]:
        """
        Build and return a list of DoubleStrandNucleicAcid objects.

        Parameters
        ----------
        entity : L{Structure}, L{Model} or L{Chain}
            Double-stranded nucleic acids are searched for in this object.
        pairing_rules : optional
            Class instance with rules for proper pairing.
            `PDBNucleicAcids.BasePairsRules.WatsonCrickBasePairRules`
            is the default.

        Returns
        -------
        all_dsna_list : list[DoubleStrandNucleicAcid]
            list if all DoubleStrandNucleicAcid found in the input entity.

        """
        # build nucleic acids
        builder = NABuilder()
        na_list = builder.build_nucleic_acids(
            entity, standard_nucleotides=False
        )

        already_paired = []
        all_dsna_list = []

        for na1 in na_list:
            for na2 in na_list:
                dsna_list, already_paired = self._get_dsnas_from_nas(
                    na1, na2, pairing_rules, already_paired
                )

                all_dsna_list += dsna_list

        return all_dsna_list

    def _get_dsnas_from_nas(
        self,
        na1: NucleicAcid,
        na2: NucleicAcid,
        pairing_rules: BasePairRules,
        already_paired: list[Residue],
    ) -> list[DoubleStrandNucleicAcid]:
        """
        Get DoubleStrandNucleicAcid's from NucleicAcid's.

        Return list of double-stranded nucleic acids but also list of paired
        residues.
        """
        nucleic_chain_ids = [na1.get_chain_id(), na2.get_chain_id()]

        # from 2 nucleic acids
        # 1-or-many segments of paired nucleic acids
        dsna_list = []

        dsna = DoubleStrandNucleicAcid()
        for res1 in na1:
            res2 = search_paired_base(
                res1,
                nucleic_chain_ids=nucleic_chain_ids,
                pairing_rules=pairing_rules,
            )

            # This new algorithm to build DSNA addresses structures like 1AWC
            # with many interruptions
            # and nicked DNA like 1CW0 too probably

            # discontinuity by unpaired or already paired bases
            if (
                res2 is None
                or res1 in already_paired  # is already paired
                or res2 in already_paired  # is already paired
                or res2 not in na2  # not in the target nucleic acid
                or NABuilder()._is_connected(res1, res2)  # not connected
                or NABuilder()._is_connected(res2, res1)  # not connected
            ):
                if len(dsna) > 0:
                    # start of discontinuity, save DSNA and start a new one
                    dsna_list.append(dsna)
                dsna = DoubleStrandNucleicAcid()

            # there is a valid base pair
            else:
                # base pair is not connected to the rest of the DSNA ...
                if len(dsna) > 0 and not (
                    (
                        # at least one of the two residues is NOT connected
                        # in the "normal" order
                        NABuilder()._is_connected(dsna[-1].i_res, res1)
                        and NABuilder()._is_connected(res2, dsna[-1].j_res)
                    )
                    or (
                        # at least one of the two residues is NOT connected
                        # in the "reverse" order
                        NABuilder()._is_connected(dsna[-1].j_res, res1)
                        and NABuilder()._is_connected(res2, dsna[-1].i_res)
                    )
                ):
                    # save DSNA and start a new one
                    dsna_list.append(dsna)
                    dsna = DoubleStrandNucleicAcid()

                    # save base pair
                    dsna.append(BasePair(res1, res2, pairing_rules))
                    already_paired += [res1, res2]

                # base pair is connected to the rest of DSNA
                elif len(dsna) > 0 and (
                    # at least one of the two residues IS connected
                    # in the "normal" order
                    NABuilder()._is_connected(dsna[-1].i_res, res1)
                    and NABuilder()._is_connected(res2, dsna[-1].j_res)
                ):
                    # save base pair
                    dsna.append(BasePair(res1, res2, pairing_rules))
                    already_paired += [res1, res2]

                # base pair is connected to the rest of DSNA
                elif len(dsna) > 0 and (
                    # at least one of the two residues IS connected
                    # in the "reverse" order
                    NABuilder()._is_connected(dsna[-1].j_res, res1)
                    and NABuilder()._is_connected(res2, dsna[-1].i_res)
                ):
                    # save base pair
                    dsna.append(BasePair(res2, res1, pairing_rules))
                    already_paired += [res1, res2]

                # base pair is the start of a DSNA
                elif len(dsna) == 0:
                    # save base pair
                    dsna.append(BasePair(res1, res2, pairing_rules))
                    already_paired += [res1, res2]

        if len(dsna) > 0:
            # if at the end there is still a DoubleStrandNucleicAcid
            # with some base pairs
            dsna_list.append(dsna)

        return dsna_list, already_paired
