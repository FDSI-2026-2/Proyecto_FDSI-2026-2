# Trabajo Pendiente

## Alta Prioridad

- Configurar proteccion de rama para exigir los jobs de CI antes de fusionar.
- Configurar `SONAR_TOKEN`, `SONAR_PROJECT_KEY` y `SONAR_ORGANIZATION`, o retirar el workflow condicional si SonarQube Cloud no se usara.
- Regenerar y revisar resultados experimentales antes de publicar metricas, indicando commit, configuracion, semilla, proveedor y fecha.
- Revocar cualquier token expuesto fuera de GitHub Secrets y reemplazarlo por un secreto del repositorio.

## Arquitectura y Seguridad

- Anadir pruebas de integracion opcionales contra Gemini y Ollama, separadas de la suite sin red.
- Definir timeouts, reintentos y clasificacion de errores para los proveedores LLM en el adaptador de infraestructura.
- Disenar el protocolo de solicitud y recepcion de corroboracion para mensajes retenidos en `CORROBORATE`.
- Anclar el log de auditoria a almacenamiento externo inmutable si se usa fuera del prototipo.
- Implementar el adaptador AutoGen solo si se incorpora ese runtime; el nucleo ya se integra a traves de `MessageBus` y `TextGenerator`.

## Reproducibilidad y Operacion

- Regenerar el archivo `.lock` con hashes correspondiente cuando se modifique un manifiesto de dependencias y revisar el diff de versiones resueltas.
- Publicar artefactos de experimentos validados en una version o repositorio de datos con su manifiesto de ejecucion.
- Anadir observabilidad externa (OpenTelemetry o Langfuse) si se requiere trazabilidad operativa mas alla del log local.
- DVC no esta soportado. Si se requiere versionado de datos o artefactos, seleccionar y documentar una herramienta con un flujo mantenido y probado.
