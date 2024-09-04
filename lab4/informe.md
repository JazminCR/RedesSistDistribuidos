# Análisis del tráfico de red

**Materia**: *Redes y Sistemas Distribuidos*.

**Laboratorio 4**: Red.

**Integrantes**: Acosta, Mateo Lucas & Caruso Rojo, Jazmín & Gallegos, Lucas Oscar.

[Video del laboratorio 4 - análisis, implementación de algoritmo y resultados](https://drive.google.com/file/d/1mAyVuiQCaqDi_FC8vRaCrQTfVs00J_Ly/view?usp=sharing)

## Resumen

Este proyecto se enfoca en el análisis del tráfico de una red. Para ello utilizamos OMNeT++ y simulación discreta. El objetivo principal es proponer y diseñar una solución de enrutamiento, es decir, encontrar o determinar las rutas a seguir para enviar paquetes de un origen a un destino.

## Introducción

La principal función de la capa de red es enrutar paquetes, es decir, tiene que determinar la ruta o camino que deben seguir los paquetes a medida que fluyen de un emisor a un receptor. Los algoritmos que calculan esto se conocen como algoritmos de enrutamiento.

Primero analizaremos el tráfico y rendimiento de una red que utiliza un algoritmo de enrutamiento muy básico. Luego, implementaremos un algoritmo que aumente/mejore la eficiencia de la misma. 

### Modelo de red

Como modelo tenemos una red con forma de anillo compuesta por 8 nodos. Cada nodo cuenta con dos capas de enlace, cada una conectada a un vecino. El sistema de enrutamiento que se utiliza se basa en enviar los paquetes hacia el siguiente nodo (vecino) en sentido horario.

![modelo_red](https://github.com/JazminCR/graficos_lab3/blob/main/red_anillo.png?raw=true)

**Configuraciones**:

*interArrivalTime* indica cada cuánto tiempo se va a generar el paquete.

*packetByteSize* indica el tamaño del paquete en Bytes.

*destination* identifica el nodo destino.

### Casos de estudio

- **Caso 1**: los nodos 0 y 2 envían paquetes al nodo 5.

```Network.node[{0,2}].app.interArrivalTime = exponential(1)```

```Network.node[{0,2}].app.packetByteSize = 125000```

```Network.node[{0,2}].app.destination = 5```

- **Caso 2**: todos los nodos (0, 1, 2, 3, 4, 6 y 7) le envían paquetes al nodo 5.

```Network.node[{0,1,2,3,4,6,7}].app.interArrivalTime = exponential(1)```

```Network.node[{0,1,2,3,4,6,7}].app.packetByteSize = 125000```

```Network.node[{0,1,2,3,4,6,7}].app.destination = 5```

### Métricas

Para realizar el análisis recopilamos diversas estadísticas que nos proporcionan una visión integral del funcionamiento del enrutamiento.

Las estadísticas son las siguientes (tener en cuenta que los valores obtenidos pueden variar en distintas corridas):

- **Paquetes enviados**: cantidad de paquetes enviados desde los nodos emisores.

- **Paquetes recibidos**: cantidad de paquetes que recibió el nodo receptor.

- **Demora de entrega de paquetes**: mide el tiempo que tarda un paquete desde que se genera hasta que llega a su destino.

- **Cantidad de saltos utilizados por cada paquete**: mide la cantidad de nodos que un paquete atraviesa desde su origen hasta su destino.

- **Utilización de los búferes**: mide la ocupación de los búferes en los nodos.

### Análisis caso 1

| enviados | recibidos | delay | saltos | 
|----------|-----------|-------|--------|
|    390   |    196    |   51  |    4   |
|          |           |       |        |

![pkt](https://github.com/JazminCR/graficos_lab3/blob/main/pkt_t1_c1.png?raw=true)

![buferes](https://github.com/JazminCR/graficos_lab3/blob/main/todos_bufer_nodos_1.png?raw=true)

El tamaño del búfer indica cuántos paquetes están esperando ser procesados en el enlace.
El nodo 0 tiene un tamaño significativamente grande, lo cual quiere decir que está experimentando una acumulación de paquetes mayor (está sobrecargado), esto se debe a que el nodo recibe los paquetes generados por el nodo 2 pero a la vez él también genera sus propios paquetes.
Los nodos 1, 6 y 7 tienen un tamaño similar y pequeño de búfer ya que ellos reciben paquetes y casi inmediatamente los envían, es decir que están equilibrados. 
Los nodos 3 y 4 tienen su búfer desocupado ya que no están siendo utilizados para enviar paquetes.
Podemos notar entonces un desequilibrio general en la red debido a que se hace uso excesivo de algunos canales mientras otros quedan vacíos, esto es ineficiente.

Además, por la congestión y cuellos de botella generados, aproximadamente la mitad de lo paquetes enviados se pierden.

El retardo mide el tiempo desde que se crea un paquete hasta que llega a su destino.
El nodo 5 (el destino de los paquetes) muestra un retardo promedio de 51,15 unidades de tiempo con una desviación estándar de 28,38. Este retardo puede considerarse significativo, indicando que los paquetes tardan un tiempo considerable en llegar al destino debido a la congestión (los paquetes pasan mucho tiempo en búfer).

El conteo de saltos indica por cuántos nodos intermedio ha pasado el paquete antes de llegar a su destino.
El nodo 5 muestra un conteo de saltos promedio de 3.92 con una desviación estándar de 0,99(supongamos en promedio 4). Esto es razonable ya que los paquetes provienen de los nodos 0 y 2, y, del nodo 0 al 5 hay 3 enlaces, y del 2 al 5 hay 5, por lo tanto tiene sentido que en promedio sean 4 los saltos que dan. 

Como conclusión de este análisis podemos decir que el algoritmo de enrutamiento utilizado no aprovecha eficientemente la red, sería mejor si los paquetes hacen menos saltos, o si se dispersan entre los diferentes nodos, es decir, si utilizan todos los enlaces para su envío, y así evitar congestión. Esto puede mejorarse implementando un algoritmo que tenga en cuenta lo nombrado anteriormente.

### Análisis caso 2

| enviados | recibidos | delay | saltos | 
|----------|-----------|-------|--------|
|   1380   |    200    |   65  |   2.1  |
|          |           |       |        |

![pkt](https://github.com/JazminCR/graficos_lab3/blob/main/pkt_t1_c2.png?raw=true)

![buferes_intervalo1](https://github.com/JazminCR/graficos_lab3/blob/main/todos_bufer_nodos_12_i1.png?raw=true)

Podemos observar que los búferes de los nodos 0, 1, 2, 3, 6 y 7 se sobrecargan, es decir que en ellos se genera demasiado tráfico debido a que todos producen paquetes y además les llegan los paquetes generados por sus anteriores. 
El nodo 4 no recibe paquetes de los demás, entonces sólo tiene los paquetes que él genera, por lo tanto tiene un tamaño de búfer mucho menor.

Puede notarse una gran pérdida de paquetes.

Esta red no se encuentra en equilibrio justamente porque la mayoría de los búferes están siendo sobrecargados.

Logicamente si aumentamos el intervalo de generación se van a generar menos paquetes en cada nodo, y por lo tanto, la cantidad que va a transmitirse será menor, disminuyendo asi la probabilidad de congestión.
Al establecer el intervalo en 7 dejamos más tiempo al paquete que se genera en el nodo más lejano del nodo destino (porque en esta tarea asumimos red de 8 nodos). Sabiendo que los canales tienen una tasa de 1Mbps, cada paquete generado va a tardar un segundo en enviarse al nodo vecino, por lo que el paquete del nodo más lejano tardará 7 segundos en llegar al nodo destino (puede que esto no sea exactamente así puesto que el intervalo es aleatorio, y podría pasar que algunos paquetes salgan antes o después provocando que se acumulen). De esta forma aumentamos al máximo la probabilidad de que se mande un paquete a la vez por canal (con el menor tiempo posible para que se genera lo mayor cantidad que se pueda) reduciendo la posibilidad de que se acumulen paquetes en algún búfer, y para cuando hayan llegado se estarán generando otros 7 paquetes y enviando de la misma forma. 
Para dar una respuesta más general, podemos decir que si la cantidad de nodos es N, el intervalo de generación para que la red esté en equilibrio debe ser N - 1.

## Métodos

En esta sección se podrá ver el algoritmo implementado para solucionar el problema de enrutamiento, y los resultados obtenidos.

### Implementación del algoritmo

Teniendo en cuenta que la red es circular, la idea principal de nuestro algoritmo es ver si conviene enviar el paquete desde el nodo origen hacia el destino en sentido horario o antihorario, a esto lo hacemos calculando la ruta más corta.

El algoritmo de enrutamiento que implementamos se basa en que cada nodo genere un paquete *hello* y lo envíe en sentido antihorario (si se envia en sentido horario la lógica se invierte). Estos paquetes irán recorriendo la red, al tener ésta una topología circular, terminarán llegando al nodo que los generó. 

La estructura de los paquetes *hello* es una herencia de la clase *packet* definida en *Packet.msg* ya que ambos comparten los atributos nodo origen, destino, cantidad de saltos y un bool que indica si el paquete es de tipo *hello*. Estos paquetes tienen un atributo extra que es un arreglo (en un principio vacío) de los nodos por los que va pasando.

Gracias a esa tabla, una vez que el paquete llega al nodo que lo generó, éste podrá extraer datos acerca de la topología de la red, tanto de la cantidad de nodos como la distancia a cada uno.

Al contar con esta información y teniendo en cuenta que la red tiene forma de anillo, es decir que es circular, el nodo más distante (de cada uno) se encontrará en la posición *sizeNed/2 - 1* (en el caso que la cantidad de nodos sea impar, el resultado es el nodo más distante en sentido horario debido a que los paquetes *hello* se mandan en sentido antihorario). 

De esta forma, los índices de la tabla en cierto sentido representan la distancia a cada uno de los nodos. Si el nodo destino se encuentra en una posición mayor que la del nodo más distante al nodo origen significa que la distancia más corta al destino es en sentido horario. De lo contrario, la distancia más corta al destino es en sentido antihorario.

Entonces, el algoritmo de enrutamiento diseñado para elegir hacia dónde mandar los paquetes parte de que los paquetes *hello* se mandan en sentido antihorario y de la suposición de que nos encontramos en una topología de red circular (con cualquier cantidad de nodos), buscando así en la tabla el nodo destino para luego inferir sobre la posición de éste en la misma y decidir por cuál interfaz enviarlo.

¿Qué cambios observamos al implementarlo?

### Resultado/Análisis caso 1

| enviados | recibibos | delay | saltos | 
|----------|-----------|-------|--------|
|    390   |    379    |   7   |    3   |
|          |           |       |        |

![pkt](https://github.com/JazminCR/graficos_lab3/blob/main/pkt_t2_c1.png?raw=true)

![buferes_caso1](https://github.com/JazminCR/graficos_lab3/blob/main/todos_bufer_nodos_t2_c1.png?raw=true)

En este caso podemos observar una gran diferencia. Mientras que antes el búfer del nodo 0 se sobrecargaba, los búferes de los nodos 1, 2, 6 y 7 estaban dentro de todo equilibrados, y los de los nodos 3 y 4 no se utilizaban, ahora el uso de la red está más en equilibrio ya que ningún nodo se satura y casi todos son utilizados por igual. Esto se debe a que gracias al algoritmo, el nodo 0 envía los paquetes en sentido horario, y el nodo 2 en sentido antihorario, es decir que cada uno elige la manera más corta para llegar a destino. Esto implica que el búfer del nodo 0 ahora sólo tiene los paquetes generados por él mismo, y ya no recibe los generados por el nodo 2.
El único búfer vacío es el del nodo 1 debido a que es justo el que se encuentra entre medio del 0 y el 2 (los paquetes no pasan por acá).
El resto de los búferes tienen un tamaño similar ya que ellos sólo se encargan de recibir y enviar paquetes.
Podemos decir que el algoritmo mejora el equilibrio de la red, reduciendo la congestión y utilizando más eficientemente los recursos disponibles. 

Se puede ver la gran mejora en relación a paquetes enviados y recibidos, la pérdida es muy mínima.

El delay obtenido es de aproximadamente 7 unidades de tiempo, esto es mucho menor que el que se tenía sin la implementación del algoritmo gracias a que se reduce mucho la congestión (los paquetes pasan poco tiempo en búfer).

Además obtuvimos que, en promedio, los saltos que realiza cada paquete son 3, es decir que este aspecto también cambió positivamente.

### Resultado/Análisis caso 2

| enviados | recibidos | delay | saltos | 
|----------|-----------|-------|--------|
|   1380   |    398    |   62  |   1.9  |
|          |           |       |        |

![pkt](https://github.com/JazminCR/graficos_lab3/blob/main/pkt_t2_c2.png?raw=true)

![buferes_caso2](https://github.com/JazminCR/graficos_lab3/blob/main/todos_bufer_nodos_t2_c2.png?raw=true)

En este caso la mejora es menos notable debido a que si todos los nodos generan y la red tiene forma de anillo entonces de cualquier forma la mayoria de los búferes van a estar sobrecargados (porque generan y seguramente reciben de al menos un vecino) dado que una vez que el algoritmo encuentra el camino más corto desde un nodo origen, éste último enviará todos los paquetes por el mismo enlace.

Si bien sigue habiendo pérdida de paquetes, puede observarse un incremento de los paquetes recibidos.

Respecto a las métricas de delay y de saltos por paquete no se logra ver una mejora significativa en comparación con el algoritmo de enrutamiento inicial (por lo explicado antes).

### Conclusión

Con el análisis del caso 1 podemos decir que el uso de la red fue mucho más eficiente gracias a la implementación del algoritmo de enrutamiento propuesto, casi todos los paquetes llegaron a destino, la demora y saltos fue menor, y el uso de los búferes y enlaces estuvo más equilibrado. Por lo tanto, el algoritmo funciona como queriamos y logra asignarle a cada paquete la ruta óptima hacia su destino.
La mejora en el caso 2 no es tan notoria debido a que cuando todos los nodos transmiten datos a un único nodo, ese nodo se convierte en un punto de concentración del tráfico, independientemente de la dirección en la que los paquetes se manden, el nodo receptor tendrá que manejar todo lo que le entre, lo cual puede causar un cuello de botella. Si el nodo de destino está abrumado por la cantidad de datos que recibe, la mejora del enrutamiento no tiene un impacto significativo en la eficiencia general.

## Discusiones

### Logros

Entender el funcionamiento de la red y aprender sobre el enrutamiento de la misma. 
Proponer e implementar un algoritmo que mejora el rendimiento de la red.

### Limitaciones

La limitación principal de este algoritmo es que funciona para redes con forma de anillo. No se garantiza su eficiencia en redes de otro tipo.
Además, para que el algoritmo funcione correctamente, el costo de los enlaces debe ser 1. Si este valor cambia entonces tampoco puede asegurarse efectividad.
Se asume que la red no va a variar (por ej: no pueden caerse nodos) mientras se está ejecutando la simulación.
Una vez que el algoritmo encuentra en la tabla de un nodo origen por dónde debe enviar los paquetes, mandará todos por la misma ruta.

### Posibles mejoras

Para mejorar el algoritmo se podría implementar la detección de caída de nodos y el cálculo de costo de los enlaces. Estaría bueno que sea consciente del costo de los enlaces en tiempo real, es decir que se vayan actualizando para que, si algún canal se congestiona, se pueda mandar paquetes por uno más eficiente. Y, sobretodo modificarlo para que funcione de manera óptima para cualquier topología de red.

## Referencias

- Kurose, J. F. & Ross, K. W. (2020). *Redes de Computadoras: Un Enfoque Descendente* (7a ed.). Pearson.
- Tanenbaum, A. S. & Wetherall, D. J. (2011). *Redes de Computadoras* (5a ed.). Pearson.

## Anexo: uso de inteligencias artificiales

Inteligencia utilizada: *ChatGPT 4o*

**Pregunta**: Cómo puedo hacer una tabla en formato md de este estilo: delay = 1 saltos = 2 enviados = 3 recibidos = 4

**Respuesta**: Para crear una tabla en formato Markdown (md) con los datos proporcionados, puedes organizar los valores en una estructura tabular. Aquí tienes un ejemplo de cómo puedes hacerlo:
| Parámetro  | Valor |
|------------|-------|
| delay      | 1     |
| saltos     | 2     |
| enviados   | 3     |
| recibidos  | 4     |

**Interpretación**: Sirvió el ejemplo que dió pero decidimos hacerla en formato horizontal.

Inteligencia utilizada: *ChatGPT 3.5*

**Pregunta**: nosotros en un proyecto tenemos un packet Packet { atributos } dentro de un  archivo Packet.msg. Mi idea es hacer otro .msg llamando helloPacket que herede de packet , como lo puedo hacer ?

**Respuesta**: En OMNeT++, puedes crear nuevos tipos de mensajes y paquetes utilizando archivos .msg. Estos archivos te permiten definir nuevas clases de mensajes y paquetes que heredan de otras clases. Para crear un paquete HelloPacket que herede de Packet, debes definir ambos paquetes en archivos .msg.

Aquí hay una guía paso a paso sobre cómo hacerlo:

Paso 1: Definir el archivo Packet.msg
Primero, define el archivo Packet.msg que contiene la definición base del paquete Packet.

```
// Packet.msg
cplusplus {{
#include <omnetpp.h>
}}

packet Packet {
    int srcAddr;
    int destAddr;
    // Otros atributos comunes
}
```

Paso 2: Definir el archivo HelloPacket.msg
Luego, define el archivo HelloPacket.msg que hereda de Packet.

```
// HelloPacket.msg
cplusplus {{
#include "Packet_m.h"  // Incluir el archivo generado por Packet.msg
}}

packet HelloPacket extends Packet {
    int helloAttr1;
    int helloAttr2;
    // Otros atributos específicos de HelloPacket
}
```

Paso 3: Compilar los archivos .msg
Para que OMNeT++ genere las clases correspondientes, asegúrate de compilar ambos archivos .msg utilizando el compilador de mensajes de OMNeT++. Esto generará los archivos .h y .cc necesarios para que puedas usarlos en tu código C++.

Paso 4: Usar los paquetes en tu código C++
Después de definir y compilar los archivos .msg, puedes usar las clases generadas en tu código C++.

```
#include "HelloPacket_m.h"

class Net : public cSimpleModule {
protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

Define_Module(Net);

void Net::initialize() {
    // Inicialización del módulo
}

void Net::handleMessage(cMessage *msg) {
    if (HelloPacket *helloPkt = dynamic_cast<HelloPacket *>(msg)) {
        // Procesar el paquete HelloPacket
        int src = helloPkt->getSrcAddr();
        int dest = helloPkt->getDestAddr();
        int attr1 = helloPkt->getHelloAttr1();
        int attr2 = helloPkt->getHelloAttr2();

        // Realizar operaciones con los atributos
        EV << "HelloPacket recibido: "
           << "src=" << src << ", dest=" << dest
           << ", attr1=" << attr1 << ", attr2=" << attr2 << endl;

        // Otras operaciones
        delete helloPkt;
    } else {
        // Procesar otros tipos de mensajes
        delete msg;
    }
}
```
Resumen
Definir el paquete base (Packet) en un archivo .msg.
Definir el paquete derivado (HelloPacket) en otro archivo .msg, utilizando la palabra clave extends para indicar la herencia.
Compilar los archivos .msg para generar las clases correspondientes.
Usar las clases generadas en tu código C++.
Este enfoque te permitirá crear jerarquías de paquetes en OMNeT++ y aprovechar la herencia para estructurar mejor tus tipos de mensajes y paquetes. Si necesitas más ayuda o tienes alguna otra pregunta, no dudes en preguntar.

**Interpretación**: no nos funcionó, al probarlo tiraba muchos errores (quizás por la compilación separada de los archivos). Logramos lo que queríamos definiendo los dos paquetes en el mismo archivo y usando *extends*.
