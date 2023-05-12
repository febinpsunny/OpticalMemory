import os
import sys
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math
from alive_progress import alive_bar

#MemoryCOnfigs= ['3D_DRAM', '2D_DRAM', 'PCM_ISSCC', 'COSMOS_EPCM', 'COSMOS_OPCM', 'COSMOS_OPCM_TO',
#                'ICCAD2023-Am-Res-1b','ICCAD2023-Cr-Res-1b','ICCAD2023-Am-Res-2b','ICCAD2023-Cr-Res-2b','ICCAD2023-Am-Res-4b','ICCAD2023-Cr-Res-4b']
#CycleTime = [1.3e9, 666e6, 400e6, 1e9, 1e9, 400e6,1e9, 1e9, 1e9, 1e9, 1e9, 1e9]

MemoryCOnfigs=['ICCAD2023-Am-Res-1b','ICCAD2023-Cr-Res-1b','ICCAD2023-Am-Res-2b','ICCAD2023-Cr-Res-2b','ICCAD2023-Am-Res-4b','ICCAD2023-Cr-Res-4b']
CycleTime = [1e9, 1e9, 1e9, 1e9, 1e9, 1e9]

PlotConfigs=['ICCAD2023-Am-Res-1b','ICCAD2023-Cr-Res-1b','ICCAD2023-Am-Res-2b','ICCAD2023-Cr-Res-2b','ICCAD2023-Am-Res-4b','ICCAD2023-Cr-Res-4b']

PlotDict ={'3D_DRAM':'indigo', '2D_DRAM':'lavender', 'PCM_ISSCC':'plum', 'COSMOS_EPCM':'red', 'COSMOS_OPCM':'orange', 'COSMOS_OPCM_TO':'xkcd:azure',
           'ICCAD2023-Am-Res-1b':'xkcd:pumpkin','ICCAD2023-Cr-Res-1b':'xkcd:light rose','ICCAD2023-Am-Res-2b':'xkcd:wheat','ICCAD2023-Cr-Res-2b':'xkcd:pink',
           'ICCAD2023-Am-Res-4b':'xkcd:eggshell','ICCAD2023-Cr-Res-4b':'xkcd:merlot'}

OutDir='/home/febinps/OpticalMemoryTrace/NVMainRuns/Outputs/'
DestDir='/home/febinps/OpticalMemoryTrace/NVMainRuns/Analysis/'

TraceDir='/home/febinps/OpticalMemoryTrace/Traces/'
ConfigDir='/home/febinps/OpticalMemoryTrace/NVMainRuns/Configs/'
R_W_Traces='/home/febinps/OpticalMemoryTrace/R_W_Traces/'
RWOutputs='/home/febinps/OpticalMemoryTrace/NVMainRuns/RWOutputs/'
RWAnalysis='/home/febinps/OpticalMemoryTrace/NVMainRuns/RWAnalysis/'

nvmainBinary='/home/febinps/NVmain/nvmain.prof'


def SimulationRuns(runCyc="100000"):
    print("Performing NVMain simulations on the main memory configurations using traces")

    for config in MemoryCOnfigs:
        for OldOutput in os.listdir(OutDir):
            if config in OldOutput:
                os.remove(os.path.join(OutDir, OldOutput))

    MaxProgressbarVal = len(MemoryCOnfigs)*(len(os.listdir(TraceDir))-8)
    runCycles=runCyc

    with alive_bar(MaxProgressbarVal) as bar:
        for config in MemoryCOnfigs:
            print(config)
            for trace in os.listdir(TraceDir):
                if '.milc' in trace or '.soplex' in trace or '.lbm' in trace or '.mcf' in trace or '.leslie3d' in trace or '.zeusmp' in trace or '.txt' in trace or '.wrf' in trace:
                    continue
                else:
                    bar()
                    cmd=nvmainBinary+" "+ConfigDir+config+".config "+TraceDir+trace+" "+runCycles+" >>"+OutDir+config+"_"+trace
                    os.system(cmd)
def RWSimRuns(runCyc="100000"):
    print("Performing NVMain Read/Write throughput simulations on the main memory configurations")
    os.system("rm "+RWOutputs+"*")
    MaxProgressbarVal = len(MemoryCOnfigs)*len(os.listdir(R_W_Traces))
    runCycles=runCyc
    with alive_bar(MaxProgressbarVal) as bar:
        for config in MemoryCOnfigs:
            print(config)
            for trace in os.listdir(R_W_Traces):
                bar()
                cmd=nvmainBinary+" "+ConfigDir+config+".config "+R_W_Traces+trace+" "+runCycles+" >>"+RWOutputs+config+"_"+trace
                os.system(cmd)
            

