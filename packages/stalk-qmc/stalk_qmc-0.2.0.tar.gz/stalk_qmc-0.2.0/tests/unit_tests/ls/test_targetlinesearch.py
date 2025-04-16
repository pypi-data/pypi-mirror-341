#!/usr/bin/env python

from numpy import array, isnan, linspace, where
from pytest import raises

from stalk.params.PesFunction import PesFunction
from stalk.util import match_to_tol
from stalk import TargetLineSearch

from ..assets.h2o import get_structure_H2O, get_hessian_H2O, pes_H2O
from ..assets.helper import Gs_N200_M7

__author__ = "Juha Tiihonen"
__email__ = "tiihonen@iki.fi"
__license__ = "BSD-3-Clause"


# test TargetLineSearch class
def test_TargetLineSearch_init():

    with raises(TypeError):
        # Cannot init without fit_func/kind
        TargetLineSearch()
    # end with

    # Test init with zero input
    tls = TargetLineSearch(fit_kind='pf3')
    # TargetLineSearchBase properties
    assert tls.settings.N == 200
    assert tls.settings.fit_func.args['pfn'] == 3
    assert tls.settings.sgn == 1
    assert tls.settings.fraction == 0.025
    assert tls.target_settings.Gs is None
    assert tls.target_settings.fit_func.args['pfn'] == 3
    assert tls.target_settings.sgn == 1
    assert tls.target_settings.fraction == 0.025
    assert tls.target_settings.M == 0
    assert tls.target_settings.N == 0
    assert tls.target_settings.bias_mix == 0.0
    assert tls.target_settings.bias_order == 1
    assert tls.target_settings.target.x0 == 0.0
    assert tls.target_settings.target.y0 == 0.0
    assert tls.target_settings.target.x0_err == 0.0
    assert tls.target_settings.target.y0_err == 0.0
    assert tls.target_settings.interp is None
    assert tls.target_settings.interp_kind is None
    assert tls.target_interp is None
    assert not tls.valid_target
    # LineSearch properties
    assert len(tls) == 0
    assert not tls.valid
    assert tls.d is None
    assert tls.direction == 0.0
    assert tls.structure is None
    assert tls.hessian is None
    assert tls.W_max is None
    assert tls.Lambda is None
    assert tls.enabled
    assert tls.R_max == 0.0
    assert tls.sigma == 0.0
    assert len(tls.grid) == 0
    assert len(tls.offsets) == 0
    assert len(tls.values) == 0
    assert len(tls.errors) == 0
    assert tls.get_shifted_params() is None
    # TargetLineSearch properties
    assert tls.sigma_opt is None
    assert tls.W_opt is None
    assert tls.R_opt is None
    assert tls.grid_opt is None
    assert tls.Gs is None
    assert tls.Ws is None
    assert tls.M == 0
    assert tls.E_mat is None
    assert tls.W_mat is None
    assert tls.S_mat is None
    assert tls.T_mat is None
    assert tls.epsilon is None
    assert not tls.setup
    assert not tls.resampled
    assert not tls.optimized

    # Test init with only offsets input
    structure = get_structure_H2O()
    hessian = get_hessian_H2O()
    W = 0.2
    d = 1
    tls = TargetLineSearch(
        fit_kind='pf3',
        structure=structure,
        hessian=hessian,
        d=d,
        W=W
    )
    assert len(tls) == 7
    # Bias without valid target is nan
    assert isnan(tls.compute_bias_of(R=1.0)[2])
    with raises(AssertionError):
        # Cannot setup optimization without valid data
        tls.setup_optimization()
    # end with
    with raises(AssertionError):
        # Cannot generate error surface without valid data
        tls.generate_error_surface()
    # end with
    with raises(AssertionError):
        # Cannot insert sigma data without valid resampling
        tls.insert_sigma_data(0.1)
    # end with
    with raises(AssertionError):
        # Cannot insert sigma data without valid resampling
        tls.insert_W_data(0.1)
    # end with
    with raises(AssertionError):
        tls.optimize(0.1)
    # end with
    with raises(AssertionError):
        tls.statistical_cost()
    # end with

# end def


