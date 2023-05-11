import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import os

DestDir='/home/febinps/OpticalMemoryTrace/NVMainRuns/Analysis/'
MemoryCOnfigs= ['3D_DRAM', '2D_DRAM', 'PCM_ISSCC', 'COSMOS_EPCM', 'COSMOS_OPCM', 'COSMOS_OPCM_TE', 'ICCAD2023-Am-Res','ICCAD2023-Cr-Res']
AverageLatency=[]
AvgBandWidth=[]
RdThroughput=[]
WrThroughput=[]
EPB=[]
fileno=0
for Analysis_file in MemoryCOnfigs:
    fileno=fileno+1
    appName =[]
    with open(DestDir+Analysis_file, 'r') as f:
        for line in f:
            Line = line.split(",")
            appName.append(Line[0])
            AverageLatency.append(float(Line[1]))
            AvgBandWidth.append(float(Line[2]))
            EPB.append(float(Line[5]))
    print(len(appName))

spacing=[-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3]
colors = ['indigo','lavender','plum','red','orange','azure']
labels= MemoryCOnfigs #sorted(os.listdir(DestDir))
colors = ['indigo','lavender','plum','red','orange','xkcd:azure','xkcd:pink','xkcd:wheat']

for i in range(0,fileno):
    print(len(AverageLatency[i::len(appName)]))

fig, ax =plt.subplots()

for i in range(0,fileno):
    if (i+1)*len(appName) < len(AverageLatency):
        ax.bar(np.arange(len(appName))+spacing[i],AverageLatency[i*len(appName):(i+1)*len(appName)],width=0.1,align='center',
        color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)
    else:
        ax.bar(np.arange(len(appName))+spacing[i],AverageLatency[i*len(appName)::],width=0.1,align='center',
        color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)

#ax.set_ylim([0.5,1])
ax.set_xticks(np.arange(len(appName)))
ax.set_xticklabels(appName,fontsize='15',weight ='bold')
ax.set_ylabel('Average latency values', fontsize='30',weight ='bold') 
ax.legend(ncol=4,loc ='upper left',bbox_to_anchor=(-0.01,1.15),fontsize='20')#,mode='expand')
#plt.legend(loc=1, fontsize = 'x-large')
#plt.title('EPB Analysis: Aggressive values',fontsize='40',weight ='bold')
fig.tight_layout()
plt.yscale('log')
plt.xticks(rotation=30,horizontalalignment='right')
plt.yticks(fontsize='25')
plt.show()

fig, ax =plt.subplots()

for i in range(0,fileno):
    if (i+1)*len(appName) < len(AvgBandWidth):
        ax.bar(np.arange(len(appName))+spacing[i],AvgBandWidth[i*len(appName):(i+1)*len(appName)],width=0.1,align='center',
        color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)
    else:
        ax.bar(np.arange(len(appName))+spacing[i],AvgBandWidth[i*len(appName)::],width=0.1,align='center',
        color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)

#ax.set_ylim([0.5,1])
ax.set_xticks(np.arange(len(appName)))
ax.set_xticklabels(appName,fontsize='15',weight ='bold')
ax.set_ylabel('Average Bandwithd (MBps)', fontsize='30',weight ='bold') 
ax.legend(ncol=4,loc ='upper left',bbox_to_anchor=(-0.01,1.15),fontsize='20')#,mode='expand')
#plt.legend(loc=1, fontsize = 'x-large')
#plt.title('EPB Analysis: Aggressive values',fontsize='40',weight ='bold')
fig.tight_layout()
plt.yscale('log')
plt.xticks(rotation=30,horizontalalignment='right')
plt.yticks(fontsize='25')
plt.show()

fig, ax =plt.subplots()

for i in range(0,fileno):
    if (i+1)*len(appName) < len(EPB):
        ax.bar(np.arange(len(appName))+spacing[i],EPB[i*len(appName):(i+1)*len(appName)],width=0.1,align='center',
        color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)
    else:
        ax.bar(np.arange(len(appName))+spacing[i],EPB[i*len(appName)::],width=0.1,align='center',
        color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)

#ax.set_ylim([0.5,1])
ax.set_xticks(np.arange(len(appName)))
ax.set_xticklabels(appName,fontsize='15',weight ='bold')
ax.set_ylabel('EPB values (J/bit)', fontsize='30',weight ='bold') 
ax.legend(ncol=4,loc ='upper left',bbox_to_anchor=(-0.01,1.15),fontsize='20')#,mode='expand')
#plt.legend(loc=1, fontsize = 'x-large')
#plt.title('EPB Analysis: Aggressive values',fontsize='40',weight ='bold')
fig.tight_layout()
plt.yscale('log')
plt.xticks(rotation=30,horizontalalignment='right')
plt.yticks(fontsize='25')
plt.show()

# DestDir='/home/febin/Linux2/OpticalMemoryTrace/NVMainRuns/RWAnalysis/'
# for Analysis_file in sorted(os.listdir(DestDir)):
#     with open(DestDir+Analysis_file, 'r') as f:
#         for line in f:
#             Line = line.split(",")
#             if 'Read' in Line[0]:
#                 RdThroughput.append(float(Line[2]))
#             elif 'Write' in Line[0]:
#                 WrThroughput.append(float(Line[2]))

# RdThroughput = np.array(RdThroughput)
# WrThroughput = np.array(WrThroughput)

# colors = ['xkcd:indigo','xkcd:lavender','xkcd:plum','xkcd:red','xkcd:orange','xkcd:azure']

# fig, ax =plt.subplots()

# ax.bar(np.arange(len(labels)), RdThroughput/1024, color=colors, edgecolor='black')
# ax.set_ylabel('Read Throughput(GBps)', fontsize='30',weight ='bold') 
# plt.xticks(np.arange(len(labels)), labels, fontsize='20',rotation=30,horizontalalignment='right')
# plt.yticks(fontsize='25')

# plt.show()

# fig, ax =plt.subplots()

# ax.bar(np.arange(len(labels)), WrThroughput/1024, color=colors, edgecolor='black')
# ax.set_ylabel('Write Throughput (GBps)', fontsize='30',weight ='bold') 
# plt.xticks(np.arange(len(labels)), labels, fontsize='20',rotation=30,horizontalalignment='right')
# plt.yticks(fontsize='25')

# plt.show()