"""
Creates Figure 3 - The sensitivity of absolute mobility to the rank correlation in various simulated scenarios
This figure requires no input file
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def gaussian_rhoc(rho):
    """
    Convert rank correlation to gaussian copula correlation
    rc = (6/pi) * arcsin(rho/2)
    """
    return (6/np.pi) * np.arcsin(rho/2)

def absmob_logn(g, s1, s2, rho):
    """
    Implements the bivariate log-normal model. Gets income growth, top
    10% income shares and intergenerational correlation as input and
    calculates the resulting absolute mobility
    
    Parameters:
    g: income growth rate (%)
    s1: top 10% income share for parent generation (%)
    s2: top 10% income share for child generation (%)
    rho: intergenerational correlation coefficient
    
    Returns:
    Absolute mobility probability
    """
    # Convert percentages to decimals
    g = g / 100
    s1 = s1 / 100
    s2 = s2 / 100
    
    # Calculate standard deviations from income shares
    # Using inverse normal distribution
    sig1 = norm.ppf(0.9) - norm.ppf(1 - s1)
    sig2 = norm.ppf(0.9) - norm.ppf(1 - s2)
    
    # Calculate means
    mu1 = 0
    mu2 = np.log(1 + g) + sig1**2/2 - sig2**2/2
    
    # Calculate absolute mobility using normal CDF
    numerator = mu2 - mu1
    denominator = np.sqrt(sig1**2 + sig2**2 - 2*rho*sig1*sig2)
    
    A = norm.cdf(numerator / denominator)
    
    return A

# Clear any existing plots
plt.close('all')

# Define rho range
rhoo = np.arange(0, 1.01, 0.01)

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Case A: Sharp decrease in inequality
ax1 = axes[0, 0]
h1 = ax1.plot(gaussian_rhoc(rhoo), 100*absmob_logn(10, 50, 30, rhoo), 
              ':k', linewidth=2, label='10% growth')
h2 = ax1.plot(gaussian_rhoc(rhoo), 100*absmob_logn(50, 50, 30, rhoo), 
              color=[0.5, 0.5, 0.5], linewidth=2, label='50% growth')
h3 = ax1.plot(gaussian_rhoc(rhoo), 100*absmob_logn(100, 50, 30, rhoo), 
              '-.k', linewidth=2, label='100% growth')
h4 = ax1.plot(gaussian_rhoc(rhoo), 100*absmob_logn(400, 50, 30, rhoo), 
              '--', color=[0, 0.4470, 0.7410], linewidth=2, label='400% growth')

ax1.set_ylim([0, 100])
ax1.set_xticks(np.arange(0, 1.1, 0.1))
ax1.set_yticks(np.arange(0, 101, 10))
ax1.legend(loc='lower right', fontsize=10, frameon=False)
ax1.set_title('A: Sharp decrease in inequality')
ax1.set_ylabel('Absolute mobility (%)')
ax1.set_xlabel('Rank correlation')
ax1.annotate('Mid-century US', xy=(0.23, 86.4), xytext=(0.2, 78),
             arrowprops=dict(arrowstyle='->', color='black'), fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Case B: No change in inequality
ax2 = axes[0, 1]
h1 = ax2.plot(gaussian_rhoc(rhoo), 100*absmob_logn(10, 30, 30, rhoo), 
              ':k', linewidth=2, label='10% growth')
h2 = ax2.plot(gaussian_rhoc(rhoo), 100*absmob_logn(50, 30, 30, rhoo), 
              color=[0.5, 0.5, 0.5], linewidth=2, label='50% growth')
h3 = ax2.plot(gaussian_rhoc(rhoo), 100*absmob_logn(100, 30, 30, rhoo), 
              '-.k', linewidth=2, label='100% growth')
h4 = ax2.plot(gaussian_rhoc(rhoo), 100*absmob_logn(400, 30, 30, rhoo), 
              '--', color=[0, 0.4470, 0.7410], linewidth=2, label='400% growth')

ax2.set_ylim([0, 100])
ax2.set_xticks(np.arange(0, 1.1, 0.1))
ax2.set_yticks(np.arange(0, 101, 10))
ax2.legend(loc='lower right', fontsize=10, frameon=False)
ax2.set_title('B: No change in inequality')
ax2.set_ylabel('Absolute mobility (%)')
ax2.set_xlabel('Rank correlation')
ax2.annotate('Late 20th century France', xy=(0.24, 27), xytext=(0.30, 21),
             arrowprops=dict(arrowstyle='->', color='black'), fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Case C: Mild increase in inequality
ax3 = axes[1, 0]
h1 = ax3.plot(gaussian_rhoc(rhoo), 100*absmob_logn(10, 30, 35, rhoo), 
              ':k', linewidth=2, label='10% growth')
h2 = ax3.plot(gaussian_rhoc(rhoo), 100*absmob_logn(50, 30, 35, rhoo), 
              color=[0.5, 0.5, 0.5], linewidth=2, label='50% growth')
h3 = ax3.plot(gaussian_rhoc(rhoo), 100*absmob_logn(100, 30, 35, rhoo), 
              '-.k', linewidth=2, label='100% growth')
h4 = ax3.plot(gaussian_rhoc(rhoo), 100*absmob_logn(400, 30, 35, rhoo), 
              '--', color=[0, 0.4470, 0.7410], linewidth=2, label='400% growth')

ax3.set_ylim([0, 100])
ax3.set_xticks(np.arange(0, 1.1, 0.1))
ax3.set_yticks(np.arange(0, 101, 10))
ax3.legend(loc='lower left', fontsize=10, frameon=False)
ax3.set_title('C: Mild increase in inequality')
ax3.set_ylabel('Absolute mobility (%)')
ax3.set_xlabel('Rank correlation')
ax3.grid(True, alpha=0.3)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Case D: Sharp increase in inequality
ax4 = axes[1, 1]
h1 = ax4.plot(gaussian_rhoc(rhoo), 100*absmob_logn(10, 30, 45, rhoo), 
              ':k', linewidth=2, label='10% growth')
h2 = ax4.plot(gaussian_rhoc(rhoo), 100*absmob_logn(50, 30, 45, rhoo), 
              color=[0.5, 0.5, 0.5], linewidth=2, label='50% growth')
h3 = ax4.plot(gaussian_rhoc(rhoo), 100*absmob_logn(100, 30, 45, rhoo), 
              '-.k', linewidth=2, label='100% growth')
h4 = ax4.plot(gaussian_rhoc(rhoo), 100*absmob_logn(400, 30, 45, rhoo), 
              '--', color=[0, 0.4470, 0.7410], linewidth=2, label='400% growth')

ax4.set_ylim([0, 100])
ax4.set_xticks(np.arange(0, 1.1, 0.1))
ax4.set_yticks(np.arange(0, 101, 10))
ax4.legend(loc='lower left', fontsize=10, frameon=False)
ax4.set_title('D: Sharp increase in inequality')
ax4.set_ylabel('Absolute mobility (%)')
ax4.set_xlabel('Rank correlation')
ax4.annotate('Late 20th century Australia', xy=(0.65, 32), xytext=(0.68, 36),
             arrowprops=dict(arrowstyle='->', color='black'), fontsize=10)
ax4.grid(True, alpha=0.3)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

# Adjust layout
plt.tight_layout()

# Save the figure in multiple formats
plt.savefig('figure3.jpg', dpi=1200, bbox_inches='tight', facecolor='white')
plt.savefig('figure3.pdf', bbox_inches='tight', facecolor='white')
plt.savefig('figure3.eps', bbox_inches='tight', facecolor='white')

plt.show()
plt.close('all')

print("Figure 3 has been created and saved in JPG, PDF, and EPS formats.")
print("\nThe script now uses the correct gaussian_rhoc() and absmob_logn() function implementations.")