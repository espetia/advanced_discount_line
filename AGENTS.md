# AGENTS.md - Guía para Agentes de IA

Este documento sirve como guía de contexto para cualquier agente de Inteligencia Artificial que interactúe con este repositorio. El proyecto actual es un módulo básico para **Odoo 15**.

## Objetivo del Proyecto

Desarrollar, mantener y gestionar un módulo para Odoo 15. Según el directorio actual, el módulo parece llamarse `advanced_discount_line`. El código sugerido o modificado por la IA deberá apegarse estrictamente a las convenciones de este framework y versión.

## Estructura Estándar del Módulo (Odoo 15)

Al analizar, crear o modificar archivos en este proyecto, el agente debe respetar e interactuar con la siguiente estructura de directorios:

*   `__init__.py`: (Obligatorio) Inicializa el módulo de Python y carga los subdirectorios con código fuente (ej., `models`, `controllers`).
*   `__manifest__.py`: (Obligatorio) Archivo de configuración del módulo (nombre, versión, categoría, autor, dependencias a otros módulos, listas de archivos XML/CSV a cargar, etc.).
*   `models/`: Contiene los archivos Python con la lógica de negocio y definición de modelos de base de datos (heredando de `models.Model` o `models.AbstractModel`).
*   `views/`: Contiene los archivos XML que definen la interfaz de usuario en el backend (vistas de formulario, árbol/lista, kanban, menús de navegación y acciones de ventana).
*   `security/`: 
    *   `ir.model.access.csv`: Definición de permisos CRUD (Create, Read, Update, Delete) para los grupos de usuarios sobre los modelos.
    *   `*.xml`: Reglas de acceso a nivel de registro (Row-Level Security) y definición de nuevos grupos de usuarios.
*   `data/`: Archivos XML o CSV utilizados para cargar registros estáticos iniciales, valores por defecto, o automatizaciones (Cron jobs).
*   `demo/`: Archivos con datos de demostración para entornos de pruebas.
*   `controllers/`: Lógica para endpoints HTTP y rutas del portal web/frontend de Odoo (`http.Controller`).
*   `static/`: Recursos estáticos servidos al navegador. 
    *   `src/js/`, `src/css/`, `src/scss/`: Código del lado del cliente.
    *   `src/xml/`: Plantillas QWeb usadas por el framework de JavaScript (OWL en Odoo 15).
    *   `description/icon.png`: Icono representativo del módulo.
*   `wizard/`: Controladores para modelos transitorios (`models.TransientModel`) que se usan generalmente en ventanas modales (pop-ups) para recolectar información de los usuarios antes de ejecutar una acción masiva.
*   `reports/`: Vistas de reportes impresos o en PDF usando plantillas QWeb, y sus acciones asociadas.
*   `i18n/`: Archivos de internacionalización y traducción (`.pot`, `.po`).

## Reglas Críticas y Convenciones para el Agente

1.  **Versión Core:** Todo el código sugerido (Python, XML, vistas web OWL, etc.) debe ser **100% compatible con Odoo 15**. Las APIs de versiones anteriores (ej. de Odoo 12) o posteriores (ej. Odoo 16+) no deben ser usadas a menos que tengan compatibilidad cruzada certificada.
2.  **Registro de Archivos (XML/CSV):**
    *   Al crear nuevos archivos en `views/`, `security/`, `data/`, `reports/`, etc., es un requerimiento imperativo agregarlos a la lista `"data": [...]` o `"security": [...]` dentro del archivo `__manifest__.py`. Poner especial atención al orden (la seguridad suele ir primero).
3.  **Archivos Python:**
    *   Todo archivo Python recién creado (`.py`) debe ser importado en su respectivo `__init__.py` de la carpeta local. Y esa carpeta debe ser importada por el `__init__.py` de la raíz del módulo.
    *   Utilizar la API estándar: `from odoo import models, fields, api, _, exceptions`.
4.  **Seguridad por Defecto:** 
    *   Cada nuevo modelo en base de datos **requiere obligatoriamente** la asignación de permisos iniciales en `security/ir.model.access.csv`. Si se olvida, el módulo lanzará un warning y no podrá ser operado en la interfaz gráfica.
5.  **Buenas Prácticas Odoo:**
    *   Usar herencias de clase o vistas (XPath) en lugar de sobrescribir el código nativo directamente.
    *   Aprovechar los campos computados (`compute`) y las dependencias (`@api.depends`) adecuadamente.

## Flujo de Acción Sugerido

Si ocurre una petición de la persona usuaria para agregar o modificar funciones:
1. Revisa o solicita ver `__manifest__.py` para comprender el contexto actual.
2. Empieza definiendo o analizando el esquema de base de datos en `models/`.
3. Crea las reglas y permisos en `security/`.
4. Estructura visualmente los datos en `views/`.
5. Si hubiesen acciones adicionales interactivas, incorpóralas en `wizard/`, `controllers/`, o modifica las vistas con assets en `static/`.
