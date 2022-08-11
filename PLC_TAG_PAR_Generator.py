#from asyncore import write
import csv
#from email import header
from io import TextIOWrapper
#from operator import length_hint
#from tabnanny import verbose
flag = False
#verbose_level=True
verbose_level=False
PAR_Generator_Enable=True
#PAR_Generator_Enable=False
HMI_Tag_Generator_Enable=True
#Espacio caracter arabe para usar en parameter files = " "
plc_file = open("AllenBradley/plc_export.csv")
type(plc_file)

hmi_file_ai= open("AllenBradley/export_plantilla_HMI.csv")
type(hmi_file_ai)

hmi_file_di= open("AllenBradley/export_plantilla_HMI_DI.csv")
type(hmi_file_di)
hmi_file_sdv= open("AllenBradley/export_plantilla_HMI_SDV.csv")
type(hmi_file_sdv)
hmi_file_pid= open("AllenBradley/export_plantilla_HMI_PID.csv")
type(hmi_file_pid)

csvreader = csv.reader(plc_file)
hmi_csvreader_ai = csv.reader(hmi_file_ai,quoting=csv.QUOTE_NONE)
hmi_csvreader_di = csv.reader(hmi_file_di,quoting=csv.QUOTE_NONE)
hmi_csvreader_sdv = csv.reader(hmi_file_sdv,quoting=csv.QUOTE_NONE)
hmi_csvreader_pid = csv.reader(hmi_file_pid,quoting=csv.QUOTE_NONE)

header = []
hmi_header_ai=[]
hmi_header_sdv=[]
hmi_header_pid=[]



for i in range(0,7):#Skip unuseful lines to get header
    header = next(csvreader)

hmi_header_ai = next(hmi_csvreader_ai)
hmi_header_di = next(hmi_csvreader_di)
hmi_header_sdv = next(hmi_csvreader_sdv)
hmi_header_pid = next(hmi_csvreader_pid)
rows = []
for row in csvreader:
        rows.append(row)

hmi_rows_ai=[]
for hmi_row in hmi_csvreader_ai:
    hmi_rows_ai.append(hmi_row)
    #print(hmi_row)
hmi_rows_di=[]
for hmi_row in hmi_csvreader_di:
    hmi_rows_di.append(hmi_row)
    #print(hmi_row)
hmi_rows_sdv=[]
for hmi_row in hmi_csvreader_sdv:
    hmi_rows_sdv.append(hmi_row)
    #print(hmi_row)
hmi_rows_pid=[]
for hmi_row in hmi_csvreader_pid:
    hmi_rows_pid.append(hmi_row)
    #print(hmi_row)
plc_file.close
hmi_file_ai.close
hmi_file_di.close
hmi_file_sdv.close
hmi_file_pid.close

def list2str(data,mode):
    data = str(data)
    if mode==1:
        data = data.replace(' ','')
    data = data.replace("'",'')
    data = data.replace('[','')
    data = data.replace(']','')
    #data = data.replace('\\t','')  
    return data

def row2tag(Tag,data):
    data = str(data)
    data = data.replace("@",Tag)
    data = data.replace("PLC","[PLC]")
    return data