def MemAnalysis():
    print("Performing analysis on the NVMain simulation outputs")
    CPUFreq = 1e9  
    PktSize=128
    TotalWrites=0
    TotalReads=0
    AvgBandWidth=0
    SimCycles=0
    TotalEnergyConsumption=0
    AverageLatency=0

    for config in MemoryCOnfigs:
        for OldOutput in os.listdir(DestDir):
            if config in OldOutput:
                os.remove(os.path.join(DestDir, OldOutput))

    for Output in sorted(os.listdir(OutDir)):
        appName=Output.split("_")[-1]
        BW_count=0
        BW=0
        AverageLatency=0
        CycTime=0

        for name, cyc in zip(MemoryCOnfigs,CycleTime):
            if name in Output:
                CycTime=1/cyc
                FilePath=DestDir+name

        if CycTime!=0:
            TotalReads=0
            TotalWrites=0
            with open(OutDir+Output,'r') as Outfile:
                if '.milc' in Output or '.soplex' in Output or '.lbm' in Output or '.mcf' in Output or '.leslie3d' in Output or '.zeusmp' in Output or '.txt' in Output or '.wrf' in Output:
                    continue
                else:
                    for line in Outfile:
                        if '.reads' in line:
                            TotalReads += int(line.split()[1])
                        if '.writes' in line:
                            TotalWrites += int(line.split()[1])
                        if 'simCycles' in line:
                            SimCycles = int(line.split()[3])
                        if 'bandwidth' in line:
                            bw = ''.join(c for c in line.split()[1] if c in '0123456789.+-e')
                            if bw == '-':
                                BW += 0.0
                            else:
                                BW += float(bw)
                            BW_count+=1
                        if 'totalEnergy' in line:
                            te = ''.join(c for c in line.split()[1] if c in '0123456789.+-e')
                            if te == '-':
                                TotalEnergyConsumption = 0
                            else:
                                if 'DRAM' in Output:
                                    TotalEnergyConsumption = float(''.join(c for c in line.split()[1] if c in '0123456789.+-e'))*CycTime*9e-3 
                                    #DRAMs calculate energy in mA*t and hence need this further modification
                                else:
                                    TotalEnergyConsumption = float(''.join(c for c in line.split()[1] if c in '0123456789.+-e'))*CycTime
                        if 'WaitAverage' in line or 'averageLatency' in line:
                            al = ''.join(c for c in line.split()[1] if c in '0123456789.')
                            if al == '':
                                AverageLatency += 0
                            else:
                                AverageLatency += float(''.join(c for c in line.split()[1] if c in '0123456789.'))*CycTime
            simTime = SimCycles/CPUFreq
            AvgBandWidth = BW/BW_count
            EPB = TotalEnergyConsumption*SimCycles/((TotalReads+TotalWrites)*PktSize)
            RdThroughput = TotalReads*PktSize/(10e9*simTime)
            WrThroughput = TotalWrites*PktSize/(10e9*simTime)
            with open(FilePath, 'a', newline='') as file:
                writer = csv.writer(file)
                row = [appName,AverageLatency,AvgBandWidth,RdThroughput,WrThroughput,EPB]
                writer.writerow(row)


