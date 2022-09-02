from bs4 import BeautifulSoup

import os

outfile_path = "combined_plots.js"
raw_plot_dir = "raw_plots"

for raw_plot_filename in os.listdir(raw_plot_dir):
    with open(f"{raw_plot_dir}/{raw_plot_filename}", "r") as raw_plot_file:
        soup = BeautifulSoup(raw_plot_file.read())
        scriptTag = soup.find_all("script")[0]
        js = scriptTag.text.strip()
        with open(outfile_path, "a") as outfile:
            outfile.write("\n\n\n" + js + "\n\n\n")
