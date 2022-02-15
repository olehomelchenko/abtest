from math import sqrt
from pprint import pprint
import numpy as np
from scipy.stats import norm
from matplotlib import ticker
from matplotlib.pyplot import Figure


@ticker.FuncFormatter
def major_formatter(x, pos):
    # return "[%.2f]" % x
    return f"{x * 100:.1f}%"


class Processor:
    def __init__(self, data: str) -> None:
        """
        Parse string GET argument to dict of values
        and make calculations like z-score and p-value

        Args:
            data (str): data in format "size:conv;size2:conv2;..."
            example: "1000:150;1000:140;1000:160;100:16"
        """
        self.init_data = data
        self.variations_list = self._parse_init_data()
        self.variations_dict = self.to_dict()

    def _parse_init_data(self) -> list:
        data = self.init_data

        lst = [item.split(":") for item in data.split(";")]
        for i, l in enumerate(lst):
            lst[i] = [float(item) for item in l]
        return lst

    def to_dict(self) -> dict:
        var_list = self.variations_list.copy()
        variations = [
            {"size": item[0], "conv": item[1], "cr": item[1] / item[0]}
            for item in var_list
        ]

        for v in variations:
            rate = v["cr"]
            v["std"] = sqrt(rate * (1 - rate) / v["size"])
        control = variations[0]
        for v in variations[1:]:
            v["z"] = (v["cr"] - control["cr"]) / sqrt(
                control["std"] ** 2 + v["std"] ** 2
            )
            v["p"] = norm().sf(v["z"])

        return {"variations": variations}

    def get_plot_figure(
        self, dpi=96, x=800, y=450, axis_off=True, linewidth=1
    ) -> Figure:
        d = self.variations_dict["variations"]

        # def create_norm_figure(testdata, dpi=96, x=800, y=450, axis_off=True, linewidth=1):
        # set figure size based on pixels and dpi
        fig = Figure(figsize=(x / dpi, y / dpi), dpi=dpi)

        # add a single subplot to the figure
        ax = fig.add_subplot(1, 1, 1)

        if len(self.variations_dict) >= 2:
            raise NotImplementedError

        # get standard deviations for both experiments
        std_a = d[0]["std"]
        std_b = d[1]["std"]

        # get borders for X axis, +-6 STD from rates
        min_std = min(std_a, std_b)
        max_std = max(std_a, std_b)

        min_rate = min(d[0]["cr"], d[1]["cr"])
        max_rate = max(d[0]["cr"], d[1]["cr"])

        min_x = min_rate - 6 * min_std
        max_x = max_rate + 6 * max_std

        # generate array for X axis
        click_rate = np.linspace(min_x, max_x, 300)

        # generate Y values for both distributions
        prob_a = norm(d[0]["cr"], std_a).pdf(click_rate)
        prob_b = norm(d[1]["cr"], std_b).pdf(click_rate)

        # plot both distributions on the subplot
        ax.plot(
            click_rate, prob_a, label="A", color="blue", alpha=0.5, linewidth=linewidth
        )
        ax.plot(
            click_rate,
            prob_b,
            label="B",
            color="orange",
            alpha=0.5,
            linewidth=linewidth,
        )

        # set X and Y labels
        ax.set_xlabel("Conversion rate")
        ax.set_ylabel("Probability")

        # define top borders for vertical lines in the center of the "bell"
        max_y_a = norm(d[0]["cr"], std_a).pdf(d[0]["cr"])
        max_y_b = norm(d[1]["cr"], std_b).pdf(d[1]["cr"])

        # plot vertical lines
        ax.vlines(d[0]["cr"], ymin=0, ymax=max_y_a, color="blue", alpha=0.3)
        ax.vlines(d[1]["cr"], ymin=0, ymax=max_y_b, color="orange", alpha=0.3)

        # remove ticks on axes
        ax.tick_params(axis="both", which="both", length=0)

        # remove borders around the subplot
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)

        ax.xaxis.set_major_formatter(major_formatter)

        fig.tight_layout()

        if axis_off:
            ax.axis("off")
            fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
        else:
            ax.legend(frameon=False)
        return fig

