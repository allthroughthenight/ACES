
def linearWaveForm():
    record=db(db.linearWaveForm.id>0).count()
    labelTable={'waveHeight':'Wave Height [m]',
                'wavePeriod':'Wave Period [m]',
                'waveBreakRatio':'Wave Break Ratio',
                'waterDepth':'Water Depth[m]'
                }
    form1=SQLFORM(db.linearWaveForm,record-1,labels=labelTable,showid=False)
    return form1

def AcesCall(formVars):
    import subprocess
    ##formVars=dict(waveHeight=0.85,wavePeriod=6.0,waveBreakRatio=0.78,waterDepth=3.0)
    WaveHeight=float(formVars['waveHeight'])
    WavePeriod=float(formVars['wavePeriod'])
    WaveBrk=float(formVars['waveBreakRatio'])
    WaterDepth=float(formVars['waterDepth'])
    

    varList="H=%(H)f;T=%(T)f;d=%(d)f;" %dict(H=WaveHeight,T=WavePeriod,d=WaterDepth)
    varDict=dict(varList=varList, octFile=request.folder+'/models/Waves/linear_wave_theory.m')
    cmdString='octave -q --eval="%(varList)ssource(\'%(octFile)s\')"' % varDict
    a=subprocess.Popen(cmdString, shell=True, stdout=subprocess.PIPE)
    out,err=a.communicate()
    session.WaveHeight=WaveHeight
    return out
