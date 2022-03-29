import tkinter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from utils import get_deposits_of_a_fund, parse_dates_to_linspace, get_fund_value
from constants import *


def plot_profits_per_deposit(db, fig, ax: plt.Axes, fund_name, dates, visualization_options=None):
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
        #current_fund_value = 9.551  # Aqui va la funcion que devuelve el valor del fondo
        current_fund_value = get_fund_value(fund_name)
        print(current_fund_value)
        value_per_deposit = []
        dates = []

        if visualization_options['percentage'] == OPTIONS_FOR_PERCENT[0]:
            for item in deposits:
                value_per_deposit.append(((current_fund_value - float(item[4])) / float(item[4])) * 100)
                dates.append(item[1])
            fig.suptitle('Rentabilidades en procentaje')
        else:
            for item in deposits:
                value_per_deposit.append(item[2] * ((current_fund_value - float(item[4])) / float(item[4])))
                dates.append(item[1])
            fig.suptitle('Rentabilidades')

        # Create a list with the colors for the plot, green if +, red if -
        plot_colors = list_of_colors_for_barplot(value_per_deposit)

        if visualization_options['spacing'] == OPTIONS_FOR_SPACING[1]:
            dates_linspace = parse_dates_to_linspace(dates)
            bar_container = ax.bar(dates_linspace, value_per_deposit, width=0.4, tick_label=dates, color=plot_colors)
            # set ticks every week
            ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            # set major ticks format
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        else:
            # Aqui tengo que poner para plotear igualmente espaciado
            bar_container = ax.bar(range(len(value_per_deposit)), value_per_deposit, width=0.4, color=plot_colors)
            ax.set_xticks(range(len(value_per_deposit)), labels=dates, rotation=30, ha='right', fontsize='8')
            #ax.set_xticklabels()

        if visualization_options['percentage'] == OPTIONS_FOR_PERCENT[0]:
            #add_value_label(ax, dates, value_per_deposit)
            ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
            ax.bar_label(bar_container,labels=[f'{x:.2f}%' for x in value_per_deposit],
                         label_type='center', rotation=0, fontsize=9)
        else:
            ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
            ax.bar_label(bar_container, labels=[f'{x:.2f}\N{euro sign}' for x in value_per_deposit],
                         label_type='center', rotation=0, fontsize=9)
        ax.axhline(color='dimgray')

        return True

def list_of_colors_for_barplot(values_list) -> list:
    color_list = []
    for value in values_list:
        if value < 0:
            color_list.append('firebrick')
        else:
            color_list.append('limegreen')
    return color_list


@ticker.FuncFormatter
def major_formatter(x, pos):
    return f'[{x:.2f}]'


def add_value_label(ax: plt.Axes, x_list, y_list):
    for i in range(1, len(x_list)+1):
        ax.text(i, y_list[i-1]/2, f'{y_list[i-1]:.2f}%', ha="center")


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
