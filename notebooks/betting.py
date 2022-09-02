import plotly.express as px
import numpy as np
from tqdm import tqdm
import plotly.graph_objects as go
import math
from rich import print as rprint


def o2p(odds: int, spread: int = 20) -> float:
    """
    Convert moneyline odds into an implied probability, for a given spread.
    """
    assert (
        abs(odds) >= 100
    ), f"Spread betting odds are always at least +- 100: you provided {odds}"

    # The spread means that the payout is less than it should be, i.e. that the moneyline odds are lower than they should be (for the probability)
    odds = odds + spread / 2
    if abs(odds) < 100:
        odds += 200

    if odds >= 100:  # This is the underdog
        return 100 / (odds + 100)
    else:  # This is the favourite
        odds = abs(odds)
        return odds / (100 + odds)


def p2o(p: float) -> int:
    """
    Convert a probability to moneyline odds
    """
    assert p > 0 and p < 1, f"Probabilities must be in (0,1), you provided p = {p}"
    if p == 0.5:
        return 100
    if p < 0.5:
        return round(100 / p - 100)
    else:
        return -round(100 * p / (1 - p))


def odds_complement(odds: int, spread: int = 20) -> int:
    """
    Get the complementary moneyline odds, for a given spread.
    """
    true_spread = p2o(1 - o2p(odds, spread))
    if true_spread >= 100 and true_spread - (spread / 2) < 100:
        diff = true_spread - 100
        return round(-100 - (spread / 2) - diff)
    else:
        return round(true_spread - (spread / 2))


def payout(odds: int, include_stake: bool = True) -> float:
    """
    Calculate the payout of a $1 bet at the given odds, taking into account whether you recover your stake on winning.
    """
    assert (
        abs(odds) >= 100
    ), f"Spread betting odds are always at least +- 100: you provided {odds}"

    if odds >= 100:  # This is the underdog
        profit = odds / 100
    else:  # This is the favourite
        odds = abs(odds)
        profit = 100 / odds

    if include_stake:
        return 1 + profit
    else:
        return profit


def spread_from_odds(odds: int):
    """
    I couldn't be bothered to write a nice function to express these, so I just eyeballed it based on looking at a bunch of bets across
    various sites, generally erring on the conservative (high) side - you'll probably find lower spreads in reality.
    """
    odds = abs(odds)

    thresholds = [200, 300, 400, 600, 50000]
    mults = [0.3, 0.5, 0.8, 1.5, 3]

    for threshold, mult in zip(thresholds, mults):
        if odds < threshold:
            return odds * mult


