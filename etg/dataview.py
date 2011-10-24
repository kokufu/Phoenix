#---------------------------------------------------------------------------
# Name:        etg/dataview.py
# Author:      Kevin Ollivier
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_dataview"
NAME      = "dataview"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 
            'wxDataViewColumn',
            'wxDataViewCtrl',
            'wxDataViewEvent',
            'wxDataViewItem',
            'wxDataViewItemAttr',
            'wxDataViewModel',
            'wxDataViewModelNotifier',
            'wxDataViewRenderer',
         ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    #module.items.append(etgtools.TypedefDef(type='void*', name='wxPyLongPtr'))
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxDataViewModel')
    c.abstract = True
    # Ignore the stock GetValue API, we handle it in src/dataviewhelpers.sip
    c.find('GetValue').ignore()
    
    c.addDtor()
        
    c = module.find('wxDataViewRenderer')
    c.abstract = True
    
    c = module.find('wxDataViewCtrl')
    
    module.includePyCode('src/dataview_ex.py')
    
    tools.fixWindowClass(c)
    
    module.addItem(tools.wxArrayWrapperTemplate('wxDataViewItemArray', 'wxDataViewItem', module))
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

