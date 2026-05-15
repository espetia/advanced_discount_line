# Advanced Discount Line

Este es un módulo desarrollado para Odoo 15 enfocado en agregar una capa avanzada de configuración, restricciones de permisos, cadenas de aprobación y gestión de listas de precios para las órdenes de venta y sus líneas.

## Características Principales

*   **Configuración por Reglas de Descuento:** Permite predefinir qué porcentajes exactos de descuento están permitidos dentro del sistema, validando fechas de vigencia, productos permitidos, clientes, usuarios y montos mínimos.
*   **Reglas de Incremento en Líneas:** Además de descuentos, el módulo permite agregar porcentajes de incremento en las líneas de venta (`increment`), sujetos a configuraciones de restricción similares a los descuentos (fechas, productos, usuarios, clientes, monto mínimo).
*   **Cadena de Aprobación de Descuentos:** Si un usuario no tiene permiso directo en la configuración de la regla para aplicar un descuento, la orden requerirá aprobación. Pasará por un flujo (`pending_approval` -> `approved`) basado en escalones configurados según el porcentaje de descuento máximo de la orden y notificará a los aprobadores por correo electrónico.
*   **Control de Listas de Precios por Cliente:** Restringe qué listas de precios puede usar un cliente en específico. También se pueden marcar listas de precios como "Genéricas" (`is_generic`) para que estén disponibles para cualquier cliente sin restricciones específicas.
*   **Control de Edición de Precios Unitarios:** Controla la modificación del precio unitario en las líneas de venta. Sólo los usuarios con el permiso específico o los productos marcados explícitamente con "Siempre editar precio unitario" (`always_edit_price_unit`) permiten la modificación manual del precio.

## Uso del Módulo

1.  **Configuraciones Base:**
    *   **Reglas de Descuento / Incremento:** Vaya a las configuraciones respectivas en el menú de Ventas. Cree registros indicando el porcentaje y llenando los campos condicionales a su conveniencia.
    *   **Cadenas de Aprobación:** Configure los escalones de aprobación indicando el rango de porcentaje de descuento y el usuario aprobador correspondiente.
    *   **Listas de Precios:** Marque listas de precios como genéricas en su configuración, o asigne listas específicas directamente en la pestaña de ventas de cada cliente.
    *   **Productos:** En la ficha del producto, bajo la pestaña de ventas, puede habilitar la opción para permitir siempre la edición de su precio unitario.

2.  **Operación de Ventas Diaria:**
    *   Al crear una orden y seleccionar un cliente, el sistema filtrará y solo permitirá elegir las listas de precios autorizadas (o las genéricas).
    *   Al agregar líneas e indicar un **Descuento** o **Incremento**, se evaluarán las reglas preconfiguradas. Si se comete una infracción de uso (ejemplo, fecha expirada o producto no promocionado), una Alerta Roja (ValidationError) explicará el motivo exacto, evitando guardar la línea.
    *   Si las reglas de descuento se cumplen pero el usuario no está entre los permitidos directamente, la orden requerirá aprobación para poder confirmarse.
    *   El usuario solicitará la aprobación; la orden cambiará a estado "Pendiente de Aprobación" y se enviará un correo automático al aprobador correspondiente. Una vez aprobada, podrá ser confirmada y procesada.

## Detalles Técnicos y Desarrollo
*   **Responsabilidad Única (SRP):** Las validaciones de modelo recaen en decoradores API `@api.constrains` en `sale.order.line` y `sale.order`. Eso provee integridad en base de datos ya sea que el registro venga por la UI web, importación CSV, XML-RPC o procesos automáticos.
*   **Internacionalización (i18n):** El código base está desarrollado en Inglés y cuenta con traducciones automatizadas desde el archivo `/i18n/es_MX.po` para terminales enfocadas al mercado Hispano.
