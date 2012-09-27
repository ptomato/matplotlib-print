import matplotlib
import matplotlib.backends.backend_tkagg
import Tkinter as tk
import win32print
from print_toolbar_common import PrintToolbar

_OldToolbarClass = matplotlib.backends.backend_tkagg.NavigationToolbar2TkAgg


class _Dialog(tk.Toplevel):
    """Dialog class from Tkinter book:
    http://effbot.org/tkinterbook/tkinter-dialog-windows.htm"""
    def __init__(self, parent, title=None):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.result = None
        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
        self.initial_focus.focus_set()

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        return 1  # override

    def apply(self):
        pass  # override


class PrintSetupDialogTk(_Dialog):
    """
    Print setup dialog for Tk backend
    """
    def __init__(self, parent, auto, fit, dpi, printer):
        self.success = False
        self.auto = tk.BooleanVar()
        self.auto.set(auto)
        self.fit = tk.BooleanVar()
        self.fit.set(fit)
        self.dpi = tk.StringVar()
        self.dpi.set(str(dpi))
        self.printer = tk.StringVar()
        self.printer.set(printer)
        _Dialog.__init__(self, parent, title='Print Setup')

    def body(self, master):
        # Enumerates local and network printers according to MSDN docs
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS,
            None, 1)
        printer_names = [name for (flags, desc, name, comment) in printers]

        # Create GUI
        tk.Label(master, text='Print to:').grid(row=0, column=0, sticky=tk.E)
        tk.OptionMenu(master, self.printer, *printer_names).grid(row=0,
            column=1, sticky=tk.W)
        tk.Label(master, text='DPI:').grid(row=1, column=0, sticky=tk.E)
        tk.Spinbox(master, from_=1, to=600, textvariable=self.dpi).grid(row=1,
            column=1, sticky=tk.W)
        tk.Checkbutton(master, text='Auto portrait or landscape',
            var=self.auto).grid(row=2, columnspan=2, sticky=tk.W)
        tk.Checkbutton(master, text='Fit to printer margins',
            var=self.fit).grid(row=3, columnspan=2, sticky=tk.W)

    def apply(self):
        self.success = True

    def show_modal(self):
        self.wait_window()
        return (self.success, self.auto.get(), self.fit.get(),
            int(self.dpi.get()), self.printer.get())


class NavigationToolbar2TkAgg(_OldToolbarClass, PrintToolbar):

    def __init__(self, *args, **kw):
        _OldToolbarClass.__init__(self, *args, **kw)
        PrintToolbar.__init__(self, *args, **kw)

        # Add print setup button
        b = tk.Button(master=self, text='Page Setup', padx=2, pady=2,
            image=None, command=self._on_page_setup)
        b.pack(side=tk.LEFT)

        # Add print button
        b = tk.Button(master=self, text='Print', padx=2, pady=2, image=None,
            command=self._on_print)
        b.pack(side=tk.LEFT)

    def _on_page_setup(self):
        """Page setup dialog"""
        dialog = PrintSetupDialogTk(self.window,
            self._auto_orientation, self._fit_to_margin, self._dpi,
            self._printer_name)
        code, auto, fit, dpi, prn = dialog.show_modal()
        if code:
            (self._auto_orientation, self._fit_to_margin,
                self._dpi, self._printer_name) = auto, fit, dpi, prn

    def _on_print(self):
        self.print_figure()

matplotlib.backends.backend_tkagg.NavigationToolbar2TkAgg = NavigationToolbar2TkAgg
