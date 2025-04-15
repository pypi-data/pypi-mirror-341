import re
import keras
import numpy as np
import tensorflow as tf
from rdkit import Chem

from molcraft import ops
from molcraft import chem 
from molcraft import features 
from molcraft import featurizers
from molcraft import tensors
from molcraft import descriptors

    
def Graph(
    inputs,
    atom_features: list[features.Feature] | str | None = 'auto',
    bond_features: list[features.Feature] | str | None = 'auto',
    super_atom: bool = True,
    radius: int | float | None = None,
    self_loops: bool = False,
    include_hs: bool = False,
    **kwargs,
):
    featurizer = featurizers.MolGraphFeaturizer(
        atom_features=atom_features,
        bond_features=bond_features,
        molecule_features=[AminoAcidType()],
        super_atom=super_atom,
        radius=radius,
        self_loops=self_loops,
        include_hs=include_hs,
        **kwargs,
    )

    inputs = [
        residues[x] for x in ['G'] + inputs
    ]
    tensor_list = [featurizer(x) for x in inputs]
    return tf.stack(tensor_list, axis=0)


def GraphLookup(graph: tensors.GraphTensor) -> 'GraphLookupLayer':
    lookup = GraphLookupLayer()
    lookup._build(graph)
    return lookup


@keras.saving.register_keras_serializable(package='molcraft')
class GraphLookupLayer(keras.layers.Layer):

    def call(self, indices: tf.Tensor) -> tensors.GraphTensor:
        indices = tf.sort(tf.unique(tf.reshape(indices, [-1]))[0])
        graph = self.graph[indices]
        sizes = graph.context['size']
        max_index = keras.ops.max(indices)
        sizes = tf.tensor_scatter_nd_update(
            tensor=tf.zeros([max_index + 1], dtype=indices.dtype),
            indices=indices[:, None],
            updates=sizes
        )
        graph = graph.update(
            {
                'context': {
                    'size': sizes
                }
            },
        )
        return tensors.to_dict(graph)
    
    def _build(self, x):

        if isinstance(x, tensors.GraphTensor):
            tensor = tensors.to_dict(x)
            self._spec = tf.nest.map_structure(
                tf.type_spec_from_value, tensor
            )
        else:
            self._spec = x

        self._graph = tf.nest.map_structure(
            lambda s: self.add_weight(
                shape=s.shape, 
                dtype=s.dtype, 
                trainable=False,
                initializer='zeros'
            ),
            self._spec
        )

        if isinstance(x, tensors.GraphTensor):
            tf.nest.map_structure(
                lambda v, x: v.assign(x),
                self._graph, tensor
            )

        graph = tf.nest.map_structure(
            keras.ops.convert_to_tensor, self._graph
        )
        self._graph_tensor = tensors.from_dict(graph)
        
    def get_config(self):
        config = super().get_config()
        spec = keras.saving.serialize_keras_object(self._spec)
        config['spec'] = spec
        return config 
    
    @classmethod
    def from_config(cls, config: dict) -> 'GraphLookupLayer':
        spec = config.pop('spec')
        spec = keras.saving.deserialize_keras_object(spec)
        layer = cls(**config)
        layer._build(spec)
        return layer

    @property 
    def graph(self) -> tensors.GraphTensor:
        return self._graph_tensor
    

