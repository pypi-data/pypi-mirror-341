"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2022
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import gzip
import typing as h
from multiprocessing import Process as process_t

from babelplot.task.plotting import NewPlotFunctionsTemplate, SetDefaultPlotFunction
from babelplot.task.showing import ShowHTMLPlotWithPyQt
from babelplot.type.dimension import dim_e
from babelplot.type.figure import figure_t as base_figure_t
from babelplot.type.frame import frame_t as base_frame_t
from babelplot.type.plot import plot_t as base_plot_t
from babelplot.type.plot_function import plot_function_h
from babelplot.type.plot_type import plot_e
from bokeh.embed import file_html as HTMLofBackendContent  # noqa
from bokeh.layouts import column as NewBackendColLayout  # noqa
from bokeh.layouts import grid as NewBackendGridLayout  # noqa
from bokeh.layouts import row as NewBackendRowLayout  # noqa
from bokeh.models.renderers import GlyphRenderer as backend_plot_t  # noqa
from bokeh.plotting import figure as backend_frame_t  # noqa
from bokeh.resources import INLINE  # noqa

NAME = "bokeh"


class backend_figure_t: ...


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
        return plot_t(
            title=title,
            property=kwargs.copy(),
            backend_name=self.backend_name,
            raw=plot_function(self.raw, *args, **kwargs),
        )


@d.dataclass(slots=True, repr=False, eq=False)
class figure_t(base_figure_t):

    layout: h.Any = d.field(init=False, default=None)

    def _NewBackendFigure(self, *args, **kwargs) -> backend_figure_t:
        """"""
        return backend_figure_t()  # self.raw is never used.

    def _NewFrame(
        self,
        row: int,
        col: int,
        *args,
        title: str | None = None,
        dim: dim_e = dim_e.XY,
        **kwargs,
    ) -> frame_t:
        """"""
        return frame_t(
            title=title,
            dim=dim,
            backend_name=self.backend_name,
            raw=backend_frame_t(title=title, **kwargs),
        )

    def AdjustLayout(self) -> None:
        """"""
        # arranged_frames must be composed of list since Bokeh does not support tuples
        # here!
        n_rows, n_cols = self.shape
        arranged_frames = [n_cols * [None] for _ in range(n_rows)]
        for frame, (row, col) in zip(self.frames, self.locations):
            raw = frame.raw
            if raw.renderers.__len__() == 0:
                _ = backend_frame_t.text(
                    raw,
                    x=(0,),
                    y=(0,),
                    text=("Empty Frame",),
                    text_font_size="30px",
                    text_color="#FF0000",
                )
            arranged_frames[row][col] = raw

        # Bokeh does not support inserting None as an indicator of empty space. As a
        # workaround, the frames are currently flattened (and None_s are filtered out).
        should_be_filtered = False
        for one_row in arranged_frames:
            if any(_ is None for _ in one_row):
                should_be_filtered = True
                break
        if should_be_filtered:
            arranged_frames = [_ for one_row in arranged_frames for _ in one_row]
            arranged_frames = list(filter(lambda _: _ is not None, arranged_frames))
            arranged_frames = [arranged_frames]
            n_rows = 1
            n_cols = arranged_frames[0].__len__()

        if n_rows > 1:
            if n_cols > 1:
                layout = NewBackendGridLayout(arranged_frames)
            else:
                column = [_row[0] for _row in arranged_frames]
                layout = NewBackendColLayout(column)
        else:
            layout = NewBackendRowLayout(arranged_frames[0])

        self.layout = layout

    def _BackendShow(self, modal: bool, /) -> None:
        """"""
        try:
            html = HTMLofBackendContent(self.layout, INLINE)
            html = gzip.compress(html.encode())
        except ValueError as exception:
            html = f"""
                <!DOCTYPE html>
                <html>
                <body>
                    <h1>Figure cannot be shown</h1>
                    <p>{str(exception)}</p>
                </body>
                </html>
            """

        process = process_t(target=ShowHTMLPlotWithPyQt, args=(html,))
        process.start()

        if modal:
            process.join()
        else:
            self.showing_process = process


def _DefaultFunction(type_: plot_e, frame_dim: int, /) -> plot_function_h:
    """"""

    def Actual(frame: backend_frame_t, *args, **kwargs) -> backend_plot_t:
        """"""
        args = ", ".join(map(lambda _: type(_).__name__, args))
        kwargs = ", ".join(
            f"{_key}={type(_vle).__name__}" for _key, _vle in kwargs.items()
        )

        return backend_frame_t.text(
            frame,
            x=(0,),
            y=(0,),
            text=(
                f"Unhandled Plot Request\n{type_.name}.{frame_dim}\nargs: {args}\nkwargs: {kwargs}",
            ),
            text_font_size="30px",
            text_align="center",
            text_color="#FF0000",
        )

    return Actual


PLOTS = NewPlotFunctionsTemplate()
PLOTS[plot_e.SCATTER][0] = backend_frame_t.scatter
SetDefaultPlotFunction(PLOTS, _DefaultFunction)


TRANSLATIONS = {
    "color_face": "fill_color",
    "opacity": "alpha",
    ("AddFrame", "azimuth"): None,
    ("AddFrame", "elevation"): None,
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
