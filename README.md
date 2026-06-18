

https://github.com/user-attachments/assets/a4406b3d-ac66-41ab-a749-b24701df9efd

# 🏢 CorpVL — Sistema de Autenticación Empresarial en la Nube

Sistema de login empresarial desplegado en producción sobre AWS EC2, con autenticación segura y asistente virtual con IA integrada. Funciona como punto de entrada al ecosistema VL, enviando datos de cada sesión a VL Analytics para análisis de tráfico en tiempo real.

**Demo en vivo:** http://54.85.49.76

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3 + Flask |
| Base de datos | SQLite + bcrypt |
| Servidor web | Nginx (reverse proxy) |
| Proceso | Gunicorn (2 workers) |
| Sistema | systemd (arranque automático) |
| Infraestructura | AWS EC2 t2.micro (Free Tier) |
| IA integrada | Anthropic Claude API |

---

## Funcionalidades

-  Login seguro con contraseñas encriptadas (bcrypt)
-  Asistente virtual **Leo** con IA conversacional en español (Claude API)
-  Tracking automático de visitas hacia VL Analytics
-  Panel de administración protegido con autenticación
-  Gestión de usuarios — búsqueda por email y eliminación de cuentas
-  Servicio systemd — se recupera solo ante cualquier fallo
-  Gunicorn como servidor WSGI de producción

---

## Arquitectura

---

## Proyectos externos conectados

- [VL Analytics](https://github.com/leonardov243-byte/vl-analytics) — Panel de analíticas que recibe y procesa los datos de cada sesión iniciada en CorpVL

---

## Autor

**Leonardo Vieira** — Desarrollado y desplegado integramente en AWS EC2.
