#ramulator CPUtrace to NVMain trace converter

import os

#NVmain trace format:
# CYCLE R/W ADDRESS DATA ID
#Ramulator CPU trace format
# CPU-INST-COUNT-BEFORE-M/Y-OP ADDR-READ-DEC
# CPU-INST-COUNT-BEFORE-M/Y-OP ADDR-READ-DEC ADDR-WRTBCK-DEC

#Diectroy with all Ramulator traces
RamDir='/home/febin/Linux2/OpticalMemoryTrace/Ramulator_CPUTraces'

#Destination directory for all NVMain traces
NVMDir='/home/febin/Linux2/OpticalMemoryTrace/NVMainTracesFrmRamulator'

for traceName in os.listdir(RamDir):
    srcTrace=os.path.join(RamDir,traceName)
    cycle_count =0
    with open(srcTrace,'r') as f:
        for line in f:
            ADDR_W=0
            #ID and DATA are placeholders as Ramulator doesnt provide this but NVMain need it
            ID = 0
            DATA='f9ffff4881c480000000ebad9090909053488b074885c00f84a5000000448b05446d27008b1d46312700488d57104c8b1d936c27004c8b156c6c270031c9448b'
            #print(line)
            contents = line.split()
            cycle_count+=int(contents[0])
            ADDR_RD = hex(int(contents[1]))
            if len(contents)>2:
                ADDR_W = hex(int(contents[2]))
            destTrace = os.path.join(NVMDir,traceName)
            with open(destTrace,'a+') as f1:
                nline = str(cycle_count)+' '+'R'+' '+str(ADDR_RD)+' '+DATA+' '+str(ID)
                f1.write(nline)
                f1.write('\n')
                if ADDR_W:
                    nline = str(cycle_count)+' '+'W'+' '+str(ADDR_W)+' '+DATA+' '+str(ID)
                    f1.write(nline)
                    f1.write('\n')
            
