# Servic App - Documentación Principal

## Introducción

Servic App es una plataforma que conecta usuarios con prestadores de servicios, permitiendo la gestión integral de perfiles, servicios, contrataciones y administración desde distintos roles.

---

## Índice de Documentación

- [Guía para Usuario Cliente](./README-USER.md)
- [Guía para Prestador de Servicios](./README-PROVIDER.md)
- [Guía para Administrador](./README-ADMIN.md)

---

## Instalación del proyecto

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd servic-app
```

### 2. Crear y activar un entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

- Copia el archivo `.env.example` y renómbralo a `.env`.
- Completa los valores requeridos según tu entorno (base de datos, claves, etc).

### 5. Aplicar migraciones y crear superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

---

## Diagrama General de la Aplicación

_A continuación puedes agregar el diagrama global de la app. Puedes incluir:_

- [_Un enlace a un visor de diagramas_](https://mermaid.live/view#pako:eNp1lM1y2jAQx19Fo0NPQLENmPjQlvCZr06mtD1Q96DYC2hiJI8styEMj5RTb710prxYVxIBM0lvkvan3f2vtLuhiUyBRrRer8cikWLOF1EsCMnYWpY6IilbKDAHegkriIgAWU-ZureMlPf2JBb2-jyTP5MlU5p8Hhg7Ib1vMb0QPOEypt9Jvf6OnOPJJ1jwQitJ3pJrueACbQ4_t0jf28T0758vRckUlySRq91v8T6mWwf1PaTIdPdk4YGHDocPeSYVIwWoHyZYcfA48Cw1NFRfCq2YPmIHauiokaHGUGguBcO4Fq84GzlsbJ2xjM958oozl99H6bT4VsutQq8slaoiw69igcV66YpXlQYnSgMM20sSSIGwjORMQEbM2lwy9WQJ3_06FnMQOOlBVVTpimo0kTdkdGLLn5OEvXl8Yq4WF40TY_wKxN7ZPSGUsGOpXOp7dTMkR5VndtIPunw0T2WGvt3bHBM5avGdFlfNXq7kHdpJLpWTf6zZsFrWWfXsOd7IxOsrQMGg5tzW8GXEkYs4tsmVd0ASUNq--GmVx46bGO62vMuqX-JYjomjLvz_FdRhFw679G2TJNyEffELLx105dvvALlmb5FdssfXvuyVg68NfMMUJgcC1Ups6sL0HzZXnoFmhwvX7sKNX_3jScZBaDjpl4ZNdF-swO2H-_14v5_s98J0zNTKJb08P_gR3ocNKZYsx8Gi4UHv37DQ6wzIDJPDro6EFDiAaI2uQK0YT3FYbQwXUzuSYhrh0o4kGostcqzUcroWCY20KqFGlSwXSxrNWVbgrsxTpmHAca6x1TOCzTSTsrql0YY-0KjV7jT8sNvxu61m0G22vU6NrvE4bAQtr9MNw-5ZN-w02-1tjT5aD81GN2w3m17g--3QC8-aeANSrqW6cZPWDtwaXSgjZZ-UApGC6stSaBqFre0_h4u2pQ)
- [_Imagen del diagrama SERVIC-APP_](./assets/ServicApp.png)

---

## Notas para programadores y contribuyentes

- Consulta la guía específica de tu rol que quieras ver.
- Para contribuir, abre un Pull Request o Issue siguiendo las normas del repositorio.

---

© Servic App
