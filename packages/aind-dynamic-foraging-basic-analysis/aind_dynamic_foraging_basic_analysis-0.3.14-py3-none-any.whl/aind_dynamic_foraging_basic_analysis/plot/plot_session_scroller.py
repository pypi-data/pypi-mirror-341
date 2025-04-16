"""Plot foraging session in a standard format.
This is supposed to be reused in plotting real data or simulation data to ensure
a consistent visual representation.
"""

import numpy as np
from matplotlib import pyplot as plt

from aind_dynamic_foraging_data_utils import nwb_utils as nu
from aind_dynamic_foraging_basic_analysis.licks import annotation as a
from aind_dynamic_foraging_basic_analysis.plot.style import (
    STYLE,
    FIP_COLORS,
)


def plot_session_scroller(  # noqa: C901 pragma: no cover
    nwb,
    ax=None,
    fig=None,
    processing="bright",
    metrics=[],
    plot_list=[
        "FIP",
        "bouts",
        "go cue",
    ],
):
    """
    Creates an interactive plot of the session.
    Plots left/right licks/rewards, and go cues

    pressing "left arrow" scrolls backwards in time
    pressing "right arrow" scrolls forwards in time
    pressing "up arrow" zooms out, in time
    pressing "down arrow" zooms in, in time
    prssing "h", for home, sets the xlimits to (first event, last event)

    nwb, an nwb like object that contains attributes: df_events, session_id
        and optionally contains attributes fip_df, df_licks

    ax is a pyplot figure axis. If None, a new figure is created

    processing (str) processing method for FIP data to plot

    metrics (list of strings), list of metrics to plot. Must be a
        column in nwb.df_trials

    plot_list (list of strings), list of annotations and features to plot

    EXAMPLES:
    plot_foraging_session.plot_session_scroller(nwb)
    """

    approved_plot_list = [
        "bouts",
        "go cue",
        "rewarded lick",
        "cue response",
        "baiting",
        "FIP",
        "lick artifacts",
    ]
    unapproved = set(plot_list) - set(approved_plot_list)
    if len(unapproved) > 0:
        print("Unknown plot_list options: {}".format(list(unapproved)))
        return

    if not hasattr(nwb, "df_events"):
        print("computing df_events first")
        nwb.df_events = nu.create_events_df(nwb)
        df_events = nwb.df_events
    else:
        df_events = nwb.df_events
    if hasattr(nwb, "fip_df") and ("FIP" in plot_list):
        fip_df = nwb.fip_df
    else:
        fip_df = None
    if hasattr(nwb, "df_licks"):
        df_licks = nwb.df_licks
    elif ("bouts" in plot_list) or ("cue response" in plot_list) or ("rewarded lick" in plot_list):
        print("computing df_licks first")
        nwb.df_licks = a.annotate_licks(nwb)
        df_licks = nwb.df_licks
    else:
        df_licks = None
    if not hasattr(nwb, "df_trials"):
        print("computing df_trials")
        nwb.df_trials = nu.create_df_trials(nwb)
        df_trials = nwb.df_trials
    else:
        df_trials = nwb.df_trials

    if ax is None:
        if fip_df is None:
            fig, ax = plt.subplots(figsize=(15, 5))
        else:
            fig, ax = plt.subplots(figsize=(15, 8))

    xmin = df_events.iloc[0]["timestamps"]
    x_first = xmin
    x_last = df_events.iloc[-1]["timestamps"]
    xmax = xmin + 20
    ax.set_xlim(xmin, xmax)

    params = {
        "left_lick_bottom": 0,
        "left_lick_top": 0.25,
        "right_lick_bottom": 1.25,
        "right_lick_top": 1.5,
        "left_reward_bottom": 0.25,
        "left_reward_top": 0.5,
        "right_reward_bottom": 1,
        "right_reward_top": 1.25,
        "probs_bottom": 0.75,
        "probs_top": 1.5,
        "go_cue_bottom": 0,
        "go_cue_top": 1.5,
        "metrics_bottom": 1.5,
        "metrics_top": 2.5,
        "G_1_dff-bright_bottom": 2.5,
        "G_1_dff-bright_top": 3.5,
        "G_2_dff-bright_bottom": 3.5,
        "G_2_dff-bright_top": 4.5,
        "R_1_dff-bright_bottom": 4.5,
        "R_1_dff-bright_top": 5.5,
        "R_2_dff-bright_bottom": 5.5,
        "R_2_dff-bright_top": 6.5,
        "G_1_dff-poly_bottom": 2.5,
        "G_1_dff-poly_top": 3.5,
        "G_2_dff-poly_bottom": 3.5,
        "G_2_dff-poly_top": 4.5,
        "R_1_dff-poly_bottom": 4.5,
        "R_1_dff-poly_top": 5.5,
        "R_2_dff-poly_bottom": 5.5,
        "R_2_dff-poly_top": 6.5,
        "G_1_dff-exp_bottom": 2.5,
        "G_1_dff-exp_top": 3.5,
        "G_2_dff-exp_bottom": 3.5,
        "G_2_dff-exp_top": 4.5,
        "R_1_dff-exp_bottom": 4.5,
        "R_1_dff-exp_top": 5.5,
        "R_2_dff-exp_bottom": 5.5,
        "R_2_dff-exp_top": 6.5,
    }
    yticks = [
        (params["left_lick_top"] - params["left_lick_bottom"]) / 2 + params["left_lick_bottom"],
        (params["right_lick_top"] - params["right_lick_bottom"]) / 2 + params["right_lick_bottom"],
        (params["left_reward_top"] - params["left_reward_bottom"]) / 2
        + params["left_reward_bottom"],
        (params["right_reward_top"] - params["right_reward_bottom"]) / 2
        + params["right_reward_bottom"],
        (params["probs_top"] - params["probs_bottom"]) * -0.33 + params["probs_bottom"],
        (params["probs_top"] - params["probs_bottom"]) * 0 + params["probs_bottom"],
        (params["probs_top"] - params["probs_bottom"]) * 0.33 + params["probs_bottom"],
        (params["metrics_top"] - params["metrics_bottom"]) * 0.25 + params["metrics_bottom"],
        (params["metrics_top"] - params["metrics_bottom"]) * 0.5 + params["metrics_bottom"],
        (params["metrics_top"] - params["metrics_bottom"]) * 0.75 + params["metrics_bottom"],
        params["metrics_top"],
    ]
    ylabels = [
        "left licks",
        "right licks",
        "left reward",
        "right reward",
        "1",
        "0",
        "1",
        "0.25",
        "0.5",
        "0.75",
        "metrics",
    ]
    ycolors = ["k", "k", "r", "r", "darkgray", "darkgray", "darkgray", "k"]

    if fip_df is not None:
        fip_channels = [
            "G_2_dff-{}".format(processing),
            "G_1_dff-{}".format(processing),
            "R_2_dff-{}".format(processing),
            "R_1_dff-{}".format(processing),
        ]
        present_channels = fip_df["event"].unique()
        for index, channel in enumerate(fip_channels):
            if channel in present_channels:
                yticks.append(
                    (params[channel + "_top"] - params[channel + "_bottom"]) * 1
                    + params[channel + "_bottom"]
                )
                ylabels.append(channel)
                color = FIP_COLORS.get(channel, "k")
                ycolors.append(color)
                C = fip_df.query("event == @channel").copy()
                d_min = C["data"].min()
                d_max = C["data"].max()
                d_range = d_max - d_min
                t1 = 0.25
                t2 = 0.5
                t3 = 0.75
                p1 = d_min + t1 * d_range
                p2 = d_min + t2 * d_range
                p3 = d_min + t3 * d_range
                yticks.append(
                    params[channel + "_bottom"]
                    + (params[channel + "_top"] - params[channel + "_bottom"]) * t1
                )
                yticks.append(
                    params[channel + "_bottom"]
                    + (params[channel + "_top"] - params[channel + "_bottom"]) * t2
                )
                yticks.append(
                    params[channel + "_bottom"]
                    + (params[channel + "_top"] - params[channel + "_bottom"]) * t3
                )
                ylabels.append(str(round(p1, 3)))
                ylabels.append(str(round(p2, 3)))
                ylabels.append(str(round(p3, 3)))
                ycolors.append("darkgray")
                ycolors.append("darkgray")
                ycolors.append("darkgray")
                C["data"] = C["data"] - d_min
                C["data"] = C["data"].values / (d_max - d_min)
                C["data"] += params[channel + "_bottom"]
                ax.plot(C.timestamps.values, C.data.values, color)
                ax.axhline(params[channel + "_bottom"], color="k", linewidth=0.5, alpha=0.25)

    if ("bouts" not in plot_list) or (df_licks is None):
        left_licks = df_events.query('event == "left_lick_time"')
        left_times = left_licks.timestamps.values
        ax.vlines(
            left_times,
            params["left_lick_bottom"],
            params["left_lick_top"],
            alpha=1,
            linewidth=2,
            color="gray",
        )

        right_licks = df_events.query('event == "right_lick_time"')
        right_times = right_licks.timestamps.values
        ax.vlines(
            right_times,
            params["right_lick_bottom"],
            params["right_lick_top"],
            alpha=1,
            linewidth=2,
            color="gray",
        )
    else:
        cmap = plt.get_cmap("tab20")
        bouts = df_licks.bout_number.unique()
        for b in bouts:
            bout_left_licks = df_licks.query(
                '(bout_number == @b)&(event=="left_lick_time")'
            ).timestamps.values
            bout_right_licks = df_licks.query(
                '(bout_number == @b)&(event=="right_lick_time")'
            ).timestamps.values
            ax.vlines(
                bout_left_licks,
                params["left_lick_bottom"],
                params["left_lick_top"],
                alpha=1,
                linewidth=2,
                color=cmap(np.mod(b, 20)),
            )
            ax.vlines(
                bout_right_licks,
                params["right_lick_bottom"],
                params["right_lick_top"],
                alpha=1,
                linewidth=2,
                color=cmap(np.mod(b, 20)),
            )

    if ("rewarded lick" in plot_list) and (df_licks is not None):
        # plot licks that trigger left rewards
        left_rewarded_licks = df_licks.query(
            '(event == "left_lick_time")&(rewarded)'
        ).timestamps.values
        ax.plot(
            left_rewarded_licks,
            [params["left_lick_top"]] * len(left_rewarded_licks),
            "ro",
            label="rewarded lick",
        )

        # Plot licks that trigger right rewards
        right_rewarded_licks = df_licks.query(
            '(event == "right_lick_time")&(rewarded)'
        ).timestamps.values
        ax.plot(
            right_rewarded_licks, [params["right_lick_bottom"]] * len(right_rewarded_licks), "ro"
        )

    if ("cue response" in plot_list) and (df_licks is not None):
        # plot cue responsive licks
        left_cue_licks = df_licks.query(
            '(event == "left_lick_time")&(cue_response)'
        ).timestamps.values
        ax.plot(
            left_cue_licks,
            [
                params["left_lick_bottom"]
                + (params["left_lick_top"] - params["left_lick_bottom"]) / 2
            ]
            * len(left_cue_licks),
            "bD",
            label="cue responsive lick",
        )
        right_cue_licks = df_licks.query(
            '(event == "right_lick_time")&(cue_response)'
        ).timestamps.values
        ax.plot(
            right_cue_licks,
            [
                params["right_lick_bottom"]
                + (params["right_lick_top"] - params["right_lick_bottom"]) / 2
            ]
            * len(right_cue_licks),
            "bD",
        )

    if "baiting" in plot_list:
        # Plot baiting
        bait_right = df_trials.query("bait_right")["goCue_start_time_in_session"].values
        bait_left = df_trials.query("bait_left")["goCue_start_time_in_session"].values
        ax.plot(
            bait_right, [params["right_lick_top"] - 0.05] * len(bait_right), "ms", label="baited"
        )
        ax.plot(bait_left, [params["left_lick_bottom"] + 0.05] * len(bait_left), "ms")

    if "lick artifacts" in plot_list:
        artifacts_right = df_licks.query('likely_artifact and (event=="right_lick_time")')[
            "timestamps"
        ].values
        artifacts_left = df_licks.query('likely_artifact and (event=="left_lick_time")')[
            "timestamps"
        ].values
        ax.plot(
            artifacts_right,
            [params["right_lick_top"]] * len(artifacts_right),
            "d",
            color="darkorange",
            label="lick artifact",
        )
        ax.plot(
            artifacts_left,
            [params["left_lick_bottom"]] * len(artifacts_left),
            "d",
            color="darkorange",
        )

    left_reward_deliverys = df_events.query('event == "left_reward_delivery_time"')
    left_times = left_reward_deliverys.timestamps.values
    ax.vlines(
        left_times,
        params["left_reward_bottom"],
        params["left_reward_top"],
        alpha=1,
        linewidth=2,
        color="black",
        label="reward times",
    )

    right_reward_deliverys = df_events.query('event == "right_reward_delivery_time"')
    right_times = right_reward_deliverys.timestamps.values
    ax.vlines(
        right_times,
        params["right_reward_bottom"],
        params["right_reward_top"],
        alpha=1,
        linewidth=2,
        color="black",
    )

    go_cues = df_events.query('event == "goCue_start_time"')
    go_cue_times = go_cues.timestamps.values
    if "go cue" in plot_list:
        ax.vlines(
            go_cue_times,
            params["go_cue_bottom"],
            params["go_cue_top"],
            alpha=0.75,
            linewidth=1,
            color="b",
            label="go cue",
        )

    # plot metrics
    ax.axhline(params["metrics_bottom"], color="k", linewidth=0.5, alpha=0.25)
    go_cue_times_doubled = np.repeat(go_cue_times, 2)[1:]

    pR = params["probs_bottom"] + df_trials["reward_probabilityR"] / 4
    pR = np.repeat(pR, 2)[:-1]
    ax.fill_between(
        go_cue_times_doubled, params["probs_bottom"], pR, color="b", label="pR", alpha=0.4
    )

    pL = params["probs_bottom"] - df_trials["reward_probabilityL"] / 4
    pL = np.repeat(pL, 2)[:-1]

    ax.fill_between(
        go_cue_times_doubled, pL, params["probs_bottom"], color="r", label="pL", alpha=0.4
    )

    # plot metrics if they are available
    for metric in metrics:
        if metric in df_trials:
            values = df_trials[metric] + params["metrics_bottom"]
            ax.plot(go_cue_times, values, label=metric)
        else:
            print('Metric "{}" not available in df_trials'.format(metric))

    # Clean up plot
    ax.legend(framealpha=1, loc="lower left", reverse=True)
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels, fontsize=STYLE["axis_ticks_fontsize"])

    for tick, color in zip(ax.get_yticklabels(), ycolors):
        tick.set_color(color)
    ax.set_xlabel("time (s)", fontsize=STYLE["axis_fontsize"])
    if fip_df is None:
        ax.set_ylim(0, 2.5)
    else:
        ax.set_ylim(0, 6.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if fip_df is not None:
        ax.set_title(nwb.session_id + ", FIP processing: {}".format(processing))
    else:
        ax.set_title(nwb.session_id)
    plt.tight_layout()

    def on_key_press(event):
        """
        Define interaction resonsivity
        """
        x = ax.get_xlim()
        xmin = x[0]
        xmax = x[1]
        xStep = (xmax - xmin) / 4
        if event.key == "<" or event.key == "," or event.key == "left":
            xmin -= xStep
            xmax -= xStep
        elif event.key == ">" or event.key == "." or event.key == "right":
            xmin += xStep
            xmax += xStep
        elif event.key == "up":
            xmin -= xStep
            xmax += xStep
        elif event.key == "down":
            xmin += xStep * (2 / 3)
            xmax -= xStep * (2 / 3)
        elif event.key == "h":
            xmin = x_first
            xmax = x_last
        ax.set_xlim(xmin, xmax)
        plt.draw()

    kpid = fig.canvas.mpl_connect("key_press_event", on_key_press)  # noqa: F841

    return fig, ax
