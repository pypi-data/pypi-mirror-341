#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Abstracted FLAME beam state class.
"""

import flame
import logging
import numpy as np

from flame_utils.misc import is_zeros_states
from flame_utils.misc import machine_setter
from flame_utils.misc import alias

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016-2017, Facility for Rare Isotope beams, " \
                "Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"


_LOGGER = logging.getLogger(__name__)

DUMMY_LAT = {'sim_type':'MomentMatrix',
                'elements':[{'name':'mk', 'type':'marker'}]}
DUMMY_MACHINE = flame.Machine(DUMMY_LAT)

KEY_MAPPING = {
        'IonChargeStates': 'IonZ',
        'IonEk': 'ref_IonEk',
        'IonEs': 'ref_IonEs',
        'NCharge': 'IonQ',
}

c0 = 2.99792458e8 # m/s

@alias
class BeamState(object):
    """FLAME beam state, from which simulated results could be retrieved.

   Class attributes of reference beam parameter:

    .. autosummary ::
        pos
        ref_beta
        ref_bg
        ref_gamma
        ref_IonEk
        ref_IonEs
        ref_IonQ
        ref_IonW
        ref_IonZ
        ref_phis
        ref_SampleIonK
        ref_Brho


   Class attributes of actual beam parameter:

    .. autosummary ::
        beta
        bg
        gamma
        IonEk
        IonEs
        IonQ
        IonW
        IonZ
        phis
        SampleIonK
        Brho
        moment0
        moment0_rms
        moment0_env
        moment1
        moment1_env
        xcen
        xrms
        xpcen
        xprms
        ycen
        yrms
        ypcen
        yprms
        zcen
        zrms
        zpcen
        zprms
        xcen_all
        xrms_all
        xpcen_all
        xprms_all
        ycen_all
        yrms_all
        ypcen_all
        yprms_all
        zcen_all
        zrms_all
        zpcen_all
        zprms_all
        xemittance
        xnemittance
        yemittance
        ynemittance
        zemittance
        znemittance
        xemittance_all
        xnemittance_all
        yemittance_all
        ynemittance_all
        zemittance_all
        znemittance_all
        xtwiss_beta
        xtwiss_alpha
        xtwiss_gamma
        ytwiss_beta
        ytwiss_alpha
        ytwiss_gamma
        ztwiss_beta
        ztwiss_alpha
        ztwiss_gamma
        xtwiss_beta_all
        xtwiss_alpha_all
        xtwiss_gamma_all
        ytwiss_beta_all
        ytwiss_alpha_all
        ytwiss_gamma_all
        ztwiss_beta_all
        ztwiss_alpha_all
        ztwiss_gamma_all
        couple_xy
        couple_xpy
        couple_xyp
        couple_xpyp
        couple_xy_all
        couple_xpy_all
        couple_xyp_all
        couple_xpyp_all
        last_caviphi0
        transfer_matrix

    Configuration methods

    .. autosummary ::
        clone
        set_twiss
        get_twiss
        set_couple
        get_couple

    Parameters
    ----------
    s :
        FLAME state object Created by `allocState()`
    bmstate :
        BeamState object, priority: high
    machine :
        FLAME machine object, priority: middle
    latfile :
        FLAME lattice file name, priority: low

    Notes
    -----
    -   If more than one keyword parameters are provided,
        the selection policy follows the priority from high to low.

    -   If only ``s`` is assigned with all-zeros states (usually created by
        ``allocState({})`` method), then please note that this state can only
        propagate from the first element, i.e. ``SOURCE``
        (``from_element`` parameter of ``run()`` or ``propagate()`` should be 0),
        or errors happen; the better initialization should be passing one of
        keyword parameters of ``machine`` and ``latfile`` to initialize the
        state to be significant for the ``propagate()`` method.

    -   1. These attributes are only valid for the case of ``sim_type`` being
           defined as ``MomentMatrix``, which is de facto the exclusive option
           used at FRIB.
        2. If the attribute is an array, new array value should be assigned
           instead of by element indexing way, e.g.

        >>> bs = BeamState(s)
        >>> print(bs.moment0)
        array([[ -7.88600000e-04],
                [  1.08371000e-05],
                [  1.33734000e-02],
                [  6.67853000e-06],
                [ -1.84773000e-04],
                [  3.09995000e-04],
                [  1.00000000e+00]])
        >>> # the right way to just change the first element of the array
        >>> m_tmp = bs.moment0
        >>> m_tmp[0] = 0
        >>> bs.moment0 = m_tmp
        >>> print(bs.moment0)
        array([[  0.00000000e+00],
                [  1.08371000e-05],
                [  1.33734000e-02],
                [  6.67853000e-06],
                [ -1.84773000e-04],
                [  3.09995000e-04],
                [  1.00000000e+00]])
        >>> # while this way does not work: ms.moment0[0] = 0
    """
    _aliases = {
        'xcen_all': 'x0',
        'ycen_all': 'y0',
        'xpcen_all': 'xp0',
        'ypcen_all': 'yp0',
        'zcen_all': 'phi0',
        'zpcen_all': 'dEk0',
        'phicen_all': 'phi0',
        'dEkcen_all': 'dEk0',
        'xrms': 'x0_rms',
        'yrms': 'y0_rms',
        'xprms': 'xp0_rms',
        'yprms': 'yp0_rms',
        'zrms': 'phi0_rms',
        'zprms': 'dEk0_rms',
        'phirms': 'phi0_rms',
        'dEkrms': 'dEk0_rms',
        'zrms_all': 'phirms_all',
        'zprms_all': 'dEkrms_all',
        'xcen': 'x0_env',
        'ycen': 'y0_env',
        'xpcen': 'xp0_env',
        'ypcen': 'yp0_env',
        'zcen': 'phi0_env',
        'zpcen': 'dEk0_env',
        'phicen': 'phi0_env',
        'dEkcen': 'dEk0_env',
        'cenvector': 'moment0_env',
        'cenvector_all': 'moment0',
        'rmsvector': 'moment0_rms',
        'beammatrix_all': 'moment1',
        'beammatrix': 'moment1_env',
        'transmat': 'transfer_matrix',
        'xeps': 'xemittance',
        'yeps': 'yemittance',
        'zeps': 'zemittance',
        'xeps_all': 'xemittance_all',
        'yeps_all': 'yemittance_all',
        'zeps_all': 'zemittance_all',
        'xepsn': 'xnemittance',
        'yepsn': 'ynemittance',
        'zepsn': 'znemittance',
        'xepsn_all': 'xnemittance_all',
        'yepsn_all': 'ynemittance_all',
        'zepsn_all': 'znemittance_all',
        'xtwsb': 'xtwiss_beta',
        'ytwsb': 'ytwiss_beta',
        'ztwsb': 'ztwiss_beta',
        'xtwsb_all': 'xtwiss_beta_all',
        'ytwsb_all': 'ytwiss_beta_all',
        'ztwsb_all': 'ztwiss_beta_all',
        'xtwsa': 'xtwiss_alpha',
        'ytwsa': 'ytwiss_alpha',
        'ztwsa': 'ztwiss_alpha',
        'xtwsa_all': 'xtwiss_alpha_all',
        'ytwsa_all': 'ytwiss_alpha_all',
        'ztwsa_all': 'ztwiss_alpha_all',
        'xtwsg': 'xtwiss_gamma',
        'ytwsg': 'ytwiss_gamma',
        'ztwsg': 'ztwiss_gamma',
        'xtwsg_all': 'xtwiss_gamma_all',
        'ytwsg_all': 'ytwiss_gamma_all',
        'ztwsg_all': 'ztwiss_gamma_all',
        'cxy': 'couple_xy',
        'cxpy': 'couple_xpy',
        'cxyp': 'couple_xyp',
        'cxpyp': 'couple_xpyp',
        'cxy_all': 'couple_xy_all',
        'cxpy_all': 'couple_xpy_all',
        'cxyp_all': 'couple_xyp_all',
        'cxpyp_all': 'couple_xpyp_all',
    }
    def __init__(self, s=None, **kws):
        _bmstate = kws.get('bmstate', None)
        _machine = kws.get('machine', None)
        _latfile = kws.get('latfile', None)
        self._states = None

        if s is None:
            if _bmstate is not None:
                self.state = _bmstate
            else:
                _m = machine_setter(_latfile, _machine, 'BeamState')
                if _m is not None:
                    self._states = _m.allocState({})
        else:
            self._states = s

        if self._states is not None:
            if is_zeros_states(self._states):
                _m = machine_setter(_latfile, _machine, 'BeamState')
                if _m is not None:
                    _m.propagate(self._states, 0, 1)
                else:
                    _LOGGER.warning(
                    "BeamState: " \
                     "Zeros initial states, get true values by " \
                     "parameter '_latfile' or '_machine'.")

        self.dm = DUMMY_MACHINE

    @property
    def state(self):
        """flame._internal.State: FLAME state object, also could be
        initialized with BeamState object"""
        return self._states

    @state.setter
    def state(self, s):
        if isinstance(s, flame._internal.State):
            self._states = s.clone()
        elif isinstance(s, BeamState):
            self._states = s.clone().state

    @property
    def pos(self):
        """float: longitudinally propagating position, [m]"""
        return getattr(self._states, 'pos')

    @pos.setter
    def pos(self, x):
        setattr(self._states, 'pos', x)

    @property
    def ref_beta(self):
        """float: speed in the unit of light velocity in vacuum of reference
        charge state, Lorentz beta, [1]"""
        return getattr(self._states, 'ref_beta')

    @ref_beta.setter
    def ref_beta(self, x):
        setattr(self._states, 'ref_beta', x)
        ref_IonEk = _get_ek_from_beta(x, self.ref_IonEs)
        self.set_IonEk(ref_IonEk = ref_IonEk)

    @property
    def ref_bg(self):
        """float: multiplication of beta and gamma of reference charge state, [1]"""
        return getattr(self._states, 'ref_bg')

    @ref_bg.setter
    def ref_bg(self, x):
        setattr(self._states, 'ref_bg', x)
        ref_beta = 1.0/np.sqrt(1.0+1.0/x/x)
        ref_IonEk = _get_ek_from_beta(ref_beta, self.ref_IonEs)
        self.set_IonEk(ref_IonEk = ref_IonEk)

    @property
    def ref_gamma(self):
        """float: relativistic energy of reference charge state, Lorentz gamma, [1]"""
        return getattr(self._states, 'ref_gamma')

    @ref_gamma.setter
    def ref_gamma(self, x):
        setattr(self._states, 'ref_gamma', x)
        ref_beta = np.sqrt(1.0-1.0/x/x)
        ref_IonEk = _get_ek_from_beta(ref_beta, self.ref_IonEs)
        self.set_IonEk(ref_IonEk = ref_IonEk)

    @property
    def ref_IonEk(self):
        """float: kinetic energy of reference charge state, [eV/u]
        """
        return getattr(self._states, 'ref_IonEk')

    @ref_IonEk.setter
    def ref_IonEk(self, x):
        self.set_IonEk(ref_IonEk = x)

    @property
    def ref_IonEs(self):
        """float: rest energy of reference charge state, [eV/u]
        """
        return getattr(self._states, 'ref_IonEs')

    @ref_IonEs.setter
    def ref_IonEs(self, x):
        setattr(self._states, 'ref_IonEs', x)
        self.dm.propagate(self.state)

    @property
    def ref_IonQ(self):
        """int: macro particle number of reference charge state, [1]
        """
        return getattr(self._states, 'ref_IonQ')

    @ref_IonQ.setter
    def ref_IonQ(self, x):
        setattr(self._states, 'ref_IonQ', x)
        self.dm.propagate(self.state)

    @property
    def ref_IonW(self):
        """float: total energy of reference charge state, [eV/u],
        i.e. :math:`W = E_s + E_k`"""
        return getattr(self._states, 'ref_IonW')

    @ref_IonW.setter
    def ref_IonW(self, x):
        setattr(self._states, 'ref_IonW', x)
        self.set_IonEk(ref_IonEk = x-self.ref_IonEs)

    @property
    def ref_IonZ(self):
        """float: reference charge to mass ratio,
        e.g. :math:`^{33^{+}}_{238}U: Q(33)/A(238)`, [Q/A]"""
        return getattr(self._states, 'ref_IonZ')

    @ref_IonZ.setter
    def ref_IonZ(self, x):
        setattr(self._states, 'ref_IonZ', x)

    @property
    def ref_phis(self):
        """float: absolute synchrotron phase of reference charge state,
        [rad]"""
        return getattr(self._states, 'ref_phis')

    @ref_phis.setter
    def ref_phis(self, x):
        setattr(self._states, 'ref_phis', x)
        for i, v in enumerate(self.phis):
            self.set_moment0('z', position=v-x, cs=i)

    @property
    def ref_SampleIonK(self):
        """float: wave-vector in cavities with different beta values of
        reference charge state, [rad]"""
        return getattr(self._states, 'ref_SampleIonK')

    @property
    def ref_SampleFreq(self):
        """float: sampling frequency of reference charge state, [Hz]"""
        return getattr(self._states, 'ref_SampleFreq')

    @ref_SampleFreq.setter
    def ref_SampleFreq(self, x):
        setattr(self._states, 'ref_SampleFreq', x)
        self.dm.propagate(self.state)

    @property
    def ref_Brho(self):
        """float: magnetic rigidity of reference charge state, [Tm]"""
        return get_brho(self.ref_IonEk, self.ref_IonZ, self.ref_IonEs)

    @ref_Brho.setter
    def ref_Brho(self, x):
        ref_IonEk = _get_ek_from_brho(x, self.ref_IonZ, self.ref_IonEs)
        self.set_IonEk(ref_IonEk = ref_IonEk)

    @property
    def beta(self):
        """Array: speed in the unit of light velocity in vacuum of all charge
        states, Lorentz beta, [1]"""
        return getattr(self._states, 'beta')

    @beta.setter
    def beta(self, x):
        setattr(self._states, 'beta', x)
        IonEk = _get_ek_from_beta(x, self.IonEs)
        self.set_IonEk(IonEk = IonEk)

    @property
    def bg(self):
        """Array: multiplication of beta and gamma of all charge states, [1]"""
        return getattr(self._states, 'bg')

    @bg.setter
    def bg(self, x):
        setattr(self._states, 'bg', x)
        beta = 1.0/np.sqrt(1.0+1.0/x/x)
        IonEk = _get_ek_from_beta(beta, self.IonEs)
        self.set_IonEk(IonEk = IonEk)

    @property
    def gamma(self):
        """Array: relativistic energy of all charge states, Lorentz gamma, [1]"""
        return getattr(self._states, 'gamma')

    @gamma.setter
    def gamma(self, x):
        setattr(self._states, 'gamma', x)
        beta = np.sqrt(1.0-1.0/x/x)
        IonEk = _get_ek_from_beta(beta, self.IonEs)
        self.set_IonEk(IonEk = IonEk)

    @property
    def IonEk(self):
        """Array: kinetic energy of all charge states, [eV/u]"""
        return getattr(self._states, 'IonEk')

    @IonEk.setter
    def IonEk(self, x):
        setattr(self._states, 'IonEk', x)
        self.set_IonEk(IonEk = x)

    @property
    def IonEs(self):
        """Array: rest energy of all charge states, [eV/u]"""
        return getattr(self._states, 'IonEs')

    @IonEs.setter
    def IonEs(self, x):
        setattr(self._states, 'IonEs', x)
        self.dm.propagate(self.state)

    @property
    def IonQ(self):
        """Array: macro particle number of all charge states

        Notes
        -----
        This is what ``NCharge`` means in the FLAME lattice file.
        """
        return getattr(self._states, 'IonQ')

    @IonQ.setter
    def IonQ(self, x):
        setattr(self._states, 'IonQ', x)
        self.dm.propagate(self.state)

    @property
    def IonW(self):
        """Array: total energy of all charge states, [eV/u],
        i.e. :math:`W = E_s + E_k`"""
        return getattr(self._states, 'IonW')

    @IonW.setter
    def IonW(self, x):
        setattr(self._states, 'IonW', x)
        self.set_IonEk(IonEk = x-self.IonEs)

    @property
    def IonZ(self):
        """Array: all charge to mass ratios

        Notes
        -----
        This is what ``IonChargeStates`` means in the FLAME lattice file.
        """
        return getattr(self._states, 'IonZ')

    @IonZ.setter
    def IonZ(self, x):
        setattr(self._states, 'IonZ', x)

    @property
    def phis(self):
        """Array: absolute synchrotron phase of all charge states, [rad]"""
        return getattr(self._states, 'phis')

    @phis.setter
    def phis(self, x):
        setattr(self._states, 'phis', x)
        for i, v in enumerate(x):
            self.set_moment0('z', position=v-self.ref_phis, cs=i)

    @property
    def SampleIonK(self):
        """Array: wave-vector in cavities with different beta values of all
        charge states, [rad]"""
        return getattr(self._states, 'SampleIonK')

    @property
    def SampleFreq(self):
        """Array: sampling frequency of all charge states, [Hz]"""
        return getattr(self._states, 'SampleFreq')

    @SampleFreq.setter
    def SampleFreq(self, x):
        setattr(self._states, 'SampleFreq', x)
        self.dm.propagate(self.state)

    @property
    def Brho(self):
        """float: magnetic rigidity of reference charge state, [Tm]"""
        return get_brho(self.IonEk, self.IonZ, self.IonEs)

    @Brho.setter
    def Brho(self, x):
        IonEk = _get_ek_from_brho(x, self.IonZ, self.IonEs)
        self.set_IonEk(IonEk = IonEk)

    @property
    def moment0_env(self):
        """Array: weight average of centroid for all charge states, array of
        ``[x, x', y, y', phi, dEk, 1]``, with the units of
        ``[mm, rad, mm, rad, rad, MeV/u, 1]``.

        Notes
        -----
        The physics meanings for each column are:

        - ``x``: x position in transverse plane;
        - ``x'``: x divergence;
        - ``y``: y position in transverse plane;
        - ``y'``: y divergence;
        - ``phi``: longitudinal beam length, measured in RF frequency;
        - ``dEk``: kinetic energy deviation w.r.t. reference charge state;
        - ``1``: should be always 1, for the convenience of handling
          corrector (i.e. ``orbtrim`` element)
        """
        return getattr(self._states, 'moment0_env')

    @property
    def moment0_rms(self):
        """Array: rms beam envelope, part of statistical results from
        ``moment1``.

        Notes
        -----
        The square of ``moment0_rms`` should be equal to the diagonal
        elements of ``moment1``.

        See Also
        --------
        moment1 : covariance matrices of all charge states
        """
        return getattr(self._states, 'moment0_rms')

    @property
    def moment0(self):
        """Array: centroid for all charge states, array of
        ``[x, x', y, y', phi, dEk, 1]``"""
        return getattr(self._states, 'moment0')

    @moment0.setter
    def moment0(self, x):
        setattr(self._states, 'moment0', x)

    @property
    def moment1(self):
        r"""Array: covariance matrices of all charge states, for each charge
        state, the covariance matrix could be written as:

        .. math::

          \begin{array}{ccccccc}
              \color{red}{\left<x \cdot x\right>} & \left<x \cdot x'\right> & \left<x \cdot y\right> & \left<x \cdot y'\right> & \left<x \cdot \phi\right> & \left<x \cdot \delta E_k\right> & 0 \\
              \left<x'\cdot x\right> & \color{red}{\left<x'\cdot x'\right>} & \left<x'\cdot y\right> & \left<x'\cdot y'\right> & \left<x'\cdot \phi\right> & \left<x'\cdot \delta E_k\right> & 0 \\
              \left<y \cdot x\right> & \left<y \cdot x'\right> & \color{red}{\left<y \cdot y\right>} & \left<y \cdot y'\right> & \left<y \cdot \phi\right> & \left<y \cdot \delta E_k\right> & 0 \\
              \left<y'\cdot x\right> & \left<y'\cdot x'\right> & \left<y'\cdot y\right> & \color{red}{\left<y'\cdot y'\right>} & \left<y'\cdot \phi\right> & \left<y'\cdot \delta E_k\right> & 0 \\
              \left<\phi \cdot x\right> & \left<\phi \cdot x'\right> & \left<\phi \cdot y\right> & \left<\phi \cdot y'\right> & \color{red}{\left<\phi \cdot \phi\right>} & \left<\phi \cdot \delta E_k\right> & 0 \\
              \left<\delta E_k  \cdot x\right> & \left<\delta E_k  \cdot x'\right> & \left<\delta E_k  \cdot y\right> & \left<\delta E_k  \cdot y'\right> & \left<\delta E_k  \cdot \phi\right> & \color{red}{\left<\delta E_k  \cdot \delta E_k\right>} & 0 \\
              0                    & 0                     & 0                    & 0                     & 0                       & 0                      & 0
          \end{array}
        """
        return getattr(self._states, 'moment1')

    @moment1.setter
    def moment1(self, x):
        setattr(self._states, 'moment1', x)

    @property
    def moment1_env(self):
        """Array: averaged covariance matrices of all charge states"""
        return getattr(self._states, 'moment1_env')

    @property
    def x0(self):
        """Array: x centroid for all charge states, [mm]"""
        return self._states.moment0[0]

    @x0.setter
    def x0(self, x):
        if x.shape == self.x0.shape:
            for i, v in enumerate(x):
                self.set_moment0('x', position=v, cs=i)
        else:
            raise ValueError('input shape {} does not match to the original shape {}'.format(x.shape, self.x0.shape))

    @property
    def xp0(self):
        """Array: x centroid divergence for all charge states, [rad]"""
        return self._states.moment0[1]

    @xp0.setter
    def xp0(self, x):
        if x.shape == self.xp0.shape:
            for i, v in enumerate(x):
                self.set_moment0('x', momentum=v, cs=i)
        else:
            raise ValueError('input shape {} does not match to the original shape {}'.format(x.shape, self.xp0.shape))

    @property
    def y0(self):
        """Array: y centroid for all charge states, [mm]"""
        return self._states.moment0[2]

    @y0.setter
    def y0(self, x):
        if x.shape == self.y0.shape:
            for i, v in enumerate(x):
                self.set_moment0('y', position=v, cs=i)
        else:
            raise ValueError('input shape {} does not match to the original shape {}'.format(x.shape, self.y0.shape))

    @property
    def yp0(self):
        """Array: y centroid divergence for all charge states, [rad]"""
        return self._states.moment0[3]

    @yp0.setter
    def yp0(self, x):
        if x.shape == self.yp0.shape:
            for i, v in enumerate(x):
                self.set_moment0('y', momentum=v, cs=i)
        else:
            raise ValueError('input shape {} does not match to the original shape {}'.format(x.shape, self.yp0.shape))

    @property
    def phi0(self):
        """Array: longitudinal beam length, measured in RF frequency for all
        charge states, [rad]"""
        return self._states.moment0[4]

    @phi0.setter
    def phi0(self, x):
        if x.shape == self.phi0.shape:
            for i, v in enumerate(x):
                self.set_moment0('z', position=v, cs=i)
        else:
            raise ValueError('input shape {} does not match to the original shape {}'.format(x.shape, self.phi0.shape))

    @property
    def dEk0(self):
        """Array: kinetic energy deviation w.r.t. reference charge state,
        for all charge states, [MeV/u]"""
        return self._states.moment0[5]

    @dEk0.setter
    def dEk0(self, x):
        if x.shape == self.dEk0.shape:
            for i, v in enumerate(x):
                self.set_moment0('z', momentum=v, cs=i)
        else:
            raise ValueError('input shape {} does not match to the original shape {}'.format(x.shape, self.dEk0.shape))

    @property
    def x0_env(self):
        """float: weight average of all charge states for :math:`x`, [mm]"""
        return self._states.moment0_env[0]

    @x0_env.setter
    def x0_env(self, x):
        if isinstance(x, (int, float)):
            for i in range(len(self.x0)) :
                self.set_moment0('x', position=x, cs=i)
        else:
            raise ValueError('input type should be a float.')

    @property
    def xp0_env(self):
        """float: weight average of all charge states for :math:`x'`, [rad]"""
        return self._states.moment0_env[1]

    @xp0_env.setter
    def xp0_env(self, x):
        if isinstance(x, (int, float)):
            for i in range(len(self.xp0)) :
                self.set_moment0('x', momentum=x, cs=i)
        else:
            raise ValueError('input type should be a float.')

    @property
    def y0_env(self):
        """float: weight average of all charge states for :math:`y`, [mm]"""
        return self._states.moment0_env[2]

    @y0_env.setter
    def y0_env(self, x):
        if isinstance(x, (int, float)):
            for i in range(len(self.y0)) :
                self.set_moment0('y', position=x, cs=i)
        else:
            raise ValueError('input type should be a float.')

    @property
    def yp0_env(self):
        """float: weight average of all charge states for :math:`y'`, [rad]"""
        return self._states.moment0_env[3]

    @yp0_env.setter
    def yp0_env(self, x):
        if isinstance(x, (int, float)):
            for i in range(len(self.yp0)) :
                self.set_moment0('y', momentum=x, cs=i)
        else:
            raise ValueError('input type should be a float.')

    @property
    def phi0_env(self):
        """float: weight average of all charge states for :math:`\phi`,
        [rad]"""
        return self._states.moment0_env[4]

    @phi0_env.setter
    def phi0_env(self, x):
        if isinstance(x, (int, float)):
            for i in range(len(self.phi0)) :
                self.set_moment0('z', position=x, cs=i)
        else:
            raise ValueError('input type must be a float.')

    @property
    def dEk0_env(self):
        """float: weight average of all charge states for :math:`\delta E_k`,
        [MeV/u]"""
        return self._states.moment0_env[5]

    @dEk0_env.setter
    def dEk0_env(self, x):
        if isinstance(x, (int, float)):
            for i in range(len(self.dEk0)) :
                self.set_moment0('z', momentum=x, cs=i)
        else:
            raise ValueError('input type must be a float.')

    @property
    def xrms_all(self):
        """Array: general rms beam envelope for :math:`x` of all charge states, [mm]"""
        return np.sqrt(self._states.moment1[0, 0, :])

    @property
    def xprms_all(self):
        """Array: general rms beam envelope for :math:`x'` of all charge states, [rad]"""
        return np.sqrt(self._states.moment1[1, 1, :])

    @property
    def yrms_all(self):
        """Array: general rms beam envelope for :math:`y` of all charge states, [mm]"""
        return np.sqrt(self._states.moment1[2, 2, :])

    @property
    def yprms_all(self):
        """Array: general rms beam envelope for :math:`y'` of all charge states, [rad]"""
        return np.sqrt(self._states.moment1[3, 3, :])

    @property
    def phirms_all(self):
        """Array: general rms beam envelope for :math:`\phi` of all charge states, [rad]"""
        return np.sqrt(self._states.moment1[4, 4, :])

    @property
    def dEkrms_all(self):
        """Array: general rms beam envelope for :math:`\delta E_k` of all charge states, [MeV/u]"""
        return np.sqrt(self._states.moment1[5, 5, :])

    @property
    def x0_rms(self):
        """float: general rms beam envelope for :math:`x`, [mm]"""
        return self._states.moment0_rms[0]

    @property
    def xp0_rms(self):
        """float: general rms beam envelope for :math:`x'`, [rad]"""
        return self._states.moment0_rms[1]

    @property
    def y0_rms(self):
        """float: general rms beam envelope for :math:`y`, [mm]"""
        return self._states.moment0_rms[2]

    @property
    def yp0_rms(self):
        """float: general rms beam envelope for :math:`y'`, [rad]"""
        return self._states.moment0_rms[3]

    @property
    def phi0_rms(self):
        """float: general rms beam envelope for :math:`\phi`, [rad]"""
        return self._states.moment0_rms[4]

    @property
    def dEk0_rms(self):
        """float: general rms beam envelope for :math:`\delta E_k`, [MeV/u]"""
        return self._states.moment0_rms[5]

    @property
    def last_caviphi0(self):
        """float: Last RF cavity's driven phase, [deg]"""
        try:
            ret = self._states.last_caviphi0
        except AttributeError:
            print("python-flame version should be at least 1.1.1")
            ret = None
        return ret

    @property
    def transfer_matrix(self):
        """Array: Transfer matrix of the last element"""
        return self._states.transmat

    def clone(self):
        """Return a copy of Beamstate object.
        """
        return BeamState(self._states.clone())

    def __repr__(self):
        try:
            moment0_env = ','.join(["{0:.6g}".format(i) for i in self.moment0_env])
            return "BeamState: moment0 mean=[7]({})".format(moment0_env)
        except AttributeError:
            return "Incompleted initializaion."

    @property
    def xemittance(self):
        """float: weight average of geometrical x emittance, [mm-mrad]"""
        return np.sqrt(np.linalg.det(self._states.moment1_env[0:2, 0:2]))*1e3

    @property
    def yemittance(self):
        """float: weight average of geometrical y emittance, [mm-mrad]"""
        return np.sqrt(np.linalg.det(self._states.moment1_env[2:4, 2:4]))*1e3

    @property
    def zemittance(self):
        """float: weight average of geometrical z emittance, [rad-MeV/u]"""
        return np.sqrt(np.linalg.det(self._states.moment1_env[4:6, 4:6]))

    @property
    def xemittance_all(self):
        """Array: geometrical x emittance of all charge states, [mm-mrad]"""
        return np.array([np.sqrt(np.linalg.det(self._states.moment1[0:2, 0:2, i]))*1e3 for i in range(len(self.bg))])

    @property
    def yemittance_all(self):
        """Array: geometrical y emittance of all charge states, [mm-mrad]"""
        return np.array([np.sqrt(np.linalg.det(self._states.moment1[2:4, 2:4, i]))*1e3 for i in range(len(self.bg))])

    @property
    def zemittance_all(self):
        """Array: geometrical z emittance of all charge states, [rad-MeV/u]"""
        return np.array([np.sqrt(np.linalg.det(self._states.moment1[4:6, 4:6, i])) for i in range(len(self.bg))])

    @property
    def xnemittance(self):
        """float: weight average of normalized x emittance, [mm-mrad]"""
        return self.ref_bg*self.xeps

    @property
    def ynemittance(self):
        """float: weight average of normalized y emittance, [mm-mrad]"""
        return self.ref_bg*self.yeps

    @property
    def znemittance(self):
        """float: weight average of normalized z emittance, [rad-MeV/u]"""
        return self.ref_bg*self.zeps

    @property
    def xnemittance_all(self):
        """Array: normalized x emittance of all charge states, [mm-mrad]"""
        return self.ref_bg*self.xeps_all

    @property
    def ynemittance_all(self):
        """Array: normalized y emittance of all charge states, [mm-mrad]"""
        return self.ref_bg*self.yeps_all

    @property
    def znemittance_all(self):
        """Array: normalized z emittance of all charge states, [rad-MeV/u]"""
        return self.ref_bg*self.zeps_all

    @property
    def xtwiss_beta(self):
        """float: weight average of twiss beta x, [m/rad]"""
        return self._states.moment1_env[0, 0]/self.xeps

    @property
    def ytwiss_beta(self):
        """float: weight average of twiss beta y, [m/rad]"""
        return self._states.moment1_env[2, 2]/self.yeps

    @property
    def ztwiss_beta(self):
        """float: weight average of twiss beta z, [rad/MeV/u]"""
        return self._states.moment1_env[4, 4]/self.zeps

    @property
    def xtwiss_beta_all(self):
        """Array: twiss beta x of all charge states, [m/rad]"""
        return self._states.moment1[0, 0, :]/self.xeps_all

    @property
    def ytwiss_beta_all(self):
        """Array: twiss beta y of all charge states, [m/rad]"""
        return self._states.moment1[2, 2, :]/self.yeps_all

    @property
    def ztwiss_beta_all(self):
        """Array: twiss beta z of all charge states, [rad/MeV/u]"""
        return self._states.moment1[4, 4, :]/self.zeps_all

    @property
    def xtwiss_alpha(self):
        """float: weight average of twiss alpha x, [1]"""
        return -self._states.moment1_env[0, 1]/self.xeps*1e3

    @property
    def ytwiss_alpha(self):
        """float: weight average of twiss alpha y, [1]"""
        return -self._states.moment1_env[2, 3]/self.yeps*1e3

    @property
    def ztwiss_alpha(self):
        """float: weight average of twiss alpha z, [1]"""
        return -self._states.moment1_env[4, 5]/self.zeps

    @property
    def xtwiss_alpha_all(self):
        """Array: twiss alpha x of all charge states, [1]"""
        return -self._states.moment1[0, 1, :]/self.xeps_all*1e3

    @property
    def ytwiss_alpha_all(self):
        """Array: twiss alpha y of all charge states, [1]"""
        return -self._states.moment1[2, 3, :]/self.yeps_all*1e3

    @property
    def ztwiss_alpha_all(self):
        """Array: twiss alpha z of all charge states, [1]"""
        return -self._states.moment1[4, 5, :]/self.zeps_all

    @property
    def xtwiss_gamma(self):
        """float: weight average of twiss gamma x, [rad/m]"""
        return (1.0 + self.xtwiss_alpha**2)/self.xtwiss_beta

    @property
    def ytwiss_gamma(self):
        """float: weight average of twiss gamma y, [rad/m]"""
        return (1.0 + self.ytwiss_alpha**2)/self.ytwiss_beta

    @property
    def ztwiss_gamma(self):
        """float: weight average of twiss gamma z, [MeV/u/rad]"""
        return (1.0 + self.ztwiss_alpha**2)/self.ztwiss_beta

    @property
    def xtwiss_gamma_all(self):
        """Array: twiss gamma x of all charge states, [rad/m]"""
        return (1.0 + self.xtwiss_alpha_all**2)/self.xtwiss_beta_all

    @property
    def ytwiss_gamma_all(self):
        """Array: twiss gamma y of all charge states, [rad/m]"""
        return (1.0 + self.ytwiss_alpha_all**2)/self.ytwiss_beta_all

    @property
    def ztwiss_gamma_all(self):
        """Array: twiss gamma z of all charge states, [MeV/u/rad]"""
        return (1.0 + self.ztwiss_alpha_all**2)/self.ztwiss_beta_all

    @property
    def couple_xy(self):
        """float: weight average of normalized x-y coupling term, [1]"""
        return self.get_couple('x', 'y', cs=-1)

    @property
    def couple_xpy(self):
        """float: weight average of normalized xp-y coupling term, [1]"""
        return self.get_couple('xp', 'y', cs=-1)

    @property
    def couple_xyp(self):
        """float: weight average of normalized x-yp coupling term, [1]"""
        return self.get_couple('x', 'yp', cs=-1)

    @property
    def couple_xpyp(self):
        """float: weight average of normalized xp-yp coupling term, [1]"""
        return self.get_couple('xp', 'yp', cs=-1)

    @property
    def couple_xy_all(self):
        """Array: normalized x-y coupling term of all charge states, [1]"""
        return np.array([self.get_couple('x', 'y', cs=i) for i in range(len(self.bg))])

    @property
    def couple_xpy_all(self):
        """Array: normalized xp-y coupling term of all charge states, [1]"""
        return np.array([self.get_couple('xp', 'y', cs=i) for i in range(len(self.bg))])

    @property
    def couple_xyp_all(self):
        """Array: normalized x-yp coupling term of all charge states, [1]"""
        return np.array([self.get_couple('x', 'yp', cs=i) for i in range(len(self.bg))])

    @property
    def couple_xpyp_all(self):
        """Array: normalized xp-yp coupling term of all charge states, [1]"""
        return np.array([self.get_couple('xp', 'yp', cs=i) for i in range(len(self.bg))])

    def set_IonEk(self, IonEk=None, ref_IonEk=None):
        """Set longitudinal parameters based on reference/actual enargy

        Parameters
        ----------
        IonEk : Array
            Kinetic energy of all charge state, [eV/u]
        ref_IonEk : float
            kinetic energy of reference charge state, [eV/u]

        Note
        ----
        `moment0` will be updated based by the input energy
        """
        if IonEk is not None:
            if self._states.IonEk.shape != IonEk.shape:
                raise ValueError('input shape {} does not match to the original shape {}'.format(
                    self._states.IonEk.shape, IonEk.shape))
            setattr(self._states, 'IonEk', IonEk)
        if ref_IonEk is not None:
            if isinstance(ref_IonEk, (int, float)):
                setattr(self._states, 'ref_IonEk', ref_IonEk)
            else:
                raise ValueError('input type must be a float.')
        for i, v in enumerate(self.IonEk):
            self.set_moment0('z', momentum=(v-self.ref_IonEk)*1e-6, cs=i)
        self.dm.propagate(self.state)

    def set_moment0(self, coor, position=None, momentum=None, cs=0):
        """Set moment0 vector based on the centroid information

        Parameters
        ----------
        coor : str
            Coordinate of the twiss parameter, 'x', 'y', or 'z'.
        position : float
            Centroid position of the phase space, [mm] of 'x' and 'y', [rad] for 'z'.
        momentum : float
            Centroid momentum of the phase space, [rad] of 'x' and 'y', '[MeV/u] for 'z'.
        cs : int
            Index of the charge state to set parameter.

        Notes
        -----
        'z momentum' means the energy deviation from the reference energy.
        """
        if coor == 'x':
            idx = [0, 1]
        elif coor == 'y':
            idx = [2, 3]
        elif coor == 'z':
            idx = [4, 5]
        else:
            _LOGGER.error("Invalid coordinate type. It must be 'x', 'y', or 'z'.")
            return None

        vec = self._states.moment0

        if position is None:
            position = vec[idx[0], cs]

        if momentum is None:
            momentum = vec[idx[1], cs]

        vec[idx[0], cs] = position
        vec[idx[1], cs] = momentum

        self._states.moment0 = vec

        if coor == 'z':
            phis = self._states.phis
            phis[cs] = self._states.ref_phis + position
            self._states.phis = phis

            ek = self._states.IonEk
            ek[cs] = self._states.ref_IonEk + momentum*1e6
            self._states.IonEk = ek

        self.dm.propagate(self.state)

    def set_twiss(self, coor, alpha=None, beta=None, rmssize=None, emittance=None, nemittance=None, cs=0):
        """Set moment1 matrix by using Twiss parameter.

        Parameters
        ----------
        coor : str
            Coordinate of the twiss parameter,　'x', 'y', or 'z'.
        alpha : float
            Twiss alpha, [1].
        beta : float
            Twiss beta, [m/rad] for 'x' and 'y', [rad/MeV/u] for 'z'.
        rmssize : float
            RMS size of the real space, [mm] of 'x' and 'y', [rad] for 'z'.
        emittance : float
            Geometrical (Unnormalized) emittance, [mm-mrad] for 'x' and 'y', [rad-MeV/u] for 'z'.
        nemittance : float
            Normalized emittance, [mm-mrad] for 'x' and 'y', [rad-MeV/u] for 'z'.
        cs : int
            Index of the charge state to set parameter.

        Notes
        -----
        'nemittance' is ignored if both 'emittance' and 'nemittance' are input.
        """
        eps = emittance
        neps = nemittance
        if eps is None and neps is None:
            eps = getattr(self, coor + 'emittance_all')[cs]
        elif eps is not None and neps is not None:
            _LOGGER.warning("'nemittance' is ignored by 'emittance' input.")

        if eps is None:
            gam = 1.0 + self.ref_IonEk/self.ref_IonEs
            bg  = np.sqrt(gam*gam - 1.0)
            eps = neps/bg

        if beta is None and rmssize is None:
            beta = getattr(self, coor + 'twiss_beta_all')[cs]
        elif beta is None and rmssize is not None:
            beta = rmssize*rmssize/eps
        elif beta is not None and rmssize is None:
            beta = float(beta)
        else:
            _LOGGER.error("Invalid twiss input. It support to input only beta OR rmssize.")
            return None

        alpha = getattr(self, coor + 'twiss_alpha_all')[cs] if alpha is None else alpha

        mat = self._states.moment1
        mcs = mat[:, :, cs]
        mat[:, :, cs] = twiss_to_matrix(coor, alpha, beta, eps, matrix=mcs)
        self._states.moment1 = mat
        self.dm.propagate(self.state)

    def get_twiss(self, coor, cs=0):
        """Get twiss parameters of moment1 matrix

        Parameters
        ----------
        coor : str
            Coordinate of the twiss parameter,　'x', 'y', or 'z'.
        cs : int
            Index of the charge state (-1 for weight average of all charge states).

        Returns
        -------
        twiss : array
            Twiss [alpha, beta, gamma] of the beam.
        """

        if coor == 'x':
            if cs == -1:
                tws = np.array([self.xtwsa, self.xtwsb, self.xtwsg])
            else:
                tws = np.array([self.xtwsa_all[cs], self.xtwsb_all[cs], self.xtwsg_all[cs]])
        elif coor == 'y':
            if cs == -1:
                tws = np.array([self.ytwsa, self.ytwsb, self.ytwsg])
            else:
                tws = np.array([self.ytwsa_all[cs], self.ytwsb_all[cs], self.ytwsg_all[cs]])
        elif coor == 'z':
            if cs == -1:
                tws = np.array([self.ztwsa, self.ztwsb, self.ztwsg])
            else:
                tws = np.array([self.ztwsa_all[cs], self.ztwsb_all[cs], self.ztwsg_all[cs]])
        else:
            _LOGGER.error("Invalid coordinate type. It must be 'x', 'y', or 'z'.")
            return None

        return tws

    def get_couple(self, coor1, coor2, cs=0):
        """Get normalized coupling term of moment1 matrix

        Parameters
        ----------
        coor1 : str
            First coordinate of the coupling term, 'x', xp, 'y', 'yp', 'z', or 'zp'.
        coor2 : str
            Second coordinate of the coupling term, 'x', xp, 'y', 'yp', 'z', or 'zp'.
        cs : int
            Index of the charge state (-1 for weight average of all charge states).

        Returns
        -------
        term : float
            Normalized coupling term of ``coor1`` and ``coor2`` of ``cs``-th charge state.
        """
        if cs == -1:
            mat = self._states.moment1_env
        else:
            mat = self._states.moment1[:, :, cs]

        return get_couple(mat, coor1, coor2)

    def set_couple(self, coor1, coor2, value=0.0, cs = 0):
        """Set normalized coupling term of moment1 matrix

        Parameters
        ----------
        coor1 : str
            First coordinate of the coupling term, 'x', xp, 'y', 'yp', 'z', or 'zp'.
        coor2 : str
            Second coordinate of the coupling term, 'x', xp, 'y', 'yp', 'z', or 'zp'.
        value : float
            Normalized coupling term, (-1 ~ +1) [1].
        cs : int
            Index of the charge state.
        """
        mat = self._states.moment1
        mcs = mat[:, :, cs]
        mat[:, :, cs] = set_couple(mcs, coor1, coor2, value)
        self._states.moment1 = mat
        self.dm.propagate(self.state)

