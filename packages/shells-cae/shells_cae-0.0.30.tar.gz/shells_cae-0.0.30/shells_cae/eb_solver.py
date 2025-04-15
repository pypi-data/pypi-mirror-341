import cffi
import os
import numpy as np
import sys

from typing import Callable, TypedDict

import matplotlib.pyplot as plt

__all__ = ['PointMassTrajectorySolver', 'PointMassTrajectoryHSolver']


def load_lib():
    HERE = os.path.dirname(__file__)
    if sys.platform.startswith('linux'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "lib", "libsextbal.so"))
    elif sys.platform.startswith('win32'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "libsextbal.dll"))
    else:
        raise Exception('Неподдерживаемая платформа')
    ffi = cffi.FFI()

    ffi.cdef(
        '''
        void count_eb(double *y0, double d, double q, double *cx_list, double *mach_list, int n_mach,\n
        double max_distance, double tstep, double tmax);
        '''
    )
    ffi.cdef(
        '''
        void dense_count_eb(double *y_array, double d, double q, double *cx_list, double *mach_list, int n_mach,\n
        double max_distance, double tstep, double tmax, int *n_tsteps);
        '''
    )

    ffi.cdef(
        '''
        typedef struct shell{
        double d;
        double L;
        double q;
        double A;
        double B;
        double mu;
        double c_q;
        double h;
        } shell;
        '''
    )

    ffi.cdef(
        '''
        void dense_count_eb_h(
        double *y_array,
        double *cx_list, double *mach_list, int n_mach,
        shell *ashell,
        double *diag_vals,
        double eta,
        double sigma_dop,
        double delta_dop,
        double *sigma_array,
        double *delta_array,
        double max_distance,
        double tstep,
        double tmax,
        int *n_tsteps
        );
        '''
    )
    bal_lib = ffi.dlopen(LIB_FILE_NAME)
    return ffi, bal_lib


FFI, EBAL_LIB = load_lib()

G = 9.80665
rho0 = 1.226


def runge_kutta4_stepper(f, y0, t0, t_end, dt, args=tuple()):
    n = 0
    ys = y0.copy()
    while t0 < t_end:
        K1 = f(t0, ys, *args)
        K2 = f(t0 + 0.5 * dt, ys + dt * K1 / 2, *args)
        K3 = f(t0 + 0.5 * dt, ys + dt * K2 / 2, *args)
        K4 = f(t0 + dt, ys + dt * K3, *args)
        ys += dt * (K1 + 2 * K2 + 2 * K3 + K4) / 6
        t0 += dt
        n += 1
        yield n, t0, ys.copy()


@np.vectorize
def tau(y: float):
    '''
    Изменение виртуальной температуры с высотой НАА до 31 км
    :param y: Высота, м
    :return: Виртуальная температура, К
    '''
    if y < 9324:
        return 288.9 - 0.006328 * y
    elif 9300 <= y < 12000:
        return 230. - 0.006328 * (y - 9324.) + 0.0000011777 * (y - 9324.) ** 2
    elif y >= 12000:
        return 221.5


@np.vectorize
def a_zv(y: float):
    '''
    Функция изменения скорости звука с высотой НАА
    :param y: Высота, м
    :return: Скорость звука, м/с
    '''
    return 20.0478 * np.sqrt(tau(y))


@np.vectorize
def rho(y: float):
    '''
    Функция изменения плотности воздуха по НАА до высоты 31 км
    :param y:
    :return:
    '''

    if y < 11000:
        return 1.206 * (1. - (0.006328 * y) / tau(0.)) ** 4.3987363
    else:
        return 0.355 * np.exp(-0.000154235681 * (y - 11000))