@keras.saving.register_keras_serializable(package='molcraft')
class Gather(keras.layers.Layer):

    def __init__(
        self, 
        padding: list[tuple[int]] | tuple[int] | int = 1, 
        mask_value: int = 0,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.padding = padding
        self.mask_value = mask_value
        self.supports_masking = True

    def get_config(self):
        config = super().get_config()
        config['mask_value'] = self.mask_value 
        config['padding'] = self.padding
        return config 
    
    def call(self, inputs: tuple[tf.Tensor, tf.Tensor]) -> tf.Tensor:
        data, indices = inputs 
        # if self.padding:
        #     padding = self.padding
        #     if isinstance(self.padding, int):
        #         padding = [(self.padding, 0)]
        #     if isinstance(self.padding, tuple):
        #         padding = [self.padding] 
        #     data_rank = len(keras.ops.shape(data))
        #     for _ in range(data_rank - len(padding)):
        #         padding.append((0, 0))
        #     data = keras.ops.pad(data, padding)
        return ops.gather(data, indices) 
    
    def compute_mask(
        self, 
        inputs: tuple[tf.Tensor, tf.Tensor], 
        mask: bool | None = None
    ) -> tf.Tensor | None:
        # if self.mask_value is None:
        #     return None
        _, indices = inputs
        return keras.ops.not_equal(indices, self.mask_value)
    

@keras.saving.register_keras_serializable(package='molcraft')
class AminoAcidType(descriptors.Descriptor):

    def __init__(self, vocab=None, **kwargs):
        vocab = [
            "A", "C", "D", "E", "F", "G", "H", "I", "K", "L", 
            "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y",
        ]
        super().__init__(vocab=vocab, **kwargs)

    def call(self, mol: chem.Mol) -> list[str]:
        residue = residues_reverse.get(mol.canonical_smiles)
        if not residue:
            raise KeyError(f'Could not find {mol.canonical_smiles} in `residues_reverse`.')
        mol = chem.remove_hs(mol)
        return _extract_residue_type(residues_reverse[mol.canonical_smiles])
    
def sequence_split(sequence: str):
    patterns = [
        r'(\[[A-Za-z0-9]+\]-[A-Z]\[[A-Za-z0-9]+\])', # N-term mod + mod
        r'([A-Z]\[[A-Za-z0-9]+\]-\[[A-Za-z0-9]+\])', # C-term mod + mod
        r'([A-Z]-\[[A-Za-z0-9]+\])', # C-term mod
        r'(\[[A-Za-z0-9]+\]-[A-Z])', # N-term mod
        r'([A-Z]\[[A-Za-z0-9]+\])', # Mod
        r'([A-Z])', # No mod
    ]
    return [match.group(0) for match in re.finditer("|".join(patterns), sequence)]

residues = {
    "A": "N[C@@H](C)C(=O)O",
    "C": "N[C@@H](CS)C(=O)O",
    "C[Carbamidomethyl]": "N[C@@H](CSCC(=O)N)C(=O)O",
    "D": "N[C@@H](CC(=O)O)C(=O)O",
    "E": "N[C@@H](CCC(=O)O)C(=O)O",
    "F": "N[C@@H](Cc1ccccc1)C(=O)O",
    "G": "NCC(=O)O",
    "H": "N[C@@H](CC1=CN=C-N1)C(=O)O",
    "I": "N[C@@H](C(CC)C)C(=O)O",
    "K": "N[C@@H](CCCCN)C(=O)O",
    "K[Acetyl]": "N[C@@H](CCCCNC(=O)C)C(=O)O",
    "K[Crotonyl]": "N[C@@H](CCCCNC(C=CC)=O)C(=O)O",
    "K[Dimethyl]": "N[C@@H](CCCCN(C)C)C(=O)O",
    "K[Formyl]": "N[C@@H](CCCCNC=O)C(=O)O",
    "K[Malonyl]": "N[C@@H](CCCCNC(=O)CC(O)=O)C(=O)O",
    "K[Methyl]": "N[C@@H](CCCCNC)C(=O)O",
    "K[Propionyl]": "N[C@@H](CCCCNC(=O)CC)C(=O)O",
    "K[Succinyl]": "N[C@@H](CCCCNC(CCC(O)=O)=O)C(=O)O",
    "K[Trimethyl]": "N[C@@H](CCCC[N+](C)(C)C)C(=O)O",
    "L": "N[C@@H](CC(C)C)C(=O)O",
    "M": "N[C@@H](CCSC)C(=O)O",
    "M[Oxidation]": "N[C@@H](CCS(=O)C)C(=O)O",
    "N": "N[C@@H](CC(=O)N)C(=O)O",
    "P": "N1[C@@H](CCC1)C(=O)O",
    "P[Oxidation]": "N1CC(O)C[C@H]1C(=O)O",
    "Q": "N[C@@H](CCC(=O)N)C(=O)O",
    "R": "N[C@@H](CCCNC(=N)N)C(=O)O",
    "R[Deamidated]": "N[C@@H](CCCNC(N)=O)C(=O)O",
    "R[Dimethyl]": "N[C@@H](CCCNC(N(C)C)=N)C(=O)O",
    "R[Methyl]": "N[C@@H](CCCNC(=N)NC)C(=O)O",
    "S": "N[C@@H](CO)C(=O)O",
    "T": "N[C@@H](C(O)C)C(=O)O",
    "V": "N[C@@H](C(C)C)C(=O)O",
    "W": "N[C@@H](CC(=CN2)C1=C2C=CC=C1)C(=O)O",
    "Y": "N[C@@H](Cc1ccc(O)cc1)C(=O)O",
    "Y[Nitro]": "N[C@@H](Cc1ccc(O)c(N(=O)=O)c1)C(=O)O",
    "Y[Phospho]": "N[C@@H](Cc1ccc(OP(O)(=O)O)cc1)C(=O)O",
    "[Acetyl]-A": "N(C(C)=O)[C@@H](C)C(=O)O",
    "[Acetyl]-C": "N(C(C)=O)[C@@H](CS)C(=O)O",
    "[Acetyl]-D": "N(C(=O)C)[C@H](C(=O)O)CC(=O)O",
    "[Acetyl]-E": "N(C(=O)C)[C@@H](CCC(O)=O)C(=O)O",
    "[Acetyl]-F": "N(C(C)=O)[C@@H](Cc1ccccc1)C(=O)O",
    "[Acetyl]-G": "N(C(=O)C)CC(=O)O",
    "[Acetyl]-H": "N(C(=O)C)[C@@H](Cc1[nH]cnc1)C(=O)O",
    "[Acetyl]-I": "N(C(=O)C)[C@@H]([C@H](CC)C)C(=O)O",
    "[Acetyl]-K": "N(C(C)=O)[C@@H](CCCCN)C(=O)O",
    "[Acetyl]-L": "N(C(=O)C)[C@@H](CC(C)C)C(=O)O",
    "[Acetyl]-M": "N(C(=O)C)[C@@H](CCSC)C(=O)O",
    "[Acetyl]-N": "N(C(C)=O)[C@@H](CC(=O)N)C(=O)O",
    "[Acetyl]-P": "N1(C(=O)C)CCC[C@H]1C(=O)O",
    "[Acetyl]-Q": "N(C(=O)C)[C@@H](CCC(=O)N)C(=O)O",
    "[Acetyl]-R": "N(C(C)=O)[C@@H](CCCN=C(N)N)C(=O)O",
    "[Acetyl]-S": "N(C(C)=O)[C@@H](CO)C(=O)O",
    "[Acetyl]-T": "N(C(=O)C)[C@@H]([C@H](O)C)C(=O)O",
    "[Acetyl]-V": "N(C(=O)C)[C@@H](C(C)C)C(=O)O",
    "[Acetyl]-W": "N(C(C)=O)[C@@H](Cc1c2ccccc2[nH]c1)C(=O)O",
    "[Acetyl]-Y": "N(C(C)=O)[C@@H](Cc1ccc(O)cc1)C(=O)O"
}

residues_reverse = {}
def register_peptide_residues(residues: dict[str, str]):
    for residue, smiles in residues.items():
        residues[residue] = Chem.MolToSmiles(Chem.MolFromSmiles(smiles))
        residues_reverse[residues[residue]] = residue
    
register_peptide_residues(residues)

def _extract_residue_type(residue_tag: str) -> str:
    pattern = r"(?<!\[)[A-Z](?![\w-])"
    return [match.group(0) for match in re.finditer(pattern, residue_tag)][0]