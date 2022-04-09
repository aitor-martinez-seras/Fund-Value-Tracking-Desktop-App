import tkinter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from utils import get_deposits_of_a_fund, parse_dates_to_linspace, get_fund_value
from constants import *


def plot_profits_per_deposit(db, fig, ax: plt.Axes, fund_name, dates, visualization_options=None) -> bool:
    """

    :return:
    """
    ax.cla()
    deposits = get_deposits_of_a_fund(db, fund_name, dates)
    # If there is less than one deposit, then we can't print nothing
    if len(deposits) < 1:
        return False
    else:
        # DB structure: Id, Date, Deposit, Participations, Participation value
        current_participation_value = get_fund_value(fund_name)
        print(current_participation_value)
        value_per_deposit = []
        dates = []

        if visualization_options['percentage'] == OPTIONS_FOR_PERCENT[0]:
            for item in deposits:
                # (current_participation_value - Participation_value) = win or loss per participation i.e. the
                # difference between each participation current value and the value paid for it
                value_per_deposit.append(((current_participation_value - float(item[4])) / float(item[4])) * 100)
                dates.append(item[1])
            fig.suptitle('Rentabilidades en procentaje')
        else:
            for item in deposits:
                # item[2] to mulitply the win or loss per participation with the number of participations
                value_per_deposit.append(item[2] * ((current_participation_value - float(item[4])) / float(item[4])))
                dates.append(item[1])
            fig.suptitle('Rentabilidades')

        # Create a list with the colors for the plot, green if +, red if -
        plot_colors = list_of_colors_for_barplot(value_per_deposit)

        if visualization_options['spacing'] == OPTIONS_FOR_SPACING[1]:
            dates_linspace = parse_dates_to_linspace(dates)
            bar_container = ax.bar(dates_linspace, value_per_deposit, width=0.65, tick_label=dates, color=plot_colors)
            # set ticks every week
            ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            # set major ticks format
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        else:
            bar_container = ax.bar(range(len(value_per_deposit)), value_per_deposit, width=0.4, color=plot_colors)
            ax.set_xticks(range(len(value_per_deposit)), labels=dates, rotation=30, ha='right', fontsize='8')
            #ax.set_xticklabels()

        if visualization_options['percentage'] == OPTIONS_FOR_PERCENT[0]:
            #add_value_label(ax, dates, value_per_deposit)
            ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
            ax.bar_label(bar_container, labels=[f'{x:.2f}%' for x in value_per_deposit],
                         label_type='center', rotation=0, fontsize=9)
        else:
            ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
            ax.bar_label(bar_container, labels=[f'{x:.2f}\N{euro sign}' for x in value_per_deposit],
                         label_type='center', rotation=0, fontsize=9)
        # Plot a horizontal gray bar in the 0 value
        ax.axhline(color='dimgray')
        # Returns True to confirm that the graphic was plotted
        return True

def list_of_colors_for_barplot(values_list) -> list:
    color_list = []
    for value in values_list:
        if value < 0:
            color_list.append('firebrick')
        else:
            color_list.append('forestgreen')
    return color_list


@ticker.FuncFormatter
def major_formatter(x, pos):
    return f'[{x:.2f}]'


def add_value_label(ax: plt.Axes, x_list, y_list):
    for i in range(1, len(x_list)+1):
        ax.text(i, y_list[i-1]/2, f'{y_list[i-1]:.2f}%', ha="center")


def plot_profits_per_fund(db, fig, ax: plt.Axes, fund_names, dates, visualization_options=None) -> bool or list:
    # Clear plot
    ax.cla()
    not_plotted = [] # To store which of the funds could not be plotted
    funds_balances = []
    for index, fund in enumerate(fund_names):
        deposits = get_deposits_of_a_fund(db, fund, dates)
        # If no deposits were made to the fund in the specified dates, the name is stored for showing a warning
        # message and code goes to next iteration
        if len(deposits) == 0:
            not_plotted.append(fund)
            continue
        #               [0] [1]      [2]        [3]             [4]
        # DB structure: Id, Date, Deposit, Participations, Participation value
        current_participation_value = get_fund_value(fund)
        print(current_participation_value)
        money_spent_on_fund = 0.0
        sum_of_participations = 0.0
        for item in deposits:
            money_spent_on_fund += float(item[2])
            sum_of_participations += float(item[3])
        # Calculate the fund current value as the number of participations times the current value of one participation
        fund_current_value = sum_of_participations * current_participation_value
        balance = fund_current_value - money_spent_on_fund
        if visualization_options['percentage'] == OPTIONS_FOR_PERCENT[0]:
            # Transform balance into percentage
            funds_balances.append((balance / money_spent_on_fund) * 100)
            fig.suptitle('Rentabilidades en procentaje')
        else:
            funds_balances.append(balance)
            fig.suptitle('Rentabilidades')
    # In case there is no deposits for any of the funds, don't plot anything
    if len(funds_balances) == 0:
        return not_plotted
    # Pop names that are not going to be plotted
    for i in not_plotted:
        fund_names.remove(i)
    # Create a list with the colors for the plot, green if +, red if -
    plot_colors = list_of_colors_for_barplot(funds_balances)
    # Plot
    print(fund_names)
    print(funds_balances)
    # To handle the event of only having one bar, we plot two empty bars
    if len(fund_names) == 1:
        funds_balances = [0, funds_balances[0], 0]
        bar_container = ax.bar([0, 1, 2], funds_balances, width=0.65, tick_label=['', fund_names[0], ''],
                               color=['black', plot_colors[0], 'black'])
    else:
        bar_container = ax.bar([x for x in range(len(funds_balances))], funds_balances,
                           width=0.65, tick_label=fund_names, color=plot_colors)
    # Plot the value inside the bars of the plot, distinguishing between percentage and abs value
    if visualization_options['percentage'] == OPTIONS_FOR_PERCENT[0]:
        # add_value_label(ax, dates, value_per_deposit)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        ax.bar_label(bar_container, labels=[f'{x:.2f}%' for x in funds_balances],
                     label_type='center', rotation=0, fontsize=9)
    else:
        ax.bar_label(bar_container, labels=[f'{x:.2f}\N{euro sign}' for x in funds_balances],
                     label_type='center', rotation=0, fontsize=9)
        ax.set_title(f'Rentabilidad total entre los fondos'
                     f' \u2192 {sum(funds_balances):.3f} \N{euro sign}', y=0.995)
    # Plot a horizontal gray bar in the 0 value
    ax.axhline(color='dimgray')
    # Returns True to confirm that the graphic was plotted
    if not_plotted == []:
        not_plotted = True
    return not_plotted





def create_plot(canvas: FigureCanvasTkAgg, toolbar: NavigationToolbar2Tk):
    """
    Draws the selected plot and then makes it appear in the GUI along with a interactive toolbar
    :param canvas: FigureCanvasTkAgg object, that is a tk.DrawingArea
    :param toolbar: NavigationToolbar2Tk object
    :return:
    """
    canvas.draw()
    toolbar.update()
    #canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    canvas.get_tk_widget().pack(side=tkinter.TOP)
    toolbar.pack()