def RWMemAnalysis():
    print("Performing analysis on the Read/Write simulation outputs")
    CPUFreq = 1e9  
    PktSize=128

    for config in MemoryCOnfigs:
        for OldOutput in os.listdir(RWAnalysis):
            if config in OldOutput:
                os.remove(os.path.join(RWAnalysis, OldOutput))

    for Output in sorted(os.listdir(RWOutputs)):
        appName=Output.split("_")[-1]
        BW_count=0
        BW=0
        AverageLatency=0

        for name, cyc in zip(MemoryCOnfigs,CycleTime):
            if name in Output:
                CycTime=1/cyc
                FilePath=RWAnalysis+name
        
        with open(RWOutputs+Output,'r') as Outfile:
            for line in Outfile:
                if 'totalReadRequests' in line:
                    TotalReads = int(line.split()[1])
                if 'totalWriteRequests' in line:
                    TotalWrites = int(line.split()[1])
                if 'simCycles' in line:
                    SimCycles = int(line.split()[3])
                if 'bandwidth' in line:
                    bw = ''.join(c for c in line.split()[1] if c in '0123456789.+-e')
                    if bw == '-':
                        BW += 0.0
                    else:
                        BW += float(bw)
                    BW_count+=1
                if 'totalEnergy' in line:
                    te = ''.join(c for c in line.split()[1] if c in '0123456789.+-e')
                    if te == '-':
                        TotalEnergyConsumption = 0
                    else:
                        if 'DRAM' in Output:
                            TotalEnergyConsumption = float(''.join(c for c in line.split()[1] if c in '0123456789.+-e'))*CycTime*9e-3 
                            #DRAMs calculate energy in mA*t and hence need this further modification
                        else:
                            TotalEnergyConsumption = float(''.join(c for c in line.split()[1] if c in '0123456789.+-e'))*CycTime
                if 'WaitAverage' in line or 'averageLatency' in line:
                    al = ''.join(c for c in line.split()[1] if c in '0123456789.')
                    if al == '':
                        AverageLatency += 0
                    else:
                        AverageLatency += float(''.join(c for c in line.split()[1] if c in '0123456789.'))*CycTime
        
        simTime = SimCycles/CPUFreq
        AvgBandWidth = BW/BW_count
        EPB = TotalEnergyConsumption*SimCycles/((TotalReads+TotalWrites)*PktSize)
        RdThroughput = TotalReads*PktSize/(10e9*simTime)
        WrThroughput = TotalWrites*PktSize/(10e9*simTime)
        with open(FilePath, 'a', newline='') as file:
            writer = csv.writer(file)
            row = [appName,AverageLatency,AvgBandWidth,RdThroughput,WrThroughput,EPB]
            writer.writerow(row)


def plotGraphs():
    AverageLatency=[]
    AvgBandWidth=[]
    EPB=[]
    fileno=0
    colors=[]
    spacing=[]
    Width=float(0.75/len(PlotConfigs))

    print(Width)

    labels = PlotConfigs

    for config in PlotConfigs:
        colors.append(PlotDict[config])

    for i in range(-1*math.ceil(len(PlotConfigs)/2),math.floor(len(PlotConfigs)/2)):
        spacing.append(float(i*Width))
        
    for Analysis_file in PlotConfigs:
        fileno=fileno+1
        appName =[]
        Latency=[]
        BW=[]
        epb=[]
        with open(DestDir+Analysis_file, 'r') as f:
            for line in f:
                Line = line.split(",")
                appName.append(Line[0])
                Latency.append(float(Line[1]))
                BW.append(float(Line[2]))
                epb.append(float(Line[5]))
        appName.append("Average")
        Latency.append(float(np.average(Latency)))
        BW.append(float(np.average(BW)))
        epb.append(float(np.average(epb)))
        AverageLatency.extend(Latency)
        AvgBandWidth.extend(BW)
        EPB.extend(epb)

    for i in range(0,fileno):
        print(len(AverageLatency[i::len(appName)]))

    fig, ax =plt.subplots()

    for i in range(0,fileno):
        if (i+1)*len(appName) < len(AverageLatency):
            ax.bar(np.arange(len(appName))+spacing[i],AverageLatency[i*len(appName):(i+1)*len(appName)],width=Width,align='center',
            color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)
        else:
            ax.bar(np.arange(len(appName))+spacing[i],AverageLatency[i*len(appName)::],width=Width,align='center',
            color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)

    #ax.set_ylim([0.5,1])
    ax.set_xticks(np.arange(len(appName)))
    ax.set_xticklabels(appName,fontsize='15',weight ='bold')
    ax.set_ylabel('Average latency values', fontsize='30',weight ='bold') 
    ax.legend(ncol=3,loc ='upper left',bbox_to_anchor=(-0.01,1.15),fontsize='20')#,mode='expand')
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
            ax.bar(np.arange(len(appName))+spacing[i],AvgBandWidth[i*len(appName):(i+1)*len(appName)],width=Width,align='center',
            color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)
        else:
            ax.bar(np.arange(len(appName))+spacing[i],AvgBandWidth[i*len(appName)::],width=Width,align='center',
            color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)

    #ax.set_ylim([0.5,1])
    ax.set_xticks(np.arange(len(appName)))
    ax.set_xticklabels(appName,fontsize='15',weight ='bold')
    ax.set_ylabel('Average Bandwithd (MBps)', fontsize='30',weight ='bold') 
    ax.legend(ncol=3,loc ='upper left',bbox_to_anchor=(-0.01,1.15),fontsize='20')#,mode='expand')
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
            ax.bar(np.arange(len(appName))+spacing[i],EPB[i*len(appName):(i+1)*len(appName)],width=Width,align='center',
            color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)
        else:
            ax.bar(np.arange(len(appName))+spacing[i],EPB[i*len(appName)::],width=Width,align='center',
            color=colors[i],label=labels[i],edgecolor='black',linewidth=1.25)

    #ax.set_ylim([0.5,1])
    ax.set_xticks(np.arange(len(appName)))
    ax.set_xticklabels(appName,fontsize='15',weight ='bold')
    ax.set_ylabel('EPB values (J/bit)', fontsize='30',weight ='bold') 
    ax.legend(ncol=3,loc ='upper left',bbox_to_anchor=(-0.01,1.15),fontsize='20')#,mode='expand')
    #plt.legend(loc=1, fontsize = 'x-large')
    #plt.title('EPB Analysis: Aggressive values',fontsize='40',weight ='bold')
    fig.tight_layout()
    plt.yscale('log')
    plt.xticks(rotation=30,horizontalalignment='right')
    plt.yticks(fontsize='25')
    plt.show()

