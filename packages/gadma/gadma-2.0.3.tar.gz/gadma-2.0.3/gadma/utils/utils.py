from functools import wraps
import time
import numpy as np
import sys
import os
import tempfile
import pickle
from multiprocessing import Process, Queue, queues
import warnings
import copy
import math
import pandas
from .. import smac_available
from pathlib import Path
if smac_available:
    from smac.runhistory.runhistory import RunHistory
    from smac.tae import StatusType


def logarithm_transform(x):
    """
    Transforms ``x`` by applying ``numpy.log`` on it.
    """
    if isinstance(x, (int, float, np.integer, np.float64)):
        x = [x]
    if not isinstance(x, (list, np.ndarray)):
        return x
    x = np.array(x).astype(float)
    return np.log(x)


def _is_valid_for_log(variable):
    from .variables import ContinuousVariable, FractionVariable
    if not isinstance(variable, ContinuousVariable):
        return False
    zero_is_valid = (variable.correct_value(0) or
                     np.isclose(0, variable.domain[0]))
    return not isinstance(variable, FractionVariable) and not zero_is_valid


def apply_transform(variables, transform, x):
    """
    Applies transform to `x`. Usually is used for logarithm and exponential
    transforms. So value if `x` is transformed if it is float
    (ContinuousVariable) and does not have 0 in its domain.
    """
    if isinstance(x, list):
        x = np.array(x, dtype=get_correct_dtype(x))
    if transform == ident_transform:
        return x
    is_good = [var.log_transformed for var in variables]
    x_tr = WeightedMetaArray(x, dtype=get_correct_dtype(x))
    x_tr[is_good] = transform(x[is_good])
    # We should check float precision after transform
    for i, var in enumerate(variables):
        if var.log_transformed and hasattr(var, "_true_domain"):
            if np.isclose(x_tr[i], var._true_domain[0]):
                x_tr[i] = var._true_domain[0]
            if np.isclose(x_tr[i], var._true_domain[1]):
                x_tr[i] = var._true_domain[1]
    if isinstance(x, WeightedMetaArray):
        x_tr.metadata = x.metadata
    return x_tr


def exponent_transform(x):
    """
    Transforms ``x`` by applying ``numpy.exp`` on it.
    """
    if isinstance(x, (int, float, np.integer, np.float64)):
        x = [x]
    if not isinstance(x, (list, np.ndarray)):
        return x
    x = np.array(x).astype(float)
    return np.exp(x)


def ident_transform(x):
    """
    Identical transform. Just returns ``x``.
    """
    return x


def choose_by_weight(X, weights, nsample):
    """
    Choose ``nsample`` samples from ``X`` according to ``weights``.
    The greater weight is the greater the probability to choose sample is.

    :note: if weights is None then choice will be uniform
    """
    if weights is None:
        weights = np.ones(len(X))
    p = np.array(weights)
    p /= np.sum(p)
    return np.random.choice(X, size=nsample, replace=False)


def sort_by_other_list(x, y, reverse=False, key=None):
    """
    Sort ``x`` and ``y`` according to values in ``y``.
    """
    def ident(x):
        return x
    if key is None:
        key = ident
    sort_zip = sorted(zip(x, y), key=lambda p: key(p[1]), reverse=reverse)
    return [p[0] for p in sort_zip], [p[1] for p in sort_zip]


def fix_args(f, *args):
    r"""
    Fixes argumets of function.

    :param f: Function such that f(x, \*args)
    :param args: Tuple of function arguments.

    :returns: function that will take only x as argument.
    """
    @wraps(f)
    def fix_args_wrapper(x):
        return f(x, *args)
    return fix_args_wrapper


class CacheInfo(object):
    """
    Class for keeping cache info like one from ``functools.lru_cache``
    cache_info.
    """
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.cache = {}
        self.all_calls = []

    def __str__(self):
        return f"hits: {self.hits}, misses: {self.misses}"


def lru_cache(func):
    """
    Our lru cache. We want to get cache itself while functools.lru_cache
    could not do it.
    Please, be carefull as it could be some attributes named the same way
    and it will be ruined. We use it for our decorator :func:`cache_func`.
    """
    func.cache_info = CacheInfo()

    @wraps(func)
    def lru_cache_wrapper(*args):
        try:
            ret = func.cache_info.cache[args]
            func.cache_info.hits += 1
        except KeyError:
            ret = func(*args)
            func.cache_info.cache[args] = ret
            func.cache_info.misses += 1
        func.cache_info.all_calls.append([args, ret])
        return ret
    return lru_cache_wrapper


