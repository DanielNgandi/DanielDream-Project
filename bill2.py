import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

# Coefficients from your regression analysis
intercept = 1.200
design_coeff = 0.500
market_coeff = -0.150
pricing_coeff = 0.250
technology_coeff = 0.450

# Generate hypothetical data for the example
np.random.seed(42)  # for reproducibility
sample_size = 100
design_preferences = np.linspace(-2, 2, sample_size)  # Vary design preferences
market_trends = np.linspace(-2, 2, sample_size)  # Vary market trends
pricing_considerations = np.linspace(-2, 2, sample_size)  # Vary pricing considerations

# Calculate predicted values for each factor
predicted_design = intercept + design_coeff * design_preferences
predicted_market = intercept + market_coeff * market_trends
predicted_pricing = intercept + pricing_coeff * pricing_considerations

# Hypothetical residuals for illustration
residuals = np.random.randn(sample_size)

# Line Fit Plot for Design Preferences
plt.figure(figsize=(15, 6))
plt.subplot(1, 3, 1)
stats.probplot(residuals, dist="norm", plot=plt)
plt.title("Normal Probability Plot of Residuals")

# Line Fit Plot for Design Preferences
plt.subplot(1, 3, 2)
plt.scatter(predicted_design, residuals, alpha=0.7)
plt.axhline(y=0, color='r', linestyle='--', linewidth=2)
plt.title("Line Fit Plot of Residuals for Design Preferences")
plt.xlabel("Predicted Intentions")
plt.ylabel("Residuals")

# Line Fit Plot for Market Trends
plt.subplot(1, 3, 3)
plt.scatter(predicted_market, residuals, alpha=0.7)
plt.axhline(y=0, color='r', linestyle='--', linewidth=2)
plt.title("Line Fit Plot of Residuals for Market Trends")
plt.xlabel("Predicted Intentions")
plt.ylabel("Residuals")

# Additional Line Fit Plot for Pricing Considerations
plt.figure(figsize=(6, 6))
plt.scatter(predicted_pricing, residuals, alpha=0.7)
plt.axhline(y=0, color='r', linestyle='--', linewidth=2)
plt.title("Line Fit Plot of Residuals for Pricing Considerations")
plt.xlabel("Predicted Intentions")
plt.ylabel("Residuals")

plt.tight_layout()
plt.show()
