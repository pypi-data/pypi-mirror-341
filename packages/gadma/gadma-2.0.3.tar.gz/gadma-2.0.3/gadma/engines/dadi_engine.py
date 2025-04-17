from . import register_engine
from .dadi_moments_common import DadiOrMomentsEngine
from ..models import CustomDemographicModel, Epoch, Split
from ..utils import DynamicVariable
from .. import SFSDataHolder, dadi_available
import numpy as np


class DadiEngine(DadiOrMomentsEngine):
    """
    Engine for using :py:mod:`dadi` for demographic inference.

    Citation of :py:mod:`dadi`:

    Gutenkunst RN, Hernandez RD, Williamson SH, Bustamante CD (2009)
    Inferring the Joint Demographic History of Multiple Populations
    from Multidimensional SNP Frequency Data. PLoS Genet 5(10): e1000695.
    https://doi.org/10.1371/journal.pgen.1000695
    """

    id = 'dadi'  #:
    extrapolation = "make_extrap_log_func"  #:
    if dadi_available:
        import dadi as base_module
        inner_data_type = base_module.Spectrum  #:

    @staticmethod
    def _get_kwargs(event, var2value):
        """
        Builds kwargs for dadi.Integration functions (one_pop, two_pops,
        three_pops).

        :param event: build for this event
        :type event: event.Epoch
        :param var2value: dictionary {variable: value}, it is required because
            the dynamics values should be fixed.
        """
        ret_dict = {'T': event.time_arg}
        for i in range(event.n_pop):
            if event.n_pop == 1:
                arg_name = 'nu'
            else:
                arg_name = 'nu%d' % (i + 1)

            if event.dyn_args is not None:
                dyn_arg = event.dyn_args[i]
                dyn = DadiEngine.get_value_from_var2value(var2value, dyn_arg)
                if dyn == 'Sud':
                    ret_dict[arg_name] = event.size_args[i]
                else:
                    ret_dict[arg_name] = 'nu%d_func' % (i + 1)
            else:
                ret_dict[arg_name] = event.size_args[i]

        if event.mig_args is not None:
            for i in range(event.n_pop):
                for j in range(event.n_pop):
                    if i == j:
                        continue
                    ret_dict['m%d%d' % (i + 1, j + 1)] = event.mig_args[i][j]
        if event.sel_args is not None:
            if event.n_pop == 1:
                arg_name = 'gamma'
            else:
                arg_name = 'gamma%d' % (i + 1)
            for i in range(event.n_pop):
                ret_dict[arg_name] = event.sel_args[i]
        if event.dom_args is not None:
            if event.n_pop == 1:
                arg_name = 'h'
            else:
                arg_name = 'h%d' % (i + 1)
            for i in range(event.n_pop):
                ret_dict[arg_name] = event.dom_args[i]
        return ret_dict

    def _inner_func(self, values, ns, pts):
        """
        Simulates expected SFS for proposed values of variables.

        :param values: values of variables
        :param ns: sample sizes of simulated SFS
        :param pts: grid points for numerical solution
        """
        var2value = self.model.var2value(values)

        if isinstance(self.model, CustomDemographicModel):
            values_list = [var2value[var] for var in self.model.variables]
            return self.model.function(values_list, ns, pts)

        dadi = self.base_module

        xx = dadi.Numerics.default_grid(pts)
        phi = dadi.PhiManip.phi_1D(xx)

        addit_values = {}
        for ind, event in enumerate(self.model.events):
            if isinstance(event, Epoch):
                if event.dyn_args is not None:
                    for i in range(event.n_pop):
                        dyn_arg = event.dyn_args[i]
                        value = self.get_value_from_var2value(var2value,
                                                              dyn_arg)
                        if value != 'Sud':
                            func = DynamicVariable.get_func_from_value(value)
                            y1 = self.get_value_from_var2value(
                                var2value, event.init_size_args[i])
                            y2 = self.get_value_from_var2value(
                                var2value, event.size_args[i])
                            x_diff = self.get_value_from_var2value(
                                var2value, event.time_arg)
                            addit_values['nu%d_func' % (i + 1)] = func(
                                y1=y1,
                                y2=y2,
                                x_diff=x_diff)
                kwargs_with_vars = self._get_kwargs(event, var2value)
                kwargs = {x: self.get_value_from_var2value(var2value, y)
                          for x, y in kwargs_with_vars.items()}
                kwargs = {x: addit_values.get(y, y)
                          for x, y in kwargs.items()}
                if event.n_pop == 1:
                    phi = dadi.Integration.one_pop(phi, xx, **kwargs)
                if event.n_pop == 2:
                    phi = dadi.Integration.two_pops(phi, xx, **kwargs)
                if event.n_pop == 3:
                    phi = dadi.Integration.three_pops(phi, xx, **kwargs)
            elif isinstance(event, Split):
                if event.n_pop == 1:
                    phi = dadi.PhiManip.phi_1D_to_2D(xx, phi)
                else:
                    func_name = "phi_%dD_to_%dD_split_%d" % (
                        event.n_pop, event.n_pop + 1, event.pop_to_div + 1)
                    phi = getattr(dadi.PhiManip, func_name)(xx, phi)

        if self.model.has_inbreeding:
            inbr_list = []
            for i in range(len(self.model.inbreeding_args)):
                inbr_arg = self.model.inbreeding_args[i]
                value = self.get_value_from_var2value(var2value,
                                                      inbr_arg)
                inbr_list.append(value)

            sfs = dadi.Spectrum.from_phi_inbreeding(phi, ns, [xx] * len(ns),
                                                    inbr_list, [2] * len(ns))
        else:
            sfs = dadi.Spectrum.from_phi(phi, ns, [xx] * len(ns))

        if self.model.has_p_misid:
            value = self.get_value_from_var2value(
                var2value,
                self.model.p_misid
            )
            sfs = (1 - value) * sfs + value * dadi.Numerics.reverse_array(sfs)

        return sfs

    def simulate(self, values, ns, sequence_length, population_labels, pts):
        """
        Returns simulated expected SFS for :attr:`demographic_model` with
        values as parameters. Simulation is performed with :attr:`self.pts`
        as grid points for numerical solutions.

        :param values: values of demographic model parameters.
        :param ns: sample sizes of the simulated SFS.
        """
        dadi = self.base_module
        extrap_func = getattr(dadi.Numerics, self.extrapolation)
        func_ex = extrap_func(self._inner_func)
        # print(values, ns, pts)
        model = func_ex(values, ns, pts)
        if population_labels is not None:
            model.pop_ids = population_labels
        # TODO: Nref
        return model

    def get_theta(self, values, pts):
        return super(DadiEngine, self).get_theta(values, pts)

    def evaluate(self, values, pts):
        try:
            return super(DadiEngine, self).evaluate(values, pts)
        except AttributeError as e:
            message = str(e).strip()
            if message != "'MaskedArray' object has no attribute 'folded'":
                raise e
            # We should write None for theta if we failed to evaluate
            key = self._get_key(values, pts)
            self.saved_add_info[key] = None
            return None

    def generate_code(self, values, filename, pts,
                      nanc=None, gen_time=None, gen_time_units=None):
        return super(DadiEngine, self).generate_code(values, filename, pts,
                                                     nanc, gen_time,
                                                     gen_time_units)

    def draw_data_comp_plot(self, values, pts, save_file=None, vmin=None):
        return super(DadiEngine, self).draw_data_comp_plot(
            values=values,
            grid_sizes=pts,
            save_file=save_file,
            vmin=vmin
        )


if dadi_available:
    register_engine(DadiEngine)
