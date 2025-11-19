from fasthtml.common import FastHTML, Div, H1
import matplotlib.pyplot as plt

from employee_events.query_base import QueryBase
from employee_events.employee import Employee
from employee_events.team import Team

from utils import load_model

from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent


class ReportDropdown(Dropdown):
    label = "Select User"

    def build_component(self, model, **kwargs):
        return super().build_component(model=model, label=self.label, **kwargs)

    def component_data(self, model, **kwargs):
        return model.names()


class Header(BaseComponent):
    def build_component(self, **kwargs):
        return H1("Employee / Team Dashboard")


class LineChart(MatplotlibViz):
    def visualization(self, model, asset_id, **kwargs):
        df = model.event_counts(asset_id)
        df = df.fillna(0)
        df = df.set_index("Day")
        df = df.sort_index()

        df = df.cumsum()
        df.columns = ["Positive", "Negative"]

        fig, ax = plt.subplots()
        df.plot(ax=ax)

        self.set_axis_styling(ax, border_color="black", font_color="black")
        ax.set_title("Cumulative Event Counts")
        ax.set_xlabel("Date")
        ax.set_ylabel("Events")

        return fig


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, model, asset_id, **kwargs):
        data = model.model_data(asset_id)
        proba = self.predictor.predict_proba(data)
        pred = proba[0][1]

        fig, ax = plt.subplots()
        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)

        self.set_axis_styling(ax, border_color="black", font_color="black")
        return fig


class NotesTable(DataTable):
    def component_data(self, model, entity_id, **kwargs):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name="profile_type",
            hx_get="/update_dropdown",
            hx_target="#selector"
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]


class Report(CombinedComponent):
    children = [
        Header(),
        DashboardFilters(),
        LineChart(),
        BarChart(),
        NotesTable()
    ]


app = FastHTML()


@app.get("/")
def root():
    report = Report()
    return report(1, Employee())


@app.get("/employee/{id}")
def employee_page(id: str):
    report = Report()
    return report(id, Employee())


@app.get("/team/{id}")
def team_page(id: str):
    report = Report()
    return report(id, Team())


@app.get("/update_dropdown")
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    if r.query_params["profile_type"] == "Team":
        return dropdown(None, Team())
    return dropdown(None, Employee())


@app.post("/update_data")
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data["profile_type"]
    id = data["user-selection"]

    if profile_type == "Employee":
        return RedirectResponse(f"/employee/{id}", status_code=303)
    return RedirectResponse(f"/team/{id}", status_code=303)


app.serve()