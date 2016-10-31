db.define_table('linearWaveForm',
                Field('waveHeight','double','default',0.85),
                Field('wavePeriod','double','default',3.00),
                Field('waveBreakRatio','double','default',0.78),
                Field('waterDepth','double','default',6.0)
    )

db.linearWaveForm.waveHeight.requires<=25.0
db.linearWaveForm.wavePeriod.requires<=20.0
db.linearWaveForm.waveBreakRatio.requires<=0.86
db.linearWaveForm.waterDepth.requires<=80.0