def cache_func(f, maxeval=None):
    """
    Cashes function with one argument.
    :param f: function such that f(x).
    :returns: function that is cashed.
    """
    @lru_cache
    @wraps(f)
    def tuple_wrapper(x_tuple):
        x_is_float = np.all([isinstance(el, float) for el in x_tuple])
        dtype = float if x_is_float else object
        return f(np.array(x_tuple, dtype=dtype))

    @wraps(tuple_wrapper)
    def cache_wrapper(x):
        if maxeval is not None and tuple_wrapper.cache_info.misses >= maxeval:
            return None
        try:
            return tuple_wrapper(tuple(x))
        except TypeError as e:
            warnings.warn(f"Error occurred during caching: {e}. "
                          f"Got vector {x} of type {type(x)}. Please, send "
                          f"this warning to ekaterina.e.noskova@gmail.com.")
            return f(x)

    cache_wrapper.cache_info = tuple_wrapper.cache_info
    return cache_wrapper


# def cache_func_2d(f):
#     """
#     Cashes function with two arguments.
#     :param f: function such that f(x, y).
#     :returns: function that is cashed.
#     """
#     @lru_cache
#     @wraps(f)
#     def tuple_wrapper(x_y_tuple):
#         x, y = x_y_tuple
#         if isinstance(y, tuple) and isinstance(y[0], tuple):
#             y = np.array(y)
#         return f(x, y)
#
#     @wraps(tuple_wrapper)
#     def cache_wrapper(x, y):
#         y_tuple = tuple(y)
#         if (isinstance(y, (list, np.ndarray)) and
#                 isinstance(y[0], (list, np.ndarray))):
#             for i in range(len(y_tuple)):
#                 y_tuple[i] = tuple(y_tuple[i])
#         return tuple_wrapper(tuple(x), y_tuple)
#
#     cache_wrapper.cache_info = tuple_wrapper.cache_info
#     return cache_wrapper


# def nan_fval_to_inf(f):
#     """
#     Wrappes function to return infinity instead nan.
#     """
#     @wraps(f)
#     def nan_fval_to_inf_wrapper(x):
#         y = f(x)
#         if y is None or np.isnan(y):
#             return np.inf
#         return y
#     return nan_fval_to_inf_wrapper


def eval_wrapper(f, eval_file=None):
    r"""
    Returns good function for optimization. Each evaluation of function will
    be written in file. If needed function will be cached.

    :param f: function. Is called as f(x, \*args).
    :param args: tuple of arguments.
    :param eval_file: file to write evaluations.
    :param cache: if True then function will be cached.
    """
    time_init = time.time()
    first_line = '\t'.join(['Time of evaluation start', 'Function value',
                            'Parameters values', 'Evaluation time'])
    if eval_file is not None:
        if not check_file_existence(eval_file):
            open(eval_file, 'w').close()
        if not os.stat(eval_file).st_size == 0:
            with open(eval_file, 'r') as fl:
                line = next(fl)
        if os.stat(eval_file).st_size == 0 or line.strip() != first_line:
            with open(eval_file, 'a') as fl:
                print(first_line, file=fl, sep='\t')

    @wraps(f)
    def eval_wrapper_f(x):
        time_start = time.time()
        y = f(x)
        time_end = time.time()
        if eval_file is not None:
            with open(eval_file, 'a') as fl:
                print(time_start - time_init, y, list(x),
                      time_end - time_start, file=fl, sep='\t')
        return y
    return eval_wrapper_f


def run_f_and_save_result_into_queue(f, queue, *args, **kwargs):
    """
    Runs f with args and kwargs and save the result of run into queue.
    """
    result = f(*args, **kwargs)
    queue.put(result)


def timeout(f, time):
    """
    Wraps function so that its execution time has limit of `time` seconds.
    The limitation is made via multiprocessing.Process.
    """

    @wraps(f)
    def timeout_wrapper(*args, **kwargs):
        q = Queue()
        p = Process(target=run_f_and_save_result_into_queue, name=f.__name__,
                    args=(f, q, *args), kwargs=kwargs)
        p.daemon = True
        p.start()
        p.join(time)
        if p.is_alive():
            p.terminate()
            p.join()
        try:
            return q.get(timeout=0.1)
        except queues.Empty:
            return None
    return timeout_wrapper


