import os
import csv

OutDir='/home/febin/Linux2/OpticalMemoryTrace/NVMainRuns/Outputs/'
DestDir='/home/febin/Linux2/OpticalMemoryTrace/NVMainRuns/Analysis/'

for OldOutput in os.listdir(DestDir):
    os.remove(os.path.join(DestDir, OldOutput))

numcyclerun = 10000000
CPUFreq = 1e9
simTime = numcyclerun/CPUFreq

MemoryCOnfigs= ['3D_DRAM', '2D_DRAM', 'PCM_ISSCC', 'COSMOS_EPCM', 'COSMOS_OPCM', 'COSMOS_OPCM_TE', 'ICCAD2023-Am-Res','ICCAD2023-Cr-Res']
CycleTime = [1.3e9, 666e6, 400e6, 1e9, 1e9, 1e9, 1e9, 1e9]

PktSize=128
TotalWrites=0
TotalReads=0
AvgBandWidth=0
SimCycles=0
TotalEnergyConsumption=0
AverageLatency=0

for Output in sorted(os.listdir(OutDir)):
    appName=Output.split("_")[-1]
    BW_count=0
    BW=0
    AverageLatency=0

    for name, cyc in zip(MemoryCOnfigs,CycleTime):
        if name in Output:
            CycTime=11/cyc
            FilePath=DestDir+name
   
    with open(OutDir+Output,'r') as Outfile:
        if '.milc' in Output or '.soplex' in Output or '.lbm' in Output or '.mcf' in Output or '.leslie3d' in Output or '.zeusmp' in Output or '.txt' in Output:
            continue
        else:
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
                            TotalEnergyConsumption = float(''.join(c for c in line.split()[1] if c in '0123456789.+-e'))*1e-9*9e-3 
                            #DRAMs calculate energy in mA*t and hence need this further modification
                        else:
                            TotalEnergyConsumption = float(''.join(c for c in line.split()[1] if c in '0123456789.+-e'))*1e-9
                if 'WaitAverage' in line or 'averageLatency' in line:
                    al = ''.join(c for c in line.split()[1] if c in '0123456789.')
                    if al == '':
                        AverageLatency += 0
                    else:
                        AverageLatency += float(''.join(c for c in line.split()[1] if c in '0123456789.'))*CycTime
    
    AvgBandWidth = BW/BW_count
    EPB = TotalEnergyConsumption/((TotalReads+TotalWrites)*PktSize)
    RdThroughput = TotalReads*PktSize/(10e9*simTime)
    WrThroughput = TotalWrites*PktSize/(10e9*simTime)
    with open(FilePath, 'a', newline='') as file:
        writer = csv.writer(file)
        row = [appName,AverageLatency,AvgBandWidth,RdThroughput,WrThroughput,EPB]
        writer.writerow(row)