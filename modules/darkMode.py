# Combines all of the dark mode plotting into a single function.
def darkPlot(axName, backgroundColor, axisColor):
    axName.set(facecolor=backgroundColor)
    axName.spines['bottom'].set_color(axisColor)
    axName.spines['top'].set_color(axisColor) 
    axName.spines['right'].set_color(axisColor)
    axName.spines['left'].set_color(axisColor)
    axName.tick_params(axis='x', colors=axisColor)
    axName.tick_params(axis='y', colors=axisColor, which='both')
    axName.yaxis.label.set_color(axisColor)
    axName.xaxis.label.set_color(axisColor)
    axName.title.set_color(axisColor)

    return axName