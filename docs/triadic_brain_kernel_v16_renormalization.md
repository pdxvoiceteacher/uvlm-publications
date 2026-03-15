# Triadic Brain Kernel v16

## Knowledge Field Renormalization

## 1 Purpose

Discovery operates across scales:

- node
- → corridor
- → river
- → terrace
- → paradigm

Without scale normalization:

- small discoveries vanish
- large structures dominate

Renormalization preserves discovery across scales.

## 2 Knowledge Field

State:

\[
\Psi(x,t)
\]

Define scale transform:

\[
x \to \lambda x
\]

Field transforms:

\[
\Psi'(x) = \lambda^{\alpha}\,\Psi(\lambda x)
\]

## 3 Renormalization Operator

Define operator:

\[
\mathcal{R}_{\lambda}[\Psi] = \mathrm{coarse\_grain}(\Psi, \lambda)
\]

## 4 Renormalized PDE

Original discovery equation:

\[
\frac{\partial \Psi}{\partial t} = D\nabla^2\Psi - \nabla\cdot(\Psi\nabla\Phi) + S
\]

Renormalized system:

\[
\frac{\partial \Psi_{\ell}}{\partial t} = D_{\ell}\nabla^2\Psi_{\ell} - \nabla\cdot(\Psi_{\ell}\nabla\Phi_{\ell}) + S_{\ell}
\]

## 5 Scale Flow

Define RG flow:

- dD/d\ell
- d\Phi/d\ell
- dS/d\ell

Stable terraces correspond to fixed points:

- \(\beta(D)=0\)
- \(\beta(\Phi)=0\)

## 6 Terrace Stability Condition

Terrace exists when:

- \(\partial\Psi/\partial t \approx 0\)
- \(\nabla\Psi \approx 0\)

but

- \(\partial^2\Psi/\partial x^2 > 0\)

(local minimum of \(\Phi\)).

## 7 Scientific Interpretation

| Regime | RG Interpretation |
| --- | --- |
| corridor | relevant operator |
| river | scale-stable flow |
| terrace | fixed point |
| orthodoxy | metastable trap |
| rupture | RG bifurcation |

## 8 Renormalization Kernel

CoherenceLattice module:

`python/src/coherence/kernel/renormalization.py`

```python
import numpy as np


def coarse_grain(field, scale):
    n = len(field)//scale
    return np.mean(field.reshape(n, scale), axis=1)


def renormalize(field, scale):
    coarse = coarse_grain(field, scale)
    return coarse / np.max(coarse)
```

## 9 Result

With Kernel v16:

- small discoveries survive scaling
- corridors merge into rivers
- rivers stabilize terraces

The architecture now behaves like a knowledge renormalization group.
