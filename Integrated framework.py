import math

def factorial(f):
    if f == 0:
        return 1
    else:
        return f * factorial(f-1)

def toList(NestedTuple):
    return list(map(toList, NestedTuple)) if isinstance(NestedTuple, (list, tuple)) else NestedTuple
def Init():
    global minSpeed
    global MaxSpeed
    global MaximumNumber
    global MaximumHeadway 
    global vehTypesEquipped
    global sigTypesAttributes
    global LinkTypesAttributes
    global GV
    global EV
    global GVCAV
    global SCAV
    global LinkA
    global LinkB
    global LinkC
    global LinkD
    global SignalA
    global SignalB
    global SignalC
    global SignalD
    
    minSpeed = CurrentScript.AttValue('minSpeed')
    MaxSpeed = CurrentScript.AttValue('MaxSpeed')
    MaximumNumber = CurrentScript.AttValue('MaximumNumber')
    MaximumHeadway = CurrentScript.AttValue('MaximumHeadway')
    vehTypesAttributes = Vissim.Net.VehicleTypes.GetMultipleAttributes(['No', 'ReceiveSignalInformation','GV','EV','GVCAV','SCAV'])
    
    vehTypesEquipped = [x[0] for x in vehTypesAttributes if x[1] == True]
    GV = [x[0] for x in vehTypesAttributes if x[2] == True]
    EV = [x[0] for x in vehTypesAttributes if x[3] == True]
    GVCAV = [x[0] for x in vehTypesAttributes if x[4] == True]
    SCAV = [x[0] for x in vehTypesAttributes if x[5] == True]



    LinkTypesAttributes =  Vissim.Net.Links.GetMultipleAttributes(['No', 'LinkA', 'LinkB', 'LinkC', 'LinkD'])
    LinkA = [x[0] for x in LinkTypesAttributes if x[1] == True]
    LinkB = [x[0] for x in LinkTypesAttributes if x[2] == True]
    LinkC = [x[0] for x in LinkTypesAttributes if x[3] == True]
    LinkD = [x[0] for x in LinkTypesAttributes if x[4] == True]
    
    
    
    
    sigTypesAttributes =  Vissim.Net.SignalControllers.ItemByKey(1).SGs.GetMultipleAttributes(['No', 'SignalA', 'SignalB', 'SignalC', 'SignalD'])
    SignalA = [x[0] for x in sigTypesAttributes if x[1] == True]
    SignalB = [x[0] for x in sigTypesAttributes if x[2] == True]
    SignalC = [x[0] for x in sigTypesAttributes if x[3] == True]
    SignalD = [x[0] for x in sigTypesAttributes if x[4] == True]
    # This functions gets and updates each vehicle state at the network

def GetVissimDataVehicles():
    global vehsAttributes
    global vehsAttNames
    vehsAttributes = []
    vehsAttNames = []
    vehsAttributesNames = ['No', 'VehType\No','Speed' , 'DesSpeed', 'OrgDesSpeed', 'DistanceToSigHead', 'SpeedMaxForGreenStart', 'SpeedMinForGreenEnd', 'Acceleration', 'Lane\Link', 'SpeedMaxForGreenStart1', 'SpeedMinForGreenEnd1']
    vehsAttributes = toList(Vissim.Net.Vehicles.GetMultipleAttributes(vehsAttributesNames))
    vehsAttNames = {}
    cnt = 0
    for att in vehsAttributesNames:
        vehsAttNames.update({att: cnt})
        cnt += 1



# This function takes the specification of each signal
def GetSignalsData():
    global SignalAttributes
    global SigAttNames
    SignalAttributes = []
    SigAttNames = []
    SignalAttributesNames = ['No','Name', 'GreenStart', 'GreenEnd','TimeUntilNextGreen','TimeUntilNextRed', 'SignalA', 'SignalB', 'SignalC', 'SignalD','SigState', 'GreenTimeDuration' ,'LastCAVPos','SigState', 'SC\CycSec', 'Seconds', 'TimeUntilNextGreen1','TimeUntilNextRed1', 'GreenStart1', 'GreenEnd1' ]
    SignalAttributes = toList(Vissim.Net.SignalControllers.ItemByKey(1).SGs.GetMultipleAttributes(SignalAttributesNames))
    SigAttNames = {}
    ctt = 0
    for ftt in SignalAttributesNames:
        SigAttNames.update({ftt: ctt})
        ctt+=1


