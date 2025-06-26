# Guía Cliente

## Introducción

Esta guía está dirigida a los usuarios que desean buscar, contratar y calificar servicios dentro de la plataforma Servic App. Aquí encontrarás ejemplos prácticos para testear la API usando Insomnia, así como explicaciones de cada flujo y endpoint relevante para el usuario común.

---

## Índice

- [Registro e Inicio de Sesión](#registro-e-inicio-de-sesión)
- [Gestión de Perfil](#gestión-de-perfil)
- [Exploración de Servicios](#exploración-de-servicios)
- [Contratación de Servicios](#contratación-de-servicios)
- [Calificación de Servicios](#calificación-de-servicios)
- [Errores Comunes](#errores-comunes)
- [Notas Importantes](#notas-importantes)
- [Diagrama de Flujo](#diagrama-de-flujo)

---

## 1. Registro e Inicio de Sesión

### Registro de Cuenta

```http
POST /api/register/
Content-Type: application/json

{
    "email": "usuario@ejemplo.com",
    "password": "contraseña123",
    "password2": "contraseña123",
    "first_name": "Nombre",
    "last_name": "Apellido"
}
```

**Respuesta Exitosa (201 Created):**

```json
{
  "user": {
    "email": "usuario@ejemplo.com",
    "first_name": "Nombre",
    "last_name": "Apellido"
  },
  "refresh": "token_refresh",
  "access": "token_access",
  "message": "Usuario registrado exitosamente"
}
```

### Inicio de Sesión

```http
POST /api/login/
Content-Type: application/json

{
    "email": "usuario@ejemplo.com",
    "password": "contraseña123"
}
```

**Respuesta Exitosa (200 OK):**

```json
{
  "refresh": "token_refresh",
  "access": "token_access",
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "username": "usuario",
    "user_type": "common"
  }
}
```

---

## 2. Gestión de Perfil

### Ver Perfil

```http
GET /api/profile/
Authorization: Bearer {token_access}
```

**Respuesta Exitosa (200 OK):**

```json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "first_name": "Nombre",
  "last_name": "Apellido",
  "user_type": "common"
}
```

### Actualizar Perfil

```http
PUT /api/profile/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "first_name": "Nuevo Nombre",
    "last_name": "Nuevo Apellido"
}
```

---

## 3. Exploración de Servicios

### Ver Listado de Servicios

```http
GET /api/services/
Authorization: Bearer {token_access}
```

**Parámetros de Filtrado:**

- `category`: ID de categoría
- `status`: active
- `price_type`: hourly/fixed/negotiable
- `city`, `state`, `country`, `min_price`, `max_price`, `available_day`

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
    "status": "active",
    "created_at": "2024-03-15T10:30:00Z"
  }
]
```

### Ver Detalles de Servicio

```http
GET /api/services/1/
Authorization: Bearer {token_access}
```

**Respuesta Exitosa (200 OK):**

```json
{
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
```

---

## 4. Contratación de Servicios

### Crear Contrato

```http
POST /api/contracts/create/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "service": 1,
    "start_date": "2024-03-20T14:00:00Z",
    "description": "Reparación de fuga en baño principal",
    "location": "Av. Principal 123, Ciudad"
}
```

**Respuesta Exitosa (201 Created):**

```json
{
  "id": 1,
  "service": 1,
  "service_title": "Reparación de Plomería",
  "client": 1,
  "client_name": "Nombre Apellido",
  "provider": 2,
  "provider_name": "Carlos Plomero",
  "status": "pending",
  "status_display": "Pendiente",
  "start_date": "2024-03-20T14:00:00Z",
  "end_date": null,
  "description": "Reparación de fuga en baño principal",
  "location": "Av. Principal 123, Ciudad",
  "price": "50.00",
  "client_rating": null,
  "client_review": null,
  "provider_rating": null,
  "provider_review": null,
  "created_at": "2024-03-15T10:30:00Z",
  "updated_at": "2024-03-15T10:30:00Z"
}
```

### Ver Contratos

```http
GET /api/contracts/
Authorization: Bearer {token_access}
```

**Respuesta Exitosa (200 OK):**

```json
[
  {
    "id": 1,
    "service": 1,
    "service_title": "Reparación de Plomería",
    "client": 1,
    "client_name": "Nombre Apellido",
    "provider": 2,
    "provider_name": "Carlos Plomero",
    "status": "accepted",
    "status_display": "Aceptado",
    "start_date": "2024-03-20T14:00:00Z",
    "end_date": null,
    "description": "Reparación de fuga en baño principal",
    "location": "Av. Principal 123, Ciudad",
    "price": "50.00",
    "client_rating": null,
    "client_review": null,
    "provider_rating": null,
    "provider_review": null,
    "created_at": "2024-03-15T10:30:00Z",
    "updated_at": "2024-03-15T10:30:00Z"
  }
]
```

### Calificar Servicio

```http
PUT /api/contracts/1/review/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "client_rating": 5,
    "client_review": "Excelente servicio, muy profesional y puntual"
}
```

**Respuesta Exitosa (200 OK):**

```json
{
  "id": 1,
  "service": 1,
  "service_title": "Reparación de Plomería",
  "client": 1,
  "client_name": "Nombre Apellido",
  "provider": 2,
  "provider_name": "Carlos Plomero",
  "status": "completed",
  "status_display": "Completado",
  "start_date": "2024-03-20T14:00:00Z",
  "end_date": "2024-03-20T16:00:00Z",
  "description": "Reparación de fuga en baño principal",
  "location": "Av. Principal 123, Ciudad",
  "price": "50.00",
  "client_rating": 5,
  "client_review": "Excelente servicio, muy profesional y puntual",
  "provider_rating": 5,
  "provider_review": "Cliente muy amable y cooperativo",
  "created_at": "2024-03-15T10:30:00Z",
  "updated_at": "2024-03-15T10:30:00Z"
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
  "error": "La fecha seleccionada no está disponible"
}
```

---

## Notas Importantes

1. Siempre incluir el token JWT en los headers
2. Las fechas deben ser futuras
3. Las calificaciones solo se pueden hacer en servicios completados
4. Los contratos solo se pueden crear para servicios activos

---

## Diagrama de Flujo

- [Diagrama de usuario cliente (imagen)](./assets/ClienteServic.png)
- [Enlace al diagrama de usuario cliente (Mermaid)](https://mermaid.live/view#pako:eNptks2OmzAQx1_F8l4hJUCWxIdWXUiyqdoemqqHwB4sGIgVYyNjuslGeaQ-Q6X2xWoc6EZVfRrP_zdf9pxxLgvABLuum4lcipJVJBMIcXqSnSaooJWC3qH3UANBAqRbUHWwjJQH68mEDS-5fM73VGn0Nel1hN6nG8FyJp-Q675FD-kXqFirlURv0EdZMfF0xR6sHKfLY8OloqgF9b0Pawc9tnqSrhjX_5ETKy_Tb4AK0JRzaI3xFxuopaVW518_E2iBIjOsSaapene5AisDoO3vH5Zbp7F6hcYca6s9pmtoNZPiVR9bebTAxhTZDtUNUjfctFXIsdDmttCHNKaclSyn_zZssc_SUjsz-_haq1v_1dXqEwe0QyXjnNwBgNO_8gHIXRAEg-0-s0Lvid8csYNrUDVlhfn4c58hw_Z7M0yMab8XZ-JiONppuT2JHBOtOnCwkl21x6SkvDW3rimohoSZHaH1iDRU7KS8vWJyxkdMpvNoMr_3vMBfzKMo9GcOPmHi-mE0mS2CyJxp4PteeHHwi00wnYQLw4X3nj_z5rPQBEDBtFSfrjtrV9fBleoHGVpSIApQseyExmR2-QNelua-)

---

© Servic App
