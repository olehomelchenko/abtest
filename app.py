from fastapi import FastAPI, Response
from processing import Processor
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


app = FastAPI()


@app.get("/")
def main():
    return {"message": "Hello world"}


@app.get("/getjson")
def get_json(data: str):
    p = Processor(data)
    # p.parse_init_data()
    return p.variations_dict


@app.get("/plot")
def plot(data: str, linewidth="1", x="800", y="450", axis_off=False):
    p = Processor(data)
    x = int(x)
    y = int(y)
    linewidth = int(linewidth) or 1

    fig = p.get_plot_figure(axis_off=axis_off, linewidth=linewidth, x=x, y=y)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), media_type="image/png")

