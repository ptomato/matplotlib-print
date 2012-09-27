import matplotlib.backends.backend_wx
import wx
import win32print
from print_toolbar_common import PrintToolbar

_OldToolbarClass = matplotlib.backends.backend_wx.NavigationToolbar2Wx


class PrintSetupDialogWx(wx.Dialog):
    """
    Print setup dialog for Wx backend
    """
    def __init__(self, parent, auto, fit, dpi, printer, *args, **kw):
        super(PrintSetupDialogWx, self).__init__(parent, *args, **kw)
        self.SetTitle('Print Setup')

        # Enumerates local and network printers according to MSDN docs
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS,
            None, 1)
        printer_names = [name for (flags, desc, name, comment) in printers]

        # Create GUI
        pnl = wx.Panel(self)
        self.auto = wx.CheckBox(pnl, label='Auto portrait or landscape')
        self.auto.SetValue(auto)
        self.fit = wx.CheckBox(pnl, label='Fit to printer margins')
        self.fit.SetValue(fit)
        self.dpi = wx.SpinCtrl(pnl, min=1, max=600, initial=dpi)
        self.printer = wx.ComboBox(pnl, style=wx.CB_READONLY,
            choices=printer_names)
        self.printer.SetStringSelection(printer)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(pnl, label='Print to:'), flag=wx.ALIGN_CENTER)
        hbox2.Add(self.printer)
        vbox2.Add(hbox2, flag=wx.ALL, border=6)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(pnl, label='DPI:'), flag=wx.ALIGN_CENTER)
        hbox1.Add(self.dpi)
        vbox2.Add(hbox1, flag=wx.ALL, border=6)
        vbox2.Add(self.auto, flag=wx.ALL, border=6)
        vbox2.Add(self.fit, flag=wx.ALL, border=6)
        pnl.SetSizer(vbox2)

        bbox = wx.StdDialogButtonSizer()
        ok = wx.Button(self, id=wx.ID_OK)
        cancel = wx.Button(self, id=wx.ID_CANCEL)
        bbox.AddButton(ok)
        bbox.AddButton(cancel)
        bbox.Realize()

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(pnl, proportion=1,
            flag=wx.ALL | wx.EXPAND, border=5)
        vbox1.Add(bbox,
            flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(vbox1)
        vbox1.Fit(self)

    def get_values(self):
        return (self.auto.GetValue(),
            self.fit.GetValue(),
            self.dpi.GetValue(),
            self.printer.GetValue())


class NavigationToolbar2Wx(_OldToolbarClass, PrintToolbar):
    # ID for print event
    ON_PRINT = wx.NewId()
    ON_PAGE_SETUP = wx.NewId()

    def __init__(self, *args, **kw):
        _OldToolbarClass.__init__(self, *args, **kw)
        PrintToolbar.__init__(self, *args, **kw)

        self.AddSeparator()

        # Add print setup button
        self.AddSimpleTool(self.ON_PAGE_SETUP,
            wx.ArtProvider.GetBitmap(wx.ART_HELP_PAGE),
            'Page Setup',
            'Choose printer and layout page')
        wx.EVT_TOOL(self, self.ON_PAGE_SETUP, self._on_page_setup)
        # Add print button
        self.AddSimpleTool(self.ON_PRINT,
            wx.ArtProvider.GetBitmap(wx.ART_PRINT),
            'Print',
            'Print the current graph to the printer')
        wx.EVT_TOOL(self, self.ON_PRINT, self._on_print)

    def _on_page_setup(self, evt):
        """Page setup dialog"""
        dialog = PrintSetupDialogWx(self,
            self._auto_orientation, self._fit_to_margin, self._dpi,
            self._printer_name)
        if dialog.ShowModal() == wx.ID_OK:
            (self._auto_orientation, self._fit_to_margin,
                self._dpi, self._printer_name) = dialog.get_values()
        dialog.Destroy()

    def _on_print(self, evt):
        self.print_figure()

matplotlib.backends.backend_wx.NavigationToolbar2Wx = NavigationToolbar2Wx
