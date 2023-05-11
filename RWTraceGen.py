#ramulator CPUtrace to NVMain trace converter

import os
import random

#NVmain trace format:
# CYCLE R/W ADDRESS DATA ID
#Ramulator CPU trace format
# CPU-INST-COUNT-BEFORE-M/Y-OP ADDR-READ-DEC
# CPU-INST-COUNT-BEFORE-M/Y-OP ADDR-READ-DEC ADDR-WRTBCK-DEC

#Diectroy with all Ramulator traces
RamDir='/home/febin/Linux2/OpticalMemoryTrace/Ramulator_CPUTraces'

#Destination directory for all NVMain traces
NVMDir='/home/febin/Linux2/OpticalMemoryTrace/R_W_Traces/'

ID = 0
DATA='f9ffff4881c480000000ebad9090909053488b074885c00f84a5000000448b05446d27008b1d46312700488d57104c8b1d936c27004c8b156c6c270031c9448b'

cycle_count =0
destTrace = 'ReadTrace'
with open(NVMDir+destTrace,'a+') as f1:
    for cycle_count in range(1,100001):
        ADDR_RD = hex(random.randint(int(0xfffff),int(0xfffffffffffff0)))
        nline = str(cycle_count)+' '+'R'+' '+str(ADDR_RD)+' '+DATA+' '+str(ID)
        f1.write(nline)
        f1.write('\n')

cycle_count =0
destTrace = 'WriteTrace'
with open(NVMDir+destTrace,'a+') as f1:
    for cycle_count in range(1,100001):
        ADDR_RD = hex(random.randint(int(0xfffff),int(0xfffffffffffff0)))
        nline = str(cycle_count)+' '+'W'+' '+str(ADDR_RD)+' '+DATA+' '+str(ID)
        f1.write(nline)
        f1.write('\n')
            
