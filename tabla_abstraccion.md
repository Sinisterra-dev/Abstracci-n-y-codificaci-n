# Tabla de Abstracción – Fase 2

## Nombre del Estudiante
Hernando Arbey Robles Puentes

## Planteamiento del Problema
La empresa **Constructora Mejor** requiere una aplicación para gestionar los datos básicos del pago de nómina de sus empleados, que permita calcular el valor a pagar según el cargo desempeñado y los días laborados. La aplicación debe contar con una interfaz gráfica amigable que permita guardar, calcular y mostrar un reporte del valor a pagar.

---

## Tabla 1 – Elementos para la Abstracción

| Nombre de la Clase y Ámbito de Visibilidad | Nombre de las Propiedades / Atributos (con tipo de dato) | Nombre del Método | Fórmula Matemática |
|---|---|---|---|
| `public GestionEmpleados` | `str – identificacion` | `calcular_pago()` → `float` | `total = valor_dia[cargo] × dias_laborados` |
| | `str – nombre` | Retorna el costo total de nómina a pagar al empleado según su cargo y días laborados. | |
| | `str – genero` | | |
| | `str – cargo` | | |
| | `int – dias_laborados` | | |
| | `str – fecha_registro` | | |
| | `dict – VALOR_DIA` (constante de clase) | | |

### Tabla de valores por cargo

| Cargo | Valor Día |
|---|---|
| Servicios Generales | $ 40.000 |
| Administrativo | $ 50.000 |
| Electricista | $ 60.000 |
| Mecánico | $ 80.000 |
| Soldador | $ 90.000 |

---

## Requerimientos Funcionales Identificados

1. **Login**: Ventana inicial con nombre del autor, nombre de la aplicación y campo de contraseña enmascarada (`show="*"`). Contraseña genérica: `4682`.
2. **Registro de Empleado**: Formulario con campos: Identificación, Nombre completo, Género (radio button), Cargo laboral (lista desplegable), Días laborados, Fecha de registro (automática), Valor día de trabajo (deshabilitado, calculado automáticamente).
3. **Guardar Registro**: Botón que instancia la clase `GestionEmpleados` con los datos ingresados.
4. **Calcular Nómina / Mostrar Reporte**: Botón que llama al método `calcular_pago()` y abre la ventana de reporte.
5. **Salir**: Botón con confirmación de salida.
6. **Reporte**: Ventana que muestra todos los datos del empleado y el valor total a pagar.

---

*Nota: Esta tabla documenta la abstracción previa a la codificación conforme al Anexo 2 del curso.*
