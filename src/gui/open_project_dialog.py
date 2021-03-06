#===============================================================================
# Delphos - a decision-making tool for community-based marine conservation.
# 
# @copyright	2007 Ecotrust
# @author		Tim Welch
# @contact		twelch at ecotrust dot org
# @license		GNU GPL 2 
# 
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.  The full license for this distribution
# has been made available in the file LICENSE.txt
#
# $Id$
#
# @summary - 
#===============================================================================

import os
import re
from os import path

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from open_project_ui import Ui_OpenProjectDialog

class OpenProjectDialog(QDialog, Ui_OpenProjectDialog):
    """Manages the open project dialog
    """
    def __init__(self, gui_manager, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.gui_manager = gui_manager
        self.isError = False	#Error flag for form processing
        self.errorMsg = ""
        self.default_file_extension = "dlp"	#Also defined in accept regex below
        
        self.filename = ""
        self.project_path = ""
        
        #Connect slots to signals
        QObject.connect(self.project_browse_button,QtCore.SIGNAL("clicked()"), self.process_browse)
        QObject.connect(self.open_button_box,QtCore.SIGNAL("accepted()"), self.process_accept)
        QObject.connect(self.open_button_box,QtCore.SIGNAL("rejected()"), self.process_reject)
        
        self.retranslate() #Translate the UI

    def process_browse(self):
        """Processes clicking of browse button
        """
        fd = QtGui.QFileDialog(self)
        fd.setFileMode(QFileDialog.ExistingFile)
        fd.setFilter("*.dlp")
        full_name = fd.getOpenFileName()

        self.filename = path.basename(str(full_name))
        self.project_path = path.dirname(str(full_name))

        #Put path & filename into textbox
        self.project_path_edit.setText(full_name)

    def process_accept(self):
        """Processes clicking of OK button in dialog
        """
        self.project_type = ""

        if not self.filename:
            self.isError = True
            QMessageBox.critical(self,self.open_project_error, self.sel_project_str)
        elif not re.search('[.]'+self.default_file_extension+'$', self.filename):
            self.isError = True
            QMessageBox.critical(self,self.open_project_error, self.valid_extension+self.default_file_extension)


        if self.isError:
            self.isError = False
        else:
            self.emit(SIGNAL("open_project_info_collected"), self.filename, self.project_path)
            
    def process_reject(self):
        """Processes clicking of Cancel button in dialog
        """
        self.hide()
        
    def retranslate(self):
        #self. = QApplication.translate("", "", "", QApplication.UnicodeUTF8)   
        self.open_project_error = QApplication.translate("OpenProjectDialog", "Open Project Error", "", QApplication.UnicodeUTF8)        
        self.sel_project_str = QApplication.translate("OpenProjectDialog", "Please select a project by clicking the browse button", "", QApplication.UnicodeUTF8)        
        self.valid_extension = QApplication.translate("OpenProjectDialog ", "You did not choose a valid Delphos project file with an extension of: ", "", QApplication.UnicodeUTF8)        