def get_correct_dtype(x):
    x_is_float = np.all([isinstance(el, float) for el in x])
    return float if x_is_float else object


class WeightedMetaArray(np.ndarray):
    """
    Array with metadata.

    :param array: array to keep.
    :param dtype: dtype of elements of the array.
    :param order: see ``numpy.ndarray`` for more information.
    """
    def __new__(cls, array, dtype=None, order=None):
        if dtype is None:
            dtype = get_correct_dtype(array)
        obj = np.asarray(np.array(array, dtype=get_correct_dtype(array)),
                         dtype=dtype, order=order).view(cls)
        obj.metadata = ""
        obj.weights = np.ones(obj.shape)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.metadata = getattr(obj, 'metadata', [{}]*(obj.ndim+1))
        self.weights = getattr(obj, 'weights', [{}]*(obj.ndim+1))

    def __str__(self):
        super_str = super(WeightedMetaArray, self).__str__()
        if hasattr(self, 'metadata'):
            return super_str + '\t' + self.metadata
        return super_str

    def str_as_list(self):
        super_str = str(list(self))
        if hasattr(self, 'metadata'):
            return super_str + '\t' + self.metadata
        return super_str

    def __repr__(self):
        super_str = super(WeightedMetaArray, self).__repr__()
        if hasattr(self, 'metadata'):
            return super_str + '\t' + self.metadata
        return super_str

#    def serialize(self):
#        return (self, self.weights, self.metadata)
#
#    def deserialize(self, data):
#        self = WeightedMetaArray(data[0])
#        self.weights = data[1]
#        self.metadata = data[2]


def serialize_meta_array(x):
    """
    Transforms ``x`` to pickle it.
    """
    if isinstance(x, WeightedMetaArray):
        return (x, x.weights, x.metadata)
    return x


def deserialize_meta_array(x):
    """
    Transforms back pickles version of ``x``.
    """
    if isinstance(x, tuple):
        arr = WeightedMetaArray(x[0])
        arr.weights = x[1]
        arr.metadata = x[2]
        return arr
    return x


def update_by_one_fifth_rule(value, const, was_improved):
    """
    Updates ``value`` according to 'one-fifth' rule and ``const``. Used in
    genetic algorithm.

    :param value: Value to change.
    :param const: Const for rule.
    :param was_improved: Bool if fitness was improved or not.
    """
    if was_improved:
        return value * const
    return value / (const) ** (0.25)


def abspath(path):
    return os.path.abspath(os.path.expanduser(path))


def check_file_existence(path_to_file):
    return os.path.exists(path_to_file) and os.path.isfile(path_to_file)


def check_dir_existence(path_to_dir):
    return os.path.exists(path_to_dir) and os.path.isdir(path_to_dir)


def ensure_file_existence(path_to_file):
    filename = abspath(path_to_file)
    if not check_file_existence(filename):
        open(filename, 'w').close()
    return filename


def ensure_dir_existence(path_to_dir, check_emptiness=False):
    dirname = abspath(path_to_dir)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if os.listdir(dirname) != [] and check_emptiness:
        raise RuntimeError(f"Directory {path_to_dir} is not empty\nYou can "
                           f"write:  rm -rf {dirname}\t to remove directory.")
    return dirname


def module_name_from_path(path):
    """
    Returns name for module that will be imported from given path.
    """
    # Remove \\ and : from windows path
    module_name = path.strip().replace("\\", ".").replace(":", ".")
    # Remove / from Linux path
    module_name = module_name.replace("/", ".")
    # Replace all .. with one . TODO replace all repeats with one dot.
    module_name = module_name.replace("..", ".")
    # Remove .py
    module_name.rstrip(".py")
    return module_name


def is_pickleable(obj):
    """
    Returns True if obj could be dumped with pickle.
    """
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'wb') as tmp:
            pickler = pickle.Pickler(tmp)
            pickler.dump(obj)
        return True
    except pickle.PicklingError:
        return False
    finally:
        os.remove(path)