def generate_source(state, sconf=None):
    """Generate/Update FLAME source element from FLAME beam state object.

    Parameters
    ----------
    state :
        BeamState object, (also accept FLAME internal State object).
    sconf : dict
        Configuration of source element, if None, generate new one from state.

    Returns
    -------
    ret : dict
        FLAME source element configuration.

    Notes
    -----
    All zeros state may not produce reasonable result, for this case, the
    recommended way is to create a `BeamState` object with `latfile` or
    `machine` keyword parameter, e.g. `s = BeamState(s0, machine=m)`, then
    use `s` as the input of `generate_source`.

    See Also
    --------
    get_element : Get element from FLAME machine or lattice.
    """
    if sconf is not None:
        sconf_indx = sconf['index']
        sconf_prop = sconf['properties']

    else:
        sconf_indx = 0
        sconf_prop = {
                'name': 'S',
                'type': 'source',
                'matrix_variable': 'S',
                'vector_variable': 'P'
        }
    # update properties
    for k, v in KEY_MAPPING.items():
        sconf_prop[k] = getattr(state, v)
    # vector/matrix variables
    p = sconf_prop.get('vector_variable', None)
    s = sconf_prop.get('matrix_variable', None)
    for i in range(len(state.IonZ)):
        sconf_prop['{0}{1}'.format(p, i)] = state.moment0[:, i]
        sconf_prop['{0}{1}'.format(s, i)] = state.moment1[:, :, i].flatten()

    return {'index': sconf_indx, 'properties': sconf_prop}

