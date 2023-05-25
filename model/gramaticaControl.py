from tkinter import END

class Gramatica:
    def __init__(self):
        self.gramaticaPunto = []
        self.gramaticaLeida = []
        self.terminalesMasNoTerminales = []
        self.terminales = []
        self.noTerminales = []
        self.estados = []
        self.transiciones = []

    # operacion LR(0)
    def lr0(self,I):
        lr0 = I
        for it in I:
            if it not in lr0:
                lr0.append(it)
            x, y = it.split(".")
            if y == "":  # . Seguido por terminal, sin operación, salta al siguiente ciclo
                continue
            v = y[0]
            if v in self.noTerminales:  # . Seguido por un no Terminal , Join in B->.γ
                res = self.obtenerGramNoTerminal(v)
                for re in res:
                    if re not in lr0:
                        lr0.append(re)
        return lr0
    
    def obtenerGramNoTerminal(self,v):
        res = []
        for gram in self.gramaticaPunto:
            index = gram.find("->")
            if gram[0] == v and gram[index + 2] == ".":
                res.append(gram)
        return res
    
    def agregarPunto(self):
        # gramática aumentada
        str0 = "S'->." + self.gramaticaLeida[0][0]
        self.gramaticaPunto.append(str0)
        str1 = "S'->" + self.gramaticaLeida[0][0] + "."
        self.gramaticaPunto.append(str1)

        for gram in self.gramaticaLeida:
            for i in range(len(gram) - 2):
                tmp = gram[:3 + i] + "." + gram[3 + i:]
                self.gramaticaPunto.append(tmp)

    def irA(self, I, v):
        temporal = []
        for it in I:
            x, y = it.split(".")
            if y != "":
                if y[0] == v:
                    new_it = x + y[0] + "." + y[1:]
                    temporal.append(new_it)
        if len(temporal) != 0:
            nuevoEstado = self.lr0(temporal)
            return nuevoEstado

    def estaEnEstados(self, nuevoEstado):
        if nuevoEstado is None:
            return -1
        nuevoSet = set(nuevoEstado)
        num = 0
        for item in self.estados:
            viejoSet = set(item)
            if viejoSet == nuevoSet:
                return num
            num = num + 1
        return -1
    
    def dividirTerminalesYNoTerminales(self):
        for s in self.gramaticaLeida:
            x, y = s.split("->")

            if x not in self.noTerminales:
                self.noTerminales.append(x)

            for v in y:
                if v.isupper():
                    if v not in self.noTerminales:
                        self.noTerminales.append(v)
                else:
                    if v not in self.terminales:
                        self.terminales.append(v)
        self.terminales.append("$")
        self.terminalesMasNoTerminales.extend(self.noTerminales)
        self.terminalesMasNoTerminales.extend(self.terminales)

    def myAppend(self, xx, v, xy):
        t = []
        t.append(xx)
        t.append(v)
        t.append(xy)
        self.transiciones.append(t)


    def esLR0(self):
        for item in self.estados:
            shiftNum = 0
            protocolNum = 0
            for it in item:
                x, y = it.split(".")
                if y == "":
                    protocolNum = protocolNum + 1
                elif y[0] in self.terminales:
                    shiftNum = shiftNum + 1
            if protocolNum > 1 or (protocolNum >= 1 and shiftNum >= 1):
                print("\nNO es una gramática LR(0)")

    def obtenerEstados(self):
        estado = []
        estado.append(self.gramaticaPunto[0])
        it = self.lr0(estado)
        num = 0
        self.estados.append(it)
        num = num + 1

        for estado in self.estados:
            for v in self.terminalesMasNoTerminales:
                nuevoEstado = self.irA(estado, v)

                if nuevoEstado is not None:
                    if self.estaEnEstados(nuevoEstado) == -1:
                        self.estados.append(nuevoEstado)
                        x = self.estaEnEstados(estado)
                        y = self.estaEnEstados(nuevoEstado)
                        self.myAppend(x, v, y)
                        num = num + 1
                    else:
                        x = self.estaEnEstados(estado)
                        y = self.estaEnEstados(nuevoEstado)
                        self.myAppend(x, v, y)