def GeneratePARFile(Tag:str, TYPE:str):
    conn_name="PLC"
    path_file="AllenBradley/PAR"
    path_file_udt="AllenBradley/PAR/UDT"
    ai_params=['BP','EU_MAX','EU_MIN','SP_HH','SP_H','SP_L','SP_LL','EU','XMTR_FAULT','TRIP_HH','TRIP_H','TRIP_L','TRIP_LL','SPB_S']
    ai_params_extra=['Tag','Unidad_EU','Descripcion']
    ai_params_extra2=['TD','TD1','TD2','TIME_SD']
    pid_params=['PV','XMTR_FAULT','EU_MAX','EU_MIN','SP','P','I','D','CVM','CV_MAX','CV_MIN','CV','MODE','SP_HLIMIT','SP_LLIMIT']
    pid_param_extra=['Tag','Descripcion','Unidad_PV','Unidad_SP','%']
    motor_params=['BP','AVBLE','LR','AM','CMD_STR','CMD_STP','SD_CMD','OUT','FDBK','FAULT']
    motor_params_extra=['Tag','Bomba de Inyeccion']
    motor_params_extra2=['KQ','AM_STATUS']
    motor_params_vfd=['FDBK','FAULT']
    motor_params_vfd_extra=['Vel medida','Salida Man']
    di_params=['SIG_IN','BP','TD2','TRIP','SBP_S','TIME_SD','XMTR_FAULT']
    di_params_extra=['OK','Estado_1','Tag','Descripcion','seg','min']
    sdv_params=['SD','BP','OPEN','CLOSE','AUTO_RST','ZIC','ZIO','RESET','SOV','FAULT']
    sdv_params_extra=['Tag','Descripcion']
    sdv_params_extra2=['RST','Time_OUT','MA']
    udt_valv_param_extra=['Tag','Descripcion']
    udt_valv_params=['Inp_Abrir','Inp_Cerrar','Sts_Abierta','Sts_Cerrada','Sts_Falla','Out_Apertura','Enc_On','Inp_Reset']
    intlk_params=['IN01','IN02','IN03','IN04','IN05','IN06','IN07','IN08','IN09','IN10','IN11','IN12','IN13','IN14','IN15','IN16']
    #intlk_params_extra=['',]

    if PAR_Generator_Enable:
        Tag_ok=Tag.replace("_","-")
        print(TYPE)
        pass
        if TYPE is "F_AI":
            Tag_ok=Tag_ok[4:]
            with open(f'{path_file}/{Tag}.par','w',encoding="utf-16") as f:

                for index,param in enumerate(ai_params):
                    print(f'#{index+1}=[{conn_name}]{Tag}.{param}\n')
                    f.write(f'#{index+1}=[{conn_name}]{Tag}.{param}\n')
                for i,extra in enumerate(ai_params_extra):
                    if extra == "Tag":
                        extra = extra.replace("Tag",Tag_ok)
                        print(f'#{index+i+2}={extra}\n')
                        f.write(f'#{index+i+2}={extra}\n')
                    elif extra == "Unidad_EU":
                        if ((Tag.find('FIT') != -1) or (Tag.find('FI') != -1) or (Tag.find('FT') != -1)) :
                            extra = "m3/dia"
                            print(f'#{index+i+2}={extra}\n')
                            f.write(f'#{index+i+2}={extra}\n')
                        elif ((Tag.find('LIT') != -1) or (Tag.find('LI') != -1) or (Tag.find('LT') != -1)) :
                            extra = "m"
                            print(f'#{index+i+2}={extra}\n')
                            f.write(f'#{index+i+2}={extra}\n')
                        elif ((Tag.find('PIT') != -1) or (Tag.find('PI') != -1) or (Tag.find('PT') != -1)) :
                            extra = "kg/cm2"
                            print(f'#{index+i+2}={extra}\n')
                            f.write(f'#{index+i+2}={extra}\n')
                        else:
                            extra = "Unidad"
                            print(f'#{index+i+2}={extra}\n')
                            f.write(f'#{index+i+2}={extra}\n')
                    elif extra == "Descripcion":
                        if (Tag.find('FIT') != -1) or (Tag.find('FT') != -1) :
                            extra = "Transmisor de Caudal "+Tag_ok
                            print(f'#{index+i+2}={extra}\n')
                            f.write(f'#{index+i+2}={extra}\n')
                        elif (Tag.find('PIT') != -1) or (Tag.find('PT') != -1) :
                            extra = "Transmisor de Presion "+Tag_ok
                            print(f'#{index+i+2}={extra}\n')
                            f.write(f'#{index+i+2}={extra}\n')
                        elif (Tag.find('LIT') != -1) or (Tag.find('LT') != -1) :
                            extra = "Transmisor de Nivel "+Tag_ok
                            print(f'#{index+i+2}={extra}\n')
                            f.write(f'#{index+i+2}={extra}\n')
                        elif (Tag.find('TIT') != -1) or (Tag.find('TT') != -1) :
                            extra = "Transmisor de Temperatura "+Tag_ok
                            print(f'#{index+i+2}={extra}\n')
                            f.write(f'#{index+i+2}={extra}\n')
                        elif Tag.find('Velocidad') != -1 :
                            extra = "Feedback de Velocidad de "+Tag_ok
                            print(f'#{index+i+2}={extra}\n')
                            f.write(f'#{index+i+2}={extra}\n')
                        else:
                            print(f'#{index+i+2}={extra}\n')
                            f.write(f'#{index+i+2}={extra}\n')
                    else:
                        print(f'#{index+i+2}={extra}\n')
                        f.write(f'#{index+i+2}={extra}\n')
                    
                for i2,extra2 in enumerate(ai_params_extra2):
                    print(f'#{index+i+i2+3}=[{conn_name}]{Tag}.{extra2}\n')
                    f.write(f'#{index+i+i2+3}=[{conn_name}]{Tag}.{extra2}\n')
            f.close()
        if TYPE is "F_PID":
            Tag_ok=Tag_ok[4:]
            if (Tag_ok.find('T') != -1) :
                Tag_Ctrl=Tag_ok.replace("T","C")
            else:
                Tag_Ctrl=Tag_ok
            with open(f'{path_file}/{Tag}.par','w',encoding="utf-16") as f:
                for pid_index,pid_param in enumerate(pid_params):
                    print(f'#{pid_index+1}=[{conn_name}]{Tag}.{pid_param}\n')
                    f.write(f'#{pid_index+1}=[{conn_name}]{Tag}.{pid_param}\n')
                for i,extra in enumerate(pid_param_extra):
                    if extra == "Tag":
                        extra = extra.replace("Tag",Tag_Ctrl)
                        print(f'#{pid_index+i+2}={extra}\n')
                        f.write(f'#{pid_index+i+2}={extra}\n')
                    elif extra == "Descripcion":
                        if (Tag.find('FIT') != -1) or (Tag.find('FT') != -1) :
                            extra = "Control de Caudal "+Tag_Ctrl
                            print(f'#{pid_index+i+2}={extra}\n')
                            f.write(f'#{pid_index+i+2}={extra}\n')
                        elif (Tag.find('PIT') != -1) or (Tag.find('PT') != -1) :
                            extra = "Control de Presion "+Tag_Ctrl
                            print(f'#{pid_index+i+2}={extra}\n')
                            f.write(f'#{pid_index+i+2}={extra}\n')
                        elif (Tag.find('LIT') != -1) or (Tag.find('LT') != -1) :
                            extra = "Control de Nivel "+Tag_Ctrl
                            print(f'#{pid_index+i+2}={extra}\n')
                            f.write(f'#{pid_index+i+2}={extra}\n')
                        elif (Tag.find('TIT') != -1) or (Tag.find('TT') != -1) :
                            extra = "Control de Temperatura "+Tag_ok
                            print(f'#{pid_index+i+2}={extra}\n')
                            f.write(f'#{pid_index+i+2}={extra}\n')
                        elif Tag.find('Velocidad') != -1 :
                            extra = "Feedback de Velocidad de "+Tag_ok
                            print(f'#{pid_index+i+2}={extra}\n')
                            f.write(f'#{pid_index+i+2}={extra}\n')
                        else:
                            print(f'#{pid_index+i+2}={extra}\n')
                            f.write(f'#{pid_index+i+2}={extra}\n')
                    elif extra == "Unidad_PV" or extra == "Unidad_SP":
                        if ((Tag.find('FIT') != -1) or (Tag.find('FI') != -1) or (Tag.find('FT') != -1)) :
                            extra = "m3/dia"
                            print(f'#{pid_index+i+2}={extra}\n')
                            f.write(f'#{pid_index+i+2}={extra}\n')
                        elif ((Tag.find('LIT') != -1) or (Tag.find('LI') != -1) or (Tag.find('LT') != -1)) :
                            extra = "m"
                            print(f'#{pid_index+i+2}={extra}\n')
                            f.write(f'#{pid_index+i+2}={extra}\n')
                        elif ((Tag.find('PIT') != -1) or (Tag.find('PI') != -1) or (Tag.find('PT') != -1)) :
                            extra = "kg/cm2"
                            print(f'#{pid_index+i+2}={extra}\n')
                            f.write(f'#{pid_index+i+2}={extra}\n')
                        else:
                            extra = "Unidad"
                            print(f'#{pid_index+i+2}={extra}\n')
                            f.write(f'#{pid_index+i+2}={extra}\n')
                    else:
                        print(f'#{pid_index+i+2}={extra}\n')
                        f.write(f'#{pid_index+i+2}={extra}\n')
            f.close()
        if TYPE is "F_MOTOR":
            Tag_ok=Tag_ok[4:]
            with open(f'{path_file}/{Tag}.par','w',encoding="utf-16") as f:
                for motor_index,motor_param in enumerate(motor_params):
                    if motor_param == "BP":
                        print(f'#{motor_index+1}=[{conn_name}]{Tag}_INTLK.{motor_param}\n')
                        f.write(f'#{motor_index+1}=[{conn_name}]{Tag}_INTLK.{motor_param}\n')
                    else:
                        print(f'#{motor_index+1}=[{conn_name}]{Tag}.{motor_param}\n')
                        f.write(f'#{motor_index+1}=[{conn_name}]{Tag}.{motor_param}\n')
                for i,extra in enumerate(motor_params_extra):
                    if extra == "Tag":
                        Tag_ok=Tag.replace("_","-")
                        extra = extra.replace("Tag",Tag_ok)
                        print(f'#{motor_index+i+2}={extra}\n')
                        f.write(f'#{motor_index+i+2}={extra}\n')
                    else:
                        Tag_ok=Tag.replace("_","-")
                        print(f'#{motor_index+i+2}={extra} {Tag_ok}\n')
                        f.write(f'#{motor_index+i+2}={extra} {Tag_ok}\n')
                for i2,extra2 in enumerate(motor_params_extra2):
                    print(f'#{motor_index+i+i2+3}=[{conn_name}]{Tag}.{extra2}\n')
                    f.write(f'#{motor_index+i+i2+3}=[{conn_name}]{Tag}.{extra2}\n')
            f.close()
            with open(f'{path_file}/{Tag}_VFD.par','w',encoding="utf-16") as f2:
                for i_vfd,extra in enumerate(motor_params_extra):
                    if extra == "Tag":
                        Tag_ok=Tag.replace("_","-")
                        extra = extra.replace("Tag",Tag_ok)
                        print(f'#{i_vfd+1}={extra}\n')
                        f2.write(f'#{i_vfd+1}={extra}\n')
                    else:
                        Tag_ok=Tag.replace("_","-")
                        print(f'#{i_vfd+1}={extra}\n')
                        f2.write(f'#{i_vfd+1}={extra}\n')
                for i_vfd2,motor_param_vfd in enumerate(motor_params_vfd):
                        print(f'#{i_vfd+i_vfd2+2}=[{conn_name}]{Tag}.{motor_param_vfd}\n')
                        f2.write(f'#{i_vfd+i_vfd2+2}=[{conn_name}]{Tag}.{motor_param_vfd}\n')
                for i_vfd3,extra in enumerate(motor_params_vfd_extra):
                        print(f'#{i_vfd3+i_vfd+i_vfd2+3}={extra}\n')
                        f2.write(f'#{i_vfd3+i_vfd+i_vfd2+3}={extra}\n')
            f2.close()
        if TYPE is "F_DI":
            Tag_ok=Tag_ok[4:]
            high_low=""
            with open(f'{path_file}/{Tag}.par','w',encoding="utf-16") as f:

                for di_index,di_param in enumerate(di_params):
                    print(f'#{di_index+1}=[{conn_name}]{Tag}.{di_param}\n')
                    f.write(f'#{di_index+1}=[{conn_name}]{Tag}.{di_param}\n')
                for i,extra in enumerate(di_params_extra):
                    if extra == "Tag":
                        extra = extra.replace("Tag",Tag_ok)
                        print(f'#{di_index+i+2}={extra}\n')
                        f.write(f'#{di_index+i+2}={extra}\n')
                    elif extra == "Estado_1":
                        if ((Tag.find('FSH') != -1) or (Tag.find('PSH') != -1) or (Tag.find('LSH') != -1)) :
                            extra = "H"
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                        elif ((Tag.find('FSL') != -1) or (Tag.find('PSL') != -1) or (Tag.find('LSL') != -1)) :
                            extra = "L"
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                        else:
                            extra = "ACTIVO"
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')

                    elif extra == "Descripcion":
                        if (Tag.find('FS') != -1) or (Tag.find('FT') != -1) :
                            if Tag.find('H') != -1:
                                high_low="Alto"
                            elif Tag.find('L') != -1:
                                high_low="Bajo"
                            else:
                                high_low=""
                            extra = f"Indicador de Caudal {high_low}"+Tag_ok
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                        elif (Tag.find('PS') != -1) or (Tag.find('PT') != -1) :
                            if Tag.find('H') != -1:
                                high_low="Alta"
                            elif Tag.find('L') != -1:
                                high_low="Baja"
                            else:
                                high_low=""
                            extra = f"Indicador de {high_low} Presion "+Tag_ok
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                        elif (Tag.find('LS') != -1) or (Tag.find('LT') != -1) :
                            if Tag.find('LSH') != -1:
                                high_low="Alto"
                            elif Tag.find('LSL') != -1:
                                high_low="Bajo"
                            else:
                                high_low=""
                            extra = f"Indicador de {high_low} Nivel "+Tag_ok
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                        elif (Tag.find('TS') != -1) or (Tag.find('TT') != -1) :
                            extra = "Termostato "+Tag_ok
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                        elif Tag.find('HS')!= -1 :
                            extra = "Pulsador de emergencia "+Tag_ok
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                        elif Tag.find('UF')!= -1 :
                            extra = "Falla de bomba P"+Tag_ok[2:]
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                        elif Tag.find('UE')!= -1 :
                            extra = "Estado de bomba P"+Tag_ok[2:]
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                        elif Tag.find('US')!= -1 :
                            extra = "Local/Remoto P"+Tag_ok[2:]
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                        else :
                            extra = "Descripcion "+Tag_ok
                            print(f'#{di_index+i+2}={extra}\n')
                            f.write(f'#{di_index+i+2}={extra}\n')
                    
                    else:
                        print(f'#{di_index+i+2}={extra}\n')
                        f.write(f'#{di_index+i+2}={extra}\n')
            f.close()
        if TYPE is "UDT_Valvula":
            with open(f'{path_file}/{Tag}.par','w',encoding="utf-16") as f:
                
                for i,extra in enumerate(udt_valv_param_extra):
                    if extra == "Tag":
                        extra = extra.replace("Tag",Tag_ok)
                        print(f'#{i+1}={extra}\n')
                        f.write(f'#{i+1}={extra}\n')
                    elif extra == "Descripcion":
                        extra = "Valvula de Control"
                        print(f'#{i+1}={extra}\n')
                        f.write(f'#{i+1}={extra}\n')
                    else:
                        print(f'#{i+1}={extra}\n')
                        f.write(f'#{i+1}={extra}\n')
                for udt_v_index,udt_v_param in enumerate(udt_valv_params):
                    if udt_v_param == "BP":
                        f.write(f'#{udt_v_index+i+2}=[{conn_name}]{Tag}_INTLK.{udt_v_param}\n')
                    elif udt_v_param == "RESET":
                        f.write(f'#{udt_v_index+i+2}=[{conn_name}]{Tag}_INTLK.{udt_v_param}\n')
                    else:
                        f.write(f'#{udt_v_index+i+2}=[{conn_name}]{Tag}.{udt_v_param}\n')
                    print(f'#{udt_v_index+i+2}=[{conn_name}]{Tag}.{udt_v_param}\n')
            f.close()
        if TYPE is "F_SDV":
            with open(f'{path_file}/{Tag}.par','w',encoding="utf-16") as f:
                for sdv_index,sdv_param in enumerate(sdv_params):
                    if sdv_param == "BP":
                        f.write(f'#{sdv_index+1}=[{conn_name}]{Tag}_INTLK.{sdv_param}\n')
                    elif sdv_param == "RESET":
                        f.write(f'#{sdv_index+1}=[{conn_name}]{Tag}_INTLK.{sdv_param}\n')
                    else:
                        f.write(f'#{sdv_index+1}=[{conn_name}]{Tag}.{sdv_param}\n')
                    print(f'#{sdv_index+1}=[{conn_name}]{Tag}.{sdv_param}\n')
                    
                for i,extra in enumerate(sdv_params_extra):
                    if extra == "Tag":
                        extra = extra.replace("Tag",Tag_ok)
                        print(f'#{sdv_index+i+2}={extra}\n')
                        f.write(f'#{sdv_index+i+2}={extra}\n')
                    elif extra == "Descripcion":
                        extra = "Valvula ON/OFF"
                        print(f'#{sdv_index+i+2}={extra}\n')
                        f.write(f'#{sdv_index+i+2}={extra}\n')
                    else:
                        print(f'#{sdv_index+i+2}={extra}\n')
                        f.write(f'#{sdv_index+i+2}={extra}\n')
                for i2,extra2 in enumerate(sdv_params_extra2):
                    print(f'#{sdv_index+i+i2+3}=[{conn_name}]{Tag}.{extra2}\n')
                    f.write(f'#{sdv_index+i+i2+3}=[{conn_name}]{Tag}.{extra2}\n')
            f.close()
        if TYPE is "F_INTLK":
            j = 0
            k = 0
            l = 0
            with open(f'{path_file}/{Tag}.par','w',encoding="utf-16") as f:
                for intlk_index,intlk_param in enumerate(intlk_params):
                    print(f'#{intlk_index+1}=[{conn_name}]{Tag}.{intlk_param}\n')
                    f.write(f'#{intlk_index+1}={{[{conn_name}]{Tag}.{intlk_param}}}\n')
                for i in range(intlk_index+2,200):

                    if i == 32 :
                        f.write(f'#{i}={{[{conn_name}]{Tag}.First_Out}}\n')
                    elif i >= 51 and i <= 66 :
                        l=l+1
                        f.write(f'#{i}={l}\n')
                    elif i == 99 :
                        f.write(f'#{i}={{[{conn_name}]{Tag}.RESET}}\n')
                    elif i == 100 :
                        #Siendo el formato del Tag = TAG_INTLK, se le sacan los ultimos 6 caracteres
                        FinalTag=Tag_ok[:-6]
                        f.write(f'#{i}={FinalTag}\n')
                    elif i >= 101 and i <= 116 :
                        k=k+1
                        f.write(f'#{i}=\' \n')
                    elif i >= 151 and i <= 166 :
                        j=j+1
                        f.write(f'#{i}=\'Tripped\'\n')
                    else:
                        f.write(f'#{i}=\'Empty\'\n')
                # for i,extra in enumerate(intlk_params_extra):
                #     print(f'#{intlk_index+i+2}={extra}\n')
                #     f.write(f'#{intlk_index+i+2}={extra}\n')
            f.close()

