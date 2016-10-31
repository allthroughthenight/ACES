from enthought.traits.api import Float, HasTraits, Instance

class Widget (HasTraits):
    cost  = Float(0.0)
    tax   = Float(0.0)
    taxRate=Float(0.1)
    def __init__(self):
        self.on_trait_change(self.update_cost,name=['cost', 'taxRate'])

    def update_cost(self):
        self.tax=self.cost*self.taxRate

