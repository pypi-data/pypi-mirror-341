"""Core module for extracting Protein-DNA interfaces."""

from Bio.PDB.Polypeptide import PPBuilder
from Bio.PDB.NeighborSearch import NeighborSearch
from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom
from Bio.PDB.PDBExceptions import PDBConstructionException

import pandas as pd

from PDBNucleicAcids.NucleicAcid import NABuilder
from PDBNucleicAcids.NucleicAcid import DSNABuilder
from PDBNucleicAcids.NucleicAcid import DoubleStrandNucleicAcid

import copy

import warnings


class Interface:
    """
    Extract Protein-DNA interface.

    Parameters
    ----------
    structure : Bio.PDB.Structure
        Biopython Structure entity.
    protein_chain_id : str
        Chain id of a protein that may interact with DNA.
    search_radius : float | int, optional
        Search radius, measured in Armstrong, within which Protein-DNA
        interactions are found. Default is 4.0

    """

    def __init__(self, structure, protein_chain_id, search_radius=4.0) -> None:
        self.structure = structure
        self.protein_chain_id = protein_chain_id
        self.search_radius = search_radius

        self.contacts = self._extract_contacts()

        dna_atoms = self.get_dna_atoms()
        self._dna_chain_ids = list(
            {atom.parent.parent.id for atom in dna_atoms}
        )

    def __repr__(self) -> str:
        """Return string representation of the nucleic acid."""
        return f"<Interface chains={self.protein_chain_id}:\
{''.join(self._dna_chain_ids)} contacts={len(self.contacts)} search_radius=\
{self.search_radius}>"

    def _extract_contacts(self) -> list[tuple[Atom]]:
        """
        Extract interface contacts (PRIVATE).

        Raises
        ------
        PDBConstructionException
            In case of `protein_chain_id` not being a protein chain.

        Returns
        -------
        list[tuple[Atom]]
            List of pairs of atoms, first one is DNA, second is proteic.

        """
        # get all the atoms from the nucleic acids, in most cases DNA
        na_builder = NABuilder()
        na_list = na_builder.build_nucleic_acids(self.structure)
        na_atoms = []
        for na in na_list:
            na_atoms.extend(na.get_atoms())
        na_atoms = list(set(na_atoms))

        na_chain_ids = [na.get_chain_id() for na in na_list]

        # get all the atoms from the protein chain
        protein_chain = self.structure[0][self.protein_chain_id]
        pp_builder = PPBuilder()
        pp_list = pp_builder.build_peptides(protein_chain)

        # check if given chain id is actually a protein
        if not pp_list:
            raise PDBConstructionException(
                f"No polypeptides found in the input protein \
chain id: {self.protein_chain_id}"
            )

        pp_atoms = []
        for pp in pp_list:
            for res in pp:
                pp_atoms.extend(res.get_atoms())
        pp_atoms = list(set(pp_atoms))

        # Crea una lista con tutti gli atomi di DNA e proteina
        all_atoms = na_atoms + pp_atoms

        # Filter out hydrogens
        all_atoms = [atom for atom in all_atoms if atom.element != "H"]

        # Usa NeighborSearch per trovare gli atomi vicini entro una certa
        # distanza
        ns = NeighborSearch(all_atoms)

        # Cerca gli atomi vicini entro un raggio di 4 Å tra DNA e proteina
        all_contacts = ns.search_all(self.search_radius)

        # Filtra solo i contatti, ovvero le coppied di atomi,
        # che hanno un atomo di DNA
        temp = [
            (atom1, atom2)
            for atom1, atom2 in all_contacts
            if (
                atom1.parent.parent.id in na_chain_ids
                or atom2.parent.parent.id in na_chain_ids
            )
        ]

        # Filtra solo i contatti tra DNA e proteina
        contacts = [
            (atom1, atom2)
            for atom1, atom2 in temp
            if (
                atom1.parent.parent.id in na_chain_ids
                and atom2.parent.parent.id == self.protein_chain_id
            )
        ] + [
            (atom2, atom1)
            for atom1, atom2 in temp
            if (
                atom1.parent.parent.id == self.protein_chain_id
                and atom2.parent.parent.id in na_chain_ids
            )
        ]
        # temp è utile per greedyness, prima prendi il DNA, che ha meno
        # atomi, escludendo quelli intra-proteina
        # poi escludi anche quelli intra-DNA
        # inoltre ci assicuriamo che la col 0 contenga gli atomi di DNA e
        # che col 1 contenga gli atomi di proteine
        # Ce ne assicuriamo invertendo atom1 e atom2 nella seconda lista

        return contacts

    def get_atomic_contacts(self) -> list[tuple[Atom]]:
        """
        Get interface contacts as pairs of atoms.

        Returns
        -------
        list[tuple[Atom]]
            List of pairs of atoms, first one is DNA, second is proteic.

        """
        return self.contacts

    def get_protein_atoms(self) -> list[Atom]:
        """
        Get only protein atoms in the protein-DNA interface.

        Returns
        -------
        list[Atom]
            List of protein atoms in the interface.

        """
        return list({atom_pair[1] for atom_pair in self.contacts})

    def get_dna_atoms(self) -> list[Atom]:
        """
        Get only DNA atoms in the protein-DNA interface.

        Returns
        -------
        list[Atom]
            List of DNA atoms in the interface.

        """
        return list({atom_pair[0] for atom_pair in self.contacts})

    def get_aminoacids(self) -> list[Residue]:
        """
        Get only protein residues in the protein-DNA interface.

        Returns
        -------
        list[Residue]
            List of protein reisudes in the interface.

        """
        return list({atom_pair[1].parent for atom_pair in self.contacts})

    def get_nucleotides(self) -> list[Residue]:
        """
        Get only DNA residues in the protein-DNA interface.

        Returns
        -------
        list[Residue]
            List of DNA residues in the interface.

        """
        return list({atom_pair[0].parent for atom_pair in self.contacts})

    def as_dataframe(self) -> pd.DataFrame:
        """
        Get all data from the interface, as a dataframe.

        Contains the following data fields:
            Residue hetero field
            Residue number
            Residue insertion code
            Residue name
            Atom name
            Atom alternate location
            Atom element
            Atomic coordinates (x, y, z)
            From both protein and DNA atoms
            Euclidean distance between atom pair in contact

        Returns
        -------
        df : pd.DataFrame
            All data from the interface.

        """
        data = []

        for na_atom, prot_atom in self.contacts:
            prot_res_hetfield = prot_atom.parent.id[0]
            prot_res_number = prot_atom.parent.id[1]
            prot_res_icode = prot_atom.parent.id[2]
            prot_res_name = prot_atom.parent.resname
            prot_atom_name = prot_atom.name
            prot_atom_altloc = prot_atom.altloc
            prot_atom_element = prot_atom.element
            prot_atom_coord_x = prot_atom.coord[0]
            prot_atom_coord_y = prot_atom.coord[1]
            prot_atom_coord_z = prot_atom.coord[2]

            dna_chain_id = na_atom.parent.parent.id
            dna_res_hetfield = na_atom.parent.id[0]
            dna_res_number = na_atom.parent.id[1]
            dna_res_icode = na_atom.parent.id[2]
            dna_res_name = na_atom.parent.resname
            dna_atom_name = na_atom.name
            dna_atom_altloc = na_atom.altloc
            dna_atom_element = na_atom.element
            dna_atom_coord_x = na_atom.coord[0]
            dna_atom_coord_y = na_atom.coord[1]
            dna_atom_coord_z = na_atom.coord[2]

            euclidean_distance = na_atom - prot_atom

            row = (
                self.protein_chain_id,
                prot_res_hetfield,
                prot_res_number,
                prot_res_icode,
                prot_res_name,
                prot_atom_name,
                prot_atom_altloc,
                prot_atom_element,
                prot_atom_coord_x,
                prot_atom_coord_y,
                prot_atom_coord_z,
                dna_chain_id,
                dna_res_hetfield,
                dna_res_number,
                dna_res_icode,
                dna_res_name,
                dna_atom_name,
                dna_atom_altloc,
                dna_atom_element,
                dna_atom_coord_x,
                dna_atom_coord_y,
                dna_atom_coord_z,
                euclidean_distance,
            )

            data.append(row)

        df = pd.DataFrame(
            data,
            columns=[
                "protein_chain_id",
                "prot_res_hetfield",
                "prot_res_number",
                "prot_res_icode",
                "prot_res_name",
                "prot_atom_name",
                "prot_atom_altloc",
                "prot_atom_element",
                "prot_atom_coord_x",
                "prot_atom_coord_y",
                "prot_atom_coord_z",
                "dna_chain_id",
                "dna_res_hetfield",
                "dna_res_number",
                "dna_res_icode",
                "dna_res_name",
                "dna_atom_name",
                "dna_atom_altloc",
                "dna_atom_element",
                "dna_atom_coord_x",
                "dna_atom_coord_y",
                "dna_atom_coord_z",
                "euclidean_distance",
            ],
        )

        return df

    def get_bound_double_strands(self) -> list[DoubleStrandNucleicAcid]:
        """
        Get all double-strand nucleic acids bound by the protein.

        The output double stranded nucleic acids (DSNAs) are subsequences
        of the full DSNAs found in the structure,
        since proteins usually do not bind the whole DSNA.

        This method allows for "gaps" of unbound base-pairs inside the
        DSNA, only the base pairs at the ends are trimmed accourding
        to being protein-bound or not.

        A visual example of "gaps":
            ``Input full DSNA:            GATATACAAGCCA``

            ``Protein-bound:                ****  **   ``

            ``Output protein-bound DSNA:    TATACAAG   ``

        Returns
        -------
        bound_dsna_list : list[DoubleStrandNucleicAcid]
            List of double-strand nucleic acids bound by the protein.

        """
        bound_nucleotides = self.get_nucleotides()

        builder = DSNABuilder()
        dsna_list = builder.build_double_strands(self.structure)
        bound_dsna_list = []
        for dsna in dsna_list:
            bound_dsna = copy.copy(dsna)
            while (
                len(bound_dsna) > 0
                and bound_dsna[0].i_res not in bound_nucleotides
                and bound_dsna[0].j_res not in bound_nucleotides
            ):
                # if the FIRST base pair isn't bound by protein
                # then discard it and check the next FIRST base pair
                bound_dsna.pop(0)

            while (
                len(bound_dsna) > 0
                and bound_dsna[-1].i_res not in bound_nucleotides
                and bound_dsna[-1].j_res not in bound_nucleotides
            ):
                # if the LAST base pair isn't bound by protein
                # then discard it and check the next LAST base pair
                bound_dsna.pop(-1)

            if len(bound_dsna) > 0:
                # in this case, there is an actual bound DSNA
                bound_dsna_list.append(bound_dsna)

                unbound_bps = []
                for bp in bound_dsna:
                    if (
                        bp.i_res not in bound_nucleotides
                        and bp.j_res not in bound_nucleotides
                    ):
                        unbound_bps.append(bp)

                if unbound_bps:
                    warnings.warn(
                        f"Warning: There are {len(unbound_bps)} unbound \
base-pairs inside {bound_dsna} - {unbound_bps}"
                    )

        return bound_dsna_list

    def fixed_protein_atoms_number(self, num_atoms) -> None:
        """Filter contacts by a fixed number of protein atoms."""
        # cast list into dataframe, ready to be sorted
        df = pd.DataFrame(self.contacts, columns=["na_atom", "protein_atom"])
        df["euclidean_distance"] = df.apply(
            lambda row: row["na_atom"] - row["protein_atom"], axis=1
        )

        # aggregate: for each atom, its minimum distance from DSNA
        agg = df.groupby(["protein_atom"]).min()
        agg = agg.reset_index()
        agg = agg.sort_values(by="euclidean_distance", ascending=True)

        # get closest n atoms to DSNA
        top_protein_atoms = agg.head(num_atoms)["protein_atom"].tolist()

        if len(top_protein_atoms) <= num_atoms:
            raise Exception("Not enough atoms.")

        # select contacts by top n atoms
        selected_contacts = [
            (na_atom, protein_atom)
            for na_atom, protein_atom in self.contacts
            if protein_atom in top_protein_atoms
        ]

        self.contacts = selected_contacts

    def fixed_na_atoms_number(self, num_atoms) -> None:
        """Filter contacts by a fixed number of nucleic acid atoms."""
        # cast list into dataframe, ready to be sorted
        df = pd.DataFrame(self.contacts, columns=["na_atom", "protein_atom"])
        df["euclidean_distance"] = df.apply(
            lambda row: row["na_atom"] - row["protein_atom"], axis=1
        )

        # aggregate: for each atom, its minimum distance from DSNA
        agg = df.groupby(["na_atom"]).min()
        agg = agg.reset_index()
        agg = agg.sort_values(by="euclidean_distance", ascending=True)

        # get closest n atoms to DSNA
        top_na_atoms = agg.head(num_atoms)["na_atom"].tolist()

        if len(top_na_atoms) <= num_atoms:
            raise Exception("Not enough atoms.")

        # select contacts by top n atoms
        selected_contacts = [
            (na_atom, protein_atom)
            for na_atom, protein_atom in self.contacts
            if na_atom in top_na_atoms
        ]

        self.contacts = selected_contacts


def build_interfaces(structure, search_radius=4.0) -> list[Interface]:
    """
    Extract all Protein-DNA interfaces found in a structure.

    Parameters
    ----------
    structure : Bio.PDB.Structure
        Biopython Structure entity.
    search_radius : float | int, optional
        Search radius, measured in Armstrong, within which Protein-DNA
        interactions are found. Default is 4.0

    Returns
    -------
    list
        List of all Protein-DNA interfaces found in a structure.

    """
    # build nucleic acids
    builder = NABuilder()
    na_list = builder.build_nucleic_acids(structure)
    if not na_list:
        return []

    # dna_chain_ids = list({na.get_chain_id() for na in na_list})

    # build peptides
    builder = PPBuilder()
    pp_list = builder.build_peptides(structure)
    if not pp_list:
        return []

    prot_chain_ids = list({pp[0].parent.id for pp in pp_list})

    face_list = []
    for prot_chain_id in prot_chain_ids:
        # extract interface
        face = Interface(
            structure=structure,
            protein_chain_id=prot_chain_id,
            search_radius=search_radius,
        )

        # skip empty interfaces
        if len(face.get_atomic_contacts()) > 0:
            face_list.append(face)

    return face_list
