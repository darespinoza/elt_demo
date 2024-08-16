# Extract, Load & Transform demo


Recientemente creé una demo de arquitectura ELT usando Sling, dbt y Dagster. Este proyecto demuestra el poder de combinar distintas tecnologías para lograr una solución robusta para la integración y procesamiento de datos.

Aquí un breve resumen de las tecnologías que utilicé:

Sling: Para realizar una carga incremental de una base de datos a otra (Extract & Load)
dbt: Para transformar la data usando modelos incrementales (Transform)
Dagster: Para orquestar la ejecución de los procesos ELT

Adicionalmente usé Grafana para visualizar la data transformada y Docker para contener a la arquitectura.

Github: 


For this demo of an ELT architecture, I've used Sling, dbt and Dagster. This project shows the power of combining different technologies to achieve a rosbust solution to data integration and processing.

For this demo, I've set a source database 

#ELT #IngenieriaDeDatos #Tecnologia #IntegracionDeDatos #Sling #dbt #Dagster #Grafana #Docker

```
git clone https://github.com/darespinoza/elt_demo.git
```

```
docker compose up
```