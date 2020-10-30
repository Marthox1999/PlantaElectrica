import tkinter as tk
import minizinc

window = tk.Tk()
window.title("Planta de energia de Robinson")
window.geometry("1200x650")
window.resizable(0, 0)

# Handlers


def handlesecondclick():
    model = minizinc.Model()
    print("ESTOY AQUI")
    print("var_cN, var_cH, var_cT, var_cpN, var_cpH, var_cpT, var_rcH, var_drA")
    print(var_cN, var_cH, var_cT, var_cpN,
          var_cpH, var_cpT, var_rcH, var_drA)

    retrievedData = [[0 for _ in range(int(var_days))]
                     for _ in range(int(var_clients))]
    for i in range(int(var_clients)):
        for j in range(int(var_days)):
            retrievedData[i][j] = int(data[i][j].get())

    print(retrievedData)
    model.add_string("""
        float: cN;
        float: cH;
        float: cT;
        int: cpN;
        int: cpH;
        int: cpT;
        int: n;
        int: s;
        array[int, int] of int : D;
        float: rcH;
        int: drA;
        array[1..n] of var int: pN;
        array[1..n] of var int: pH;
        array[1..n] of var int: pT;
        var int: aux = n - drA + 1;
        var float: f;
        constraint forall(i in 1..n)(sum(j in 1..s)(D[j,i]) <= cpN+cpH+cpT);
        constraint forall(i in 1..n)(sum(j in 1..s)(D[j,i]) <= pN[i]+pH[i]+pT[i]);
        constraint forall(i in 1..aux)(sum(k in i..i+drA-1)(pH[k] > cpH*rcH) < drA);
        constraint forall(i in 1..n)(pN[i] <= cpN);
        constraint forall(i in 1..n)(pH[i] <= cpH);
        constraint forall(i in 1..n)(pT[i] <= cpT);
        constraint forall(i in 1..n)(pN[i] >= 0);
        constraint forall(i in 1..n)(pH[i] >= 0);
        constraint forall(i in 1..n)(pT[i] >= 0);
        constraint f = sum(i in 1..n)(pN[i]*cN + pH[i]*cH + pT[i]*cT );
        solve minimize f;
    """)
    coin = minizinc.Solver.lookup("coinbc")
    inst = minizinc.Instance(coin, model)
    inst["cN"] = var_cN
    inst["cH"] = var_cH
    inst["cT"] = var_cT
    inst["cpN"] = var_cpN
    inst["cpH"] = var_cpH
    inst["cpT"] = var_cpT
    inst["n"] = int(var_days)
    inst["s"] = int(var_clients)
    inst["D"] = retrievedData
    inst["rcH"] = var_rcH
    inst["drA"] = var_drA
    result = inst.solve()
    print(result["pN"])
    print(result["pH"])
    print(result["pT"])
    text = "Produccion Nuclear (pN) = " + str(result["pN"]) + "\n Produccion Hidroelectrica (pH) = " + \
        str(result["pH"]) + "\n Produccion Termica (pT) = " + str(result["pT"])
    tk.Label(
        text="Resultados").grid(row=6+int(var_days)+3, column=0, columnspan=5, sticky="n", pady="20")
    tk.Label(
        text=text
    ).grid(row=6+int(var_days)+4, column=0, columnspan=5, sticky="n")


def handleclick():
    try:
        global var_cN, var_cH, var_cT, var_cpN, var_cpH, var_cpT, var_rcH, var_drA
        var_cN = int(cN.get())
        var_cH = int(cH.get())
        var_cT = int(cT.get())

        var_cpN = int(cpN.get())
        var_cpH = int(cpH.get())
        var_cpT = int(cpT.get())

        var_rcH = float(rcH.get())
        var_drA = int(drA.get())
    except:
        tk.Message(
            text="por favor ingrese valores numericos en todos los campos antes de continuar",
            master=window,
            width=500,
            background="yellow").grid(row=0, column=0, columnspan=5, sticky="n")
        return

    frame1 = tk.Canvas(window, bg="gray", height=350, width=1100)
    frame1.grid(sticky=("n", "W"), column=0, columnspan=6,
                pady=(5, 0), scrollregion=frame1.bbox('all'))
    frame1.grid_propagate(0)

    frame = tk.Frame(frame1)
    frame1.create_window((0, 0), window=frame, anchor='nw')

    global var_days
    var_days = days.get()
    global var_clients
    var_clients = clientes.get()

    if len(var_clients) == 0 or len(var_days) == 0:
        tk.Message(
            text="por favor llene todos los campos antes de continuar",
            master=window,
            width=500,
            background="yellow").grid(row=0, column=0, columnspan=5, sticky="n")
    else:
        global data
        data = [[0 for _ in range(int(var_days))]
                for _ in range(int(var_clients))]
        tk.Message(
            text="----------------------------------------------------------------------------------------------------",
            master=window,
            width=500,).grid(row=0, column=0, columnspan=5, sticky="n")
        for i in range(int(var_clients)):
            tk.Label(frame, text="cliente" + str(i+1)).grid(
                row=1+i, column=0, sticky="n", pady=10, padx=10)
            for j in range(int(var_days)):
                tk.Label(frame, text="dia" + str(j+1)).grid(
                    row=0, column=1+j, sticky="n", pady=10, padx=10)
                daily_consumption = tk.Entry(frame)
                daily_consumption.grid(
                    row=1+i, column=1+j, sticky="n", pady=10, padx=10)
                data[i][j] = daily_consumption

        ys = tk.Scrollbar(orient="vertical")
        ys.grid(row=0, rowspan=10, column=7, sticky='ns')

        xs = tk.Scrollbar(orient="horizontal")
        xs.grid(row=10, column=0, columnspan=10, sticky='we')

        tk.Button(
            text="Submit",
            command=handlesecondclick
        ).grid(row=6+int(var_days)+1, column=0, columnspan=5, sticky="n")

        frame1.configure(yscrollcommand=ys.set)
        frame1.configure(xscrollcommand=xs.set)

        ys.config(command=frame1.yview)
        xs.config(command=frame1.xview)


