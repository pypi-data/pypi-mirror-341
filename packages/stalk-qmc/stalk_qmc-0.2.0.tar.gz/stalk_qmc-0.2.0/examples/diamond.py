#!/usr/bin/env python3

# Diamond: 1D line-search example
#
# This example executes a standard line-search minimization workflow for the
# ground state of the benzene molecule, using DFT (PBE) as the surrogate
# method and Diffusion Monte Carlo (DMC) as the stochastic method.

from numpy import array

from nexus import generate_qmcpack, job
from nexus import generate_physical_system, generate_pw2qmcpack, generate_pwscf
from stalk.nexus.PwscfGeometry import PwscfGeometry
from stalk.nexus.PwscfPes import PwscfPes
from structure import Structure

from stalk.util.util import Bohr
from stalk.nexus import NexusStructure
from stalk.nexus.NexusGeometry import NexusGeometry
from stalk.nexus.NexusPes import NexusPes
from stalk.nexus.QmcPes import QmcPes
from stalk.lsi import LineSearchIteration
from stalk.params.ParameterHessian import ParameterHessian
from stalk.params.PesFunction import PesFunction
from stalk.pls.TargetParallelLineSearch import TargetParallelLineSearch
from stalk.util import EffectiveVariance

from nxs import pwscfjob, optjob, dmcjob, p2qjob

# Pseudos (execute download_pseudos.sh in the working directory)
base_dir = 'diamond/'
softpseudos = ['C.pbe_v1.2.uspp.F.upf']
scfpseudos = ['C.ccECP.upf']
qmcpseudos = ['C.ccECP.xml']
interactive = False


# Forward mapping: produce parameter values from an array of atomic positions
def forward(pos, axes):
    from stalk.params.util import mean_param
    from numpy import array
    # Redundancy helps in finding silly mistakes in the parameter mappings
    a = mean_param([
        axes[0, 0],
        axes[0, 1],
        axes[1, 1],
        axes[1, 2],
        axes[2, 0],
        axes[2, 2],
    ])
    return array([a])
# end def


def backward(params):
    a = params[0]
    axes = [
        [a, a, 0],
        [0, a, a],
        [a, 0, a]
    ]
    pos = [
        [0.0, 0.0, 0.0],
        [a / 2, a / 2, a / 2]
    ]
    return pos, axes
# end def


# Define a surrogate SCF relaxation job
def scf_vcrelax_job(structure: Structure, path, **kwargs):
    system = generate_physical_system(
        structure=structure,
        C=4,
    )
    relax = generate_pwscf(
        system=system,
        job=job(**pwscfjob),
        path=path,
        pseudos=softpseudos,
        ecutwfc=80,
        ecutrho=300,
        kgrid=(8, 8, 8),
        kshift=(0, 0, 0,),
        conv_thr=1e-9,
        identifier='vcrelax',
        calculation='vc-relax',
        input_type='generic',
        input_dft='pbe',
        occupations='smearing',
        smearing='gaussian',
        degauss=0.0001,
        nosym=False,
        mixing_beta=.7,
        electron_maxstep=200,
        forc_conv_thr=1e-4,
        ion_dynamics='bfgs',
        press=0.0,
        press_conv_thr=0.4,
    )
    return [relax]
# end def


# Define a surrogate SCF PES job that is consistent with the above relaxation
def scf_pes_job(structure: Structure, path, **kwargs):
    system = generate_physical_system(
        structure=structure,
        C=4,
    )
    scf = generate_pwscf(
        system=system,
        job=job(**pwscfjob),
        path=path,
        pseudos=softpseudos,
        ecutwfc=80,
        ecutrho=300,
        kgrid=(8, 8, 8),
        kshift=(0, 0, 0,),
        conv_thr=1e-9,
        identifier='scf',
        calculation='scf',
        input_type='generic',
        input_dft='pbe',
        occupations='smearing',
        smearing='gaussian',
        degauss=0.0001,
        nosym=False,
        mixing_beta=.7,
        electron_maxstep=200,
    )
    return [scf]
# end def