def RWplotGraphs():  
    RdThroughput=[]
    WrThroughput=[]

    colors = []

    labels = PlotConfigs

    for config in PlotConfigs:
        colors.append(PlotDict[config])

    for Analysis_file in PlotConfigs:#['3D_DRAM', '2D_DRAM', 'PCM_ISSCC', 'COSMOS_OPCM_TE', 'ICCAD2023-Cr-Res']:
        with open(RWAnalysis+Analysis_file, 'r') as f:
            for line in f:
                Line = line.split(",")
                if 'Read' in Line[0]:
                    RdThroughput.append(float(Line[2]))
                elif 'Write' in Line[0]:
                    WrThroughput.append(float(Line[2]))

    RdThroughput = np.array(RdThroughput)
    WrThroughput = np.array(WrThroughput)

    fig, ax =plt.subplots()

    ax.bar(np.arange(len(labels)), RdThroughput/1024, color=colors, edgecolor='black')
    ax.set_xticklabels(labels,fontsize='10',weight ='bold')
    ax.set_ylabel('Read Throughput(GBps)', fontsize='30',weight ='bold') 
    plt.xticks(np.arange(len(labels)), labels, fontsize='15',rotation=45,horizontalalignment='right')
    plt.yticks(fontsize='25')

    plt.show()

    fig, ax =plt.subplots()

    ax.bar(np.arange(len(labels)), WrThroughput/1024, color=colors, edgecolor='black')
    ax.set_xticklabels(labels,fontsize='10',weight ='bold')
    ax.set_ylabel('Write Throughput (GBps)', fontsize='30',weight ='bold') 
    plt.xticks(np.arange(len(labels)), labels, fontsize='15',rotation=45,horizontalalignment='right')
    plt.yticks(fontsize='25')

    plt.show()

def printHelp():
    print("Arguments expected: SIM <number of cycles> (simulates memory operation for configs for specified number of cycles) |")
    print("RWSIM <number of cycles> (simulates memory operation for read and write througput for specified number of cycles) |")
    print("MEMAN (performs just analysis without rerunning the simulations) |")
    print("RWAN (runs analyses on the available read/write throughput data) | PLOT (plots data from existing data) |")

def main():
    args = sys.argv[1:]
    if len(args)==0:
        print("No arguments passed; running the whole simulation using default run cycles.")
        printHelp()
        SimulationRuns()
        RWSimRuns()
        MemAnalysis()
        RWMemAnalysis()
        plotGraphs()
        RWplotGraphs()
    if len(args)==1:
        if args[0]=='RWAN':
            RWMemAnalysis()
            RWplotGraphs()
        elif args[0]=='MEMAN':
            MemAnalysis()
            plotGraphs()
        elif args[0]=='PLOT':
            plotGraphs()
            RWplotGraphs()
        else:
            print("Invalid arguments.")
            printHelp()
    if len(args)==2:
        if args[0]=='SIM':
            SimulationRuns(args[1])
            MemAnalysis()
            plotGraphs()
        elif args[0]=='RWSIM':
            RWSimRuns(args[1])
            RWMemAnalysis()
            RWplotGraphs()
        else:
            print("Invalid arguments.")
            printHelp()
    if len(args)>2:
        print("Invalid arguments. Please pass one argument at a time.")
        printHelp()
    

if __name__=="__main__":
    main()