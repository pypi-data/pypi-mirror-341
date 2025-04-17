from ..data import DataHolder
from ..models import Model
import copy

_registered_engines = {}


def register_engine(engine):
    """
    Registers the specified engine of the demographic inference.

    :raises ValueError: if engine with the same ``id`` was already\
                        registered.
    """
    if engine.id in _registered_engines:
        raise ValueError(f"Engine of the demographic inference '{engine.id}'"
                         f" already registered.")
    _registered_engines[engine.id] = engine


def get_engine(id):
    """
    Returns the engine of the demographic inference with the specified id.

    :raises ValueError: if engine with such ``id`` was not registered.
    """
    if id not in _registered_engines:
        raise ValueError(f"Engine of the demographic inference '{id}'"
                         f" not registered")
    return _registered_engines[id]()


def all_engines():
    """
    Returns an iterator over all registered engines of the demographic
    inference that can evaluate log-likelihood.
    """
    for engine in _registered_engines.values():
        if engine.can_evaluate:
            yield engine()


def all_available_engines():
    """
    Returns an iterator over all registered engines
    for the demographic inference.
    """
    for engine in _registered_engines.values():
        yield engine()


def all_simulation_engines():
    """
    Returns an iterator over all registered engines that can simulate
    log-likelihood for the demographic inference.
    """
    for engine in _registered_engines.values():
        if engine.can_simulate:
            yield engine()


def all_drawing_engines():
    """
    Returns an iterator over all registered engines that can draw
    plots for the demographic inference.
    """
    for engine in _registered_engines.values():
        if engine.can_draw_model:
            yield engine()


class Engine(object):
    """
    Abstract class representing an engine of the demographic inference.

    New engine should be inherited from this class.
    Engine must have at least the ``id``, ``supported_models``,
    ``supported_data`` and ``inner_data`` attributes, and
    implementations of :func:`read_data`
    and :func:`evaluate` functions of this abstract class.

    :cvar str Engine.id: the unique identifier of the engine.
    :cvar Engine.supported_models: list of supported :class:`Model` classes.
    :cvar Engine.supported_data: list of supported :class:`DataHolder` classes.
    :cvar Engine.inner_data_type: class of inner data that is used by engine.
    """
    id = ''
    supported_models = []
    supported_data = []
    inner_data_type = None

    can_evaluate = False  # evaluate value of similarity between model and data
    can_draw_model = False  # draw picture of the demographic history
    can_draw_comp = False  # draw comparison of simulated and real data
    can_simulate = False  # simulate data from proposed demographic history

    def __init__(self, data=None, model=None):
        self.data = data
        self.model = model

    @staticmethod
    def get_value_from_var2value(var2value, entity):
        return Model.get_value_from_var2value(var2value, entity)

    @classmethod
    def read_data(cls, data_holder):
        """
        Reads data from `data_holder.filename` in inner type.

        :param data_holder: Holder of data to read.
        :type data_holder: :class:`gadma.DataHolder`

        :returns: data which was read
        :rtype: ``Engine.inner_data_type``
        """
        if data_holder.__class__ not in cls.supported_data:
            raise ValueError(f"Data class {data_holder.__class__.__name__}"
                             f" is not supported by {cls.id} engine.\nThe "
                             f"supported classes are: {cls.supported_data}"
                             f" and {cls.inner_data_type}")
        return cls._read_data(data_holder)

    @classmethod
    def _read_data(cls, data_holder):
        """
        Inner method to read data_holder.
        """
        raise NotImplementedError

    def set_model(self, model):
        """
        Sets new model for the engine.

        :param model: new model.
        :type model: :class:`Model`

        :raises ValueError: when model is not supported by engine.
        """
        if model is None:
            self._model = None
            # in moments and dadi it is used to save thetas
            self.saved_add_info = {}
            return
        is_supported = False
        for cls in self.supported_models:
            if issubclass(model.__class__, cls):
                is_supported = True
        if not is_supported:
            raise ValueError(f"Model {model.__class__} is not supported "
                             f"by {self.id} engine.\nThe supported models"
                             f" are: {self.supported_models}.")
        self._model = model
        self.saved_add_info = {}

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self.set_model(model)

    def set_data(self, data):
        """
        Sets new data for the engine.

        :param data: new data.
        :type data: :class:`DataHolder` or ``inner_data_type``.

        :raises ValueError: when ``data`` is not supported by the engine.
        """
        if data is None:
            self.data_holder = None
            self.inner_data = None
            self.saved_add_info = {}
            return
        cls = data.__class__
        if self.supported_data is not None and \
                cls not in self.supported_data and \
                not isinstance(data, self.inner_data_type):
            try:
                transformed_data = self.inner_data_type(data)
                self.set_data(transformed_data)
            except:  # NOQA
                raise ValueError(f"Data class {cls} is "
                                 f"not supported by {self.id} engine.\n"
                                 f"The supported classes are: "
                                 f"{self.supported_data} and "
                                 f"{self.inner_data_type}")
        if isinstance(data, DataHolder):
            self.inner_data = self.read_data(data)
            self.data_holder = copy.deepcopy(data)
            self.update_data_holder_with_inner_data()
        elif (self.inner_data_type is not None and
                isinstance(data, self.inner_data_type)):
            self.inner_data = data
            self.data_holder = None
        self.saved_add_info = {}

    def update_data_holder_with_inner_data(self):
        raise NotImplementedError

    @property
    def data(self):
        return self.inner_data

    @data.setter
    def data(self, new_data):
        self.set_data(new_data)

    def get_N_ancestral(self, values):
        """
        Returns size of ancestral population. Is implemented for models with
        ancestral size as parameter. For dadi and moments it is not always
        True.
        """
        if hasattr(self.model, "has_anc_size") and self.model.has_anc_size:
            var2value = self.model.var2value(values)
            return self.model.get_value_from_var2value(var2value,
                                                       self.model.Nanc_size)
        raise NotImplementedError

    def evaluate(self, values, **options):
        """
        Evaluation of the objective function of the engine.

        :param values: values of variables of setted demographic model.
        """
        raise NotImplementedError

    def set_and_evaluate(self, values, model, data, options={}):
        """
        Sets model and data for the engine instance and evaluates the
        objective function via calling :func:`evaluate`.

        :param values: values of variables of the demographic model.
        :param model: model.
        :type model: class from :attr:``supported_models``
        :param data: holder of the data or raw data for the engine.
        :type data: :class:`gadma.DataHolder` or :attr:``inner_data``

        :raises ValueError: if `model` is `None` and any was not\
            set before; or if `data_holder` is `None` and any\
            was not set before.
        """
        if model is not None:
            self.set_model(model)
        if data is not None:
            self.set_data(data)
        if self.model is None:
            raise ValueError("Please set model for engine or pass it as "
                             "argument to function.")
        if self.data is None:
            raise ValueError("Please set data for engine or pass it as "
                             "argument to function.")

        return self.evaluate(values, **options)

    def generate_code(self, values, filename=None, nanc=None,
                      gen_time=None, gen_time_units="years"):
        """
        Prints nice formatted code in the format of engine to file or returns
        it as string if no file is set.

        :param values: values for the engine's model.
        :param filename: file to print code. If None then the string will
                         be returned.
        """
        raise NotImplementedError
