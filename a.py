import PySimpleGUI as sg
import os
import subprocess
import sys
sg.theme('DarkAmber')  
layout = [  [sg.Text('Change Permissions')],
            [sg.Text('IP'), sg.InputText(key="ip",size=(20,1)),
            sg.Text('Protocol'), sg.InputText(key="protocol",size=(10,1)),sg.Text('Destination Port'), sg.InputText(key="dport",size=(10,1))],
            [sg.InputCombo(('ACCEPT', 'REJECT','DROP'),default_value='ACCEPT',enable_events=True, key='action',size=(20,3)),
            sg.Button('Test'),sg.Button('Flush')],
            [sg.Button('View')],[sg.Output(size=(100,20),key="op")],[sg.Button('Clear')]]   

window = sg.Window('Linux Firewall', layout)    

def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None        
    retval = p.wait(timeout)
    
    return (retval, output)  


def create_command(type1,ip,protocol,io,dport): 
    command="sudo iptables"
    if type1!="":
        command+=" "
        command+=type1
    if protocol!="":
        command+=" -p "
        command+=protocol
    if dport!="":
        command+=" --dport "
        command+=dport
    if ip!="":
        command+=" -s "
        command+=ip
    if io!="":
        command+=" -j "
        command+=io
    return command


while True:
    event, values = window.read()
    if event in (None,):  
        break
    if event in ('Flush'):
        cmd = 'sudo iptables -F'
        os.system(cmd)
        
    if event in ('View'):
        cmd = 'sudo iptables -L'
        runCommand(cmd, window=window)

    if event in ('Test'):
        cmd=""
        action=values['action']
        cmd=create_command("-A INPUT",values["ip"],values["protocol"],action,values["dport"])
        runCommand(cmd, window=window)
        print(cmd)
        
    if event in ('Clear'):   
        window.FindElement('op').Update('')
window.close()
    
