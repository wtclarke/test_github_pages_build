import matplotlib.pyplot as plt
import json
from jinja2 import Environment, FileSystemLoader
import numpy as np
from pathlib import Path

# Output for html/figure
output = Path('html')
output.mkdir(exist_ok=True)
output_fig = output / 'figures'
output_fig.mkdir(exist_ok=True)

# Read control file
json_file = Path('input/plot_ctrl.json')
with open(json_file) as jsonfp:
    plt_ctrl = json.load(jsonfp)

# create plot
x = np.linspace(plt_ctrl['x'][0], plt_ctrl['x'][1], 21)
y = np.polyval(plt_ctrl['y'], x)
fig = plt.figure(figsize=(5, 5))
plt.plot(x, y)
fig.savefig(output_fig / 'fig1.svg', format='svg', bbox_inches='tight', pad_inches=0.0)
plt.close()

# Build pages
environment = Environment(loader=FileSystemLoader("templates/"))

template = environment.get_template("plot_page.html")
content = template.render(
    poly_coeffs=', '.join([str(x) for x in plt_ctrl['y']]),
    poly_plot='figures/fig1.svg'
)
with open(output / 'plot_page.html', mode="w", encoding="utf-8") as message:
    message.write(content)

template = environment.get_template("menu_page.html")
content = template.render(
    figure_page_name='Plot page: (' + ', '.join([str(x) for x in plt_ctrl['y']]) + ')'
)
with open(output / 'menu_page.html', mode="w", encoding="utf-8") as message:
    message.write(content)
