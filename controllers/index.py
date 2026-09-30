import web

render = web.template.render('views/')

# Estructuras de datos (FIFO)
fila_prioritaria = []
fila_normal = []

# Variables globales para control y estadísticas
contador_ticket = 1
tickets_atendidos = 0

class Index:
    def GET(self):
        # 3. Consultar siguiente ticket (se atiende primero la fila prioritaria)
        if len(fila_prioritaria) > 0:
            siguiente = fila_prioritaria[0]
        elif len(fila_normal) > 0:
            siguiente = fila_normal[0]
        else:
            siguiente = None

        # 5. Tres (o más) estadísticas
        total_espera = len(fila_prioritaria) + len(fila_normal)
        tiempo_total_estimado = sum(t['tiempo'] for t in fila_prioritaria + fila_normal)
        
        estadisticas = {
            'total_espera': total_espera,
            'tiempo_estimado': tiempo_total_estimado,
            'total_atendidos': tickets_atendidos,
            'cant_prioritarios': len(fila_prioritaria),
            'cant_normales': len(fila_normal)
        }

        return render.index(fila_prioritaria, fila_normal, siguiente, estadisticas)

    def POST(self):
        global contador_ticket, tickets_atendidos
        datos = web.input(accion=None, nombre='', problema='', prioridad='normal', tiempo='5')

        # 1. Registrar ticket
        if datos.accion == 'registrar':
            if datos.nombre.strip() and datos.problema.strip():
                try:
                    tiempo_val = int(datos.tiempo)
                except ValueError:
                    tiempo_val = 5

                nuevo_ticket = {
                    'numero': f"TK-{contador_ticket:03d}",
                    'nombre': datos.nombre.strip(),
                    'problema': datos.problema.strip(),
                    'prioridad': datos.prioridad,
                    'tiempo': tiempo_val
                }
                contador_ticket += 1

                # Clasificación según prioridad (FIFO: se agrega al final)
                if datos.prioridad == 'prioritaria':
                    fila_prioritaria.append(nuevo_ticket)
                else:
                    fila_normal.append(nuevo_ticket)

        # 2. Atender siguiente ticket (FIFO: pop(0) de prioritaria primero)
        elif datos.accion == 'atender':
            if len(fila_prioritaria) > 0:
                fila_prioritaria.pop(0)
                tickets_atendidos += 1
            elif len(fila_normal) > 0:
                fila_normal.pop(0)
                tickets_atendidos += 1

        # Redirección manual solicitada
        web.ctx.status = '303 See Other'
        web.header('Location', '/')
        return ''