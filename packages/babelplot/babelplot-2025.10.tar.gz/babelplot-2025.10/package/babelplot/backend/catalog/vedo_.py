"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2022
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
from multiprocessing import Process as process_t

from babelplot.task.color import NewConvertedColor
from babelplot.task.plotting import NewPlotFunctionsTemplate
from babelplot.type.dimension import dim_e
from babelplot.type.figure import figure_t as base_figure_t
from babelplot.type.frame import frame_t as base_frame_t
from babelplot.type.plot import plot_t as base_plot_t
from babelplot.type.plot_function import plot_function_h
from babelplot.type.plot_type import plot_e
from numpy import ndarray as array_t
from vedo import Mesh as backend_plot_t  # noqa
from vedo import Plotter as backend_figure_t  # noqa
from vedo import Volume as volume_t  # noqa

NAME = "vedo"


@d.dataclass(slots=True, repr=False, eq=False)
class plot_t(base_plot_t): ...


@d.dataclass(slots=True, repr=False, eq=False)
class frame_t(base_frame_t):

    def _NewPlot(
        self,
        plot_function: plot_function_h,
        *args,
        title: str | None = None,  # If _, then it is swallowed by kwargs!
        **kwargs,
    ) -> plot_t:
        """"""
        output = plot_t(
            title=title,
            property=kwargs.copy(),
            backend_name=self.backend_name,
            raw=plot_function(*args, **kwargs),
        )

        if output.raw is not None:
            self.raw.__iadd__(output.raw)

        return output


@d.dataclass(slots=True, repr=False, eq=False)
class figure_t(base_figure_t):

    def _NewBackendFigure(self, *args, **kwargs) -> backend_figure_t:
        """"""
        return backend_figure_t(*args, **kwargs)

    def _NewFrame(
        self,
        title: str | None,
        dim: dim_e,
        row: int,
        col: int,
        *args,
        **kwargs,
    ) -> frame_t:
        """"""
        output = frame_t(
            title=title,
            dim=dim,
            backend_name=self.backend_name,
        )

        output.raw = self.raw

        return output

    def _BackendShow(self, modal: bool, /) -> None:
        """"""
        # Passing self.raw.show().close shows the figures one by one.
        BackendShow = lambda: self.raw.show().close()

        process = process_t(target=BackendShow)
        process.start()

        if modal:
            process.join()
        else:
            self.showing_process = process


def _IsoSurface(volume: array_t, iso_value: float, *_, **kwargs) -> backend_plot_t:
    """"""
    return volume_t(volume).isosurface(value=[iso_value], **kwargs)


def _Mesh(triangles: array_t, vertices: array_t, *_, **kwargs) -> backend_plot_t:
    """"""
    output = backend_plot_t((vertices, triangles))

    if "width_edge" in kwargs:
        output.linewidth(kwargs["width_edge"])
    if "color_edge" in kwargs:
        output.linecolor(kwargs["color_edge"])
    if "color_face" in kwargs:
        output.color(c=kwargs["color_face"])

    return output


PLOTS = NewPlotFunctionsTemplate()
PLOTS[plot_e.ISOSET][1] = _IsoSurface
PLOTS[plot_e.MESH][1] = _Mesh


TRANSLATIONS = {
    (_IsoSurface, "color_edge"): None,
    (_IsoSurface, "color_face"): None,
    (_IsoSurface, "step_size"): None,
    (_IsoSurface, "width_edge"): None,
    (_Mesh, "color_face"): ("color_face", lambda _: NewConvertedColor(_, "hex", 0)),
}


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