def _get_ek_from_beta(beta, es):
    """Calculate kinetic energy [eV/u] from Lorentz beta"""
    return es/np.sqrt(1e0 - beta*beta) - es

def _get_ek_from_brho(brho, z, es):
    """Calculate kinetic energy [eV/u] from magnetic rigidity"""
    return np.sqrt(es*es + (brho*c0*z)**2) - es

def get_brho(k, z, es):
    """Get magnetic rigidity

    Parameters
    ----------
    k : float
        Kinetic energy [eV/u]
    z : float
        Charge to mass ratio, Q/A [1].
    es : float
        Rest energy [eV/u]

    Returns
    -------
    brho : float
        Magnetic rigidity [Tm].
    """
    gam = (k + es)/es
    bet = np.sqrt(1e0 - 1e0/gam/gam)
    brho = bet*(k + es)/(c0*z)
    return brho

def couple_index(coor1, coor2):
        """Get index from coordinate information"""
        crd = {'x': 0, 'xp': 1, 'y': 2, 'yp': 3, 'z': 4, 'zp': 5}

        if isinstance(coor1, str) and isinstance(coor2, str):
            if not coor1 in crd or not coor2 in crd:
                _LOGGER.error("Invalid coordinate type. It must be 'x', 'xp', 'y', 'yp', 'z', or 'zp'. ")
                return None

            c1 = crd[coor1]
            c2 = crd[coor2]
        else:
            c1 = int(coor1)
            c2 = int(coor2)

        if c1 == c2:
            _LOGGER.error("Invalid coordinate type. Combination of " + str(coor1) + " and " + str(coor2) + " is not coupling term.")
            return None

        return  c1, c2