def GetLinksData():
    global LinkAttributes
    global LinAttNames
    LinkAttributes = []
    LinkAttributes = []
    LinkAttributesNames = ['No','LinkA', 'LinkB', 'LinkC', 'LinkD']
    LinkAttributes = toList(Vissim.Net.Links.GetMultipleAttributes(LinkAttributesNames))
    LinAttNames = {}
    ppc = 0
    for ftt in LinkAttributesNames:
        LinAttNames.update({ftt: ppc})
        ppc+=1


def GetTrafficFleetData():
    global trafficAttributes
    global traAttNames
    trafficAttributes = []
    traAttNames = []
    TrafficAttributesNames = ['VehType\No','RelFlow']
    trafficAttributes = toList(Vissim.Net.VehicleCompositions.ItemByKey(5).VehCompRelFlows.GetMultipleAttributes(TrafficAttributesNames))
    traAttNames = {}
    gtp = 0
    for ptg in TrafficAttributesNames:
        traAttNames.update({ptg: gtp})
        gtp+=1



def ChangeSpeed():
    GetVissimDataVehicles()
    GetSignalsData()
    if len(vehsAttributes) > 1:
        for vehAttributes in vehsAttributes:
            if vehAttributes[vehsAttNames['VehType\No']] in vehTypesEquipped:
                No = vehAttributes[vehsAttNames['No']]
                DesSpeed = vehAttributes[vehsAttNames['DesSpeed']]
                OrgDesSpeed = vehAttributes[vehsAttNames['OrgDesSpeed']]
                Speed = vehAttributes[vehsAttNames['Speed']]
                DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                SpeedMaxForGreenStart = vehAttributes[vehsAttNames['SpeedMaxForGreenStart']]
                SpeedMinForGreenEnd = vehAttributes[vehsAttNames['SpeedMinForGreenEnd']]
                if OrgDesSpeed == None:
                    OrgDesSpeed = DesSpeed
                    vehAttributes[vehsAttNames['OrgDesSpeed']] = DesSpeed
                
                if DistanceToSigHead <= 0:
                    vehAttributes[vehsAttNames['DesSpeed']] = OrgDesSpeed
                    continue
                
                i=0
                v1=0
                vstar=[]
                while v1<= (MaxSpeed/3.6) - (minSpeed/3.6):
                    v1 = v1+(minSpeed/3.6)
                    vstar.append(v1)
                vv=[]
                for i in vstar:
                    vv.append(Speed)
                i=0
                a1=[]
                a=0
                while i < len(vv):
                    if vv[i] == vstar[i]:
                        a=0
                    if vv[i] != vstar[i]:
                        a = 4*(1-pow((vv[i]/vstar[i]),4))
                    a1.append(a)
                    i+=1
                i=0
                while i<len(vv):
                    if a1[i]> 4:
                        a1[i] = 4
                    if a1[i]<-4:
                        a1[i] = -4
                    i+=1
                t11=[]
                i=0
                t=0
                while i<len(vv):
                    if a1[i]==0:
                        t=0
                    else:
                        t=(vstar[i]-vv[i])/a1[i]
                    t11.append(t)
                    i+=1
                x3=[]
                x1=0
                t=0
                i=0
                t22=[]
                m=0
                while i<len(vv):
                    x1 = 0.5 * a1[i] * t11[i] * t11[i] + vv[i] * t11[i]
                    if x1 == DistanceToSigHead:
                        t=t11[i]
                    elif DistanceToSigHead < x1:
                        if a1[i] != 0:
                            t = (-vv[i]+math.sqrt(vv[i]*vv[i]+2*a1[i]*DistanceToSigHead))/a1[i]
                        else:
                            t = DistanceToSigHead/vv[i]
                    else:
                        x2=DistanceToSigHead-x1
                        t= t11[i] + x2/vstar[i]
                    t22.append(t)
                    i+=1
                tf1=0
                tf2=0 
                
                    
                if vehAttributes[vehsAttNames['Lane\Link']] in LinkA:
                    tf11= [x[4] for x in sigTypesAttributes if x[6] == True]
                    tf1= tf11[0]             
                    tf22 = [x[5] for x in sigTypesAttributes if x[6] == True]
                    tf2= tf22[0]
              
                    
                if vehAttributes[vehsAttNames['Lane\Link']] in LinkB:
                    tf11= [x[4] for x in sigTypesAttributes if x[7] == True]
                    tf1= tf11[0]
                    tf22= [x[5] for x in sigTypesAttributes if x[7] == True]
                    tf2= tf22[0]
                    
                if vehAttributes[vehsAttNames['Lane\Link']] in LinkC:
                    tf11= [x[4] for x in sigTypesAttributes if x[8] == True]
                    tf1= tf11[0]
                    tf22= [x[5] for x in sigTypesAttributes if x[8] == True]
                    tf2= tf22[0]
                    
                    
                if vehAttributes[vehsAttNames['Lane\Link']] in LinkD:
                    tf11= [x[4] for x in sigTypesAttributes if x[9] == True]
                    tf1= tf11[0]
                    tf22= [x[5] for x in sigTypesAttributes if x[9] == True]
                    tf1= tf11[0]
                    

                i=0
                Time=[]
                while i < len(t22):
                    uu= t22[i]
                    if uu>= tf1 and uu <= tf2:
                        Time.append(t22[i])
                    i+=1
                VVP=[]
                i=0
                while i< len(vv):
                    VP=[]
                    j=0
                    vvv=0
                    while j < t22[i]:
                        while j <= t11[i]:
                            vvv = a1[i] * j + vv[i]
                            VP.append(vvv)
                            j+=1
                        vvv = vstar[i]
                        VP.append(vvv)
                        j+=1
                    try:
                        if j<=Time[0] and j>=Time[-1]:
                            VVP.append(VP)
                    except: 
                        VVP =[[vv[i]]]
                        
                    i+=1
                AAP=[]
                i=0
                while i< len(vv):
                    AP=[]
                    j=0
                    aaa = 0
                    while j < t22[i]:
                        while j <= t11[i]:
                            aaa = a1[i]
                            AP.append(aaa)
                            j+=1
                        aaa=0
                        AP.append(aaa)
                        j+=1
                    try:
                        if j <= Time[0] and j >= Time[-1]:
                            AAP.append(AP)
                    except:
                        AAP = [[0]]
                        
                    i+=1
                F=[]
                for z in VVP:
                    for n in AAP:
                        y=0
                        i=0
                        while i < len(z):
                            y = y + z[i]
                            i+=1
                            if y < DistanceToSigHead:
                                continue
                            else:
                                break
                        f=0
                        j=0
                        while j < len(n):
                            if No == 101:
                                f = f + (0.003 * ( 1256 * n[j] + 1.3 * z[j] * z[j])* ( 1256 * n[j] + 1.3 * z[j] * z[j]) +  z[j] * (1.3 * z[j] * z[j] + 0.006 * 1256 + 9.8) + 0.95 * 1256 * n[j] * z[j])
                                j+=1
                                if j<=i:
                                    continue
                                else:
                                    break
                                F.append(f)

                            else:
                                f=f+(max((0.444 + 0.09 * z[j] * (0.333 + 0.00108 * z[j] * z[j] * 1256 * n[j]) + 0.04 * 1256 * z[j] * n[j] * n[j]), 0.444))
                                j+=1
                                if j<=i:
                                    continue
                                else:
                                    break
                                F.append(f)
                try:
                    desSpeed=VVP[F.index(min(F))][-1]
                except:
                    desSpeed= vehAttributes[vehsAttNames['Speed']]
                    
                optimalSpeed=0
                
                if SpeedMinForGreenEnd < desSpeed:
                    optimalSpeed = desSpeed
                else:
                    optimalSpeed = SpeedMinForGreenEnd
                    
                if optimalSpeed < SpeedMaxForGreenStart:
                    optimalSpeed = optimalSpeed
                else:
                    optimalSpeed = SpeedMaxForGreenStart
                if SpeedMinForGreenEnd > SpeedMaxForGreenStart:
                    optimalSpeed = OrgDesSpeed
                    

                    
                        
                vehAttributes[vehsAttNames['DesSpeed']] = optimalSpeed


        vehicleNumDesiredSpeeds = [[x[vehsAttNames['DesSpeed']], x[vehsAttNames['OrgDesSpeed']]] for x in vehsAttributes]
        Vissim.Net.Vehicles.SetMultipleAttributes(('DesSpeed', 'OrgDesSpeed'), vehicleNumDesiredSpeeds)
                