def choose(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def linear_risk(λ: float = 2):
    """
    Returns a linear risk function, with a coefficient of your choice. For most people this is ~2.
    """

    def f(x):
        if x > 0:
            return x
        return λ * x

    return f


def lets_go_mormons(
    num_bets,
    odds1,
    odds2,
    spread=20,
    promo_include_stake=False,
    risk_adjustment=linear_risk(1),
    printing=False,
    self_hedging=True,
    stress_tax=0,
):
    """
    This is the main strategy evaluation function, so named in honour of its highly lucrative debut game, BYU vs Loyola.

    We have some number (num_bets) of promotions available to us.
    For each promotion, we make an original bet on an underdog (at odds1).
    The underdog will win anywhere between [0, num_bets] of them. Calculate the probability and profit / loss of each.
    For each outcome, we receive a free bet / site credit for each loss.
    Repeat the above steps (this time betting at odds2) with the free bet, and calculate the cumulative probability & profit
    for each ultimate outcome.
    Surface these as a dictionary of the following form:
        (round_1_wins, round_2_wins, cumulative_probability): total_profit

    If 'printing' is True:
        Print a dictionary showing the profits after the original bet, and with the credits
        Print a dictionary showing the each potential combined profit, and associated likelihood
        Print the EV and risk-adjusted EV, per-promotion

    If self_hedging is true, we model the strategy as one where the player puts the same amount of money on both the underdog and the favourite, as opposed to
    just betting on the underdog. This is almost always worth doing, since it dramatically reduces the maximum loss, but if a player doesn't have enough money
    to finance both sides of the trade, doesn't want to deal with multiple sportsbookes, or has a large risk appetite, they may not wish to self hedge.

    Optionally apply a stress_tax, to account for how annoying this process is, the overall risk of an unknown unknown going wrong, and the psychic pain of depositing $1000 into a weird betting website.
    A good way to think of the stress tax is: if I only made X% profit, would this whole process have been *barely* worth it?
    I included this because some 'optimal' strategies end up being risk-free, with a very high EV, but pay out nothing most of the time (and vast amounts, rarely).
    A high stress tax penalizes these strategies in particular, nudging the optimum towards slightly lower EV strategies that have substantial payouts more often.

    Return the risk-adjusted EV per-promotion (this can then be plotted for different values of num_bets, odds, spread, etc.)
    """
    spread1 = spread_from_odds(odds1)
    spread2 = spread_from_odds(odds2)

    favourite_odds_1 = odds_complement(odds1, spread1)
    favourite_odds_2 = odds_complement(odds2, spread2)

    # The first round of betting
    real_money_profit = []
    probs = []
    for underdog_wins in range(num_bets + 1):
        favourite_wins = num_bets - underdog_wins
        if self_hedging:
            underdog_profit = (payout(odds1, False) - 1) * underdog_wins
            favourite_profit = (payout(favourite_odds_1, False) - 1) * favourite_wins
            round_1_profit = underdog_profit + favourite_profit
        else:
            round_1_profit = (payout(odds1, False)) * underdog_wins - 1 * favourite_wins

        real_money_profit.append(round_1_profit)
        probs.append(
            o2p(odds1, spread1) ** underdog_wins
            * (1 - o2p(odds1, spread1)) ** favourite_wins
            * choose(num_bets, underdog_wins)
        )

    # Then play the credits as underdogs against real money
    profits = [
        {"profit": round(x[0], 2), "prob": round(x[1], 2), "credits": num_bets - i}
        for i, x in enumerate(zip(real_money_profit, probs))
    ]

    for p in profits:
        p["credit_profits"] = []
        if p["credits"] > 0:
            for num_wins in range(p["credits"] + 1):
                num_losses = p["credits"] - num_wins
                prob = (
                    (o2p(odds2, spread2) ** num_wins)
                    * (1 - o2p(odds2, spread2)) ** num_losses
                    * choose(p["credits"], num_wins)
                )
                profit = (payout(odds2, promo_include_stake) - 1) * num_wins + payout(
                    favourite_odds_2, False
                ) * num_losses
                key = (num_wins, round(prob * p["prob"], 3))
                p["credit_profits"].append(
                    {
                        "wins": num_wins,
                        "prob": round(prob, 3),
                        "profit": round(profit, 3),
                    }
                )

    if printing:
        rprint("Profits broken down by stage")
        rprint(profits)
        rprint("-" * 20)

    profit_distilled = {}
    for item in profits:
        if not len(item["credit_profits"]):
            profit_distilled[
                (num_bets - item["credits"], item["credits"], item["prob"])
            ] = item["profit"]
        else:
            for credit_profit in item["credit_profits"]:
                key = (
                    num_bets - item["credits"],
                    credit_profit["wins"],
                    round(item["prob"] * credit_profit["prob"], 3),
                )
                profit_distilled[key] = round(
                    item["profit"] + credit_profit["profit"], 3
                )

    ev = round(
        sum([item[0][2] * (item[1] - stress_tax) for item in profit_distilled.items()]),
        3,
    )
    risk_adjusted_ev = round(
        sum(
            [
                item[0][2] * risk_adjustment(item[1] - stress_tax)
                for item in profit_distilled.items()
            ]
        ),
        3,
    )

    if printing:
        rprint(
            "Total profits, keyed by (Round 1 Wins, Round 2 Wins, Cumulative Probability)"
        )
        rprint(profit_distilled)
        rprint("-" * 20)
        rprint(f"Expected Profit (Per Promotion): {ev/num_bets*100:.1f}%")
        rprint(
            f"Risk-Adjusted Expected Profit (Per Promotion): {risk_adjusted_ev/num_bets*100:.1f}%"
        )

    return round(risk_adjusted_ev / num_bets, 3)


lets_go_mormons(
    num_bets=1,
    odds1=-100,
    odds2=1400,
    spread=20,
    promo_include_stake=False,
    risk_adjustment=linear_risk(2),
    printing=True,
    self_hedging=True,
    stress_tax=0,
)

# lets_go_mormons(
#     num_bets=1,
#     odds1=-100,
#     odds2=1400,
#     spread=20,
#     promo_include_stake=False,
#     risk_adjustment=linear_risk(1),
#     printing=True,
#     self_hedging=True,
#     stress_tax=0
# )


def plot_strategy(
    num_bets=1,
    risk_coeff=2,
    promo_include_stake=True,
    self_hedging=True,
    stress_tax=0,
    save_plot=None,
):
    """
    Show a heatmap of the risk-adjusted percentage payoff when you play your first and second round bets at the odds corresponding to your X and Y coordinates.
    This assumes a linear risk aversion, but allows you to choose your coefficient, and to specify whether the promotion free bet includes its stake.
    """
    odds_upper_bound = 400
    odds_lower_bound = 100
    odds_resolution = 10
    odds_array = np.concatenate(
        (
            np.arange(
                -odds_upper_bound, -odds_lower_bound + odds_resolution, odds_resolution
            ),
            np.arange(
                odds_lower_bound, odds_upper_bound + odds_resolution, odds_resolution
            ),
        )
    )

    X, Y = np.meshgrid(odds_array, odds_array)
    Z = np.zeros_like(X, dtype=float)

    for i in tqdm(range(Z.shape[0])):
        for j in range(Z.shape[1]):
            odds = (X[i, j], Y[i, j])
            Z[i, j] = lets_go_mormons(
                num_bets,
                *odds,
                promo_include_stake=promo_include_stake,
                risk_adjustment=linear_risk(risk_coeff),
                self_hedging=self_hedging,
                stress_tax=stress_tax,
            )

    rgb_red_to_white = [
        "rgb(255, 0, 0)",
        "rgb(255, 62, 34)",
        "rgb(255, 91, 58)",
        "rgb(255, 115, 82)",
        "rgb(255, 137, 105)",
        "rgb(255, 158, 129)",
        "rgb(255, 178, 153)",
        "rgb(255, 198, 178)",
        "rgb(255, 217, 203)",
        "rgb(255, 236, 229)",
        "rgb(255, 255, 255)",
    ]

    rgb_white_to_blue = [
        "rgb(255, 255, 255)",
        "rgb(242, 232, 255)",
        "rgb(228, 208, 255)",
        "rgb(213, 185, 255)",
        "rgb(197, 162, 255)",
        "rgb(180, 140, 255)",
        "rgb(161, 117, 255)",
        "rgb(140, 94, 255)",
        "rgb(116, 70, 255)",
        "rgb(84, 43, 255)",
        "rgb(24, 0, 255)",
    ]

    lower_bound = -200
    upper_bound = 100

    vals_red_to_white = list(np.linspace(0, 0.5, len(rgb_red_to_white)))
    vals_white_to_blue = list(np.linspace(0.5, 1, len(rgb_white_to_blue)))

    rgbs = rgb_red_to_white + rgb_white_to_blue
    vals = vals_red_to_white + vals_white_to_blue

    colorscale = [list(pair) for pair in zip(vals, rgbs)]

    rprint(colorscale)

    # fig = px.imshow(
    #     Z * 100, x=odds_array, y=odds_array, color_continuous_scale=px.colors.diverging.Picnic, color_continuous_midpoint=0
    # )

    # colorscale = [(-200, "red"), ("red", "red", "red", "red", "white", "blue"]
    fig = px.imshow(
        Z * 100, x=odds_array, y=odds_array, color_continuous_scale=colorscale
    )

    plural = "s" if num_bets > 1 else ""
    promotion_phrase = "DOES" if promo_include_stake else "DOES NOT"

    fig.update_layout(
        # title=f"<b>Risk-Adjusted % Profit-Per-Promotion</b> <br> for a strategy using <b>{num_bets}</b> promotion{plural} <br> with a risk aversion of <b>{risk_coeff}</b> <br> where a bet credit <b>{promotion_phrase}</b> return its stake</b>",
        # xaxis_title="Bet 1 Odds",
        # yaxis_title="Bet 2 Odds",
        width=300,
        height=300,
        margin={"t": 0, "r": 0, "b": 0, "l": 0},
        title_font_family="Arial",
        title_font_size=18,
        title_x=0.5,
        xaxis_range=[-odds_upper_bound, odds_upper_bound],
        yaxis_range=[-odds_upper_bound, odds_upper_bound],
        showlegend=False,
        hoverdistance=1,
    )

    fig.update(
        data=[
            {
                "hovertemplate": "Bet 1 Odds: %{x}<br>Bet 2 Odds: %{y}<br>Risk-Adjusted Profit: %{z}%<extra></extra>"
            }
        ],
        layout_coloraxis_showscale=False,
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    max_index = np.unravel_index(Z.argmax(), Z.shape)

    fig.add_trace(
        go.Scatter(
            x=[X[max_index]],
            y=[Y[max_index]],
            mode="markers+text",
            name="Optimum Odds",
            text=[f"{round(Z.max()*100, 3)}%"],
            textposition="top center",
            textfont=dict(color="black", size=18),
            marker_symbol="cross",
            marker_color="black",
            marker_size=12,
        )
    )

    fig.show()

    if save_plot is not None:
        fig.write_html(save_plot, include_plotlyjs=False)


plot_strategy(
    num_bets=1, risk_coeff=2, promo_include_stake=False, self_hedging=True, stress_tax=0
)