class _ExternalBallistics3DSolver:
    X_IDX = 0
    Y_IDX = 1
    Z_IDX = 2
    VELOCITY_IDX = 3
    OMEGA_IDX = 4
    THETA_IDX = 5
    PSI_IDX = 6

    def __init__(self, q, d, L, A, B, v0, omega0, theta0, psi0,
                 cx: Callable, cya: Callable, mxwx: Callable, mza: Callable):

        self.q = q
        self.d = d
        self.L = L
        self.A = A
        self.B = B

        self.S = 0.25 * np.pi * d ** 2
        self.Y0 = np.zeros(7)

        self.Y0[self.X_IDX] = self.Y0[self.Y_IDX] = self.Y0[self.Z_IDX] = 0.
        self.Y0[self.THETA_IDX] = theta0
        self.Y0[self.PSI_IDX] = psi0
        self.Y0[self.OMEGA_IDX] = omega0
        self.Y0[self.VELOCITY_IDX] = v0

        self.cx = cx
        self.cya = cya
        self.mxwx = mxwx
        self.mza = mza

    def delta(self, y: np.ndarray):
        '''
        Функция определяющая зависимость угла нутации от параметров движения
        :param y: Вектор переменных интегрирования
        :param A: Осевой момент
        :param S: Площадь миделя
        :param L: Длина снаряда
        :param mza: Функция момента по оси Z от числа Маха
        :return: угол нутации
        '''

        v = y[self.VELOCITY_IDX]
        omega = y[self.OMEGA_IDX]
        theta = y[self.THETA_IDX]
        h = y[self.Y_IDX]

        mach = v / a_zv(h)
        rho_h = rho(h)

        res = (2 * self.A * omega) / (self.mza(mach) * rho_h * self.S * self.L)
        res *= G * np.cos(theta) / v ** 3

        return res

    def right_side(self, t: float, y: np.ndarray, *args):
        A = self.A
        S = self.S
        q = self.q
        L = self.L

        dy = np.zeros_like(y)
        v = y[self.VELOCITY_IDX]
        h = y[self.Y_IDX]
        theta = y[self.THETA_IDX]
        psi = y[self.PSI_IDX]

        rho_h = rho(h)
        _mach = v / a_zv(h)

        _delta = self.delta(y)

        dy[self.X_IDX] = v * np.cos(theta) * np.cos(psi)
        dy[self.Y_IDX] = v * np.sin(theta)
        dy[self.Z_IDX] = -v * np.cos(theta) * np.sin(psi)
        dy[self.OMEGA_IDX] = 0.5 * self.mxwx(_mach) * rho_h * v * v / A
        dy[self.OMEGA_IDX] *= S * y[self.OMEGA_IDX] * L ** 2 / v
        dy[self.THETA_IDX] = -G * np.cos(theta) / v
        dy[self.PSI_IDX] = -self.cya(_mach, _delta) * _delta / (np.cos(theta))
        dy[self.PSI_IDX] *= 0.5 * rho_h * v * S / q

        dy[self.VELOCITY_IDX] = -self.cx(_mach, _delta) * 0.5 * S * rho_h * v * v / q
        dy[self.VELOCITY_IDX] -= G * np.sin(theta)

        return dy

    def solve(self, t0=0., t_end=150, dt=0.1):
        hit_ground = lambda t, y, *args: y[self.Y_IDX]
        hit_ground.terminal = True
        hit_ground.direction = -1
        ys = [self.Y0]
        ts = [0]
        for n, ti, ui in runge_kutta4_stepper(self.right_side, self.Y0, t0, t_end, dt):
            if ui[self.Y_IDX] < 0:
                ys.append(ui)
                ts.append(ti)
                break
            ys.append(ui)
            ts.append(ti)

        ys = np.array(ys)
        ts = np.array(ts)
        ts[-1] = ts[-1] + (0. - ys[-2, 1]) * ((ts[-1] - ts[-2]) / (ys[-1, 1] - ys[-2, 1]))
        ys[-1] = ys[-2] + (0. - ys[-2, 1]) * ((ys[-1] - ys[-2]) / (ys[-1, 1] - ys[-2, 1]))
        ys = ys.T

        omega_array = ys[self.OMEGA_IDX]

        # Определение коэффициента гироскопической устойчивости
        A = self.A
        B = self.B
        S = self.S
        L = self.L
        cur_mach_array = ys[self.VELOCITY_IDX] / a_zv(ys[self.Y_IDX])
        sigma_array = np.sqrt(
            1 - (2 * self.mza(cur_mach_array) * B * ys[self.VELOCITY_IDX] ** 2 * rho(ys[self.Y_IDX]) * S * L) / (
                        A ** 2 * ys[self.OMEGA_IDX] ** 2))

        return dict(
            t_array=ts,
            x_array=ys[self.X_IDX],
            y_array=ys[self.Y_IDX],
            z_array=ys[self.Z_IDX],
            v_array=ys[self.VELOCITY_IDX],
            omega_array=ys[self.OMEGA_IDX],
            theta_array=ys[self.THETA_IDX],
            psi_array=np.rad2deg(ys[self.PSI_IDX]),
            delta_array=np.rad2deg(self.delta(ys)),
            sigma_array=sigma_array
        )


