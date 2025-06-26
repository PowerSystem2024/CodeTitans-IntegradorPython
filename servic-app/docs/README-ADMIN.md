# Guía Admin

## Introducción

Esta guía está dirigida a los administradores de la plataforma Servic App, responsables de la gestión y supervisión global del sistema. Aquí encontrarás ejemplos prácticos para testear la API usando Insomnia, así como explicaciones de cada flujo y endpoint relevante para el rol admin.

---

## Índice

- [Panel de Administración](#panel-de-administración)
- [Gestión de Usuarios](#gestión-de-usuarios)
- [Gestión de Prestadores](#gestión-de-prestadores)
- [Gestión de Servicios](#gestión-de-servicios)
- [Errores Comunes](#errores-comunes)
- [Notas Importantes](#notas-importantes)
- [Diagrama de Flujo](#diagrama-de-flujo)

---

## 1. Panel de Administración (Django Admin)

### Acceso al Panel

- URL: `/admin/`
- Credenciales de superusuario

### Gestión de Usuarios

1. Ver listado de usuarios
2. Cambiar roles de usuario
3. Ver historial de cambios de rol
4. Gestionar permisos

### Gestión de Prestadores

1. Verificar perfiles de prestadores
2. Revisar solicitudes de prestadores
3. Gestionar certificaciones

### Gestión de Servicios

1. Aprobar/rechazar servicios
2. Gestionar categorías
3. Ver estadísticas

---

## 2. API de Administración

### Dashboard

```http
GET /api/admin/dashboard/
Authorization: Bearer {token_access}
```

**Respuesta Exitosa (200 OK):**

```json
{
  "total_users": 100,
  "total_providers": 30,
  "pending_provider_requests": 5,
  "unverified_providers": 8,
  "pending_services": 12,
  "active_services": 45
}
```

### Listar Prestadores

```http
GET /api/admin/providers/
Authorization: Bearer {token_access}
```

**Parámetros de Filtrado:**

- `is_verified`: true/false

**Respuesta Exitosa (200 OK):**

```json
[
  {
    "id": 1,
    "identification_type": "dni",
    "identification_number": "12345678",
    "phone_number": "+1234567890",
    "address": "Calle Principal 123",
    "city": "Ciudad",
    "state": "Estado",
    "country": "País",
    "certification_file": "url_archivo",
    "certification_description": "Certificado en plomería",
    "years_of_experience": 5,
    "is_verified": false,
    "created_at": "2024-03-15T10:30:00Z",
    "updated_at": "2024-03-15T10:30:00Z",
    "user_info": {
      "id": 2,
      "email": "plomero@ejemplo.com",
      "full_name": "Carlos Plomero",
      "date_joined": "2024-03-15T10:30:00Z"
    }
  }
]
```

### Verificar Prestador

```http
PUT /api/admin/providers/2/verify/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "is_verified": true,
    "admin_notes": "Documentación verificada correctamente"
}
```

**Respuesta Exitosa (200 OK):**

```json
{
  "message": "Prestador verificado exitosamente",
  "profile": {
    "id": 1,
    "identification_type": "dni",
    "identification_number": "12345678",
    "phone_number": "+1234567890",
    "address": "Calle Principal 123",
    "city": "Ciudad",
    "state": "Estado",
    "country": "País",
    "certification_file": "url_archivo",
    "certification_description": "Certificado en plomería",
    "years_of_experience": 5,
    "is_verified": true,
    "created_at": "2024-03-15T10:30:00Z",
    "updated_at": "2024-03-15T10:30:00Z"
  }
}
```

### Listar Servicios

```http
GET /api/admin/services/
Authorization: Bearer {token_access}
```

**Parámetros de Filtrado:**

- `status`: active/inactive/pending

**Respuesta Exitosa (200 OK):**

```json
[
  {
    "id": 1,
    "title": "Reparación de Plomería",
    "category_name": "Plomería",
    "provider_name": "Carlos Plomero",
    "price": "50.00",
    "price_type": "hourly",
    "location": "Ciudad",
    "primary_image": "url_imagen",
    "status": "pending",
    "created_at": "2024-03-15T10:30:00Z"
  }
]
```

### Aprobar/Rechazar Servicio

```http
PUT /api/admin/services/1/approve/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "status": "active",
    "admin_comment": "Servicio aprobado después de revisar documentación"
}
```

**Respuesta Exitosa (200 OK):**

```json
{
  "message": "Servicio active exitosamente",
  "service": {
    "id": 1,
    "title": "Reparación de Plomería",
    "description": "Servicios de plomería residencial",
    "category": 1,
    "category_name": "Plomería",
    "provider": 2,
    "provider_email": "plomero@ejemplo.com",
    "price": "50.00",
    "price_type": "hourly",
    "price_type_display": "Por Hora",
    "location": "Ciudad",
    "city": "Ciudad",
    "state": "Estado",
    "country": "País",
    "availability_start": "09:00:00",
    "availability_end": "18:00:00",
    "available_days": "Lunes,Martes,Miércoles,Jueves,Viernes",
    "status": "active",
    "status_display": "Activo",
    "images": [
      {
        "id": 1,
        "image": "url_imagen",
        "is_primary": true
      }
    ],
    "created_at": "2024-03-15T10:30:00Z",
    "updated_at": "2024-03-15T10:30:00Z"
  }
}
```

### Cambiar Rol de Usuario

```http
PUT /api/users/2/change-role/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "user_type": "provider",
    "reason": "Usuario aprobado como prestador de servicios"
}
```

**Respuesta Exitosa (200 OK):**

```json
{
  "id": 2,
  "email": "plomero@ejemplo.com",
  "user_type": "provider"
}
```

---

## Errores Comunes

### 401 Unauthorized

```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```

### 403 Forbidden

```json
{
  "detail": "No tiene permiso para realizar esta acción."
}
```

### 404 Not Found

```json
{
  "detail": "No se encontró el recurso solicitado."
}
```

### 400 Bad Request

```json
{
  "detail": "Status debe ser: active, inactive o pending"
}
```

---

## Notas Importantes

1. Solo los superusuarios pueden acceder al panel de administración
2. Los cambios de rol se registran en el historial
3. Las verificaciones de prestadores son permanentes
4. Los servicios pueden ser aprobados o rechazados
5. Se debe proporcionar una razón para los cambios de rol

---

## Diagrama de Flujo

- [Diagrama de administrador (imagen)](./assets/AdminServic.png)
- [Enlace al diagrama del admin (Mermaid)](https://mermaid.live/view#pako:eNptU02PmzAQ_SuWDz3BNkBCKg5Vd_OBKrWnVj2k9OAYB6wFD7JNu9koP2lP_Qn5Yx0bmiVqTzDz3sw8j59PlEMpaEbDMCwUB3WQVVYoQhp2hN5mpGSVFi5ha9GKjCgBYcn0o-cAPPpMoXz5oYFfvGbakq9rhxNy_72gH5XkEgr6g4The_KAmU9QSUU4tEBY2UqF2EB_8JQVUu45F6UgrCEdU6Ih7t9RpbGacXn5_Vq08kVrLPomUK6p98B0SY5EGMvKy4uxkjPj5r8hG2TlmJegGOlNz7SEEdpOoU77YsDPgOZT1Aj9053JXDVsvYZt5JR3uhd79lYLXMUzkqFBru1LYdwprp3HqbHXreUBRZJO6INs_iUOQ3I_JP_vkIkipzaeyuXMigr05YW9Ct74XhvXa8XavWREwzh4XMu4sEEfqXHxoCXzN8FdBXgyVl17rn3PHRZsJ3e6jYb0GMXTKL_B8htsc4NtbjDld3BjHRV9OBFTsw49asWTPQ9pY4-NIDs0WwM6U6DQy4WiAW2Fbpks0fknxyyo93dBM_z1_qaFOiOP9Ra-HBWnmcWVB1RDX9U0O7DGYNR3JS53LfGRsPYvBR27A5iGNDvRJ5pFyeIuiedp_C6JFovZLE0DesR0FGE6SpP5YhnN42gRnQP67DvEd8kyiZezJbIRXabzgIpS4lV8Hp6tf70BrbQ7yihKC1UKvYJeWZql5z9aLDZq)

---

© Servic App