# This calculates the number of queued up vehicles based on the Commert's formula and the corresponding green time
def NumberOfQueuedVehicles():
    GetVissimDataVehicles()
    GetTrafficFleetData()
    GetSignalsData()
    GetLinksData()

    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('Seconds',Vissim.Net.Simulation.SimulationSecond)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('Seconds',Vissim.Net.Simulation.SimulationSecond)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('Seconds',Vissim.Net.Simulation.SimulationSecond)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('Seconds',Vissim.Net.Simulation.SimulationSecond)
    C = []
    B = []
    A = []
    D = []

    for sig in SignalAttributes:
            if  sig[SigAttNames['No']] ==3 and sig[SigAttNames['SigState']] !='Red':  
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['VehType\No']] in vehTypesEquipped:                       
                        if vehAttributes[vehsAttNames['VehType\No']] in SCAV:
                            Link = vehAttributes[vehsAttNames['Lane\Link']]
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LinkNo')==5:
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',28)
                        elif vehAttributes[vehsAttNames['Speed']] ==0:
                            Link = vehAttributes[vehsAttNames['Lane\Link']]
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LinkNo')==5:
                                C.append (DistanceToSigHead)
                                CC = max (C)
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LastCount',round(CC/5))
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LastCAVPos',CC)
                                #The code for Commert formula and GEomrtric distribution for the vehicles that join the queue:
                                # Proportion_of_conventionalC = 0.65
                                # Total_arrival_rateC = 0.1
                                # sum1 = 0
                                # k = Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount')
                                # while k <= 100:
                                #     sum1 = sum1 + ((pow(((Proportion_of_conventionalC) * Total_arrival_rateC * 45), k)) / factorial(k))
                                #     k+=1
                                # sum2 = 0
                                # n = Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount')
                                # while n <= 100:
                                #     sum2 = sum2 + (n*((pow(((Proportion_of_conventionalC) * Total_arrival_rateC * 45), n)) / factorial(n)))/sum1
                                #     n+=1
                                #y1 = round(2*sum2)+ round(2*(1/(pow(2.71,(-1*Total_arrival_rateC*MaximumHeadway)))))
                                #for addressing the time of calculation based on the limitation of current system, we calculate the cooresponding y1 for each Last CAV postion until y1 hits our threshold (the Lasct CAV count is 8)
                                # then we calculate the associated green time based on the follwoing code
                                # G1= round(min(y1*1.4,27))
                                #this code gives the green time based on the considered service rate and also by the addressing the Xt
                                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount') == 0:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',13)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount') == 1:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',13)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount') == 2:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',14)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount') == 3:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',15)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount') == 4:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',18)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount') == 5:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',20)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount') == 6:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',22)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount') == 7:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',24)
                                else:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenTimeDuration',28)                                    
               
 
            
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenStart'))
               
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenEnd')-2:
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('SigState','Green')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenStart'))
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenStart'))
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenStart'))
                    continue





                
            if  sig[SigAttNames['No']] ==6 and sig[SigAttNames['SigState']] !='Red':
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['VehType\No']] in vehTypesEquipped:
                        if vehAttributes[vehsAttNames['VehType\No']] in SCAV:
                            Link = vehAttributes[vehsAttNames['Lane\Link']]
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LinkNo')==7:
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',28)
                        elif vehAttributes[vehsAttNames['Speed']] ==0:
                            Link = vehAttributes[vehsAttNames['Lane\Link']]
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LinkNo')==7:
                                B.append (DistanceToSigHead)
                                BB = max (B)
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LastCount',round(BB/5))
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LastCAVPos',BB)
                                #The code for Commert formula and GEomrtric distribution for the vehicles that join the queue:
                                # Proportion_of_conventionalC = 0.65
                                # Total_arrival_rateC = 0.1
                                # sum1 = 0
                                # k = Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount')
                                # while k <= 100:
                                #     sum1 = sum1 + ((pow(((Proportion_of_conventionalC) * Total_arrival_rateC * 45), k)) / factorial(k))
                                #     k+=1
                                # sum2 = 0
                                # n = Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount')
                                # while n <= 100:
                                #     sum2 = sum2 + (n*((pow(((Proportion_of_conventionalC) * Total_arrival_rateC * 45), n)) / factorial(n)))/sum1
                                #     n+=1
                                #y1 = round(2*sum2)+ round(2*(1/(pow(2.71,(-1*Total_arrival_rateC*MaximumHeadway)))))
                                #for addressing the time of calculation based on the limitation of current system, we calculate the cooresponding y1 for each Last CAV postion until y1 hits our threshold (the Lasct CAV count is 8)
                                # then we calculate the associated green time based on the follwoing code
                                # G1= round(min(y1*1.4,27))
                                #this code gives the green time based on the considered service rate and also by the addressing the Xt
                                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LastCount') == 0:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',13)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LastCount') == 1:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',13)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LastCount') == 2:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',14)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LastCount') == 3:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',15)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LastCount') == 4:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',18)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LastCount') == 5:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',20)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LastCount') == 6:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',22)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('LastCount') == 7:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',24)
                                else:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenTimeDuration',28)                                    
                   

           
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenStart'))
                
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenEnd')-2:
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('SigState','Green')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenStart'))
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenStart'))
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenStart'))
                    continue

            if  sig[SigAttNames['No']] ==9 and sig[SigAttNames['SigState']] !='Red':
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['VehType\No']] in vehTypesEquipped:

                        No = vehAttributes[vehsAttNames['No']]
                        DesSpeed = vehAttributes[vehsAttNames['DesSpeed']]
                        OrgDesSpeed = vehAttributes[vehsAttNames['OrgDesSpeed']]
                        Speed = vehAttributes[vehsAttNames['Speed']]
                        DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                        SpeedMaxForGreenStart1 = vehAttributes[vehsAttNames['SpeedMaxForGreenStart1']]
                        SpeedMinForGreenEnd1 = vehAttributes[vehsAttNames['SpeedMinForGreenEnd1']]
                        if vehAttributes[vehsAttNames['VehType\No']] in SCAV:
                            Link = vehAttributes[vehsAttNames['Lane\Link']]
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LinkNo')==1:
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',28)
                        elif vehAttributes[vehsAttNames['Speed']] ==0:
                            Link = vehAttributes[vehsAttNames['Lane\Link']]
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LinkNo')==1:
                                A.append (DistanceToSigHead)
                                AA = max (A)
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LastCount',round(AA/5))
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LastCAVPos',AA)
                                #The code for Commert formula and GEomrtric distribution for the vehicles that join the queue:
                                # Proportion_of_conventionalC = 0.65
                                # Total_arrival_rateC = 0.1
                                # sum1 = 0
                                # k = Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount')
                                # while k <= 100:
                                #     sum1 = sum1 + ((pow(((Proportion_of_conventionalC) * Total_arrival_rateC * 45), k)) / factorial(k))
                                #     k+=1
                                # sum2 = 0
                                # n = Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount')
                                # while n <= 100:
                                #     sum2 = sum2 + (n*((pow(((Proportion_of_conventionalC) * Total_arrival_rateC * 45), n)) / factorial(n)))/sum1
                                #     n+=1
                                #y1 = round(2*sum2)+ round(2*(1/(pow(2.71,(-1*Total_arrival_rateC*MaximumHeadway)))))
                                #for addressing the time of calculation based on the limitation of current system, we calculate the cooresponding y1 for each Last CAV postion until y1 hits our threshold (the Lasct CAV count is 8)
                                # then we calculate the associated green time based on the follwoing code
                                # G1= round(min(y1*1.4,27))
                                #this code gives the green time based on the considered service rate and also by the addressing the Xt
                                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LastCount') == 0:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',13)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LastCount') == 1:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',13)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LastCount') == 2:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',14)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LastCount') == 3:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',15)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LastCount') == 4:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',18)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LastCount') == 5:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',20)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LastCount') == 6:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',22)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('LastCount') == 7:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',24)
                                else:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenTimeDuration',28)                                    
                     

               
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenStart'))
                
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenEnd')-2:
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('SigState','Green')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).AttValue ('GreenStart'))
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenStart'))
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenStart'))
                    
                    continue


            if  sig[SigAttNames['No']] ==12 and sig[SigAttNames['SigState']] !='Red':
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['VehType\No']] in vehTypesEquipped:

                        No = vehAttributes[vehsAttNames['No']]
                        DesSpeed = vehAttributes[vehsAttNames['DesSpeed']]
                        OrgDesSpeed = vehAttributes[vehsAttNames['OrgDesSpeed']]
                        Speed = vehAttributes[vehsAttNames['Speed']]
                        DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                        SpeedMaxForGreenStart1 = vehAttributes[vehsAttNames['SpeedMaxForGreenStart1']]
                        SpeedMinForGreenEnd1 = vehAttributes[vehsAttNames['SpeedMinForGreenEnd1']]
                        if vehAttributes[vehsAttNames['VehType\No']] in SCAV:
                            Link = vehAttributes[vehsAttNames['Lane\Link']]
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LinkNo')==3:
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',28)
                        elif vehAttributes[vehsAttNames['Speed']] ==0:
                            Link = vehAttributes[vehsAttNames['Lane\Link']]
                            DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('LinkNo',Link)
                            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LinkNo',Link)
                            if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LinkNo')==3:
                                D.append (DistanceToSigHead)
                                DD = max (D)
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LastCount',round(DD/5))
                                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('LastCAVPos',DD)
                                #The code for Commert formula and GEomrtric distribution for the vehicles that join the queue:
                                # Proportion_of_conventionalC = 0.65
                                # Total_arrival_rateC = 0.1
                                # sum1 = 0
                                # k = Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount')
                                # while k <= 100:
                                #     sum1 = sum1 + ((pow(((Proportion_of_conventionalC) * Total_arrival_rateC * 45), k)) / factorial(k))
                                #     k+=1
                                # sum2 = 0
                                # n = Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('LastCount')
                                # while n <= 100:
                                #     sum2 = sum2 + (n*((pow(((Proportion_of_conventionalC) * Total_arrival_rateC * 45), n)) / factorial(n)))/sum1
                                #     n+=1
                                #y1 = round(2*sum2)+ round(2*(1/(pow(2.71,(-1*Total_arrival_rateC*MaximumHeadway)))))
                                #for addressing the time of calculation based on the limitation of current system, we calculate the cooresponding y1 for each Last CAV postion until y1 hits our threshold (the Lasct CAV count is 8)
                                # then we calculate the associated green time based on the follwoing code
                                # G1= round(min(y1*1.4,27))
                                #this code gives the green time based on the considered service rate and also by the addressing the Xt
                                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LastCount') == 0:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',13)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LastCount') == 1:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',13)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LastCount') == 2:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',14)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LastCount') == 3:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',15)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LastCount') == 4:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',18)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LastCount') == 5:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',20)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LastCount') == 6:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',22)
                                elif Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('LastCount') == 7:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',24)
                                else:
                                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenTimeDuration',28)                                    
                   

             
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenStart'))
                
                if Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('Seconds') >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenEnd')-2:
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('SigState','Green')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).SetAttValue ('SigState','Red')
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(12).AttValue ('GreenStart'))
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue ('GreenStart'))
                    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(9).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenTimeDuration')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(6).AttValue ('GreenStart'))
                    continue



                
                


 