def GenerateCSVImport(Tag:str, TYPE:str, fd:TextIOWrapper,HMI_Tag_Generator_Enable:bool,template_list:list):
    if HMI_Tag_Generator_Enable:
        #print(len(template_list))
        #print(f"fd:{fd}")
        if TYPE is "F_AI":
            for i in range(0,len(template_list)):
                aux_str=list2str(template_list[i],1)
                #aux_str=template_list[i]
                writebuff=row2tag(Tag,aux_str)
                fd.write(writebuff)
                fd.write('\n')
                print(writebuff)
        if TYPE is "F_DI":
            for i in range(0,len(template_list)):
                aux_str=list2str(template_list[i],1)
                #aux_str=template_list[i]
                writebuff=row2tag(Tag,aux_str)
                fd.write(writebuff)
                fd.write('\n')
                print(writebuff)
        if TYPE is "F_SDV":
            for i in range(0,len(template_list)):
                aux_str=list2str(template_list[i],1)
                #aux_str=template_list[i]
                writebuff=row2tag(Tag,aux_str)
                fd.write(writebuff)
                fd.write('\n')
                print(writebuff)
        if TYPE is "F_PID":
            for i in range(0,len(template_list)):
                aux_str=list2str(template_list[i],1)
                #aux_str=template_list[i]
                writebuff=row2tag(Tag,aux_str)
                fd.write(writebuff)
                fd.write('\n')
                print(writebuff)

