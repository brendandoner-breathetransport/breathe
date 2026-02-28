"""
Creates Figure H.1 - counterfactual calculations of absolute mobility in a
group of advanced economies. This script creates the plot using
'counterfactuals.mat'. This script also produces the results presented in
Table H.2 using the same data and the same calculation.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from mobility_decompose import mobility_decompose  # Import the function we created earlier

# Clear any existing plots
plt.close('all')

# Load data from MATLAB file
data = loadmat('counterfactuals.mat')

# Extract country data
AS = data['AS']
CA = data['CA']
DK = data['DK']
FI = data['FI']
FR = data['FR']
JP = data['JP']
NO = data['NO']
SW = data['SW']
UK = data['UK']
US = data['US']

# Create figure with subplots
fig, axes = plt.subplots(5, 2, figsize=(8.75, 9.88))
fig.patch.set_facecolor('white')

def plot_country(ax, country_data, title, start_year=None):
    """Helper function to plot country data"""
    
    if start_year is not None:
        # Filter data for countries that start later than 1940
        if title in ['France', 'Sweden', 'United States']:
            idx = country_data[:, 0] >= start_year
            plot_data = country_data[idx, :]
            baseline_idx = np.where(country_data[:, 0] == start_year)[0][0]
        elif title == 'Japan':
            idx = country_data[:, 0] >= 1947
            plot_data = country_data[idx, :]
            baseline_idx = np.where(country_data[:, 0] == 1947)[0][0]
        else:
            plot_data = country_data
            baseline_idx = 0
    else:
        plot_data = country_data
        baseline_idx = 0
    
    # Handle NaN values (Finland case)
    if title == 'Finland':
        valid_idx = ~np.isnan(country_data[:, 1])
        plot_data = country_data[valid_idx, :]
        baseline_idx = 0
    
    # Plot three lines
    h1 = ax.plot(plot_data[:, 0], 100 * plot_data[:, 1] / country_data[baseline_idx, 1], 
                 'k-', linewidth=3, label='Baseline')
    h2 = ax.plot(plot_data[:, 0], 100 * plot_data[:, 2] / country_data[baseline_idx, 2], 
                 '-', color=[0.6, 0.6, 0.6], linewidth=3, label='Fixed inequality')
    h3 = ax.plot(plot_data[:, 0], 100 * plot_data[:, 3] / country_data[baseline_idx, 3], 
                 '-', color=[0.2, 0.3, 0.7], linewidth=3, label='Fixed income growth')
    
    # Set plot properties
    ax.grid(True)
    ax.set_xlim([1940, 1985])
    ax.set_ylim([50, 110])
    ax.set_xticks(range(1900, 2001, 10))
    ax.set_yticks(range(0, 201, 10))
    ax.tick_params(labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('Cohort', fontsize=8)
    ax.set_ylabel('Abs. mobility, first cohort = 100%', fontsize=8)
    ax.set_title(title)
    
    # Add legend only to first subplot
    if title == 'Australia':
        ax.legend(loc='southwest', frameon=False)
    
    return plot_data

# Plot each country
countries = [
    (AS, 'Australia', None),
    (CA, 'Canada', None),
    (DK, 'Denmark', None),
    (FI, 'Finland', None),
    (FR, 'France', 1940),
    (JP, 'Japan', 1947),
    (NO, 'Norway', None),
    (SW, 'Sweden', 1940),
    (UK, 'United Kingdom', None),
    (US, 'United States', 1940)
]

for i, (country_data, title, start_year) in enumerate(countries):
    ax = axes[i//2, i%2]
    plot_data = plot_country(ax, country_data, title, start_year)
    
    # Calculate and print mobility decomposition
    if start_year is not None:
        if title == 'Japan':
            decomp_data = country_data[country_data[:, 0] >= 1947, :]
        else:
            decomp_data = country_data[country_data[:, 0] >= start_year, :]
    elif title == 'Finland':
        # Handle NaN values for Finland
        valid_idx = ~np.isnan(country_data[:, 1])
        decomp_data = country_data[valid_idx, :]
    else:
        decomp_data = country_data
    
    result = mobility_decompose(decomp_data)
    print(f'{title}: {np.round(result, 1)}')

# Adjust layout and save
plt.tight_layout()
plt.savefig('figureH1.jpg', dpi=1200, bbox_inches='tight')
plt.savefig('figureH1.pdf', bbox_inches='tight')
plt.savefig('figureH1.eps', bbox_inches='tight')
plt.show()

# Clear variables (Python garbage collection handles this automatically)
plt.close('all')