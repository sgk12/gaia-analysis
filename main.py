from astroquery.gaia import Gaia

import matplotlib.pyplot as plt
from astropy.table import Table
import pandas as pd
import numpy as np

# TO IMPORT IN GAIA DATA: UNCOMMENT THE FOLLOWING

#query = """SELECT 
#gaia.source_id, gaia.bp_g, gaia.g_rp, gaia.bp_rp, gaia.classprob_dsc_combmod_star
#FROM gaiadr3.gaia_source AS gaia
#"""

""" job = Gaia.launch_job_async(query)
results = job.get_results()

filename1 = 'magnitude_diffs.fits'
results.write(filename1, overwrite=True) """


# PARSE DATA

filename1 = 'magnitude_diffs.fits'

results_diffs = Table.read(filename1)
diffs_df = results_diffs.to_pandas()

diffs_df = diffs_df.dropna()
print(diffs_df.describe(), "hi")

diffs_df = diffs_df.sort_values(by=['bp_g'])

split_copy = diffs_df.copy(deep=True)
arrs = np.array_split(split_copy, 4)

# PLOT + DISPLAY DATA

for a in arrs:
    a = a.sort_values(by=['bp_g'])
    print(a.head())

fig, axs = plt.subplots(2, 3)
fig.suptitle('BP-G vs. G-RP Magnitudes in GAIA Catalog of Nearby Stars')

arr_pos = 0

quartiles = ['First', 'Second', 'Third', 'Fourth']

for i in range(2):
    for j in range(2):
        a = arrs[arr_pos]
        x = a['bp_g'] # similar to b-v, hot --> cool
        y = a['g_rp'] 
        axs[i, j].plot(x, y, 'ko', markersize=0.02, alpha=0.1)
        axs[i, j].set_title((quartiles[arr_pos] + " quartile probability of single stars"), fontsize=6)
        axs[i, j].set_xlim([-6, 6])
        axs[i, j].set_ylim([-6, 6])
        arr_pos += 1

x = diffs_df['bp_g']
y = diffs_df['g_rp']
axs[0, 2].plot(x, y, 'ko', markersize=0.02, alpha=0.1)
axs[0, 2].set_title(("Cumulative spectra data"), fontsize=6)

axs[1, 0].set_xlabel('Difference in flux b/w BP & G bands', fontsize=5)
axs[0, 0].set_ylabel('Difference in flux b/w G & RP bands', fontsize=5) # working

axs[-1, -1].axis('off')

for ax in axs.flat:
    ax.label_outer()

plt.show()