class ExternalBallistics3DData(TypedDict):
    q: float
    d: float
    L: float
    A: float
    B: float
    v0: float
    omega0: float
    theta0: float
    psi0: float
    cx: Callable
    cya: Callable
    mxwx: Callable
    mza: Callable


class ExternalBallistics3DSolver:
    name = 'external_ballistics_3d_solver'
    preprocessed_data: ExternalBallistics3DData = dict(
        q=None,
        d=None,
        L=None,
        A=None,
        v0=None,
        omega0=None,
        theta0=None,
        psi0=None,
        cx=None,
        cya=None,
        mxwx=None,
        mza=None
    )

    def preprocessor(self, data: dict, global_state: dict):
        v0 = data['initial_cond']['V']
        eta = data['gun_char']['eta_k']
        d = data['gun_char']['d']
        omega0 = (2 * np.pi * v0) / (eta * d)
        mach = global_state['spin73_solver']['mach']
        Cx = global_state['spin73_solver']['results']['Cx']
        Cx2 = global_state['spin73_solver']['results']['Cx2']
        Cya = np.array(global_state['spin73_solver']['results']['Cn']) - np.array(
            global_state['spin73_solver']['results']['Cx'])
        MxWx = global_state['spin73_solver']['results']['MxWx']
        Mza = global_state['spin73_solver']['results']['Mza']

        self.preprocessed_data['q'] = global_state['mcc_solver']['shell']['q']
        self.preprocessed_data['d'] = d
        self.preprocessed_data['L'] = global_state['geometry_solver']['L_all']
        self.preprocessed_data['A'] = global_state['mcc_solver']['shell']['A']
        self.preprocessed_data['B'] = global_state['mcc_solver']['shell']['B']
        self.preprocessed_data['v0'] = v0
        self.preprocessed_data['omega0'] = omega0
        self.preprocessed_data['theta0'] = data['initial_cond']['theta0']
        self.preprocessed_data['psi0'] = data['initial_cond']['psi0']
        self.preprocessed_data['cx'] = lambda _mach, _delta: np.interp(_mach, mach, Cx) + np.interp(_mach, mach,
                                                                                                    Cx2) * _delta ** 2
        self.preprocessed_data['cya'] = lambda _mach, _delta: np.interp(_mach, mach, Cya)
        self.preprocessed_data['mxwx'] = lambda _mach: np.interp(_mach, mach, MxWx)
        self.preprocessed_data['mza'] = lambda _mach: np.interp(_mach, mach, Mza)

    def run(self, data: dict, global_state: dict, t0=0., t_end=150, dt=0.1):
        true_solver = _ExternalBallistics3DSolver(
            q=self.preprocessed_data['q'],
            d=self.preprocessed_data['d'],
            L=self.preprocessed_data['L'],
            A=self.preprocessed_data['A'],
            B=self.preprocessed_data['B'],
            v0=self.preprocessed_data['v0'],
            omega0=self.preprocessed_data['omega0'],
            theta0=self.preprocessed_data['theta0'],
            psi0=self.preprocessed_data['psi0'],
            cx=self.preprocessed_data['cx'],
            cya=self.preprocessed_data['cya'],
            mxwx=self.preprocessed_data['mxwx'],
            mza=self.preprocessed_data['mza']
        )

        solution = true_solver.solve(t0=t0, t_end=t_end, dt=dt)
        global_state[ExternalBallistics3DSolver.name] = solution


