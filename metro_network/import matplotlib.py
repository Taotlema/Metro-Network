import matplotlib.pyplot as plt

# Data
categories = ['Tuition and Fees', 'Living Expenses', 'Taxes', 'Part-time Earnings']
amounts = [63440, 40800, 6730, -38400]

# Plot
fig, ax = plt.subplots()
bars = ax.bar(categories, amounts, color=['red', 'red', 'red', 'green'])

# Add labels
ax.set_ylabel('Amount ($)')
ax.set_title('2-Year cmFinancial Summary')

# Adding the data labels on the bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom')

plt.show()