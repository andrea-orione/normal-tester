#!/usr/bin/python3.9

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import math
from scipy.stats import norm

class Finestra(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.connect("destroy", Gtk.main_quit)
        self.set_resizable(False)

        header = Gtk.HeaderBar()
        header.set_title("Test Normale")
        header.set_subtitle("Versione 1.0")
        header.set_show_close_button(True)
        self.set_titlebar(header)

        boxMain = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        boxMain.set_margin_top(10)
        boxMain.set_margin_bottom(10)
        boxMain.set_margin_start(10)
        boxMain.set_margin_end(15)
        self.add(boxMain)

        gridDati = Gtk.Grid()
        boxMain.pack_start(gridDati, False, False, 0)

        labelAtteso = Gtk.Label(label = "Valore atteso: ")
        gridDati.attach(labelAtteso, 0,0,1,1)
        self.valoreAtteso = EntryOnlyNumbers(True)
        self.valoreAtteso.set_text("0.0")
        self.valoreAtteso.set_max_length(8)
        self.valoreAtteso.set_width_chars(10)
        gridDati.attach(self.valoreAtteso, 1,0,1,1)
        labelPM1 = Gtk.Label(label = u"\u00B1")
        gridDati.attach(labelPM1, 2,0,1,1)
        self.erroreAtteso = EntryOnlyNumbers(False)
        self.erroreAtteso.set_text("0.0")
        self.erroreAtteso.set_max_length(8)
        self.erroreAtteso.set_width_chars(10)
        gridDati.attach(self.erroreAtteso, 3,0,1,1)

        labelOttenuto = Gtk.Label(label = "Valore ottenuto: ")
        gridDati.attach(labelOttenuto, 0,1,1,1)
        self.valoreOttenuto = EntryOnlyNumbers(True)
        self.valoreOttenuto.set_text("0.0")
        self.valoreOttenuto.set_max_length(8)
        self.valoreOttenuto.set_width_chars(10)
        gridDati.attach(self.valoreOttenuto, 1,1,1,1)
        labelPM2 = Gtk.Label(label = u"\u00B1")
        gridDati.attach(labelPM2, 2,1,1,1)
        self.erroreOttenuto = EntryOnlyNumbers(False)
        self.erroreOttenuto.set_text("0.0")
        self.erroreOttenuto.set_max_length(8)
        self.erroreOttenuto.set_width_chars(10)
        gridDati.attach(self.erroreOttenuto, 3,1,1,1)

        boxRisultati = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        boxRisultati.set_margin_top(10)
        boxRisultati.set_margin_start(10)
        boxRisultati.set_margin_bottom(10)
        boxMain.pack_start(boxRisultati, False, False, 0)
        labelInfo = Gtk.Label(label = u"L'indice di significatività è a 5\u0025\ne i valori limiti sono Z\u209A = \u00B1 1.95996")
        labelInfo.set_justify(Gtk.Justification.CENTER)
        labelInfo.set_margin_bottom(5)
        boxRisultati.pack_start(labelInfo, False, False, 0)
        self.zVal = Gtk.Label(label = "Valore Z: ")
        self.zVal.set_xalign(0)
        self.zVal.set_margin_bottom(5)
        boxRisultati.pack_start(self.zVal, False, False, 0)
        self.pValue = Gtk.Label(label = "P-value: ")
        self.pValue.set_xalign(0)
        boxRisultati.pack_start(self.pValue, False, False, 0)

        self.checkSommaSemplice = Gtk.CheckButton.new_with_label("Somma semplice degli errori")
        self.checkSommaSemplice.set_margin_bottom(10)
        boxMain.pack_start(self.checkSommaSemplice, False, False,0)

        bottoneEsegui = Gtk.Button.new_with_label("Calcola")
        bottoneEsegui.connect("clicked", self.on_bottoneEsegui_clicked)
        boxMain.pack_start(bottoneEsegui, False, False, 0)

        self.show_all()
        Gtk.main()

    def on_bottoneEsegui_clicked(self, widget):
        x_value = float(self.valoreAtteso.get_text())
        x_error = float(self.erroreAtteso.get_text())
        y_value = float(self.valoreOttenuto.get_text())
        y_error = float(self.erroreOttenuto.get_text())

        if self.checkSommaSemplice.get_active():
            tot_error = x_error+y_error
        else:
            tot_error = math.sqrt(x_error**2 + y_error**2)
        
        try:
            Z = (y_value-x_value)/tot_error
            self.zVal.set_text(f"Valore Z: {Z:.6f}")
            pVal = norm.cdf(-abs(Z))*2
            self.pValue.set_text(f"P-value: {pVal:.6f}")
        except ZeroDivisionError:
            self.zeroDivisionErrorDialog()

    # FINITO
    def zeroDivisionErrorDialog(self):
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK, text="Divisione per zero")
        dialog.format_secondary_text("""Entrambi gli errori sono stati posti uguali a 0.
Questo non è possibile né è sensato.""")
        dialog.run()

        dialog.destroy()

# FINITO
class EntryOnlyNumbers(Gtk.Entry):
    def __init__(self, segni):
        super().__init__()
        self.segni = segni

    def do_insert_text(self, new_text, length, position):
        inserente = new_text.replace(",",".")
        nuovoTest = str(self.get_text())[:position]+str(inserente)+str(self.get_text())[position:]
        try:
            test = float(nuovoTest)
            if test<0 and not self.segni:
                return position
            self.get_buffer().insert_text(position, inserente, length)
            return position + length
        except ValueError:
            return position


if __name__ == "__main__":
    finestra = Finestra()