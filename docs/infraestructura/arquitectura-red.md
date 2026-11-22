# Arquitectura de red — SmartFactory

## 1. Objetivo

Diseñar una infraestructura virtualizada para una planta industrial simulada, separando las redes de administración, servidores y producción mediante un firewall OPNsense.

## 2. Plataforma de virtualización

- Hipervisor: Oracle VirtualBox 7.0.12
- Firewall: OPNsense 26.7
- Máquina virtual: VM-FIREWALL
- Memoria RAM: 4096 MB
- Disco virtual: 20 GB
- Sistema de archivos: UFS

## 3. Arquitectura de red

| Zona | Red de VirtualBox | Interfaz | Dirección del firewall |
|---|---|---|---|
| WAN | NAT | em0 | 10.0.2.15/24 (DHCP) |
| Administración | SF-ADMIN | em1 (LAN) | 192.168.10.1/24 |
| Servidores | SF-SERVIDORES | em2 (OPT1) | 192.168.20.1/24 |
| Producción | SF-PRODUCCION | em3 (OPT2) | 192.168.30.1/24 |

## 4. Segmentación

Se utilizan tres redes internas independientes de VirtualBox.

Esta implementación proporciona separación de redes virtuales, pero no utiliza etiquetado VLAN IEEE 802.1Q.

OPNsense actuará como puerta de enlace y punto de control del tráfico entre las redes.

## 5. Estado de implementación

### Completado

- Instalación de OPNsense en disco virtual.
- Configuración de cuatro adaptadores de red.
- Asignación de interfaces WAN, LAN, OPT1 y OPT2.
- Configuración de las tres direcciones IPv4 internas.
- Cambio de la contraseña predeterminada del administrador.

### Pendiente

- Configuración y verificación de las reglas del firewall.
- Creación de las máquinas virtuales de servidores y producción.
- Pruebas de conectividad y aislamiento entre redes.
- Validación del acceso administrativo mediante HTTPS.
- Configuración de servicios adicionales de infraestructura.

## 6. Consideraciones de seguridad

- La administración web utiliza HTTPS.
- La cuenta root tiene una contraseña personalizada.
- El servicio DHCP de las redes internas se configurará según las necesidades del laboratorio.
- Las políticas de comunicación entre zonas deberán definirse y verificarse antes de considerar segura la segmentación.