# Define a QMC workflow based on SCF, VMC Jastrow optimization and DMC
def dmc_pes_job(
    structure: Structure,
    path,
    sigma=None,
    samples=10,
    var_eff=None,
    **kwargs
):
    # Estimate the relative number of samples needed
    if isinstance(var_eff, EffectiveVariance):
        dmcsteps = var_eff.get_samples(sigma)
    else:
        dmcsteps = samples
    # end if

    # For QMCPACK, use plane-waves for better performance
    system = generate_physical_system(
        structure=structure,
        C=4,
        tiling=(2, 2, 2),
        kshift=(0, 0, 0),
        kgrid=(1, 1, 1),
    )
    scf = generate_pwscf(
        system=system,
        job=job(**pwscfjob),
        path=path + 'scf',
        pseudos=scfpseudos,
        identifier='scf',
        calculation='scf',
        input_type='generic',
        input_dft='pbe',
        nosym=False,
        nogamma=True,
        conv_thr=1e-9,
        mixing_beta=.7,
        ecutwfc=300,
        ecutrho=600,
        occupations='smearing',
        smearing='gaussian',
        degauss=0.0001,
        electron_maxstep=200,
    )
    p2q = generate_pw2qmcpack(
        identifier='p2q',
        path=path + 'scf',
        job=job(**p2qjob),
        dependencies=[(scf, 'orbitals')],
    )
    opt = generate_qmcpack(
        system=system,
        path=path + 'opt',
        job=job(**optjob),
        dependencies=[(p2q, 'orbitals')],
        cycles=6,
        identifier='opt',
        qmc='opt',
        input_type='basic',
        pseudos=qmcpseudos,
        J2=True,
        J1_size=6,
        J2_size=8,
        minmethod='oneshift',
        blocks=200,
        substeps=2,
        samples=100000,
        minwalkers=0.1,
    )
    dmc = generate_qmcpack(
        system=system,
        path=path + 'dmc',
        job=job(**dmcjob),
        dependencies=[(p2q, 'orbitals'), (opt, 'jastrow')],
        steps=dmcsteps,
        identifier='dmc',
        qmc='dmc',
        input_type='basic',
        pseudos=qmcpseudos,
        jastrows=[],
        walkers_per_rank=128,
        blocks=200,
        timestep=0.01,
        ntimesteps=1,
    )
    return [scf, p2q, opt, dmc]
# end def


# Create relaxation job generator with loader
vcrelax_job = NexusGeometry(
    func=PesFunction(scf_vcrelax_job),
    loader=PwscfGeometry({'suffix': 'vcrelax.in', 'c_pos': Bohr})
)
# Create pes job generator with loader
pes = NexusPes(
    func=PesFunction(scf_pes_job),
    loader=PwscfPes({'suffix': 'scf.in'})
)
qmcpes = NexusPes(
    func=PesFunction(dmc_pes_job),
    loader=QmcPes({'suffix': '/dmc/dmc.in.xml', 'qmc_idx': 1})
)
# Starting structure
params_init = array([1.7])
structure_init = NexusStructure(
    forward=forward,
    backward=backward,
    params=params_init,
    elem=['C', 'C'],
    units='A'
)


# 1) Surrogate: Relaxation
# Copy initial structure and relax using the relaxation job
structure_relax = structure_init.copy()
vcrelax_job.relax(
    structure_relax,
    path=base_dir + 'vcrelax/',
    interactive=interactive
)


# 2) Surrogate: Hessian
# Hessian based on the structural mappings
hessian = ParameterHessian(structure=structure_relax)
hessian.compute_fdiff(
    path=base_dir + 'fdiff',
    pes=pes,
    interactive=interactive,
)
print('Hessian:')
print(hessian)


# 3) Surrogate: Optimize line-search
# Generate a parallel line-search object that samples the
# surrogate PES around the minimum along the search directions
surrogate_file = 'surrogate.p'
surrogate = TargetParallelLineSearch(
    path=base_dir + 'surrogate/',
    fit_kind='pf3',
    load=surrogate_file,
    structure=structure_relax,
    hessian=hessian,
    pes=pes,
    window_frac=0.2,  # maximum displacement relative to Lambda of each direction
    M=15  # number of points per direction to sample
)
# Optimize the line-search according to this model to 0.01 Bohr accuracy
surrogate.optimize(
    epsilon_p=[0.02],
    fit_kind='pf3',
    M=7,
    N=400,
    reoptimize=False,
    write=surrogate_file,
)
print(surrogate)


# 4-5) Stochastic: Line-search
# return a simple 4-item DMC workflow for Nexus:
#   1: run SCF with norm-conserving ECPs to get orbitals
#   2: convert for QMCPACK
#   3: Optimize 2-body Jastrow coefficients
#   4: Run DMC with enough steps/block to meet the target errorbar sigma
#     it is important to first characterize the DMC run into var_eff
structure_qmc = structure_relax.copy()

# Run a snapshot job to sample effective variance w.r.t relative DMC samples
var_eff = qmcpes.get_var_eff(
    structure_qmc,
    path=base_dir + 'dmc_var_eff',
    samples=10,
    interactive=interactive,
)
qmcpes.args['var_eff'] = var_eff

# Finally, perform line-search iteration based on surrogate settings and DMC PES
dmc_ls = LineSearchIteration(
    surrogate=surrogate,
    path=base_dir + 'dmc_ls',
    pes=qmcpes
)
for i in range(2):
    dmc_ls.propagate(i, interactive=interactive)
# end for
dmc_ls.pls().evaluate_eqm(interactive=interactive)

# Print out the line-search performance
# Disclaimer: this example demonstrates that DMC
print(dmc_ls)