class PointMassTrajectorySolver:
    mah_list = np.array([0.4, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6,
                         1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7,
                         2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6])

    cx_list = np.array([0.157, 0.158, 0.158, 0.160, 0.190, 0.325, 0.378, 0.385, 0.381, 0.371,
                        0.361, 0.351, 0.342, 0.332, 0.324, 0.316, 0.309, 0.303, 0.297,
                        0.292, 0.287, 0.283, 0.279, 0.277, 0.273, 0.270, 0.267, 0.265,
                        0.263, 0.263, 0.261, 0.260])

    name = 'point_mass_eb_solver'

    preprocess_data = dict(
        d=None,
        q=None,
        theta_angle=None,
        v0=None,
        cx_list=None,
        mach_list=None
    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocess_data['d'] = data['gun_char']['d']
        self.preprocess_data['q'] = global_state['mcc_solver']['shell']['q']
        self.preprocess_data['theta_angle'] = data['initial_cond']['theta0']
        self.preprocess_data['v0'] = data['initial_cond']['V']
        self.preprocess_data['cx_list'] = global_state['mcdrag_solver']['cx_list']
        self.preprocess_data['mach_list'] = global_state['mcdrag_solver']['mach_list']

    def run(self, data: dict, global_state: dict):
        eb_data = self.preprocess_data
        eb_settings = data['point_mass_eb_settings']

        v0 = eb_data['v0']
        theta_angle = eb_data['theta_angle']
        q = eb_data['q']
        d = eb_data['d']

        cx_list = eb_data['cx_list']
        mach_list = eb_data['mach_list']

        max_distance = eb_settings['max_distance']
        tstep = eb_settings['tstep']
        tmax = eb_settings['tmax']

        y0 = np.array([0., 0., v0, np.deg2rad(theta_angle)], dtype=np.float64, order='F')
        cx_list = np.asfortranarray(cx_list, dtype=np.float64)
        mach_list = np.asfortranarray(mach_list, dtype=np.float64)
        y0_ptr = FFI.cast("double*", y0.__array_interface__['data'][0])
        cx_list_ptr = FFI.cast("double*", cx_list.__array_interface__['data'][0])
        mach_list_ptr = FFI.cast("double*", mach_list.__array_interface__['data'][0])

        EBAL_LIB.count_eb(
            y0_ptr, d, q, cx_list_ptr, mach_list_ptr, len(cx_list),
            max_distance, tstep, tmax
        )

        global_state[PointMassTrajectorySolver.name] = dict(L_max=y0[0],
                                                            vc=y0[2])


class PointMassTrajectoryHSolver:
    name = 'point_mass_ebh_solver'

    preprocess_data = dict(
        d=None,
        L=None,
        q=None,
        A=None,
        B=None,
        h=None,
        mu=None,
        c_q=None,
        sigma_dop=0.6,
        delta_dop=2.,
        theta_angle=None,
        v0=None,
        cx_list=None,
        mach_list=None
    )

    def preprocessor(self, data: dict, global_state: dict):
        self.preprocess_data['d'] = data['gun_char']['d']
        self.preprocess_data['eta_k'] = data['gun_char']['eta_k']
        self.preprocess_data['q'] = global_state['mcc_solver']['shell']['q']
        self.preprocess_data['L'] = global_state['geometry_solver']['L_all']
        self.preprocess_data['A'] = global_state['mcc_solver']['shell']['A']
        self.preprocess_data['B'] = global_state['mcc_solver']['shell']['B']
        self.preprocess_data['h'] = global_state['mcc_solver']['shell']['h']
        self.preprocess_data['mu'] = global_state['mcc_solver']['shell']['mu']
        self.preprocess_data['c_q'] = global_state['mcc_solver']['shell']['c_q']
        self.preprocess_data['theta_angle'] = data['initial_cond']['theta0']
        self.preprocess_data['v0'] = data['initial_cond']['V']
        self.preprocess_data['cx_list'] = global_state['kontur_solver']['cx_list']
        self.preprocess_data['mach_list'] = global_state['kontur_solver']['mach_list']


    def _get_fortran_shell(self):
        ashell = FFI.new('shell *ashell')
        ashell[0].d = self.preprocess_data['d']
        ashell[0].q = self.preprocess_data['q']
        ashell[0].A = self.preprocess_data['A']
        ashell[0].B = self.preprocess_data['B']
        ashell[0].mu = self.preprocess_data['mu']
        ashell[0].c_q = self.preprocess_data['c_q']
        ashell[0].L = self.preprocess_data['L']
        ashell[0].h = self.preprocess_data['h']

        return ashell

    # Определение по диаграмме устойчивости правильность полёта
    def stability_define(self, m, n, eta_k, h, d, hd_kr, eta_kr):
        # Гироскопическая устойчивость
        h_d = h / d

        eta_list = [i / 1000 for i in range(100)]
        h_d_sigma_list = [(eta ** 2) * m for eta in eta_list]

        # Направленность полёта
        h_d_stab_list = [eta * n for eta in eta_list]

        # Определяем устойчив ли снаряд

        # ДОДЕЛАТЬ

    def run(self, data: dict, global_state: dict):
        ebh_settings = data['settings']['point_mass_eb']

        tstep = ebh_settings['tstep']
        tmax = ebh_settings['tmax']

        eta_k = self.preprocess_data['eta_k']

        ashell = self._get_fortran_shell()

        n_tsteps = FFI.new('int *')
        n_tsteps[0] = int(tmax / tstep)

        cx_list = self.preprocess_data['cx_list']
        mach_list = self.preprocess_data['mach_list']

        cx_list = np.asfortranarray(cx_list, dtype=np.float64)
        mach_list = np.asfortranarray(mach_list, dtype=np.float64)

        y_array = np.zeros((5, n_tsteps[0]), dtype=np.float64, order='F')
        y_array[:, 0] = [0., 0., self.preprocess_data['v0'], np.deg2rad(self.preprocess_data['theta_angle']), 0.0]

        sigma_array = np.zeros(n_tsteps[0], dtype=np.float64, order='F')
        delta_array = np.zeros(n_tsteps[0], dtype=np.float64, order='F')

        diag_vals_array = np.empty(4, dtype=np.float64, order='F')

        y_array_ptr = FFI.cast("double*", y_array.__array_interface__['data'][0])
        cx_list_ptr = FFI.cast("double*", cx_list.__array_interface__['data'][0])
        mach_list_ptr = FFI.cast("double*", mach_list.__array_interface__['data'][0])
        sigma_array_ptr = FFI.cast("double*", sigma_array.__array_interface__['data'][0])
        delta_array_ptr = FFI.cast("double*", delta_array.__array_interface__['data'][0])
        diag_vals_array_ptr = FFI.cast("double*", diag_vals_array.__array_interface__['data'][0])

        EBAL_LIB.dense_count_eb_h(
            y_array_ptr,
            cx_list_ptr, mach_list_ptr, len(cx_list),
            ashell,
            diag_vals_array_ptr,
            eta_k,
            self.preprocess_data['sigma_dop'],
            np.deg2rad(self.preprocess_data['delta_dop']),
            sigma_array_ptr,
            delta_array_ptr,
            ebh_settings['max_distance'],
            tstep,
            tmax,
            n_tsteps
        )

        # Диаграмма устойчивости
        self.stability_define(m=diag_vals_array[0], n=diag_vals_array[1], eta_k=eta_k,
                              h=global_state['mcc_solver']['shell']['h'], d=data['shell_size']['d'],
                              hd_kr=diag_vals_array[2], eta_kr=diag_vals_array[3])

        t_s = np.linspace(0., tstep * n_tsteps[0], n_tsteps[0])
        y_array = y_array[:, :n_tsteps[0]]
        sigma_array = sigma_array[:n_tsteps[0]]
        delta_array = delta_array[:n_tsteps[0]]
        y_array[3] = np.rad2deg(y_array[3])

        global_state[PointMassTrajectoryHSolver.name] = dict(
            m=diag_vals_array[0],
            n=diag_vals_array[1],
            hd_kr=diag_vals_array[2],
            eta_kr=diag_vals_array[3],
            L_max=y_array[0, -1],
            vc=y_array[2, -1],
            t_array=t_s,
            x_array=y_array[0],
            y_array=y_array[1],
            v_array=y_array[2],
            theta_array=y_array[3],
            omega_array=y_array[4],
            sigma_array=sigma_array,
            delta_array=delta_array
        )


if __name__ == '__main__':
    y = np.linspace(0, 30000, 100)
    x = rho(y)

    plt.plot(y, x)
    plt.grid()
    plt.show()







