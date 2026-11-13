---
description: Cierra la task del ramo con unas pocas preguntas al alumno
---

Vas a cerrar esta task del ramo. Las métricas (tokens, modelo, tiempo, ediciones, pruebas, límites de uso) se calculan solas desde `reportes/sesiones/`, así que solo necesitas lo que únicamente el alumno sabe. Sé breve y amable.

## Paso 1 – Deduce sin preguntar
- Número de task y usuario: del nombre del repositorio (`git remote get-url origin`, formato `taskN-usuario`).

## Paso 2 – Pregunta en UN solo mensaje, numerado, y espera la respuesta
0. ¿La task quedó completa? (Completa / Parcial / No terminada)
1. ¿Usaste también el chat de Claude (claude.ai) como apoyo en esta task? (Sí/No y para qué)
2. ¿Cuántos reportes o entregables generaste?
3. ¿Quién definió el diseño o la solución: tú, la IA o ambos?
4. ¿Qué partes hiciste sin IA? (puede ser "ninguna")
5. ¿En qué nivel de autonomía crees que trabajaste? (muestra la tabla de abajo)
6. ¿Qué tan difícil fue la task, del 1 al 5? (muestra la escala de abajo)

| Nivel | Autonomía | Desarrollador | IA |
|---|---|---|---|
| L0 | Sin IA | Hace todo | No interviene |
| L1 | Asesoramiento | Planifica, programa, decide y ejecuta | Explica, responde y sugiere |
| L2 | Asistencia / Copilot | Controla el flujo y la implementación | Genera artefactos específicos y delimitados |
| L3 | Ejecución delegada | Define la tarea o el diseño y revisa | Implementa componentes sustanciales |
| L4 | Ejecución agéntica | Define objetivo y restricciones, supervisa | Planifica, edita archivos, ejecuta pruebas, depura e itera |
| L5 | Flujo liderado por IA | Establece objetivos y límites, gestiona excepciones | Descompone, coordina y ejecuta casi todo el flujo |

Dificultad: 1 = trivial (menos de 1 h) · 2 = baja · 3 = media (varios componentes, algo de depuración) · 4 = alta (integraciones, varias iteraciones) · 5 = muy alta (diseño complejo, mucha depuración).

## Paso 3 – Clasifica tú, de forma independiente
Revisa `reportes/sesiones/*.jsonl` (mensajes del alumno, archivos editados por ti, comandos y pruebas que ejecutaste) y asigna tu propio nivel, sin dejarte influir por el del alumno:
- L4 exige que la IA haya editado archivos Y ejecutado pruebas.
- L5 exige además pocas intervenciones humanas en relación con las acciones de la IA y que la IA haya descompuesto la tarea sin que el alumno le dictara los pasos.
- Si la IA solo respondió o generó fragmentos que el alumno copió: L1 o L2.
Si dudas entre dos niveles, elige el más bajo.

## Paso 4 – Guarda y confirma
1. Crea o sobrescribe `reportes/cierre.csv` con esta cabecera y una fila:
   `usuario;task;estado_task;fecha_cierre;uso_chat;n_reportes;diseno_por;partes_sin_ia;nivel_alumno;nivel_claude;dificultad;evidencia`
   (`estado_task`: Completa, Parcial o No terminada · `fecha_cierre`: fecha y hora actual en formato ISO, obtenla con `date -Iseconds` · `evidencia`: máximo 25 palabras, sin punto y coma, que justifique tu nivel).
   Si ya existía un cierre anterior, sobrescríbelo: vale el último.
2. Haz commit de `reportes/` con el mensaje "Cierre de task" y push.
3. Dile al alumno en una línea que la task quedó cerrada. Si respondió "Parcial" o "No terminada", recuérdale que puede seguir trabajando y volver a escribir "cerrar task" cuando la complete. No le muestres tu clasificación.
