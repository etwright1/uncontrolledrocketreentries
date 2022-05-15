from matplotlib import pyplot as plt

fig = plt.figure(figsize=(2.375, 2.375), dpi=300)

ax = fig.add_axes([0,0,1,1])

ax.axis('equal')
states = ['Others', 'Russia','Europe', 'China', 'United States']
risks = [0.0011,  0.0014, 0.0017, 0.0018, 0.004]
colors = ['#6C9AC0','#9382A2', '#C06C84','#F67280','#F8B195']
 
patches, texts, pcts = ax.pie(risks, labels = states, colors=colors, autopct='%1.f%%', normalize=True, startangle=90,
    wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},
    textprops={'fontsize': 7})

plt.setp(pcts, fontweight='bold')

plt.savefig('Figure 1B.svg', bbox_inches='tight')
plt.show()