def get_couple(matrix, coor1, coor2):
    """Get normalized coupling term of moment1 matrix

    Parameters
    ----------
    matrix : Array
        Covariance matrix of the beam.
    coor1 : str
        First Coordinate of the coupling term, 'x', xp, 'y', 'yp', 'z', or 'zp'.
    coor2 : str
        Second Coordinate of the coupling term, 'x', xp, 'y', 'yp', 'z', or 'zp'.

    Returns
    -------
    term : float
        Normalized coupling term of ``coor1`` and ``coor2`` of ``cs``-th charge state.
    """
    r = couple_index(coor1, coor2)
    if r is not None:
        c1, c2 = r
    else:
        return None
    mat = matrix
    fac = mat[c1, c1]*mat[c2, c2]
    term = mat[c1, c2]/np.sqrt(fac) if fac > 0.0 else 0.0

    return term

def set_couple(matrix, coor1, coor2, value=0.0):
        """Set normalized coupling term of moment1 matrix

        Parameters
        ----------
        matrix : Array
            Covariance matrix of the beam.
        coor1 : str
            First Coordinate of the coupling term, 'x', xp, 'y', 'yp', 'z', or 'zp'.
        coor2 : str
            Second Coordinate of the coupling term, 'x', xp, 'y', 'yp', 'z', or 'zp'.
        value : float
            Normalized coupling term, (-1 ~ +1) [1].
        """
        r = couple_index(coor1, coor2)
        if r is not None:
            c1, c2 = r
        else:
            return None

        mat = matrix
        fac = mat[c1, c1]*mat[c2, c2]
        term = value*np.sqrt(fac) if fac > 0.0 else 0.0
        mat[c1, c2] = mat[c2, c1] = term

        return mat

