from flask import Blueprint
from flask import render_template
from flask import request
from flask import Response

from ...core.activities import ActivityRepository
from ...core.parametric_plot import ALL_VARIABLES
from ...core.parametric_plot import CONTINUOUS_VARIABLES
from ...core.parametric_plot import DISCRETE_VARIABLES
from ...core.parametric_plot import make_parametric_plot
from ...core.parametric_plot import MARKS
from ...core.parametric_plot import ParametricPlotSpec


def make_plot_builder_blueprint(repository: ActivityRepository) -> Blueprint:
    blueprint = Blueprint("plot_builder", __name__, template_folder="templates")

    @blueprint.route("/")
    def index() -> Response:
        context = {}
        if request.args:
            spec = ParametricPlotSpec(
                mark=request.args["mark"],
                x=request.args["x"],
                y=request.args["y"],
                color=request.args.get("color", None),
                shape=request.args.get("shape", None),
                size=request.args.get("size", None),
                row=request.args.get("row", None),
                column=request.args.get("column", None),
            )
            plot = make_parametric_plot(repository.meta, spec)
            context["plot"] = plot
        return render_template(
            "plot_builder/index.html.j2",
            marks=MARKS,
            continuous=ALL_VARIABLES,
            discrete=DISCRETE_VARIABLES,
            **context,
            **request.args
        )

    return blueprint