def ChangeSpeed2():
    GetVissimDataVehicles()
    GetSignalsData()
    if len(vehsAttributes) > 1:
        for vehAttributes in vehsAttributes:
            if vehAttributes[vehsAttNames['VehType\No']] in vehTypesEquipped:
                No = vehAttributes[vehsAttNames['No']]
                DesSpeed = vehAttributes[vehsAttNames['DesSpeed']]
                OrgDesSpeed = vehAttributes[vehsAttNames['OrgDesSpeed']]
                Speed = vehAttributes[vehsAttNames['Speed']]
                DistanceToSigHead = vehAttributes[vehsAttNames['DistanceToSigHead']]
                SpeedMaxForGreenStart1 = vehAttributes[vehsAttNames['SpeedMaxForGreenStart1']]
                SpeedMinForGreenEnd1 = vehAttributes[vehsAttNames['SpeedMinForGreenEnd1']]
                if OrgDesSpeed == None:
                    OrgDesSpeed = DesSpeed
                    vehAttributes[vehsAttNames['OrgDesSpeed']] = DesSpeed
                
                if DistanceToSigHead <= 0:
                    vehAttributes[vehsAttNames['DesSpeed']] = OrgDesSpeed
                    continue
                
                i=0
                v1=0
                vstar=[]
                while v1<= (MaxSpeed/3.6) - (minSpeed/3.6):
                    v1 = v1+(minSpeed/3.6)
                    vstar.append(v1)
                vv=[]
                for i in vstar:
                    vv.append(Speed)
                i=0
                a1=[]
                a=0
                while i < len(vv):
                    if vv[i] == vstar[i]:
                        a=0
                    if vv[i] != vstar[i]:
                        a = 4*(1-pow((vv[i]/vstar[i]),4))
                    a1.append(a)
                    i+=1
                i=0
                while i<len(vv):
                    if a1[i]> 4:
                        a1[i] = 4
                    if a1[i]<-4:
                        a1[i] = -4
                    i+=1
                t11=[]
                i=0
                t=0
                while i<len(vv):
                    if a1[i]==0:
                        t=0
                    else:
                        t=(vstar[i]-vv[i])/a1[i]
                    t11.append(t)
                    i+=1
                x3=[]
                x1=0
                t=0
                i=0
                t22=[]
                m=0
                while i<len(vv):
                    x1 = 0.5 * a1[i] * t11[i] * t11[i] + vv[i] * t11[i]
                    if x1 == DistanceToSigHead:
                        t=t11[i]
                    elif DistanceToSigHead < x1:
                        if a1[i] != 0:
                            t = (-vv[i]+math.sqrt(vv[i]*vv[i]+2*a1[i]*DistanceToSigHead))/a1[i]
                        else:
                            t = DistanceToSigHead/vv[i]
                    else:
                        x2=DistanceToSigHead-x1
                        t= t11[i] + x2/vstar[i]
                    t22.append(t)
                    i+=1
                tf1=0
                tf2=0 
                
                    
                if vehAttributes[vehsAttNames['Lane\Link']] in LinkA:
                    tf11= [x[4] for x in sigTypesAttributes if x[6] == True]
                    tf1= tf11[0]             
                    tf22 = [x[5] for x in sigTypesAttributes if x[6] == True]
                    tf2= tf22[0]
              
                    
                if vehAttributes[vehsAttNames['Lane\Link']] in LinkB:
                    tf11= [x[4] for x in sigTypesAttributes if x[7] == True]
                    tf1= tf11[0]
                    tf22= [x[5] for x in sigTypesAttributes if x[7] == True]
                    tf2= tf22[0]
                    
                if vehAttributes[vehsAttNames['Lane\Link']] in LinkC:
                    tf11= [x[4] for x in sigTypesAttributes if x[8] == True]
                    tf1= tf11[0]
                    tf22= [x[5] for x in sigTypesAttributes if x[8] == True]
                    tf2= tf22[0]
                    
                    
                if vehAttributes[vehsAttNames['Lane\Link']] in LinkD:
                    tf11= [x[4] for x in sigTypesAttributes if x[9] == True]
                    tf1= tf11[0]
                    tf22= [x[5] for x in sigTypesAttributes if x[9] == True]
                    tf1= tf11[0]
                    

                i=0
                Time=[]
                while i < len(t22):
                    uu= t22[i]
                    if uu>= tf1 and uu <= tf2:
                        Time.append(t22[i])
                    i+=1
                VVP=[]
                i=0
                while i< len(vv):
                    VP=[]
                    j=0
                    vvv=0
                    while j < t22[i]:
                        while j <= t11[i]:
                            vvv = a1[i] * j + vv[i]
                            VP.append(vvv)
                            j+=1
                        vvv = vstar[i]
                        VP.append(vvv)
                        j+=1
                    try:
                        if j<=Time[0] and j>=Time[-1]:
                            VVP.append(VP)
                    except: 
                        VVP =[[vv[i]]]
                        
                    i+=1
                AAP=[]
                i=0
                while i< len(vv):
                    AP=[]
                    j=0
                    aaa = 0
                    while j < t22[i]:
                        while j <= t11[i]:
                            aaa = a1[i]
                            AP.append(aaa)
                            j+=1
                        aaa=0
                        AP.append(aaa)
                        j+=1
                    try:
                        if j <= Time[0] and j >= Time[-1]:
                            AAP.append(AP)
                    except:
                        AAP = [[0]]
                        
                    i+=1
                F=[]
                for z in VVP:
                    for n in AAP:
                        y=0
                        i=0
                        while i < len(z):
                            y = y + z[i]
                            i+=1
                            if y < DistanceToSigHead:
                                continue
                            else:
                                break
                        f=0
                        j=0
                        while j < len(n):
                            if No == 101:
                                f = f + (0.003 * ( 1256 * n[j] + 1.3 * z[j] * z[j])* ( 1256 * n[j] + 1.3 * z[j] * z[j]) +  z[j] * (1.3 * z[j] * z[j] + 0.006 * 1256 + 9.8) + 0.95 * 1256 * n[j] * z[j])
                                j+=1
                                if j<=i:
                                    continue
                                else:
                                    break
                                F.append(f)

                            else:
                                f=f+(max((0.444 + 0.09 * z[j] * (0.333 + 0.00108 * z[j] * z[j] * 1256 * n[j]) + 0.04 * 1256 * z[j] * n[j] * n[j]), 0.444))
                                j+=1
                                if j<=i:
                                    continue
                                else:
                                    break
                                F.append(f)
                try:
                    desSpeed=VVP[F.index(min(F))][-1]
                except:
                    desSpeed= vehAttributes[vehsAttNames['Speed']]
                    
                optimalSpeed=0
                
                if SpeedMinForGreenEnd1 < desSpeed:
                    optimalSpeed = desSpeed
                else:
                    optimalSpeed = SpeedMinForGreenEnd1
                    
                if optimalSpeed < SpeedMaxForGreenStart1:
                    optimalSpeed = optimalSpeed
                else:
                    optimalSpeed = SpeedMaxForGreenStart1
                if SpeedMinForGreenEnd1 > SpeedMaxForGreenStart1:
                    optimalSpeed = OrgDesSpeed
                    

                    
                        
                vehAttributes[vehsAttNames['DesSpeed']] = optimalSpeed


        vehicleNumDesiredSpeeds = [[x[vehsAttNames['DesSpeed']], x[vehsAttNames['OrgDesSpeed']]] for x in vehsAttributes]
        Vissim.Net.Vehicles.SetMultipleAttributes(('DesSpeed', 'OrgDesSpeed'), vehicleNumDesiredSpeeds)
