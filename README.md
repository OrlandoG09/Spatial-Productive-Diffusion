# Spatial Productive Diffusion: Análisis Epidemiológico del Desarrollo Industrial

Este proyecto analiza la **difusión espacial del conocimiento productivo** entre municipios utilizando modelos epidemiológicos y econometría espacial. El algoritmo cuantifica cómo las ramas industriales se "contagian" de un municipio a otro a lo largo del tiempo, distinguiendo entre contagio inducido (efecto vecindad) y contagio espontáneo.

##  Descripción

El script procesa datos geográficos y matrices de producción industrial de periodos quinquenales (2003-2023) para identificar patrones de adopción industrial. Utiliza **Python**, **GeoPandas** y **Libpysal** para:

1.  **Alineación Espacial:** Sincroniza datos censales con shapefiles municipales.
2.  **Matriz de Pesos Espaciales ($W$):** Calcula la vecindad mediante el criterio *Queen Contiguity*.
3.  **Detección de Adopciones:** Identifica cuándo un municipio adquiere una nueva capacidad productiva (rama industrial).
4.  **Clasificación del Contagio:**
    * **Inducido:** El municipio adopta una rama que sus vecinos ya poseían (Lag Espacial > 0).
    * **Espontáneo:** El municipio innova sin influencia vecinal directa.
5.  **Cálculo de Tasas:** Genera métricas de difusión por rama industrial.

## Tecnologías Utilizadas

* **Python 3.x**
* **Pandas & NumPy:** Manipulación de matrices de datos.
* **GeoPandas:** Manejo de datos geoespaciales (.shp).
* **Libpysal:** Librería de análisis espacial (Weights & Spatial Lag).
* **OpenPyXL:** Lectura y escritura de archivos Excel.

## Estructura de Datos Requerida

Para ejecutar este script, necesitas los siguientes archivos en el directorio raíz (no incluidos en el repo por privacidad):

* `mun22gw.shp`: Shapefile con la geometría de los municipios (Índice: CVEGEO).
* `Ms_1.xlsx`: Archivo de Excel con hojas por año (`2003`, `2008`, `2013`, `2018`, `2023`). Cada hoja contiene la matriz binaria de ramas industriales por municipio.

## Instalación y Uso
## 🚀 Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/OrlandoG09/Spatial-Productive-Diffusion.git](https://github.com/OrlandoG09/Spatial-Productive-Diffusion.git)
    cd Spatial-Productive-Diffusion
    ```

2.  **Crear y activar un entorno virtual (Opcional pero recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el script:**
    ```bash
    python AnalisisDE.py
    ```
  

## Resultados

El script genera un archivo `Tasas_Difusion_Por_Rama.xlsx` que contiene:
* Tasas de contagio inducido por periodo (quinquenal y acumulado).
* Tasas de aparición espontánea por periodo(quinquenal y acumulado).

Estos resultados permiten identificar qué industrias dependen de la aglomeración espacial y cuáles surgen de manera aislada.

## Autor

* **[Orlando Galván Moreno]** - *Economía y Ciencia de Datos* - [https://github.com/OrlandoG09]

---

*Este proyecto es parte de una investigación sobre la dinámica económica regional en México.*