# test TargetLineSearch class
def test_TargetLineSearch_generate():

    # Test optimization with H2O data
    structure = get_structure_H2O()
    hessian = get_hessian_H2O()
    W = 0.2
    d = 1
    M = 11
    tls = TargetLineSearch(
        fit_kind='pf3',
        structure=structure,
        hessian=hessian,
        d=d,
        W=W,
        M=M,
        pes=PesFunction(pes_H2O),
        interpolate_kind='pchip'
    )
    assert tls.valid
    assert tls.valid_target
    assert not tls.resampled
    assert not tls.optimized
    assert len(tls.grid) == M
    assert len(tls.offsets) == M
    assert len(tls.values) == M
    assert len(tls.errors) == M
    assert tls.W_max == W
    # Try disabling a middle value
    tls.disable_value(M - 3)
    assert tls.valid_W_max == W  # Does not change
    tls.enable_value(M - 3)
    # Try disabling the last value
    tls.disable_value(M - 1)
    assert tls.valid_W_max < W  # is reduced
    # Keeping the value disabled to differentiate valid grid

    # Test compute_bias_of (bias_mix=0.2)
    bias_ref_mix02 = array(
        [1.01910959e-05, 1.71548208e-03, 7.83010112e-04, 9.37330982e-04,
         3.79984493e-04, 4.10401856e-04, 3.95103303e-04, 3.69730043e-04,
         8.19348365e-04, 1.03756967e-03])
    bias_ref_order3 = array(
        [1.01882428e-05, 1.50830475e-03, 6.89785874e-04, 8.86617358e-04,
         3.69380871e-04, 3.26316902e-04, 2.74564301e-04, 1.40335632e-04,
         5.11530832e-04, 6.51067392e-04])
    Ws_ref = linspace(0.0, tls.valid_W_max, 10)
    Rs_ref = [tls._W_to_R(W) for W in Ws_ref]
    # default
    Ws0, Rs0, bias0 = tls.compute_bias_of(bias_mix=0.2)
    assert match_to_tol(Ws0, Ws_ref)
    assert match_to_tol(Rs0, Rs_ref)
    assert match_to_tol(bias0, bias_ref_mix02)
    # scalar R
    Ws1, Rs1, bias1 = tls.compute_bias_of(bias_mix=0.2, R=Rs_ref[5])
    assert match_to_tol(Ws1, [Ws_ref[5]])
    assert match_to_tol(Rs1, [Rs_ref[5]])
    assert match_to_tol(bias1, [bias_ref_mix02[5]])
    # Array R
    Ws2, Rs2, bias2 = tls.compute_bias_of(bias_mix=0.2, R=Rs_ref)
    assert match_to_tol(Ws2, Ws_ref)
    assert match_to_tol(Rs2, Rs_ref)
    assert match_to_tol(bias2, bias_ref_mix02)
    # Array W
    Ws4, Rs4, bias4 = tls.compute_bias_of(bias_order=3, W=Ws_ref)
    assert match_to_tol(Ws4, Ws_ref)
    assert match_to_tol(Rs4, Rs_ref)
    assert match_to_tol(bias4, bias_ref_order3)
    # scalar W
    Ws3, Rs3, bias3 = tls.compute_bias_of(bias_order=3, W=Ws_ref[3])
    assert match_to_tol(Ws3, [Ws_ref[3]])
    assert match_to_tol(Rs3, [Rs_ref[3]])
    assert match_to_tol(bias3, [bias_ref_order3[3]])

    # Test figure_out_adjusted_offsets
    x_offset = 0.1
    tls.target_settings.target.x0 = x_offset
    assert match_to_tol(
        tls.figure_out_adjusted_offsets(R=0.2),
        tls.figure_out_offsets(R=0.2) + x_offset
    )

    # Test setup
    assert not tls.resampled
    assert tls.E_mat is None
    assert tls.W_mat is None
    assert tls.S_mat is None
    assert tls.T_mat is None
    with raises(AssertionError):
        # Must be setup before generating
        tls.generate_error_surface()
    # end with
    with raises(AssertionError):
        # Must be setup with M > 0
        tls.setup_optimization()
    # end with
    # Test default values
    N = 20
    M = 5
    tls.target_settings.target.x0 = 0.0
    tls.setup_optimization(M=M, N=N)
    # Test default values (noise_frac=0.05)
    W_mat_ref = array([[0., 0.1, 0.2],
                       [0., 0.1, 0.2],
                       [0., 0.1, 0.2]])
    S_mat_ref = array([[0., 0., 0.],
                       [0.005, 0.005, 0.005],
                       [0.010, 0.010, 0.010]])
    # Note: this is not independently controlled. We can only consistently compare the
    # First row of E_mat
    E0_mat_ref = array([[1.29622236e-06, 3.53685589e-04, 1.86921621e-03]])
    assert match_to_tol(tls.S_mat.max() / tls.W_mat.max(), 0.05)
    assert match_to_tol(tls.W_mat, W_mat_ref)
    assert match_to_tol(tls.S_mat, S_mat_ref)
    assert match_to_tol(tls.E_mat[0], E0_mat_ref[0])
    assert all((tls.T_mat == (W_mat_ref >= S_mat_ref)).flatten())
    # Test non-default values
    W_num = 4
    sigma_num = 5
    W_max = 0.75 * tls.W_max
    noise_frac = 0.1
    # Same M and N result in that Gs are not regenerated (but other params get overlooked)
    Gs_old = tls.Gs
    tls.setup_optimization(
        M=M,
        N=N,
        W_max=W_max,
        W_num=W_num,
        sigma_num=sigma_num,
        noise_frac=noise_frac,
    )
    assert Gs_old is tls.Gs
    assert len(tls.Ws) == 3
    assert len(tls.sigmas) == 3

    # Doubling the N will enforce recomputation of the whole error surface
    tls.setup_optimization(
        M=M,
        N=N * 2,
        Gs=None,
        W_max=W_max,
        W_num=W_num,
        sigma_num=sigma_num,
        noise_frac=noise_frac,
    )
    W_mat_ref1 = array([[0., 0.05, 0.1, 0.15],
                        [0., 0.05, 0.1, 0.15],
                        [0., 0.05, 0.1, 0.15],
                        [0., 0.05, 0.1, 0.15],
                        [0., 0.05, 0.1, 0.15]])
    S_mat_ref1 = array([[0.00000, 0.00000, 0.00000, 0.00000],
                        [0.00375, 0.00375, 0.00375, 0.00375],
                        [0.00750, 0.00750, 0.00750, 0.00750],
                        [0.01125, 0.01125, 0.01125, 0.01125],
                        [0.01500, 0.01500, 0.01500, 0.01500]])
    E0_mat_ref1 = array([[1.29622236e-06, 1.41974295e-04, 3.53685589e-04, 1.07211477e-03]])
    assert tls.W_mat.max() == W_max
    assert match_to_tol(tls.S_mat.max() / tls.W_mat.max(), noise_frac)
    assert match_to_tol(tls.W_mat, W_mat_ref1)
    assert match_to_tol(tls.S_mat, S_mat_ref1)
    assert match_to_tol(tls.E_mat[0], E0_mat_ref1[0])
    assert all((tls.T_mat == (W_mat_ref1 >= S_mat_ref1)).flatten())