class StdAndFileLogger(object):
    """
    Logger for printing output both in file and stdout.
    """
    def __init__(self, log_filename, silent=False, stderr=False):
        self.terminal = sys.stdout
        self.stderror = sys.stderr
        self.use_stderr = stderr
        self.log_filename = log_filename
        self.silent = silent
        if not os.path.exists(self.log_filename):
            open(self.log_filename, 'w'). close()

    def write(self, message):
        if not self.silent:
            if self.use_stderr:
                self.stderror.write(message)
                self.stderror.flush()
            else:
                self.terminal.write(message)
                self.terminal.flush()
        with open(self.log_filename, 'a') as fl:
            fl.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass


def get_aic_score(n_params, log_likelihood):
    """
    Returns AIC score.

    :param n_params: Number of parameters of model.
    :param log_likelihood: Value of log likelihood.
    """
    return 2 * n_params - 2 * log_likelihood


def get_claic_score(engine, x0, boots, args=(),
                    eps=1e-5, log_likelihood=None, return_eps=False):
    """
    Calculate CLAIC score for the model.

    :param engine: Engine with model and data.
    :param x0: Parameters of the model.
    :param boots: Bootstrap data.
    :params args: Arguments for engine's ``evaluate`` function.
    :params log_likelihood: Value of log-likelihood for ``x0``.
    :params return_eps: If True then tuple (CLAIC, eps) is returned.
    """
    if log_likelihood is None:
        log_likelihood = engine.evaluate(x0, *args)
    eps = min(eps, 1e-2)
    claic_score = None
    while eps <= 1e-2:
        try:
            claic_component = engine.get_claic_component(x0, boots,
                                                         *args, eps)
            claic_score = 2 * claic_component - 2 * log_likelihood
            break
        except np.linalg.linalg.LinAlgError as e:
            if str(e) == 'Singular matrix':
                eps *= 10
            else:
                print(e)
                raise e
        except Exception as e:
            raise e
    if return_eps:
        return claic_score, eps
    else:
        return claic_score


# Leave-one-out cross validation for Gaussian process
def get_mu_and_sigma_rassmusen(K_inv, Y, i):
    """
    Get mu and sigma for missed element i according to Rassmusen.

    :param K_inv: Inversed covariance matrix (cov(X, X)).
    :param Y: All objectives.
    :param i: Index of element that we exclude from X and Y.

    :returns: mean and std of GP prediction for i-th element if GP is trained\
              on all X and Y excluding i-th element.
    """
    mu = Y[i] - np.dot(K_inv, Y)[i] / K_inv[i, i]
    var = 1 / K_inv[i, i]
    sigma = math.sqrt(var)
    return mu, sigma


def get_one_score(mu, sigma, y_true):
    """
    Returns LOO score for excluding one element.
    """
    return - 1 / 2 * np.log(sigma) - (y_true - mu) ** 2 / (2 * sigma)\
           - 1 / 2 * np.log(2 * math.pi)


def get_LOO_score(X_train, Y_train, gp_model,
                  mode="rassmusen", verbose=False, do_optimize=True):
    assert mode in ["rassmusen", "gp_train"]
    # 1. Train full GP
    if verbose:
        print("Begin GP training")
    t_start = time.time()
    gp_model.train(X_train, Y_train, optimize=do_optimize)
    if verbose:
        print(f"Time of GP training: {time.time() - t_start}")
    # Hyperparameters of GP TODO
    if verbose:
        print(f"Hyperparameters of GP: {gp_model.get_hypers()}")
    # 2. Get inversed covariance matrix K
    noise = gp_model.get_noise()
    if verbose:
        print(f"Inverse covariance matrix (noise: {noise})")
    K = gp_model.get_K()
    K_noise = K + noise * np.eye(K.shape[0])
    K_inv = np.linalg.inv(K_noise)
    # 3. Begin cross validation
    t_start = time.time()
    if verbose:
        print("Begin cross validation pipeline.")
    LOO_score = 0
    for i, (x, y) in enumerate(zip(X_train, Y_train)):
        if mode == "rassmusen":
            mu, sigma = get_mu_and_sigma_rassmusen(K_inv, Y_train, i)
        else:
            except_i = [el for el in range(len(X_train)) if el != i]
            if hasattr(gp_model.gp_model, "normalize_y"):
                normalizaton = gp_model.gp_model.normalize_y
                gp_model.gp_model.normalize_y = False
            gp_model.train(
                np.array(X_train)[except_i, :],
                np.array(Y_train)[except_i],
                optimize=False
            )
            if hasattr(gp_model.gp_model, "normalize_y"):
                gp_model.gp_model.normalize_y = normalizaton

            mu, sigma = gp_model.predict([X_train[i]])
            mu, sigma = mu[0], sigma[0]
        if sigma < 0:
            if verbose:
                print(f"GP without {i} sample predicts sigma < 0")
            continue
        LOO_score += get_one_score(mu, sigma, Y_train[i])
        if verbose:
            print(f"GP without {i} sample predicts (mu={mu}, sigma={sigma}) "
                  f"when y_true={Y_train[i]}")
    if verbose:
        print(f"End cross validation pipeline ({time.time() - t_start} sec.).")
        print(f"LOO score: {LOO_score}")
    return LOO_score


