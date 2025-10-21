# Calculadora de Sistemas de Colas

Aplicación en línea de comandos (CLI) en Python que permite calcular métricas de rendimiento para modelos de teoría de colas:

- **PICS**: `M/M/1` → Poisson, exponencial, 1 servidor, población infinita
- **PICM**: `M/M/k` → Poisson, exponencial, k servidores, población infinita
- **PFCS**: `M/M/1/M` → Poisson, exponencial, 1 servidor, población finita
- **PFCM**: `M/M/k/M` → Poisson, exponencial, k servidores, población finita M

Ideal para análisis de colas en servicios, manufactura, call centers, y más.

---

## 📁 Estructura del Proyecto
Queuing_simulation_models/
├── .gitignore
├── README.md
├── main.py
├── controller/
│   └── controller.py
├── Model/
│   ├── modelPFCM.py
│   ├── modelPFCS.py
│   ├── modelPICM.py
│   └── modelPICS.py
└── View/
    ├── view_PFCM.py
    ├── view_PFCS.py
    ├── view_PICM.py
    └── view_PICS.py


- **Modelo**: Contiene la lógica matemática y fórmulas.
- **Vista**: Maneja la interacción con el usuario y muestra resultados.
- **Controlador**: Orquesta el flujo entre modelo y vista.

---

## 🚀 Cómo Ejecutar

### Requisitos
- Python 3.7 o superior
- Ninguna librería externa (solo módulos estándar como `math`)