fd_hmi= open(f'AllenBradley/hmi_tags.csv','w',encoding="utf-16")
writebuff=list2str(hmi_header_ai,2)
fd_hmi.write(writebuff)
print(writebuff)
fd_hmi.write('\n')
hmi_rows_template_ai=[]
hmi_rows_template_di=[]
hmi_rows_template_sdv=[]
hmi_rows_template_pid=[]
#1er parte del template de import es igual
for i in range(0,5):
    writebuff=list2str(hmi_rows_ai[i],2)
    print(writebuff)
    fd_hmi.write(writebuff)
    fd_hmi.write('\n')
for j in range(6,len(hmi_rows_ai)+1):     
    hmi_rows_template_ai.append(hmi_rows_ai[j-1])
for k in range(6,len(hmi_rows_di)+1):     
    hmi_rows_template_di.append(hmi_rows_di[k-1])
for k in range(6,len(hmi_rows_sdv)+1):     
    hmi_rows_template_sdv.append(hmi_rows_sdv[k-1])
for k in range(6,len(hmi_rows_pid)+1):     
    hmi_rows_template_pid.append(hmi_rows_pid[k-1])


for index, row_item in enumerate(rows):
        #print(index)
        if len(row_item):
            #print("Item 1: "+row_item[0]+"--- Item 2: "+row_item[1]+"--- Item 3: "+row_item[2])
            if 'TAG' in row_item[0]:
                if 'F_AI' in row_item[0]:
                    aux_row=row_item[0]
                    taginfo=aux_row.split(";")
                    GeneratePARFile(taginfo[2],"F_AI")
                    GenerateCSVImport(taginfo[2],"F_AI",fd_hmi,HMI_Tag_Generator_Enable,hmi_rows_template_ai)
                    if verbose_level== 1:
                        print("ES AI: "+taginfo[2])
                if 'F_DI' in row_item[0]:
                    aux_row=row_item[0]
                    taginfo=aux_row.split(";")
                    GeneratePARFile(taginfo[2],"F_DI")
                    GenerateCSVImport(taginfo[2],"F_DI",fd_hmi,HMI_Tag_Generator_Enable,hmi_rows_template_di)
                    if verbose_level== 1:
                        print("ES DI: "+taginfo[2])
                if 'F_PID' in row_item[0]:
                    aux_row=row_item[0]
                    taginfo=aux_row.split(";")
                    GeneratePARFile(taginfo[2],"F_PID")
                    GenerateCSVImport(taginfo[2],"F_PID",fd_hmi,HMI_Tag_Generator_Enable,hmi_rows_template_pid)
                    if verbose_level== 1:
                        print("ES PID: "+taginfo[2])
                if 'F_MOTOR' in row_item[0]:
                    aux_row=row_item[0]
                    taginfo=aux_row.split(";")
                    GeneratePARFile(taginfo[2],"F_MOTOR")
                    if verbose_level== 1:
                        print("ES MOTOR: "+taginfo[2])
                if 'F_SDV' in row_item[0]:
                    aux_row=row_item[0]
                    taginfo=aux_row.split(";")
                    GeneratePARFile(taginfo[2],"F_SDV")
                    GenerateCSVImport(taginfo[2],"F_SDV",fd_hmi,HMI_Tag_Generator_Enable,hmi_rows_template_sdv)
                    if verbose_level== 1:
                        print("ES SDV: "+taginfo[2])
                if 'F_AO' in row_item[0]:
                    aux_row=row_item[0]
                    taginfo=aux_row.split(";")
                    if verbose_level== 1:
                        print("ES AO: "+taginfo[2])
                if 'F_INTLK' in row_item[0]:
                    aux_row=row_item[0]
                    taginfo=aux_row.split(";")
                    if verbose_level== 1:
                        print("ES INTLK: "+taginfo[2])
                    GeneratePARFile(taginfo[2],"F_INTLK")
                if 'UDT_Valvula' in row_item[0]:
                    aux_row=row_item[0]
                    taginfo=aux_row.split(";")
                    if verbose_level== 1:
                        print("ES UDT_VALV: "+taginfo[2])
                    GeneratePARFile(taginfo[2],"UDT_Valvula")
                    
fd_hmi.close()
print("--Fin de Script---")