def normalize(Y):
    Y = np.array(Y)
    Y -= np.mean(Y)
    sigma = np.std(Y)
    if sigma > 0:
        Y /= sigma
    return Y


def transform_smac(optimizer, variables, X, Y):
    from ..optimizers import SMACBayesianOptimizer
    from . import ContinuousVariable
    if not isinstance(optimizer, SMACBayesianOptimizer):
        return X, Y
    # We create run history, fill it and transform its data with rh2epm
    # It is usual pipeline for SMAC
    config_space = optimizer.get_config_space(variables=variables)
    rh2epm = optimizer.get_runhistory2epm(
        scenario=optimizer.get_scenario(
            maxeval=None,
            config_space=config_space
        )
    )
    runhistory = RunHistory()
    config = config_space.sample_configuration(1)
    for x, y in zip(X, Y):
        for var, value in zip(variables, x):
            if isinstance(var, ContinuousVariable):
                config[var.name] = float(value)
            else:
                config[var.name] = value
        runhistory.add(
            config=copy.copy(config),
            cost=y,
            time=0,
            status=StatusType.SUCCESS
        )
    X, Y = rh2epm.transform(runhistory)
    return X, Y.flatten()


def get_loo_score_for_optimizer(optimizer, variables, X, Y,
                                mode="rassmusen", verbose=False):
    """
    Optimizer has the correct kernel
    """
    from ..optimizers import GaussianProcess, SMACBayesianOptimizer
    # We transform X and Y if needed
    X, Y = transform_smac(optimizer, variables, X, Y)
    Y = normalize(Y)
    gp = optimizer.get_model(
        config_space=optimizer.get_config_space(variables)
    )
    assert isinstance(gp, GaussianProcess)
    return get_LOO_score(X_train=X, Y_train=Y, gp_model=gp,
                         mode=mode, verbose=verbose)


def get_loo_scores_for_kernels(
    optimizer,
    variables,
    X,
    Y,
    kernels=["matern52", "matern32", "rbf", "exponential"],
    mode="rassmusen",
    verbose=False
):
    assert hasattr(optimizer, "get_model")
    scores = {}
    opt = copy.copy(optimizer)
    for kernel_name in kernels:
        opt.kernel_name = kernel_name
        score = get_loo_score_for_optimizer(
            optimizer=opt,
            variables=variables,
            X=X,
            Y=Y,
            mode=mode,
            verbose=verbose
        )
        scores[kernel_name] = score
    return scores


def get_best_kernel(
    optimizer,
    variables,
    X,
    Y,
    kernels=["matern52", "matern32", "rbf", "exponential"],
    mode="rassmusen",
    verbose=False
):
    scores = get_loo_scores_for_kernels(
        optimizer=optimizer,
        variables=variables,
        X=X,
        Y=Y,
        kernels=kernels,
        mode=mode,
        verbose=verbose,
    )
    return max(scores, key=scores.get)


# Printing functions
def float_repr(value, precision=5):
    if value < 10**(-precision):
        return f"{value:.2e}"
    return f"{round(value, precision)}"


def variables_values_repr(variables, values):
    val_repr = [float_repr(val) if isinstance(val, float) else val
                for val in values]
    var_val = zip(variables, val_repr)
    x_repr = ",\t".join([f"{var.name}={val}" for var, val in var_val])
    x_repr = f"({x_repr})"
    return x_repr


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def warning_format(message, category, filename, lineno, file=None, line=None):
    return f"{bcolors.WARNING}{category.__name__}: {message}"\
           f"{bcolors.ENDC} ({filename}:{lineno})\n"
