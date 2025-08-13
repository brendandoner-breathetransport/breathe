"""
Creates Figure 2
This figure uses data on mobility measures from multiple copulas found in the
literature. The mobility measures are:
1. Spearman's rank correlation (variable r)
2. Bartholomew's index (variable b)
3. Ave. non-zero absolute jump (variable j)
4. Shorrocks' trace index (variable tr)
The variables are taken from the data file 'copulas_measures.mat'

Each variable has 28 values, based on 28 copulas, in the following order:
1. Denmark 1 (source: Jantti et al (2006))
2. Finland 1 (source: Jantti et al (2006))
3. Germany 1 (source: Eberharter (2014))
4. Norway 1 (source: Jantti et al (2006))
5. Sweden 1 (source: Jantti et al (2006))
6. UK 1 (source: Eberharter (2014))
7. UK 2 (source: Jantti et al (2006))
8. USA 1 (source: Chetty et al (2017))
9. USA 2 (source: Eberharter (2014))
10. USA 3 (source: Jantti et al (2006))
11. Denmark 2 (source: Jantti et al (2006))
12. Denmark 3 (source: Jantti et al (2006))
13. Denmark 4 (source: Jantti et al (2006))
14. Finland 2 (source: Jantti et al (2006))
15. Finland 3 (source: Jantti et al (2006))
16. Finland 4 (source: Jantti et al (2006))
17. Norway 2 (source: Jantti et al (2006))
18. Norway 3 (source: Jantti et al (2006))
19. Norway 4 (source: Jantti et al (2006))
20. Sweden 2 (source: Jantti et al (2006))
21. Sweden 3 (source: Jantti et al (2006))
22. Sweden 4 (source: Jantti et al (2006))
23. UK 3 (source: Jantti et al (2006))
24. UK 4 (source: Jantti et al (2006))
25. UK 5 (source: Jantti et al (2006))
26. USA 4 (source: Jantti et al (2006))
27. USA 5 (source: Jantti et al (2006))
28. USA 6 (source: Jantti et al (2006))
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from scipy.stats import pearsonr

# Clear any existing plots
plt.close('all')

# Load the .mat file
data = scipy.io.loadmat('copulas_measures.mat')

# Extract variables (remove metadata keys that start with '__')
variables = {k: v.flatten() if v.ndim > 1 else v for k, v in data.items() if not k.startswith('__')}
r = variables['r']   # Spearman's rank correlation
b = variables['b']   # Bartholomew's index
j = variables['j']   # Ave. non-zero absolute jump
tr = variables['tr'] # Shorrocks' trace index

# Define colors
grey = [0.5, 0.5, 0.5]
purple = [0.494, 0.184, 0.556]
black = [0, 0, 0]
blue = [0, 0.447, 0.741]
darkred = [0.635, 0.078, 0.184]

# Create figure with subplots
fig = plt.figure(figsize=(15, 12))

# Six top panels - plotting the four measures one against the other
# Subplot 1: Bartholomew's index vs Rank correlation
ax1 = plt.subplot(4, 3, 1)
plt.plot(b, r, 'ko', markersize=7, markerfacecolor=blue, markeredgewidth=2)
rho = pearsonr(b, r)[0]
plt.title(f'ρ={rho:.2f}')
plt.xlabel("Bartholomew's index", fontsize=9)
plt.ylabel('Rank correlation', fontsize=9)
plt.tick_params(labelsize=9)
plt.grid(True, alpha=0.3)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Subplot 2: Ave. non-zero absolute jump vs Rank correlation
ax2 = plt.subplot(4, 3, 2)
plt.plot(j, r, 'ko', markersize=7, markerfacecolor=blue, markeredgewidth=2)
rho = pearsonr(j, r)[0]
plt.title(f'ρ={rho:.2f}')
plt.xlabel('Ave. non-zero absolute jump', fontsize=9)
plt.ylabel('Rank correlation', fontsize=9)
plt.tick_params(labelsize=9)
plt.grid(True, alpha=0.3)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Subplot 3: Shorrocks' trace index vs Rank correlation
ax3 = plt.subplot(4, 3, 3)
plt.plot(tr, r, 'ko', markersize=7, markerfacecolor=blue, markeredgewidth=2)
rho = pearsonr(tr, r)[0]
plt.title(f'ρ={rho:.2f}')
plt.xlabel("Shorrocks' trace index", fontsize=9)
plt.ylabel('Rank correlation', fontsize=9)
plt.tick_params(labelsize=9)
plt.xlim([0.8, 1])
plt.xticks(np.arange(0.8, 1.05, 0.05))
plt.grid(True, alpha=0.3)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Subplot 4: Bartholomew's index vs Shorrocks' trace index
ax4 = plt.subplot(4, 3, 4)
plt.plot(b, tr, 'ko', markersize=7, markerfacecolor=blue, markeredgewidth=2)
rho = pearsonr(b, tr)[0]
plt.title(f'ρ={rho:.2f}')
plt.xlabel("Bartholomew's index", fontsize=9)
plt.ylabel("Shorrocks' trace index", fontsize=9)
plt.tick_params(labelsize=9)
plt.grid(True, alpha=0.3)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

# Subplot 5: Bartholomew's index vs Ave. non-zero absolute jump
ax5 = plt.subplot(4, 3, 5)
plt.plot(b, j, 'ko', markersize=7, markerfacecolor=blue, markeredgewidth=2)
rho = pearsonr(b, j)[0]
plt.title(f'ρ={rho:.2f}')
plt.xlabel("Bartholomew's index", fontsize=9)
plt.ylabel('Ave. non-zero absolute jump', fontsize=9)
plt.tick_params(labelsize=9)
plt.grid(True, alpha=0.3)
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)

# Subplot 6: Shorrocks' trace index vs Ave. non-zero absolute jump
ax6 = plt.subplot(4, 3, 6)
plt.plot(tr, j, 'ko', markersize=7, markerfacecolor=blue, markeredgewidth=2)
rho = pearsonr(tr, j)[0]
plt.title(f'ρ={rho:.2f}')
plt.xlabel("Shorrocks' trace index", fontsize=9)
plt.ylabel('Ave. non-zero absolute jump', fontsize=9)
plt.tick_params(labelsize=9)
plt.xlim([0.8, 1])
plt.xticks(np.arange(0.8, 1.05, 0.05))
plt.grid(True, alpha=0.3)
ax6.spines['top'].set_visible(False)
ax6.spines['right'].set_visible(False)

# Bottom panel - load results data
results_data = scipy.io.loadmat('figure2_results.mat')
results_vars = {k: v for k, v in results_data.items() if not k.startswith('__')}

# Extract variables from results
abs_mobility = results_vars['abs_mobility'].flatten()
results = results_vars['results']
years = np.arange(1940, 1981)  # Assuming years 1940-1980
years_mobility = results_vars.get('years_mobility', years).flatten()

# Bottom subplot spanning multiple positions
ax7 = plt.subplot(4, 3, (7, 12))

# Create filled area for min/max range
results_percent = 100 * results
min_results = np.min(results_percent, axis=0)
max_results = np.max(results_percent, axis=0)
mean_results = np.mean(results_percent, axis=0)

# Fill between min and max
plt.fill_between(years, min_results, max_results, color=blue, alpha=0.2)

# Plot the main lines
h1 = plt.plot(years_mobility, abs_mobility, 'ok-', markersize=6, 
              markerfacecolor='k', linewidth=2, label='Chetty et al.')
h2 = plt.plot(years, mean_results, '-.', color=blue, linewidth=3, 
              label='Average of empirical copulas estimates')

plt.xlim([1940, 1980])
plt.legend(frameon=False)
plt.ylabel('Pct. of children earning more than their parents', fontsize=9)
plt.xlabel('Cohort', fontsize=9)
plt.tick_params(labelsize=9)
plt.ylim([50, 100])
plt.grid(True, axis='y', alpha=0.3)
ax7.spines['top'].set_visible(False)
ax7.spines['right'].set_visible(False)

# Adjust layout and save
plt.tight_layout()
plt.subplots_adjust(hspace=0.4, wspace=0.3)

# Save the figure in multiple formats
plt.savefig('figure2.jpg', dpi=1200, bbox_inches='tight', facecolor='white')
plt.savefig('figure2.pdf', bbox_inches='tight', facecolor='white')
plt.savefig('figure2.eps', bbox_inches='tight', facecolor='white')

plt.show()
plt.close('all')

print("Figure 2 has been created and saved in JPG, PDF, and EPS formats.")