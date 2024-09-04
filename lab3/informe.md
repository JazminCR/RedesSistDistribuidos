# Análisis de flujo y congestión de redes utilizando simulación discreta

**Materia**: *Redes y Sistemas Distribuidos*.

**Laboratorio 3**: Transporte.

**Integrantes**: Acosta, Mateo Lucas & Caruso Rojo, Jazmín & Gallegos, Lucas Oscar.

[Video del laboratorio 3 - problemas, implementación de algoritmos y soluciones](https://drive.google.com/file/d/1RrTwHV-mekStIBDXzAUu9cxmJsSEnA4q/view?usp=sharing)

## Resumen

Este proyecto se enfoca en el análisis de una red de computadoras, utilizando el entorno OMNeT++ y la simulación discreta para modelar el comportamiento del sistema, considerando variables como la tasa de transferencia y la capacidad de los búferes. Durante el análisis, se identifican problemas de flujo de datos y de congestión de la red, y se muestran gráficas representativas de los mismos. Para abordar estos desafíos, se implementan algoritmos basados en la retroalimentación y utilización de paquetes de control para mantener un equilibrio entre la velocidad de transmisión y la capacidad de recepción.

## Introducción

Aquí podrás encontrar información sobre lo que trata nuestro proyecto, el modelo utilizado, los parámetros considerados, la configuración de los escenarios de prueba, las métricas y resultados obtenidos durante el análisis.

En las redes de computadoras, la capa de transporte desempeña un papel fundamental en la transferencia confiable y eficiente de datos. Sin embargo, surgen desafíos y problemas en el flujo de los mismos y la congestión de la red.
Los problemas de flujo se presentan cuando el emisor envía datos a una velocidad mucho más rápida de la que el receptor puede procesarlos. Esto puede llevar a la saturación del receptor, causando que la información se pierda o el sistema se vuelva inestable.
La congestión ocurre cuando la cantidad de datos transmitidos en una red supera la capacidad de manejo disponible, es decir que la red se satura y por lo tanto puede provocar retrasos, pérdida de paquetes e ineficiencia en la entrega de datos.

En la siguiente imagen se usa una analogía para representar estos problemas.

![Analogía](https://github.com/JazminCR/graficos_lab3/blob/main/analogia.png?raw=true)

La figura de la izquierda hace referencia a una red veloz que alimenta a un receptor de baja capacidad, es decir, hay un uso insuficiente de búfer en el receptor (problema de flujo).
Mientras que la figura de la derecha se refiere a una red lenta que alimenta a un receptor de alta capacidad, esto es una capacidad insuficiente en la red (congestión).

En este informe, explicaremos en detalle estos problemas, analizando sus causas, impacto y posibles soluciones en el contexto de la capa de transporte de las redes.

### Simulación discreta

Para abordar los problemas de flujo y congestión utilizaremos simulación discreta, una técnica que nos permite modelar y analizar el comportamiento de un sistema a lo largo del tiempo, evaluando cómo diferentes variables afectan su comportamiento y rendimiento.
En este tipo de simulación, el tiempo se divide en intervalos discretos, y los cambios en el sistema sólo se producen en estos momentos específicos.
El modelo del sistema se construye utilizando entidades discretas, como objetos o eventos, que interactúan entre sí a lo largo del tiempo. Cada entidad tiene su propio estado y comportamiento, y las interacciones entre ellas se modelan mediante reglas predefinidas. Una de las principales ventajas de la simulación discreta es su capacidad para representar sistemas complejos de una forma comprensible y manejable.

### Nuestro modelo

El modelo de sistema con el que trabajamos simula el flujo de datos a través de una red, desde la generación hasta la recepción de los mismos, pasando por una cola de espera y teniendo en cuenta la tasa de transferencia (velocidad a la que los datos pueden ser transmitidos), la demora de transmisión (tiempo que tarda un paquete en viajar desde el emisor hasta el receptor), y la memoria de búferes (espacio de almacenamiento temporal utilizado para mantener los datos que están siendo transferidos).

El sistema se compone de los siguientes módulos: 
- **NodeTx** (consta de los módulos simples Generator y Queue): simula el proceso de transmisión de datos desde el generador.
- **NodeRx** (consta de los módulos simples Sink y Queue): se encarga del proceso de recepción de datos desde la cola hasta su almacenamiento en sink.
- **Generator** (generador / emisor): produce datos en intervalos de tiempo definidos por *generationInterval* y de un tamaño especificado por *packetBySize*.
- **Queue** (cola): representa una etapa intermedia en el proceso de transferencia de datos, cuando los recibe de NodeTx los almacena temporalmente antes de que sean entregados a NodeRx. Tiene una capacidad definida por *bufferSize* y un tiempo de servicio especificado por *serviceTime*.
- **Sink** (sumidero / receptor): representa el destino final de los datos generados.

Estos módulos están conectados en una red llamada **Network** formando así el sistema completo de comunicación en la simulación.

![modelo sistema](https://github.com/JazminCR/graficos_lab3/blob/main/sistema.png?raw=true)

Vamos a analizar el impacto en el tráfico de red estableciendo como **límite máximo de la simulación** 200 segundos, y según los siguientes parámetros:
- **nodeTx.gen.generationInterval**: intervalo de tiempo exponencial en los que serán generados los paquetes. El valor irá variando entre 0,1 y 1.
- **nodeTx.gen.packetByteSize**: tamaño de paquetes en Bytes. Lo dejaremos fijo en 12500 B.
- **queue.bufferSize**: tamaño del búfer de la queue. Lo configuramos con un valor de 200 paquetes.
- **nodeTx.queue.bufferSize**: tamaño del búfer de la cola del nodo transmisor. Lo fijamos en 2000000 paquetes (valor alto).
- **nodeRx.queue.bufferSize**: tamaño del búfer de la cola del nodo receptor. También lo configuramos en 200 paquetes.

Además, como nombramos anteriormente, configuramos las conexiones con tasas (datarate) y demoras (delay) de transmisión, obteniendo así los siguientes casos de estudio:

**Caso número 1**:

La tasa de transmisión desde NodeTx hasta Queue es de 1 Mbps y la demora es de 100 us.

La tasa de transmisión desde Queue hasta NodeRx es de 1 Mbps y la demora es de 100 us.

La tasa de transmisión desde Queue hasta Sink es de 0,5 Mbps.

**Caso número 2**:

La tasa de transmisión desde NodeTx hasta Queue es de 1 Mbps y la demora es de 100 us.

La tasa de transmisión desde Queue hasta NodeRx es de 0.5 Mbps y la demora es de 100 us.

La tasa de transmisión desde Queue hasta Sink es de 1 Mbps.

### Análisis y gráficos
Para realizar el análisis, corrimos simulaciones paramétricas para cada caso de estudio, variando el intervalo de generación de paquetes, y generamos gráficas representativas de la utilización de cada una de las 3 queue (búferes) para los casos planteados.

__Cálculos a tener en cuenta para comprender el análisis:__

Paquetes de 12500 B = 100.000 b

Si la tasa de transmisión es de 1 Mbps, quiere decir que puede transmitir 1.000.000 b por segundo

Si la tasa de transmisión es de 0,5 Mbps, quiere decir que puede transmitir 500.000 b por segundo

Si el intervalo de generación es exp(0,1) quiere decir que aproximadamente se genera un paquete cada 0,1 seg.

El generador tiene la capacidad de enviar 1 Mbps, entonces por segundo puede enviar de a 10 paquetes aprox. (1 Mbps)

#### Gráficos del caso 1:

![intervalo 0.1](https://github.com/JazminCR/graficos_lab3/blob/main/c1_i01.png?raw=true)

![intervalo 0.1](https://github.com/JazminCR/graficos_lab3/blob/main/c1_i02.png?raw=true)

![intervalo 0.1](https://github.com/JazminCR/graficos_lab3/blob/main/c1_i07.png?raw=true)


#### Gráficos del caso 2:

![intervalo 0.1](https://github.com/JazminCR/graficos_lab3/blob/main/c2_i01.png?raw=true)

![intervalo 0.1](https://github.com/JazminCR/graficos_lab3/blob/main/c2_i02.png?raw=true)

![intervalo 0.1](https://github.com/JazminCR/graficos_lab3/blob/main/c2_i07.png?raw=true)

#### Gráficos de paquetes enviados y recibidos:

Además, obtuvimos los siguientes datos para cada simulación:
- (gen)**packetGen**: número total de paquetes generados (y enviados).
- (queue)**packetDrop**: número total de paquetes que fueron descartados debido a que se excedió la capacidad del búfer.
- (sink)**packetUsed**: número total de paquetes que han sido procesados.

Los gráficos a continuación valen para ambos casos.

![int 0.1](https://github.com/JazminCR/graficos_lab3/blob/main/i01_paq.png?raw=true) 
![int 0.2](https://github.com/JazminCR/graficos_lab3/blob/main/i02_paq.png?raw=true) 
![int 0.3](https://github.com/JazminCR/graficos_lab3/blob/main/i07_paq.png?raw=true)

El primer gráfico se obtiene cuando el intervalo de generación es exp(0.1) y nos da los siguientes valores:
- packetGen = 1979
- packetDrop = 770
- packetUsed = 998

El segundo gráfico corresponde al intervalo exp(0.2)
- packetGen = 989
- packetDrop = 0
- packetUsed = 976

Por último, el tercer gráfico hace referencia al intervalo exp(0.7):
- packetGen = 285
- packetDrop = 0
- packetUsed = 285

### Análisis de la ocupación de búferes en el sistema según los gráficos:

Al ver las gráficas de ambos casos, puede que parezcan muy similares, pero tienen una diferencia fundamental.
Primero, vamos a notar que comparten el gráfico del búfer del generador, esto se debe a que en ambos casos, el canal emisor-cola tiene una tasa de transferencia de 1 Mbps.
Ahora viene lo interesante, el gráfico del búfer de la queue en el caso 1 es igual al del búfer del receptor en el caso 2, mientras que el gráfico del búfer del receptor en el caso 1 es igual al del búfer de la queue en el caso 2.

¿Qué está ocurriendo? Es aquí la principal diferencia.

En el caso 1, la queue puede enviar 1 Mbps, pero sink puede recibir 0,5 Mbps. Nos encontramos en el caso en que un emisor rápido alimenta a un receptor lento.

En el caso 2, la queue puede enviar 0,5 Mbps, y sink puede recibir 1 Mbps. Este es el caso en que una red de baja capacidad alimenta a un receptor de gran capacidad.

#### Análisis de los gráficos del caso 1

Podemos notar que sin importar el intervalo que sea, el búfer de la queue se mantiene constante en 1, esto se debe a que tiene la capacidad de recibir 1 Mbps y de enviar 1 Mbps, entonces recibe y entrega sucesivamente.

Para simplificar la comprensión, omitiremos el delay en esta explicación.
Si el intervalo es exp(0,1) dijimos que el generador puede enviar como máximo 10 paquetes por segundo aproximadamente. Pero sink puede recibir de a 0,5 Mbps, es decir de a 5 paquetes por segundo. 
Es aquí donde el búfer de sink comienza a guardar los paquetes que le envían pero que todavía no puede procesar. Este búfer tiene una capacidad de 200 paquetes, es decir que cuando llegue a esa cantidad va a saturarse y no va a poder seguir guardando paquetes.
Tal como se muestra en el gráfico, se generan y reciben paquetes, pero cuando llega a los 40 segundos aproximadamente el búfer se satura conteniendo 200 paquetes, entonces, hasta este momento, se enviaron 400 paquetes y se recibieron 200. En los próximos 160 segundos, se envían 1600 paquetes pero sólo se reciben 5 paquetes por segundo, o sea 800 en total. Esto nos muestra que de los 2000 paquetes enviados, sólo se recibieron 1000.
Estos son valores aproximados ya que no se está teniendo en cuenta el tiempo de delay, y además no podemos asegurarlo con exactitud.

Este caso simboliza la situación de una red con un receptor lento, provocando pérdida de paquetes y resultando en un problema de control de flujo. Debido a que el nodo intermedio no genera un retardo de procesamiento importante y no se generan cuellos de botella en los canales, los datos pasan casi sin problema, pero al llegar a la cola (búfer) del receptor se reciben de a 0.5 Mbps, lo cual genera pérdida de paquetes si llega una cantidad mayor de datos (debido a las tasas más altas de los nodos anteriores). 

#### Análisis de los gráficos del caso 2

Aquí el búfer que se mantiene constante es el del receptor, ya que tiene la capacidad de recibir 1 Mbps y ésta es la máxima tasa con la que cuenta el sistema.

Nuevamente omitiremos el delay en la explicación.
Como en el caso anterior, si el intervalo de generación es exp(0,1) el generador enviará de a 10 paquetes por segundo, pero en este caso, la queue puede enviar de a 0,5 Mbps, es decir que recibe 10, envía 5 y a los otros 5 los debe almacenar en su búfer, el mismo tiene como tamaño máximo 200 paquetes y, cuando llegue a esa cantidad se saturará. Nuevamente, esto produce la gran pérdida de paquetes. El receptor tiene alta capacidad y por lo tanto puede recibir los paquetes sin problema.
Para interpretar los gráficos podemos notar un comportamiento similar al del primer caso. Se envían y reciben paquetes hasta que en el segundo 40, el búfer del nodo intermedio se satura con 200 paquetes. A partir de aquí, el generador seguirá enviando de a 10 paquetes (1600 en total) pero la queue sólo enviará 5 (800 en total), hasta que se cumplan los 200 segundos que dura el sistema.
Entonces nuevamente se generan 2000 paquetes pero se reciben 1000.
Como dijimos anteriormente, estos son valores aproximados.

Podemos decir entonces que en este caso, el nodo intermedio se va a encontrar saturado en cantidad de paquetes (que no puede mandar), y el receptor constante en 1. 
Esto se produce debido a que ahora tenemos un cuello de botella en el canal cola-receptor de la red que cuenta con una capacidad de 0,5 Mbps mientras que los otros canales son de 1Mbps. Por lo tanto, estamos en una situación donde el nodo emisor y el receptor son rápidos, pero el nodo intermedio es más lento, simbolizando así un problema de congestión en la red. 

#### Ambos casos

Si aumentamos el tiempo de generación de paquetes, es decir, tomamos un intervalo de exp(k) con k >= 0,2 el generador producirá, como mucho, paquetes cada 0,2 seg, es decir 5 paquetes por segundo.
Entonces, si el generador envía 0,5 Mbps ya no nos encontramos con los problemas anteriores debido a que, en el caso 1, la cola recibe los 5 paquetes y los envía a sink que ahora es capaz de recibirlos ya que cuenta con esa capacidad, por lo que a partir de aquí su búfer ya no se saturará. Y en el caso 2, la cola recibe los paquetes y puede enviarlos sin tener la necesidad de almacenarlos, por lo tanto su búfer tampoco se saturará.
Si ocurre pérdida de paquetes es mínima y ya no se debe a la saturación de los búferes.

Como conclusión, podemos decir que, en el primer caso se satura el receptor (por ser lento) y se debe a un problema de control de flujo, mientras que en el segundo caso se satura la red y se debe a un problema de congestión (específicamente por la tasa de un enlace).

**¿Cuál es la fuente limitante en cada uno?**

La fuente limitante en el caso 1 es el receptor. Si el emisor no envía más datos de los que el receptor puede procesar, entonces no se perderán datos.
En el caso 2, el factor limitante es la capacidad de transporte interno de la red. Si entran muchos datos con demasiada rapidez, ésta se congestionará y se degradará el desempeño a medida que se retrasen y pierdan paquetes.

## Métodos

En esta sección describiremos los métodos y algoritmos utilizados para abordar los problemas de flujo de datos y congestión de la red mencionados anteriormente.

### Modificación del modelo

Primero modificamos nuestro modelo de simulación. Añadimos un canal de retorno desde el nodeRx al nodeTx para que el receptor pueda acusar información que regule la tasa de transmisión (feedback).

Los problemas son resueltos por separado, pero con un algoritmo similar, en el sentido de que ambos se encargan de enviar mensajes de control al emisor desde el receptor advirtiendo del estado de los búferes. Por lo tanto, la topología de la red es idéntica en ambos escenarios.

Módulos agregados:
- **nodeTx** se compone de los módulos simples TransportTx y Sink
- **nodeRx** se compone de los módulos simples TransportRx y Sink
- **transportTx**: se encarga de manejar los dos distintos tipos de paquetes que recibe, ellos son: los producidos por el generador (data packet) y los feedback enviados por el receptor, y consta de una conexión con una queue intermedia.
- **transportRx**: se encarga de manejar los dos tipos de mensajes que le llegan, los data packet y los feedbacks que recibe de la queue intermedia, y garantiza una gestión adecuada de los mismos.

![modelo sistema2](https://github.com/JazminCR/graficos_lab3/blob/main/sistema2.png?raw=true)

Contamos con el archivo **FeedbackPkt.msg** que conta de un booleano que nos indica si debemos retrasar la transmisión de los paquetes. 

### Implementación de algoritmos

La idea del algoritmo que implementamos para solucionar el **problema del flujo de datos** se basa en enviar constantemente paquetes de control (feedback) al nodo emisor notificando el estado del búfer receptor. Definimos un umbral que representa el límite máximo de paquetes que el búfer puede contener, y un delay para el emisor (explicado con detalles más adelante). Después de realizar varias pruebas, encontramos que los valores óptimos para estos parámetros son, un umbral del 90% de la capacidad del búfer, y un delay de 0.2 segundos.
Establecimos que, si la cantidad de paquetes en el búfer receptor se encuentra por debajo del umbral fijado, el receptor envía regularmente paquetes de control al emisor para indicar que la recepción y procesamiento de datos están dentro de los límites esperados. En este caso, el emisor no introduce ninguna demora adicional en la planificación de envío de paquetes.
Por el contrario, si la cantidad de paquetes en el búfer receptor supera el umbral, el receptor envía un paquete al emisor advirtiendo de la situación. Como respuesta, el emisor introduce una demora en el próximo paquete que mande.
De esta forma, hasta que el búfer receptor no se vacíe lo suficiente (menos que el umbral), se mandará el mismo paquete de control y el emisor seguirá enviando los paquetes con la demora extra, dándole así más tiempo al receptor lento.

Para el **problema de la congestión**, en el cual no tenemos un receptor de baja capacidad sino un canal de red lento, el algoritmo hace lo mismo, con la diferencia de que el paquete de control se genera en el nodo intermedio encargado de enviar paquetes por ese canal. El nodo es el encargado de retransmitir los paquetes generados por el emisor y crear/enviar paquetes de control al nodo receptor, este último obtiene los datos para procesar, y manda el paquete de control hacia el emisor informando sobre la situación actual de congestión. Por lo tanto, en este caso es también el receptor el encargado de comunicarse con el emisor para advertirle sobre el estado del búfer. Luego el algoritmo continúa igual, es decir, el emisor introduce una demora en caso que sea necesario. Para este algoritmo, inicialmente, consideramos un umbral aleatorio del 50%, es decir, pensamos que el búfer debería detenerse cuando alcanzara la mitad de su capacidad total. Al realizar las pruebas, vimos que con este valor ocurría una pérdida mínima de paquetes, y pudimos concluir que un umbral óptimo es del 46% ya que de esta forma no hay pérdida de datos.

El **delay** es la demora adicional introducida por el emisor en la planificación de envío de paquetes, como dijimos, se implementa como una medida de control ante esas situaciones. En ambos algoritmos, lo establecimos con un valor de 0.2 segundos porque, luego de un análisis detallado del comportamiento del sistema, encontramos que permitía un buen funcionamiento sin ralentizar excesivamente la transmisión de datos.

## Resultados

Debido a que los problemas de flujo y congestión se dieron cuando el intervalo de generación de paquetes era exponencial(0.1), los gráficos obtenidos con la implementación de estos algoritmos son también en ese intervalo, así de esta manera podemos apreciar el funcionamiento de los mismos.

### Solución del flujo de datos

En el primer análisis (en la introducción), vimos que ocurría un problema de flujo debido a que un emisor rápido le enviaba muchos paquetes a un receptor lento, y que a causa de esto el búfer del último se saturaba.

![flujo](https://github.com/JazminCR/graficos_lab3/blob/main/flujo_delay02.png?raw=true)

Ampliación del gráfico del búfer receptor (que es por el cual estamos interesados):

![receptor](https://github.com/JazminCR/graficos_lab3/blob/main/flujo_d02_receptor.png?raw=true)

Ahora,  el gráfico que representa al búfer del receptor aumenta linealmente y luego hace montañitas muy pequeñas. Esto es debido a que, una vez que la capacidad del búfer pasa el umbral de 90, el receptor genera un paquete de control (feedback) y llega casi al instante al emisor, puesto que se envía por un canal (que le pusimos una velocidad de 1Mbps para fines prácticos pues no nos interesa realmente esta parte de la red en este proyecto) distinto al de cualquier paquete de datos. Una vez que le llega al emisor, éste retrasa el envío de paquetes de datos con un delay de 0.2, pero una vez que se envían los datos también llegan casi instantáneamente al receptor puesto que los canales intermedios de la red no corren riesgo de saturación puesto que ambos transportan a 1Mbps. Esto provoca que no sea tanto el tiempo que se deja al receptor para vaciar su búfer hasta que llega un nuevo paquete, por lo que probablemente para cuando llegue un nuevo paquete, el receptor haya terminado de procesar solo unos pocos y volverá a sobrepasar el umbral, lo que produce estas montañitas de alturas muy pequeñas. De esta manera, es posible controlar que el búfer del receptor no sobrepase su capacidad.

![flujo_pkt](https://github.com/JazminCR/graficos_lab3/blob/main/flujo_pkt.png?raw=true)

Como se mencionó anteriormente, si el emisor no envía más datos de los que el receptor puede procesar, entonces no se perderán datos. Y es lo que podemos observar en este gráfico, si bien el emisor genera la misma cantidad de paquetes (aprox. 2000) que en el análisis anterior, ahora envía menos (aprox. 1000) para evitar sobrecargar al receptor, y de esta manera se recibe casi la totalidad de paquetes enviados.

### Solución de la congestión de la red

El problema que teníamos era que, si entraban muchos datos con demasiada rapidez, la red se congestionaba (saturación del búfer) y se perdían paquetes.

![cong](https://github.com/JazminCR/graficos_lab3/blob/main/cong_delay02.png?raw=true)

Ampliación del gráfico del búfer del nodo intermedio:

![queue](https://github.com/JazminCR/graficos_lab3/blob/main/cong_d02_queue.png?raw=true)

Gracias a los gráficos presentados, podemos observar que esto ya no ocurre con la implementación del algoritmo. La queue0 recibe paquetes en forma lineal hasta llegar a cierto punto en donde comienza a bajar y entonces luego tiene lugar para volver a subir, y así sucesivamente, de esta manera el búfer no llega a saturarse. Esto se debe a que, cuando el búfer de la queue llega al umbral, en el tiempo que transcurre a partir desde que se crea el paquete de control y se inserta en búfer junto con los paquetes de datos, se planifican ambos envíos y se mandan a través de los canales necesarios con sus respectivas velocidades de transferencia, se siguen generando y enviando paquetes a la misma velocidad hasta que llegue la petición (al emisor) de que suceda lo contrario. Esto es lo que provoca que en el gráfico suba bastante. Una vez que el paquete de control llega al emisor es cuando empieza a disminuir la velocidad en que manda los paquetes, justificando la bajada del búfer queue, ya que en el tiempo que se atrasa la planificación de envío de paquetes el nodo intermedio sigue mandando (por lo tanto vaciando el búfer). Luego cuando el búfer se descongestiona y el emisor recibe un feedback de ésto, vuelve a transmitir paquetes a la velocidad original.

![cong_pkt](https://github.com/JazminCR/graficos_lab3/blob/main/cong_pkt.png?raw=true)

En este caso, también se controla la cantidad de paquetes que se envían a la red para evitar la saturación de la misma. Podemos notar que esto es efectivo ya que antes se recibían casi 1000 paquetes de 2000 enviados, y ahora casi 1000 de 1000 enviados.

### Ambos casos

El comportamiento del emisor se podría explicar de la siguiente manera, en nuestro algoritmo, al principio se comporta como en la primera parte del análisis ya que no sucede que algún búfer se sature. Cuando este hecho ocurre el emisor retrasa la velocidad en la que envía paquetes (pero el generador sigue creando e introduciendolos en el búfer), por lo tanto, la cantidad de paquetes en el búfer emisor aumenta. También se pueden ver momentos en que la cantidad de paquetes se mantiene lineal (parece constante), esto se refiere al hecho en que el emisor vuelve a la normalidad al recibir un feedback con el valor false (es decir, que no hay saturación de búfer) y  por lo tanto se comporta como al principio.

En el caso 1, a diferencia del caso 2, el gráfico del búfer emisor tiene menos fluctuaciones. Esto se debe a que, aunque ambos tengan el mismo delay en el emisor para tratar la pérdida, para controlar el flujo, el umbral en el receptor es del 90% de la capacidad del búfer, lo que genera que la cantidad de veces donde el emisor retrasa su velocidad de transmisión sea menor. En cambio, para controlar la congestión, el umbral en el nodo intermedio es del 46% de la capacidad de ese búfer, y en este caso la cantidad de veces que el emisor debe retrasar el envío es mayor.

**¿El algoritmo funciona por igual para el caso de estudio 1 y 2?**

No, esto no sucede. Si bien la idea en la que se basa el algoritmo es la misma, la implementación para cada caso genera consecuencias distintas. Para tratar el flujo de datos, el nodo encargado de generar los paquetes de control es el receptor. Como en este caso el problema se presenta por el receptor lento, el único canal lento por donde pasan los paquetes es el interno que conecta Rx con Sink. En otras palabras, cuando Rx genera los paquetes de control y los envía, lo hace por los canales que no son de interés para este caso, por lo que llegan muy rápido al emisor.
En cambio, para el problema de la congestión, los paquetes de control son generados por el nodo intermedio debido a la conexión lenta entre él y el receptor. Esto hace que sea más difícil la elección del valor de los parámetros umbral y delay, y la planificación de un evento de envío de feedback por el mismo canal que pasan los datos. Lo primero se debe a que si ponemos un umbral suficientemente alto, independientemente del delay, habrá pérdida de paquetes ya que cuando la capacidad del búfer supere el umbral y envíe tanto feedbacks como datos por el mismo canal se producirá más congestión, por lo que los paquetes de control tardarán más en llegar al receptor encargado de enviarlos al receptor. Esto genera un retraso de los paquetes de control importante y suficiente para, que en ese tiempo, se sigan mandando datos desde el emisor al nodo intermedio a la velocidad inicial (sin delay), acumulándose así en el búfer junto a los feedbacks guardados (provocando que el búfer se sature rápido), y probablemente, para cuando el receptor empiece a mandar con demora ya sea tarde. El segundo punto es porque mandamos por un mismo canal paquetes de datos junto con paquetes de control, por lo que tenemos más bytes a enviar por un canal lento, a causa de esto tuvimos que ver cómo diferenciar los eventos de envío de cada tipo de paquete.

Entonces, a pesar de que la idea de ambos algoritmos es la misma, las cuestiones nombradas arriba nos llevaron a pensar la implementación por caminos diferentes.

En conclusión, podemos decir que a los problemas con los que nos encontramos en la primera parte del análisis, pudimos solucionarlos gracias a la implementación de algoritmos que gestionan la cantidad de paquetes enviados (con el costo de no enviar casi el 50% de los datos), entre otras cosas, impidiendo la saturación de los búferes y la pérdida de paquetes a causa de ello.

## Gráficos complementarios

Presentamos los gráficos de carga ofrecida (lo que se transmite) vs carga útil (lo que llega a destino), y del retardo promedio de paquetes en la simulación.

### Tarea 1, caso 1:

![11](https://github.com/JazminCR/graficos_lab3/blob/main/flujo_tarea1.png?raw=true)

### Tarea 1, caso 2:

![11](https://github.com/JazminCR/graficos_lab3/blob/main/cong_tarea1.png?raw=true)



### Tarea 2, caso 1:

![11](https://github.com/JazminCR/graficos_lab3/blob/main/flujo_tarea2.png?raw=true)

### Tarea 2, caso 2:

![11](https://github.com/JazminCR/graficos_lab3/blob/main/cong_tarea2.png?raw=true)

## Discusiones

### Logros

- **Utilización eficaz de herramientas de simulación y visualización**: utilizamos OMNeT++ para simular el comportamiento de la red y obtener estadísticas, para analizarlas usamos la biblioteca Matplotlib de Python que nos permitió crear gráficos claros y concisos.
- **Optimización del rendimiento de la red**: implementar algoritmos para resolver problemas de flujo y de congestión.
- **Reducción de la pérdida de datos**: debido a que se solucionaron los problemas.

### Limitaciones

Una de las principales limitaciones con la que cuenta este proyecto, es que los modelos de OMNeT++ son simplificaciones de los sistemas reales, es decir que se ignoran detalles de hardware o software, como el daño de nodos o las tasas de transmisión variantes, y también factores ambientales, etc.

La limitación primordial de nuestro algoritmo es la selección aleatoria de los parámetros de retraso para el emisor, y del umbral para los búferes. Nosotros pudimos elegirlos en función a este contexto de red específico.
Sin embargo, al considerar la aplicación del algoritmo en escenarios con diferentes velocidades de transferencia, se hace evidente la necesidad de ajustar estos parámetros para adaptarlos a cada situación.

### Posibles mejoras

Una posible mejora del algoritmo podría ser, en lugar de fijar los valores del umbral y del delay, incorporar un sistema que monitoree continuamente el estado de la red y que ajuste estos parámetros de manera dinámica en función de las condiciones actuales. Por ejemplo, utilizar algoritmos de control adaptativo para calcular el umbral óptimo y la demora adecuada en tiempo real en respuesta a los cambios en la congestión de la red y la velocidad de transferencia.

## Referencias

- Kurose, J. F. & Ross, K. W. (2020). *Redes de Computadoras: Un Enfoque Descendente* (7a ed.). Pearson.
- Tanenbaum, A. S. & Wetherall, D. J. (2011). *Redes de Computadoras* (5a ed.). Pearson.
- *OMNeT++ Simulation Manual* (v. 6.0.3). Recuperado de [documentación](https://doc.omnetpp.org/omnetpp/manual/).

## Anexo: uso de inteligencias artificiales

Inteligencia utilizada: *ChatGPT 3.5*

**Pregunta**: Estamos haciendo un laboratorio con omnet++ en la facultad para simular una red simple de un emisor, una queue intermedia y un receptor. Nos encontramos con la situacion en la que se genera perdida de paquetes por culpa de un receptor lento. Cuestion que tenemos que hacer un informe explicando la situacion del caso con distintos intervalos de tiempo de generacion de paquetes, es decir, el emisor con un intervalo de generacion de distribucion exponencial alrededor de una media. En omnet++, esto lo teney el resultado fue óptimo.mos asi en el archivo .ini :

Network.NodeTx.gen.generationInterval = exponential(0.1) 

Esto es un caso, luego volvemos a experimentar igual pero subiendo esta media de a 0.1 (de a 100ms), osea :

Network.NodeTx.gen.generationInterval = exponential(0.2)

Network.NodeTx.gen.generationInterval = exponential(0.3)
......

y así hasta llegar a 1s. Lo que sucede, es que en el unico caso en el que se pierden paquetes es cuando el intervalo es Network.NodeTx.gen.generationInterval = exponential(0.1), y estoy tratando de explicar por que puede ser. Lo que se me ocurrio, es que justo en ese caso como la distribucion exponencial esta alrededor de 100ms es más probable que se envien 10 paquetes (o más de 5 seguro), puesto que los canales del emisor a la queue y de la queue al receptor son iguales de 1Mbps y los paquetes son de 12500 bytes, y el receptor procesa a 0.5Mbps. Siguiendo esta lógica, se me ocurrió que al tener distribuciones exponenciales alrededor de 200ms en adelante, ya se aleja lo suficiente de 100ms reduciendo bastante la probabilidad a que en algun momento el intervalo de generacion sea de 100ms, por lo que casi nunca se perderían paquetes. Esto tiene sentido? 

**Respuesta**: Sí, tiene sentido lo que estás planteando. La distribución exponencial se caracteriza por tener una tasa constante de eventos en el tiempo, donde la media (o tasa) de la distribución determina la frecuencia promedio de los eventos. En tu caso, estás utilizando una distribución exponencial con un parámetro de 0.1 para representar un intervalo de generación de paquetes alrededor de 100ms.
Cuando el intervalo de generación es muy corto (alrededor de 100ms en tu caso), es más probable que se generen múltiples paquetes antes de que el receptor pueda procesarlos completamente. Aquí hay algunos puntos para considerar:
Tasa de Generación vs. Tasa de Procesamiento: Si la tasa promedio de generación de paquetes (determinada por el parámetro de la distribución exponencial) es más rápida que la tasa de procesamiento del receptor, es probable que se acumulen paquetes en la cola intermedia (queue). Cuando la cola alcanza su capacidad máxima, es posible que ocurran descartes o pérdida de paquetes debido a un overflow.
Probabilidad de Colisión: Si el emisor está generando paquetes a una velocidad alta y estos llegan a la cola intermedia más rápido de lo que el receptor puede procesarlos, es más probable que se produzcan colisiones o pérdida de paquetes. Los paquetes que llegan mientras la cola está llena pueden ser descartados.
Impacto de la Distribución Exponencial: A medida que incrementas el parámetro de la distribución exponencial (por ejemplo, 0.2, 0.3, etc.), la media del intervalo de generación se hace más larga, lo que ralentiza la tasa de generación de paquetes. Esto reduce la probabilidad de que múltiples paquetes lleguen simultáneamente, reduciendo así el riesgo de pérdida de paquetes debido a sobrecarga en la cola o en el receptor.
En resumen, cuando el intervalo de generación es muy corto (alrededor de 100ms), es más probable que se sature la cola intermedia y se produzca pérdida de paquetes debido a la alta tasa de llegada de paquetes. A medida que aumentas el intervalo de generación, la probabilidad de saturación y pérdida de paquetes disminuye, ya que la tasa de generación se ajusta a una tasa más manejable para el receptor. Este análisis es consistente con la relación entre la tasa de generación, la capacidad de la cola y la velocidad de procesamiento del receptor en tu simulación.

**Interpretación**: Para los casos de las preguntas sobre los errores en la ejecución del programa o sobre implementación de código, probamos hacer lo que nos dice directamente porque en general si no funciona no sucede nada malo, solo no funciona (en el caso de que funcione tratamos de entender porqué y si es necesario, le preguntamos sobre esa respuesta). Para los casos sobre entendimiento de código depende de la pregunta en sí. En el caso del ejemplo de arriba, la respuesta tiene muchas similitudes con el planteo en la pregunta, ya que confirma que tiene sentido el texto y quizás lo explica más técnicamente o con otros detalles agregados. De todas formas, luego de haber recibido esto, investigamos un poco más en otras fuentes, por ejemplo, sobre qué es una distribución exponencial, su fórmula y el gráfico, como para sumar más claridad desde otro lado. Esto lo repetimos en general también para otros tipos de pregunta, y siempre que sospechamos de alguna manera de la respuesta que nos da, buscamos complementar desde otro lugar.

**Pregunta**: Estamos escribiendo un informe ciéntifico para la materia redes y sistemas distribuidos, necesito saber dos cosas: primero, cómo añadir una imagen a un archivo.md, y luego, cómo citar libros (por ejemplo: Redes de Computadoras de Tanenbaum) en la sección referencias.

**Respuesta**: Para añadir una imagen a un archivo Markdown (.md), simplemente necesitas usar la sintaxis adecuada. Aquí te muestro cómo hacerlo:

```markdown
![Texto alternativo](ruta/a/la/imagen.jpg)
```

En esta sintaxis:

- `Texto alternativo` es el texto que se mostrará si la imagen no se puede cargar.
- `ruta/a/la/imagen.jpg` es la ruta o URL de la imagen que deseas añadir.

Por ejemplo:

```markdown
![Logo de la Universidad](https://ejemplo.com/logo.png)
```

En cuanto a las citas de libros en la sección de referencias, puedes seguir el formato que te mencioné anteriormente. Aquí te doy un ejemplo:

```markdown
Tanenbaum, A. S., & Wetherall, D. J. (2011). *Redes de Computadoras* (5a ed.). Pearson Educación.
```

Simplemente lista todas tus referencias de libros al final de tu informe bajo una sección titulada "Referencias" o "Bibliografía", y utiliza el mismo formato para cada una de ellas.

**Interpretación**: probamos si era correcta la respuesta, es decir, si funcionaba y cumplía con lo que necesitábamos. Si lo hizo, así que nos fue útil usar la información que nos brindó.

**Pregunta**: Si la cantidad de paquetes que se encuentran en el buffer  aún no sobrepasa el umbral, se mandan paquetes de control desde el receptor de que está todo bien, y el emisor no agrega una demora a la planificación de envío de paquetes. De lo contrario, el paquete de control que mandará el receptor advertirá de la situación al emisor, provocando que tenga que agregar una demora al próximo paquete que mande. De esta forma, hasta que el buffer receptor no se vacíe lo suficiente (menor que el umbral), se mandará el mismo paquete de control y el emisor seguirá mandando los paquetes con una demora extra, dando más tiempo al receptor lento (problema de control de flujo). 

Puedes redactar esto de forma más clara y formal para un informe?

**Respuesta**: Por supuesto, aquí tienes una redacción más formal y adecuada para un informe:

En el contexto del sistema de comunicación propuesto, se ha implementado un mecanismo de control de flujo basado en la retroalimentación del receptor al emisor. Este mecanismo se activa cuando la cantidad de paquetes en el búfer receptor alcanza un umbral predeterminado del 90% de su capacidad total.
Cuando la cantidad de paquetes en el búfer receptor se encuentra por debajo del umbral establecido, el receptor envía regularmente paquetes de control al emisor para indicar que la recepción y procesamiento de datos están dentro de los límites esperados. En esta situación, el emisor no introduce ninguna demora adicional en la planificación de envío de paquetes.
Por el contrario, si la cantidad de paquetes en el búfer receptor supera el umbral del 90%, el receptor envía un paquete de control al emisor para alertarlo sobre la congestión potencial. Como respuesta, el emisor introduce una demora adicional en el próximo paquete que envía, lo que ralentiza ligeramente la tasa de transmisión. Esta demora adicional proporciona al receptor más tiempo para procesar los paquetes entrantes y evitar la congestión en el búfer.
Este proceso continúa iterativamente hasta que la cantidad de paquetes en el búfer receptor disminuye por debajo del umbral del 90%. Durante este período, el receptor sigue enviando regularmente el mismo paquete de control al emisor, y el emisor continúa introduciendo demoras adicionales en el envío de paquetes, asegurando así un flujo de datos controlado y eficiente.
En resumen, este enfoque de control de flujo basado en la retroalimentación receptor-emisor permite una gestión óptima de la congestión en el búfer receptor, garantizando una transmisión de datos fluida y eficiente en el sistema de comunicación.

**Interpretación**: la respuesta es quizás demasiado formal y expandida, pero nos sirvió para sacar ideas que se entiendan mejor, y hacer un uso adecuado y no repetitivo de palabras.
