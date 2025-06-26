# Guía Prestador de Servicios

## Introducción

Esta guía está dirigida a los usuarios que desean ofrecer servicios y gestionar su actividad como prestadores dentro de Servic App. Aquí encontrarás ejemplos prácticos para testear la API usando Insomnia, así como explicaciones de cada flujo y endpoint relevante para el prestador.

---

## Índice

- [Solicitud para ser Prestador](#solicitud-para-ser-prestador)
- [Gestión de Perfil de Prestador](#gestión-de-perfil-de-prestador)
- [Publicación y Gestión de Servicios](#publicación-y-gestión-de-servicios)
- [Gestión de Contratos](#gestión-de-contratos)
- [Errores Comunes](#errores-comunes)
- [Notas Importantes](#notas-importantes)
- [Diagrama de Flujo](#diagrama-de-flujo)

---

## 1. Solicitud para Convertirse en Prestador

### Crear Solicitud

```http
POST /api/provider/request/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "request_reason": "Deseo ofrecer servicios de plomería profesional con más de 5 años de experiencia"
}
```

**Respuesta Exitosa (201 Created):**

```json
{
  "id": 1,
  "user_email": "usuario@ejemplo.com",
  "user_name": "Nombre Apellido",
  "status": "pending",
  "status_display": "Pendiente",
  "request_reason": "Deseo ofrecer servicios de plomería profesional con más de 5 años de experiencia",
  "admin_response": null,
  "created_at": "2024-03-15T10:30:00Z",
  "updated_at": "2024-03-15T10:30:00Z"
}
```

### Ver Estado de Solicitud

```http
GET /api/provider/requests/
Authorization: Bearer {token_access}
```

---

## 2. Gestión de Perfil de Prestador

### Crear Perfil

```http
POST /api/provider/profile/
Authorization: Bearer {token_access}
Content-Type: multipart/form-data

{
    "identification_type": "dni",
    "identification_number": "12345678",
    "phone_number": "+1234567890",
    "address": "Calle Principal 123",
    "city": "Ciudad",
    "state": "Estado",
    "country": "País",
    "certification_file": [archivo],
    "certification_description": "Certificado en plomería profesional",
    "years_of_experience": 5
}
```

**Respuesta Exitosa (201 Created):**

```json
{
  "message": "Perfil creado exitosamente",
  "data": {
    "id": 1,
    "identification_type": "dni",
    "identification_number": "12345678",
    "phone_number": "+1234567890",
    "address": "Calle Principal 123",
    "city": "Ciudad",
    "state": "Estado",
    "country": "País",
    "certification_file": "url_archivo",
    "certification_description": "Certificado en plomería profesional",
    "years_of_experience": 5,
    "is_verified": false,
    "created_at": "2024-03-15T10:30:00Z",
    "updated_at": "2024-03-15T10:30:00Z"
  }
}
```

### Actualizar Perfil

```http
PUT /api/provider/profile/
Authorization: Bearer {token_access}
Content-Type: multipart/form-data

{
    "phone_number": "+1987654321",
    "address": "Nueva Dirección 456"
}
```

---

## 3. Publicación y Gestión de Servicios

### Crear Servicio

```http
POST /api/services/create/
Authorization: Bearer {token_access}
Content-Type: multipart/form-data

{
    "title": "Reparación de Plomería",
    "description": "Servicios de plomería residencial y comercial",
    "category": 1,
    "price": "50.00",
    "price_type": "hourly",
    "location": "Ciudad",
    "city": "Ciudad",
    "state": "Estado",
    "country": "País",
    "availability_start": "09:00:00",
    "availability_end": "18:00:00",
    "available_days": "Lunes,Martes,Miércoles,Jueves,Viernes",
    "images": [
        {
            "image": [archivo],
            "is_primary": true
        }
    ]
}
```

**Respuesta Exitosa (201 Created):**

```json
{
  "id": 1,
  "title": "Reparación de Plomería",
  "description": "Servicios de plomería residencial y comercial",
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
  "status": "pending",
  "status_display": "Pendiente",
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

### Subir Imagen de Servicio

```http
POST /api/services/1/images/
Authorization: Bearer {token_access}
Content-Type: multipart/form-data

{
    "image": [archivo],
    "is_primary": false
}
```

### Establecer Imagen Principal

```http
PUT /api/services/images/1/set-primary/
Authorization: Bearer {token_access}
```

### Eliminar Imagen

```http
DELETE /api/services/images/1/
Authorization: Bearer {token_access}
```

---

## 4. Gestión de Contratos

### Ver Contratos Recibidos

```http
GET /api/contracts/
Authorization: Bearer {token_access}
```

### Aceptar Contrato

```http
PUT /api/contracts/1/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "status": "accepted"
}
```

### Marcar Contrato en Progreso

```http
PUT /api/contracts/1/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "status": "in_progress"
}
```

### Completar Contrato

```http
PUT /api/contracts/1/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "status": "completed",
    "end_date": "2024-03-20T16:00:00Z"
}
```

### Calificar Cliente

```http
PUT /api/contracts/1/review/
Authorization: Bearer {token_access}
Content-Type: application/json

{
    "provider_rating": 5,
    "provider_review": "Cliente muy amable y cooperativo"
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
  "detail": "Solo los prestadores de servicios pueden acceder a esta funcionalidad"
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
  "certification_file": ["El archivo de certificación es obligatorio"]
}
```

---

## Notas Importantes

1. El perfil debe estar verificado para crear servicios
2. Las imágenes no deben superar 5MB
3. Solo se puede tener una imagen principal por servicio
4. Los contratos solo pueden ser actualizados por el prestador asignado
5. Las calificaciones solo se pueden hacer en servicios completados

---

## Diagrama de Flujo

- [Diagrama provider (imagen)](./assets/ProviderServic.png)
- [Enlace al diagrama provider (Mermaid)](https://mermaid.live/view#pako:eNptlN1y2jAQhV9Fo2tIwean9UXbBPIPhDS9St0LYS-gia31yDIJYXikXvUBOtO8WNdLYpwpN4y0-nR0dNB6IyOMQQay2WyGJkIz14sgNEIkao2FC0SsFhbKgltCCoEwgM1Y2QdmEB-4EhrePk_wMVoq68T3YbkuxPGPUF4aHWkM5U_RbH4WJ1QZ4UIbKuyYE64PNqH8--c0F5mF3KkY7ZdQbnfEgAgxQeaGtP8OE5J0SuRg93wlOGTwlAWPM4szWhUZWqHiVJu97GlN9p5kz2qmeO3u5RcvntHiwIISGdi5TkQMB049Y_S8tFfMQERgnZ7rSEX65fde95ypC_Y23amtwDJ42ORF3WSt9Obtkg6cFjMKhONYlVnn1XGXzFwRc05-NZpD0BVD1wR9g0iX3tE4q1wNuWZktIs0gswpW1F7r6O6sTHpjZUlWxGmKBTvirGSHDM1qSgwFCrSY8v3zISZm_dK9JMl8E7rhrlp-TephMMUUaLBOKiQUS3H291Vl-pZVbcoByJFp1d72dt66tP6xHhl7BZXOgb7oRyApcdQvoz_8zXe143Ilyqj9nHw5F7Tyt06AXFPBydoA4OG2kw2ZAo2VTqmltyUXCi58UIZ0JAbT4ZmS5wqHN6tTSQDZwtoSIvFYimDuUpymhVZrBwMNXWvSt-QTJl7xPpUBhv5JIO23z3yvU7P--i3u91Wq9dryDWV2y0qt3t-1-u0P_m-520b8pkVvCO_73v9Vp_oTrff73UaEmLt0I533xP-rDTkwpZXeTVlwVBcAyyMk0F3-w9qZGQ_)

---

© Servic App
