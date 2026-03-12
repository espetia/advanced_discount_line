# Advanced Discount Line

Este es un módulo desarrollado para Odoo 15 enfocado en agregar una capa avanzada de configuración y restricciones de permisos al porcentaje de los descuentos aplicados en las líneas de las órdenes de venta.

## Características Principales

*   **Configuración por Reglas:** Permite predefinir qué porcentajes exactos de descuento están permitidos dentro del sistema. Si el descuento a dar en la orden de venta no está configurado de antemano, el sistema bloqueará su guardado.
*   **Fechas de Vigencia:** Restringe una promoción para que sólo sea aplicable dentro de un rango de fechas. 
*   **Permitir por Producto o Tallas:** Asocia un descuento exclusivamente a los productos base (`product.template`) designados por el negocio.
*   **Autorizaciones de Usuarios:** Sólo el personal estipulado puede aplicar este porcentaje de descuento, ideal para separar autorizaciones gerenciales de vendedores rasos.
*   **Monto Mínimo Relacionado:** Exige un subtotal mínimo en la línea de venta (Cantidad x Precio Unitario) para que el descuento proceda.

## Uso del Módulo

1.  **Activación de los Permisos:** 
    El usuario encargado de generar las reglas (Ejemplo, Gerente de Ventas o Administrador) debe ser agregado al nuevo grupo de seguridad implementado: **[Ventas / Gestor de Descuentos Avanzados]**. Sin este permiso, no verá el menú de configuraciones.

2.  **Configuración:**
    Navegue a: **Ventas > Configuración > Reglas de Descuentos**.
    Allí cree un nuevo registro indicando el Porcentaje (Obligatorio), y rellenando los demás campos condicionales a su conveniencia. (Dejar un campo condicional vacío, significa que "aplica para todo", por ejemplo, dejar "Usuarios" vacío, indica que cualquier usuario puede usar esa regla del 10%).

3.  **Venta Diaria:**
    Los vendedores proceden a crear sus Órdenes de Venta normalmente. Cuando ellos modifiquen el campo numérico del **Descuento**, Odoo evaluará la orden en el fondo contra las reglas preconfiguradas. Si se comete una infracción de uso (ejemplo, fecha expirada o producto no promocionado), una Alerta Roja (ValidationError) le explicará el motivo exacto al usuario, evitando que se pueda confirmar o procesar la orden con descuentos fuera de norma.

## Detalles Técnicos y Desarrollo
*   **Responsabilidad Única (SRP):** Las validaciones de modelo recaen en el decorador API `@api.constrains('discount', 'product_id', 'product_uom_qty', 'price_unit')` en `sale.order.line`. Eso provee integridad en base de datos ya sea que el registro venga por la UI web, importación CSV, XML-RPC o procesos automáticos tipo Cron.
*   **Internacionalización (i18n):** El código base está desarrollado en Inglés y cuenta con traducciones automatizadas desde el archivo `/i18n/es_MX.po` para terminales enfocadas al mercado Hispano.