# end def


# test TargetLineSearch class
def test_TargetLineSearch_optimize():

    # Test optimize method (start over with predefined Gs)
    tls = TargetLineSearch(
        fit_kind='pf3',
        structure=get_structure_H2O(),
        hessian=get_hessian_H2O(),
        d=0,
        W=0.4,
        M=21,
        pes=PesFunction(pes_H2O),
        interpolate_kind='cubic'
    )
    # Optimization fails for epsilon near zero but exception is captured
    epsilon0 = 1e-10
    tls.optimize(epsilon0, Gs=Gs_N200_M7, fit_kind='pf2')
    assert tls.resampled
    assert not tls.optimized
    # Only one round of generation is done.
    assert tls.E_mat.shape == (3, 3)

    # Test defaults with a reasonable epsilon value
    epsilon1 = 0.03
    W_opt_ref = 0.125
    sigma_opt_ref = 0.0175
    tls.optimize(
        epsilon1,
        fit_kind='pf3',
        W_resolution=0.05,
        Gs=Gs_N200_M7,
    )
    assert tls.resampled
    assert tls.optimized
    assert tls.target_settings.N == Gs_N200_M7.shape[0]
    assert tls.target_settings.M == Gs_N200_M7.shape[1]
    assert match_to_tol(tls.W_opt, W_opt_ref)
    assert match_to_tol(tls.sigma_opt, sigma_opt_ref)
    # Semantic quality checks
    xi = where(tls.W_mat[0] == tls.W_opt)[0]
    yi = where(tls.S_mat[:, 0] == tls.sigma_opt)[0]
    assert tls.E_mat[yi, xi] < epsilon1
    assert tls.E_mat[yi + 1, xi] > epsilon1

    # Test with precise parameters and compare against hard-coded reference values
    epsilon2 = 0.02
    tls.target_settings.target.x0 = 0.0
    tls.target_settings.target.y0 = -0.5
    tls.bracket_target_bias()
    tls.optimize(
        epsilon2,
        fit_kind='pf4',
        fraction=0.05,
        Gs=Gs_N200_M7,
        W_num=4,
        sigma_num=4,
        sigma_max=0.1,
        W_resolution=0.04,
        S_resolution=0.03,
        bias_order=2,
        bias_mix=0.1,
        max_rounds=5
    )
    W_mat_ref = array([[0.        , 0.03333333, 0.05      , 0.06666667, 0.08333333,
        0.1       , 0.13333333, 0.26666667, 0.4       ],
       [0.        , 0.03333333, 0.05      , 0.06666667, 0.08333333,
        0.1       , 0.13333333, 0.26666667, 0.4       ],
       [0.        , 0.03333333, 0.05      , 0.06666667, 0.08333333,
        0.1       , 0.13333333, 0.26666667, 0.4       ],
       [0.        , 0.03333333, 0.05      , 0.06666667, 0.08333333,
        0.1       , 0.13333333, 0.26666667, 0.4       ],
       [0.        , 0.03333333, 0.05      , 0.06666667, 0.08333333,
        0.1       , 0.13333333, 0.26666667, 0.4       ],
       [0.        , 0.03333333, 0.05      , 0.06666667, 0.08333333,
        0.1       , 0.13333333, 0.26666667, 0.4       ],
       [0.        , 0.03333333, 0.05      , 0.06666667, 0.08333333,
        0.1       , 0.13333333, 0.26666667, 0.4       ]])
    S_mat_ref = array([[0.        , 0.        , 0.        , 0.        , 0.        ,
        0.        , 0.        , 0.        , 0.        ],
       [0.00416667, 0.00416667, 0.00416667, 0.00416667, 0.00416667,
        0.00416667, 0.00416667, 0.00416667, 0.00416667],
       [0.00833333, 0.00833333, 0.00833333, 0.00833333, 0.00833333,
        0.00833333, 0.00833333, 0.00833333, 0.00833333],
       [0.01666667, 0.01666667, 0.01666667, 0.01666667, 0.01666667,
        0.01666667, 0.01666667, 0.01666667, 0.01666667],
       [0.03333333, 0.03333333, 0.03333333, 0.03333333, 0.03333333,
        0.03333333, 0.03333333, 0.03333333, 0.03333333],
       [0.06666667, 0.06666667, 0.06666667, 0.06666667, 0.06666667,
        0.06666667, 0.06666667, 0.06666667, 0.06666667],
       [0.1       , 0.1       , 0.1       , 0.1       , 0.1       ,
        0.1       , 0.1       , 0.1       , 0.1       ]])
    E_mat_ref = array([[2.84214378e-08, 9.74160492e-04, 2.29013839e-03, 4.15589777e-03,
        6.62269595e-03, 9.75803681e-03, 1.80738365e-02, 8.56891567e-02,
        1.46457902e-01],
       [1.46426994e-04, 1.43040779e-02, 1.32620992e-02, 1.36510644e-02,
        1.50965237e-02, 1.73877488e-02, 2.42851402e-02, 8.88637116e-02,
        1.51254491e-01],
       [1.46427174e-04, 2.73929755e-02, 2.32308153e-02, 2.22803510e-02,
        2.28551136e-02, 2.44477965e-02, 3.02454969e-02, 9.19655926e-02,
        1.56091583e-01],
       [1.46427264e-04, 6.77506399e-02, 4.66200451e-02, 4.03298486e-02,
        3.78851767e-02, 3.78528092e-02, 4.12646656e-02, 9.80147118e-02,
        1.65847135e-01],
       [1.46427309e-04, 1.18549950e-01, 1.19761343e-01, 1.06232489e-01,
        9.95015527e-02, 7.27409379e-02, 6.57040426e-02, 1.10380286e-01,
        1.84973665e-01],
       [1.46427331e-04, 1.48034491e-01, 1.65064058e-01, 1.93926446e-01,
        2.06033895e-01, 2.10548751e-01, 2.16021568e-01, 1.40769507e-01,
        2.20791921e-01],
       [1.46427339e-04, 1.65205337e-01, 1.84635543e-01, 2.06487219e-01,
        2.33160315e-01, 2.62995798e-01, 2.88178058e-01, 1.77637809e-01,
        2.52814074e-01]])
    W_opt_ref = 0.06666666666666668
    sigma_opt_ref = 0.004166666666666667
    assert match_to_tol(tls.W_mat, W_mat_ref)
    assert match_to_tol(tls.S_mat, S_mat_ref)
    assert match_to_tol(tls.E_mat, E_mat_ref)
    assert match_to_tol(tls.W_opt, W_opt_ref)
    assert match_to_tol(tls.sigma_opt, sigma_opt_ref)
    assert tls.optimized

# end def
