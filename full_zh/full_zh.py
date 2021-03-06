import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import datetime
import sys

if len(sys.argv) < 2:
    mydate = datetime.datetime.now()
    date = mydate.strftime("%G_%B")
else:
    date = sys.argv[1]

love = int(input('Put love: '))
money = int(input('Put money: '))
hobby = int(input('Put hobby: '))
friends = int(input('Put friends: '))
health = int(input('Put health: '))
job = int(input('And job, finally: '))
# Set data
df = pd.DataFrame({
    'group': ['A'],
    'Л': [love],
    'Б': [money],
    'Х': [hobby],
    'Д': [friends],
    'З': [health],
    'Р': [job]
})

# ------- PART 1: Create background

# number of variable
categories = list(df)[1:]
N = len(categories)

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)

# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], color="grey", size=7)
plt.ylim(0, 10)

# ------- PART 2: Add plots

# Plot each individual = each line of the data
# I don't do a loop, because plotting more than 3 groups makes the chart unreadable

# Ind1
values = df.loc[0].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label=date[5:])
ax.fill(angles, values, 'b', alpha=0.1)

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

name = date + '_polnaya_zh.png'
fig.savefig(name)