# Costos


tk.Message(
    text="----Recomendamos no pasar de 5 dias 8 clientes----",
    master=window,
    width=500).grid(row=0, column=0, columnspan=5, sticky="n")

cNlabel = tk.Label(
    text="costo nuclear"
)

cN = tk.Entry()

cHlabel = tk.Label(
    text="costo hidroelectrica"
)
cH = tk.Entry()

cTlabel = tk.Label(
    text="costo termica"
)
cT = tk.Entry()

# Capacidades

cpNlabel = tk.Label(
    text="Capacidad de produccion nuclear"
)
cpN = tk.Entry()

cpHlabel = tk.Label(
    text="Capacidad de produccion hidroelectrica"
)
cpH = tk.Entry()

cpTlabel = tk.Label(
    text="Capacidad de produccion termica"
)
cpT = tk.Entry()

# Dias, Clientes y rch

rcHlabel = tk.Label(
    text="Regimen {0,1}"
)
rcH = tk.Entry()

drAlabel = tk.Label(
    text="Dias Regimen"
)
drA = tk.Entry()

dayslabel = tk.Label(
    text="Dias"
)
days = tk.Entry()

clienteslabel = tk.Label(
    text="Clientes"
)
clientes = tk.Entry()

# Interactions

firstButton = tk.Button(
    text="Submit",
    command=handleclick
)

secondButton = tk.Button(
    text="Submit",
    command=handlesecondclick
)

# PACKING COMPONENTS
cNlabel.grid(row=1, column=0, sticky="w", pady=10, padx=10)
cN.grid(row=1, column=1, sticky="w", pady=10, padx=10)
cHlabel.grid(row=2, column=0, sticky="w", pady=10, padx=10)
cH.grid(row=2, column=1, sticky="w", pady=10, padx=10)
cTlabel.grid(row=3, column=0, sticky="w", pady=10, padx=10)
cT.grid(row=3, column=1, sticky="w", pady=10, padx=10)

cpNlabel.grid(row=1, column=2, sticky="w", pady=10, padx=10)
cpN.grid(row=1, column=3, sticky="w", pady=10, padx=10)
cpHlabel.grid(row=2, column=2, sticky="w", pady=10, padx=10)
cpH.grid(row=2, column=3, sticky="w", pady=10, padx=10)
cpTlabel.grid(row=3, column=2, sticky="w", pady=10, padx=10)
cpT.grid(row=3, column=3, sticky="w", pady=10, padx=10)

tk.Label(
    text="Los valores del regimen deben estar entre 0 y 1"
).grid(row=0, column=4, columnspan=5, sticky="w", pady=10, padx=10)
rcHlabel.grid(row=1, column=4, sticky="w", pady=10, padx=10)
rcH.grid(row=1, column=5, sticky="w", pady=10, padx=10)
drAlabel.grid(row=2, column=4, sticky="w", pady=10, padx=10)
drA.grid(row=2, column=5, sticky="w", pady=10, padx=10)
dayslabel.grid(row=3, column=4, sticky="w", pady=10, padx=10)
days.grid(row=3, column=5, sticky="w", pady=10, padx=10)
clienteslabel.grid(row=4, column=4, sticky="w", pady=10, padx=10)
clientes.grid(row=4, column=5, sticky="w", pady=10, padx=10)

firstButton.grid(row=4, column=0, columnspan=5, sticky="n")

window.mainloop()
