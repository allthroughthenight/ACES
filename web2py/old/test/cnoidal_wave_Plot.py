from math import pi

from traits.api import HasTraits, Instance, DelegatesTo
from traitsui.api import View, Item, RangeEditor, UItem, Group, HGroup, VGroup
from enable.api import ComponentEditor
from chaco.api import Plot, ArrayPlotData, PlotGraphicsContext, DataLabel, VPlotContainer
from numpy import linspace, arange, sqrt
from  scipy.special import ellipk, ellipj
from ellipke import ellipke
from cnoidal_wave_Model import O1



class cnoidalView(HasTraits):
    """
    Access the model traits using DelegatesTo().
    """
    container = Instance(VPlotContainer)
    model = Instance(O1)
    
    H   =DelegatesTo('model')
    T   =DelegatesTo('model')
    d   =DelegatesTo('model')
    z   =DelegatesTo('model')
    xL  =DelegatesTo('model')
    g   =DelegatesTo('model')
    rho =DelegatesTo('model')
    time=DelegatesTo('model')

    K  = DelegatesTo('model')
    m  = DelegatesTo('model')
    A0 = DelegatesTo('model')
    A1 = DelegatesTo('model')
    B00= DelegatesTo('model')
    B10= DelegatesTo('model')
    L  = DelegatesTo('model')

    descString=DelegatesTo('model')
    
    C   = DelegatesTo('model')
    E   = DelegatesTo('model')
    Ef  = DelegatesTo('model')
    Ur  = DelegatesTo('model')
    eta = DelegatesTo('model')
    u   = DelegatesTo('model')
    w   = DelegatesTo('model')
    dudt= DelegatesTo('model')
    dwdt= DelegatesTo('model')
    pres= DelegatesTo('model')

    plotxL  = DelegatesTo('model')
    ploteta = DelegatesTo('model')
    plotuDat= DelegatesTo('model')
    plotwDat= DelegatesTo('model')

    plotu = Instance(Plot)
    plotw = Instance(Plot)
    ploty = Instance(Plot)
    

    vGroup1=VGroup(
        HGroup(Item('H',label='WaveHeight(H)' ,style = 'readonly'),
               Item('T',label='WavePeriod(T)' ,style = 'readonly'),
               Item('d',label='waterDepth(d)' ,style = 'readonly'),
               Item('Ur',label='Ursell Number(Ur)' ,style = 'readonly')
               ),
        HGroup(Item('m',label='m' ,style = 'readonly'),
               Item('L',label='Wavelength(L)' ,style = 'readonly'),
               Item('C',label='Celerity(C)' ,style = 'readonly'),
               Item('E',label='Energy density(E)' ,style = 'readonly'),
               Item('Ef',label='Energy flux(Ef)' ,style = 'readonly')
               ),
        HGroup(Item('u',label='Horz. velocity(u)' ,style = 'readonly'),
               Item('w',label='Vert. velocity(w)' ,style = 'readonly'),
               Item('dudt',label='Horz. acceleration(du/dt)' ,style = 'readonly'),
               Item('dwdt',label='Vert. acceleration(dw/dt)' ,style = 'readonly'),
               Item('pres',label='Pressure (P)' ,style = 'readonly'),
               )
        )

    traits_view = \
    View(
        Item('container', editor=ComponentEditor(), show_label=False), 
        #Group(
        #    UItem('plotu', editor=ComponentEditor(), style='custom'),
        #    ),
        #Group(
        #    UItem('plotw', editor=ComponentEditor(), style='custom'),
        #    ),
        vGroup1,
        Item('H',  label='H' , editor=RangeEditor(low=0.05,   high=10.0)),
        Item('T',  label='T' , editor=RangeEditor(low=7.00,   high=15.0)),
        resizable=True,
        width=600,
        height=650,
        title="Pump Curve",
        )
    labels=[]

    #def __init__(self,model):
    #    self.model=model
    #    self.on_trait_change(self.changePlot,name=['H','T','d'])
    
    def _container_default(self):
        model=self.model
        self.H=9.80
        H  =self.H
        K  =self.K
        m  =self.m
       
        plotxL = self.plotxL
        ploteta= self.ploteta
        plotuDat=self.plotuDat
        plotwDat=self.plotwDat
       
        data3 = ArrayPlotData(x=plotxL, y=ploteta)
        data1 = ArrayPlotData(x=plotxL, y=plotuDat)
        data2 = ArrayPlotData(x=plotxL, y=plotwDat)
        
        ploty = Plot(data3)
        plotu = Plot(data1)
        plotw = Plot(data2)
        
        
        plotu.plot(('x', 'y'), style='line', color='green')
        plotw.plot(('x', 'y'), style='line', color='blue')
        ploty.plot(('x', 'y'), style='line', color='red')

        hMax=max(plotuDat)*1.05
        hMin=min(plotuDat)*0.95
        plotu.value_range.set_bounds(hMin, hMax)

        hMax=max(plotwDat)*1.05
        hMin=min(plotwDat*0.95)
        plotw.value_range.set_bounds(hMin, hMax)
        
        ploty.y_axis.title='eta'
        plotu.y_axis.title='u'
        plotw.y_axis.title='w'

        titleString="Cnoidal Wave Theory"##%dict(D=D,d50=d50,Ld=Ld,N=N,Di=Di)
        ploty.title=titleString 

        self.plotu=plotu
        self.plotw=plotw
        self.ploty=ploty
        return VPlotContainer(plotu,plotw,ploty)

    


    def changePlot(self):
        H  =self.H
            
    
        # Get the plot's ArrayPlotData object.
        try:
            datau = self.plotu.data
            dataw = self.plotw.data 
            datay = self.ploty.data
        except AttributeError: 
            return 
            
        plotu = self.plotu
        plotw = self.plotw
        ploty = self.ploty
        
        plotxL = self.plotxL
        ploteta= self.ploteta
        plotuDat=self.plotuDat
        plotwDat=self.plotwDat

        
        
        # Update the value of Hs in the ArrayPlotData.
        datau.set_data('x', plotxL)
        datau.set_data('y', plotuDat)
        
        dataw.set_data('x', plotxL)
        dataw.set_data('y', plotwDat)

        datay.set_data('x', plotxL)
        datay.set_data('y', ploteta)

        hMax=max(plotuDat) + 0.05*abs(max(plotuDat))
        hMin=min(plotuDat) - 0.05*abs(min(plotuDat))
        plotu.value_range.set_bounds(hMin, hMax)

        hMax=max(plotwDat) + 0.05*abs(max(plotwDat))
        hMin=min(plotwDat) - 0.05*abs(min(plotwDat))
        plotw.value_range.set_bounds(hMin, hMax)


        
   
    def _H_changed(self):
        self.changePlot()
    
    def _T_changed(self):
        self.changePlot()

    def _d_changed(self):
        self.changePlot()

    def save_plot(self, filename, width=800, height=600):
        container=self.container
        container.outer_bounds=[width, height]
        container.do_layout(force=True)
        gc=PlotGraphicsContext((width, height), dpi=72)
        gc.render_component(container)
        gc.save(filename) 

if __name__ == "__main__":
    pip = O1()
    pip_viewer = cnoidalView(model=pip)
    # We use edit_traits(), so this script should be run from within ipython.
    pip_viewer.edit_traits()