def twiss_to_matrix(coor, alpha, beta, emittance, matrix=None):
    """Set covariance matrix by using Twiss parameter.

    Parameters
    ----------
    coor : str
        Coordinate of the twiss parameter,　'x', 'y', or 'z'.
    alpha : float
        Twiss alpha, [1].
    beta : float
        Twiss beta, [m/rad] for 'x' and 'y', [rad/MeV/u] for 'z'.
    emittance : float
        Geometrical (Unnormalized) emittance, [mm-mrad] for 'x' and 'y', [rad-MeV/u] for 'z'.
    matrix : Array
        Original covariance matrix of the beam
    """
    eps = emittance
    if any(np.isnan([alpha, beta, eps] + np.isinf([alpha, beta, eps]))) or 0.0 in [beta, eps]:
        _LOGGER.warning("twiss_to_matrix: " \
                        "nan, inf, beta = 0, or emittance = 0 found in coor = " + coor + \
                        ", zero emittance beam is set.")
        alpha = 0.0
        beta = 1.0
        eps = 0.0

    mat = np.zeros([7, 7]) if matrix is None else matrix
    if coor == 'x':
        idx = [0, 1]
        jdx = [2, 3, 4, 5]
        cpt = [[get_couple(mat, i, j) for i in idx] for j in jdx]
        mat[0, 0] = beta*eps
        mat[0, 1] = mat[1, 0] = -alpha*eps*1e-3
        mat[1, 1] = (1.0 + alpha*alpha)/beta*eps*1e-6
    elif coor == 'y':
        idx = [2, 3]
        jdx = [0, 1, 4, 5]
        cpt = [[get_couple(mat, i, j) for i in idx] for j in jdx]
        mat[2, 2] = beta*eps
        mat[2, 3] = mat[3, 2] = -alpha*eps*1e-3
        mat[3, 3] = (1.0 + alpha*alpha)/beta*eps*1e-6
    elif coor == 'z':
        idx = [4, 5]
        jdx = [0, 1, 2, 3]
        cpt = [[get_couple(mat, i, j) for i in idx] for j in jdx]
        mat[4, 4] = beta*eps
        mat[4, 5] = mat[5, 4] = -alpha*eps
        mat[5, 5] = (1.0 + alpha*alpha)/beta*eps
    else:
        _LOGGER.error("Invalid coordinate type. It must be 'x', 'y', or 'z'.")
        return None

    for j, cp in zip(jdx, cpt):
        for i, v in zip(idx, cp):
            mat = set_couple(mat, i, j, v)

    return mat