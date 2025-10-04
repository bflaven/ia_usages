# Ollama configuration
OLLAMA_URL = "http://localhost:11434"  # Default Ollama URL
MODEL_NAME = "mistral:7b"              # Model name in Ollama
# MODEL_NAME = "mistral:latest"  
# MODEL_NAME = "phi3.5:3.8b"  
# MODEL_NAME = "neoali/gemma3-8k:4b"  
# MODEL_NAME = "deepseek-r1:latest"
# MODEL_NAME = "embeddinggemma:latest"
# MODEL_NAME = "gemma3:1b"
# MODEL_NAME = "gemma3n:latest"
# MODEL_NAME = "phi3:14b"
# MODEL_NAME = "life4living/ChatGPT:latest"

# Request configuration
STREAM = False  # Set to True for streaming responses

# Language-based CMS categories
FR_cms_section_keywords_list = """Sports, Économie / Technologie, Culture, Environnement, France, Europe, Afrique, Amériques, Asie-Pacifique, Moyen-Orient"""
ES_cms_section_keywords_list = """América Latina, EE.UU. y Canadá, Europa, Francia, Asia-Pacífico, Medio Oriente, África, Medio Ambiente, Cultura, Economía, Ciencia y Tecnologías, Deportes"""
EN_cms_section_keywords_list = """France, Africa, Middle East, Americas, Europe, Asia-Pacific, Environment, Business / Tech, Sport, Culture"""

lang = "espagnol"

match lang:
    case "français":
        cms_section_keywords_list = FR_cms_section_keywords_list
    case "espagnol":
        cms_section_keywords_list = ES_cms_section_keywords_list
    case "anglais":
        cms_section_keywords_list = EN_cms_section_keywords_list
    case _:
        cms_section_keywords_list = FR_cms_section_keywords_list

prompt_template = """En vous inspirant des exemples de titres suivants et en adoptant le profil d'un journaliste expérimenté spécialisé dans l'actualité internationale, générez un objet JSON valide strictement conforme aux spécifications ci-dessous à partir du {{content}} fourni par l'utilisateur. Le journaliste est un professionnel rigoureux, doté d'un sens aigu de l'éthique et d'une grande curiosité pour les affaires mondiales. Il est connu pour sa capacité à rendre accessibles des sujets complexes, tout en respectant les nuances culturelles et politiques. Aucune balise de code ou formatage supplémentaire n'est autorisée. La sortie doit être un objet JSON strict pouvant être consommé directement par une API, sans texte explicatif, sans balises ou tout autre format additionnel.

Lorsque le contenu aborde plusieurs thématiques, choisissez celle qui est le plus largement développée dans le contenu figurant dans {{content}}. Développez une problématique sur cette thématique principale, puis citez plus rapidement les autres sujets ou les thématiques secondaires en les distinguant bien de la première thématique.

Exemples de titres :
1. Japon : le combat des pères pour la garde partagée
2. Le successeur du Dalaï-lama sera désigné après sa mort, la Chine veut approuver son nom
3. Ibn Battuta, l'explorateur marocain qui "fait passer Marco Polo pour un flemmard"
4. DJ Snake et Omar Sy dévoilent "Patience", l'épopée "universelle" d'un jeune exilé sénégalais
5. Trump a-t-il raison de dire que l'article 5 de l'Otan peut "s'interpréter de plusieurs façons" ?
6. Washington cesse de livrer certaines armes à l'Ukraine, Kiev convoque le chargé d'affaires américain
7. Emmanuel Grégoire, le socialiste qui rêve de succéder à Anne Hidalgo à Paris
8. Fuites, pollutions, prix… En Outre-mer, une "discrimination environnementale" dans l'accès à l'eau

Format attendu du JSON :
1. "1" : Un titre en {{ lang }} journalistique créatif, pertinent, engageant, riche en mots-clés et adapté à une diffusion sur internet et les réseaux sociaux, pour un média d'actualité internationale. Le titre doit être rédigé en {{ lang }} et respecter les règles typographiques de la presse en {{ lang }} : seule la première lettre du titre doit être en majuscule, les autres lettres en minuscules (sauf noms propres). Les titres doivent comporter entre 50 et 60 caractères (espaces compris). Le titre peut contenir une touche d'humour, mais doit toujours refléter fidèlement le contenu, sans sensationnalisme. Puisqu'il traite de l'actualité internationale, les indications de pays ou de régions sont à privilégier dans les mots-clés de ces titres.
2. "2" : Un résumé complet en {{ lang }} et concis de 8 à 10 phrases des points principaux du texte, avec 1 ou 2 mots-clés inclus pour susciter l'intérêt du lecteur. Ce résumé doit faire entre 600 et 1000 caractères, avec une préférence pour 800 caractères. Il doit résumer la thématique principale en développant une problématique sur cette thématique, sans dévoiler tous les détails, afin de susciter l'intérêt du lecteur, mettre en avant l'angle principal de l'article, en étant à la fois informatif et incitatif. Adopter un ton professionnel, clair, structuré, précis et pédagogique, adapté à un grand public exigeant. Intégrer, si pertinent, une citation ou un chiffre marquant tiré du texte, pour renforcer l'accroche et l'intérêt du chapeau. Citez ensuite les autres sujets ou thématiques secondaires en les distinguant bien de la première thématique. Pour accroître la pertinence sur la thématique principale, posez une ou deux questions rhétoriques qui invitent le lecteur à réfléchir davantage sur le sujet principal. Abordez les thématiques secondaires sous forme de questions pour susciter la curiosité du lecteur et l'inciter à lire l'article complet.
3. "3" : Un tableau de quatre à sept mots-clés ou expressions les plus pertinents du texte, que les lecteurs potentiels utiliseraient pour le rechercher. Ces mots-clés doivent être en {{ lang }}.
4. "4" : Un tableau contenant une ou plusieurs catégories en {{ lang }} à laquelle appartient le contenu, choisies strictement parmi la liste suivante : {{ cms_section_keywords_list }}. La catégorie doit être en {{ lang }} et refléter la localisation géographique ou la thématique principale du contenu.

Le résultat doit être en {{ lang }} et structuré en JSON strictement comme suit :
{
  "1": "Titre de l'article 1",
  "2": "Résumé de l'article en 8-10 phrases.",
  "3": ["Mot-clé 1", "Mot-clé 2", "Mot-clé 3", "Mot-clé 4", "Mot-clé 5"],
  "4": ["Catégorie 1", "Catégorie 2"],
}

Assurez-vous que la catégorie choisie dans le champ 4 est bien dans la langue c'est à dire en {{ lang }} et que le format de sortie est strictement respecté. Ne fournissez que l'objet JSON pur en {{ lang }}, sans aucune balise, texte explicatif, ou autre formatage non JSON. Le résultat doit être un JSON brut et valide, strictement conforme aux spécifications, prêt à être consommé par une API."""

content = """No Kings o Sin Reyes fue el eslogan bajo el que convocaron a más de 2.000 manifestaciones
con cerca de 5 millones de participantes en Estados Unidos el pasado 14 de junio. En las
calles los manifestantes rechazaron las amenazas que el presidente Donald Trump le está poniendo
a la democracia según ellos. Además fue la contrapropuesta al desfile militar en Washington
a propósito de los 250 años del ejército estadounidense. Mientras el contexto político
en partes del país está siendo violento, Guardia Nacional y Marines fueron desplegados en Los
Ángeles ante las protestas en contra de las redadas de migrantes. En Minnesota un hombre
armado mató a la representante a la Cámara Estatal Melissa Horman, quien era demócrata.
Y a todo esto se suma el arresto de un candidato alcalde de la
ciudad de Nueva York, Brad Lander. Su detención ocurrió mientras acompañaba a una persona a una
corte de temas migratorios. Se está convirtiendo Donald Trump en un rey que persigue a sus
opositores. ¿O son las manifestaciones la muestra de que la democracia de Estados Unidos está más
viva que nunca? Ese es el debate de hoy en France 24. Yo soy María Clara Calle y le doy la
bienvenida a nuestros dos invitados que nos acompañan ambos desde Miami. Ellos son Daisy
López, representante de Florida por el Partido Demócrata, y César Grajales, analista político y
director nacional de Asuntos Públicos en la iniciativa Libre, que es una organización que
promueve las políticas de libre mercado dentro de la comunidad hispana en Estados Unidos. Bienvenidos
ustedes dos. Bienvenida, como siempre, toda nuestra audiencia. Antes de comenzar, les recuerdo
que nos pueden seguir en redes sociales, donde estamos como arroba France 24 guión bajo ese y
mi cuenta personal es arroba María Claguirre. También pueden ver los episodios anteriores del debate de la Cámara Estatal.
Y también pueden escucharlos a través de Apple Podcast, Spotify, Deezer y TuneIn.
Tanto a Daisy como a César les voy a plantear una pregunta inicial. Daisy, ¿usted cree que se está incitando a la violencia política en Estados Unidos?
Pienso que sí. Soy veterana, fui militar, serví en el ejército de los Estados Unidos. Vi lo que pasó este fin de semana en los Estados Unidos.
Muchas situaciones preocupantes, diría yo. Primero, vimos cómo el presidente de los Estados Unidos ha utilizado la milicia en contra de los ciudadanos americanos.
También vimos cómo trató de hacer una parada militar al estilo de los grandes tiranos y comunistas, gobiernos comunistas del país, del mundo.
Y vimos cómo aquello resultó.
Trató de mandar un mensaje de poder y de gran fuerza, pero lo que vimos fue una parada anémica, una parada prácticamente triste.
Fue muy poca gente, no estuvo bien participada. Y lo que estamos viendo es que millones de personas salieron a la calle a protestar.
Eso sí puedo decir, que todavía la roca principal de la soberanía, de la democracia, es la violencia.
Y la violencia en la democracia americana sí continúa, sí existe. Porque tuvimos esos millones de personas que a pesar de las avanzadas que hizo el presidente en contra de ellos usando la milicia,
aún así salieron a las calles a protestar, a presentar su punto de vista, a demostrarle al presidente que no tienen miedo, que este es un país de democracia donde el partido opositor,
o las personas que están opuestas a sus ideas, tienen el derecho.
De protestar, de elevar su voz y de dar su punto de vista. Así que, por un lado es triste lo que está pasando, pero por el otro lado también estoy contenta de ver que nuestro poder como oposición, nuestro poder como democracia, continúa.
Y César Grajales, ¿usted qué opina? ¿Se está incitando a la violencia política en Estados Unidos?
Bueno, a ver, la cuestión es si la pregunta es directamente...
Esta administración está incitando a la violencia política. Si después de hacer la descripción del desfile militar y las marchas a eso se refiere, me parece que estamos viendo precisamente lo que es ejercer la libertad de expresión en los Estados Unidos de manera ordenada y correcta.
Si vamos a hablar del odio político, pues tendríamos que ir incluso hasta el 2016 o 2015.
Cuando Trump se lanza a la presidencia y los demócratas empiezan a llamar, empezando por Hillary Clinton, deplorables a todos los que apoyan a Trump.
Entonces, me parece que el desgaste político, el insulto político empezó desde los demócratas hace muchos años atrás.
Ahora, voy a ir por puntos que ha mencionado Daisy. Gracias, Daisy, por tu servicio al país.
Pero yo estuve en el desfile militar. De hecho, yo estaba uno de los invitados y estuve allí.
A mí no me parece que fuera...
Fue un desfile anémico. Por el contrario, me pareció un desfile muy inspirador.
Vi muchos veteranos, veteranos que desafortunadamente en combate perdieron alguna extremidad de su cuerpo, sea una pierna o un brazo.
Y si a uno no le inspira ver que esa persona es capaz de arriesgar la vida por la libertad de este país, no sé qué le puede inspirar a uno.
Por otro lado, viendo la cara de los niños con asombro, cómo veían las máquinas y marchar los militares.
Porque fue una historia de ejército que, por cierto, le quiero poner en contexto.
Esto no nace, de hecho, del presidente Trump.
Esto nace del mismo U.S. Army que le cuenta al presidente que quieren iniciar una celebración de los 250 años,
un cuarto de milenio del nacimiento de las fuerzas militares,
que también coincide con el inicio de la celebración que empieza el 4 de julio del 250 aniversario cuarto de milenio de los Estados Unidos
que se celebra el próximo año.
O sea, son celebraciones que vienen con relación a eso, que coincide y es anecdótico que el presidente Donald Trump cumple años junio 14.
Bueno, eso ya le toca que él le hace el reclamo a Dios.
Pero aquí el ejército no tiene la culpa de haberse fundado precisamente el 14 de junio de 1775.
No tiene nada que ver.
Por otro lado, el tema de las marchas.
Oiga, la gente marchó en orden y pudieron protestar precisamente, no reyes.
Y paradójicamente.
Paradójicamente, pues protestan algo donde precisamente no hay ningún rey.
Tienen la libertad de expresar todo lo que quieren.
Y el presidente Trump usó, porque se refiere a las marchas de California desordenadas que empezaron una semana atrás, 10 días atrás.
Pues le tocó usar la Guardia Civil, el capítulo 10, precisamente invocar eso al tener un estado de California,
un gobierno acéfalo, sin cabeza, un gobernador.
Que dejó que esto se convirtiera un desorden, un caos en California.
Una alcaldesa, esta señora Bass, que lo único que hizo fue nada.
Y al final le dio la ración a la administración cuando le tocó que llamar a toque de queda,
que por cierto terminó el día de hoy, porque había un caos y un desorden en la ciudad.
Cuando hay un gobierno estatal y un gobierno local que no tienen orden ni control,
le toca al gobierno federal proteger el bien público, la propiedad privada,
y le tocó tomar orden.
El mensaje fue recibido por los desadaptados sociales, porque el sábado se vio una marcha fantástica.
Todo el mundo salió por el país a marchar en contra de lo que consideran que no les gustan las políticas públicas del presidente,
sean migratorias.
Eso está bien.
Lo que no está bien es el caos, es el confrontamiento, es el desorden, es el daño al bien público.
Y creo que eso fue un gran mensaje y de liderazgo del presidente Trump cuando mandó a la Guardia Civil y a los Marines
en California para que se acabara de una vez el desorden y el caos.
Y los 250 años en la reacción del ejército lo viviría mil veces más.
César, discúlpame, lo interrumpo para poder continuar con el debate.
Ustedes ponen tres elementos sobre la mesa.
Les propongo que conversemos primero sobre dos de ellos.
Uno, el desfile militar.
Dos, las manifestaciones bajo el eslogan No Kings.
Y también lo que ha ocurrido en Los Ángeles.
Si bien vamos a mencionar Los Ángeles, pues fue un motivo de las manifestaciones No Kings.
¿Qué es lo que se ha hecho?
Y no profundicemos en esto, ya que eso fue otro de los episodios del debate
y poder avanzar en la discusión en la que estamos ahora.
Daisy, volviendo entonces sobre el desfile militar.
César trae a colación dos puntos.
Uno, estos eran en efecto los 250 años del ejército estadounidense.
No era una fecha cualquiera.
Y coincide además con el cumpleaños número 79 del presidente Donald Trump.
Pero además usted decía antes, Daisy, que Trump estaba imitando a países comunistas
cuando él mismo ha dicho que se incitó a la guerra.
¿Qué inspiró en los desfiles militares de Francia del 2017,
en el Día de la Bastilla, durante la primera presidencia de Donald Trump?
¿Por qué entonces no vale la pena mostrar la fuerza militar que tiene Estados Unidos,
sobre todo en un momento de guerra de Medio Oriente?
No es que los Estados Unidos no tengan el derecho, las iniciativas de mostrar fuerza.
Lo puede hacer de muchas maneras.
De hecho, salimos de la Segunda Guerra Mundial como los líderes del mundo.
Pero la política del presidente Trump,
la política de Donald Trump ha sido una de aislar a los Estados Unidos
de sus socios tradicionales europeos, de la Unión de la NATO,
de los países europeos que han sido tradicionalmente nuestros aliados.
Creo que eso le hace más daño a este presidente para proyectar fuerza
que una parada militar que realmente no se vio tan bien.
La precisión con que las paradas se ven en otros países,
la pagentía, como dicen en inglés,
la precisión con lo que hacen, eso no fue lo que vimos este sábado.
Te lo digo yo porque fui militar, yo marché, así como esos soldados.
Y la verdad que me dio pena ajena porque yo dije, bueno, no creo que...
Y yo sé muy bien, y se ha publicado ya, que él no está contento con los resultados de esa parada,
que no es lo que él estaba esperando.
Él quería algo mucho más...
Dinámico, más vibrante, ¿no?
Y como te dije al principio, el punto era mandar un mensaje,
pero como te digo, creo que lo hubiera mandado,
lo puede mandar de otras maneras más efectivas que una parada que costó,
a propósito, muchos millones de dinero.
Y otra cosa, en las bases militares se usan las paradas prácticamente toda la semana.
Yo cuando era militar, los viernes siempre se terminaba la semana yendo al campo
y ver las...
Las tropas pasar.
Eso es muy común para nosotros, era en esa época.
Es algo que a mí me encanta, me gusta, lo celebro,
pero creo que en este caso fue la estrategia equivocada.
Usted decía que este desfile militar costó millones de dólares.
Concretamente se estima que el valor fue de 45 millones de dólares.
César, en medio de un gobierno que quiere hacer recortes federales,
¿por qué invertir semejante cantidad de dinero en un desfile pasajero?
¿Por qué no se ha invertido en un desfile militar?
Porque gran parte del dinero vino de donaciones de grandes empresas.
De hecho, ahí están públicos cuáles empresas donaron para el desfile militar.
Y hay que reconocer también que las donaciones y el parte del gasto
no es precisamente en sí la gran mayoría para que marcharan los soldados.
Es para reparar las calles, por donde pasaran los tanques de guerra,
es para dejar todo como estaba.
Pero reitero, gran parte lo puso la industria privada,
desde la compañía de entretenimiento,
desde la UFC, como FedEx y muchas otras compañías privadas
que pusieron dinero para este desfile militar.
Que, por cierto, olvidamos mencionar que ese mismo día
también se celebró el Día de la Bandera,
una bandera que representa lo que es la nación,
lo que es los Estados Unidos.
A mí me parece que el contexto del día tan simbólico e importante
ameritaba precisamente el desfile militar
y resaltar la importancia de la bandera.
Y es que, en realidad, los símbolos de esta nación,
tanto el poderío militar que nos han regalado la libertad
y la posibilidad de que la gente ese mismo día marchara de manera libre,
gracias a esa constitución que tenemos en este país,
como abrazar la bandera que nos ha abrazado a todos nosotros,
una bandera que ha hundiado en momentos históricos de esta nación,
momentos felices, momentos icónicos como el hombre en la luna,
y momentos tan tristes como sobre los soldados,
los escombros de las Torres Gemelas de septiembre 11.
Y todo eso amerita la inversión para recordarle a los estadounidenses
que este país es un país resiliente y es un país que no escatima en mostrar la fuerza.
Y me parece que lo que hizo el presidente Trump era valioso, era necesario,
es patriotismo y hay que recordarle al país y a la gente que esos símbolos importan.
A propósito, César, que usted habla de los símbolos,
quiero preguntarle por uno de los hechos que ocurrió ese mismo sábado
antes de las manifestaciones de Snow King y antes del desfile militar.
Y fue el asesinato de la representante a la Cámara en el estado de Minnesota,
Melissa Horman, una demócrata.
Un hombre disfrazado de policía se presume que golpeó en su casa
y la mató tanto a ella como a su esposo.
Y antes de ir a la casa de la representante, el mismo hombre ya había pasado por la casa
de otro senador demócrata, John Hoffman, a quien hirió, a él y a su esposa.
Además, el sospechoso ya está detenido y lo que han dicho las autoridades locales
y la fiscalía es que este hombre tenía una lista negra de 45 funcionarios de Minnesota,
todos demócratas, a los que pretendía asesinar.
¿Cómo explicar esto? ¿Es un nuevo nivel de violencia que no se había visto antes
en Estados Unidos contra los políticos, concretamente contra los demócratas?
Yo no creo que tenga que ver nada con el Partido Demócrata.
Me parece más bien que es un tipo que hay que investigar más qué fue lo que sucedió,
pero recordemos que él ha hecho parte indirecta del gobierno de Minnesota,
empezando por el gobernador previo a Tim Walz y el gobernador de hoy, demócrata,
es candidato a la presidencia, Tim Walz. De hecho, fue el que lo nominó a uno de los boards,
los directores o directores en una de estas oficinas gubernamentales.
Era muy cercano al círculo político de Minnesota.
Hay que profundizar en realidad qué fue lo que pasó con este personaje,
que le encontraron también panfletos de Nockings dentro del carro.
A la mujer la encontraron huyendo con los hijos y 10 mil dólares en efectivo
y dos pistolas también en ese carro.
Yo creo que hay que quitar de la noticia el tema demócrata.
Lo que hay que ver es cuál es el trasfondo del crimen de este señor,
que yo le garantizo que es mucho más allá de la motivación política.
Ahí tiene que haber algo, tiene que haber gato encerrado.
Y lo que sí es la verdad es que los legisladores en general siempre enfrentan locos como estos.
No olvidemos el tema de Scalise cuando estaba republicano,
cuando estaba en este juego que vino un loco a dispararle y quererlo matar a él
y a los otros republicanos que estaban ahí.
Y a mí me parece que eso no tiene nada que ver con el Partido Demócrata ni los demócratas.
Es simplemente gente desadaptada social que tiene problemas mentales,
que llegan a un momento de ruptura mental y hacen este tipo de acciones.
Pero la mujer tiene que saber qué pasó desde que estuviera huyendo en un carro
con 10 mil dólares en efectivo, los hijos, pasaportes y dos armas.
Hay que pensar mucho más en eso.
Y seguro que veremos más la luz de esta noticia en unos días más.
Contrario a lo que usted dice, César, las autoridades locales y del Estado
han dicho que este asesinato podría tener motivos políticos.
Sin embargo, la investigación judicial continúa en pie.
Usted dice que el sospechoso detenido, Vance Bolter, tenía una implicación
y una relación directa con los círculos políticos de Minnesota.
Daisy, ¿qué responde usted al respecto?
Eso es realmente una exageración.
¿Qué te puedo decir?
Fabricación hasta cierto punto.
Sí, el antiguo gobernador demócrata lo había nombrado a una posición menor
de una comisión de cosas de negocios.
Y cuando el gobernador Tim Walz entró en su posición,
de esas cosas que se renuevan y lo renovó en ese cargo,
pero no hay ninguna evidencia de que Tim Walz tenía una relación con esta persona,
que lo apoyó en ninguna otra cosa,
o que tenían nada que ver el uno con otro.
Esto es muy claro que este señor estaba incitado por el clima político,
está incitado por la retórica que estamos viendo que baja desde la Casa Blanca,
estamos viendo que este señor tenía o sus familiares y amigos
dicen que era apoyador del presidente Donald Trump
y votó por el presidente Donald Trump.
Las tácticas de usar milicia y ese tipo de cosas también van en línea con eso.
Y el hecho de que tenía una lista de legisladores que son todos demócratas,
no sé cómo puede decir mi colega que esto no tiene nada que ver con los demócratas.
Claro que tiene que ver todo que ver con los demócratas.
Este señor tiene una vendetta en contra de los legisladores demócratas y actuó al respecto.
Actuó matando a dos personas.
A dos personas inocentes, hiriendo a dos más y con la intención de herir o matar a otros más.
Así que no se puede tapar el sol con un dedo.
Vimos también cómo esto viene, mi colega dice que desde el 16,
pero yo te voy a decir, esto se empeoró en enero 6,
cuando los seguidores del presidente Donald Trump atacaron el Capitolio de los Estados Unidos.
Y que resulta que desde el momento que entró a presidente los perdona.
Entonces, ¿cómo tú perdonas a criminales convictos?
Entonces ese mensaje que le está mandando es ustedes actúan en mi favor
o en pro de las cosas que nosotros queremos o creemos van a tener impunidad.
Ese es el mensaje que estás bajando de la Casa Blanca, que usted puede actuar de esta manera y todo va bien.
No va a haber consecuencias. Y esto es lo que está causando este tipo de crimen.
Usted dice que el sospechoso. Disculpeme, César, un segundo.
Disculpeme, César, un segundo. Usted dice que el sospechoso. Disculpeme, César, un segundo.
Dice Daisy que el sospechoso actuó incitado por la retórica de la Casa Blanca.
Sin embargo, de nuevo insisto, la investigación judicial continúa
y todavía no se conoce a ciencia cierta cuáles fueron los motivos del atacante.
Pero quiero preguntarle una vez más, Daisy, sobre algo que usted mencionó por encima
y que César también había mencionado antes y es la violencia política en Estados Unidos no comienza ahora,
no comienza en 2025. Y de hecho recordemos que el mismo presidente Donald Trump
en medio de su campaña electoral recibió un disparo y estuvo a centímetros de ser asesinado por un francotirador en medio de un mitin político.
Daisy, le quiero preguntar a propósito de este hecho y este atentado contra Trump.
¿La violencia política en Estados Unidos no viene entonces de tiempo atrás y es contra todos los partidos políticos?
Claro que sí, pero lo que estamos viendo donde una persona específicamente tiene una lista, un hit list, y va a la casa de un legislador y lo mata y mata a su esposo, ahí está escalando a otro nivel.
Sí, ha habido episodios como el de la antigua speaker Nancy Pelosi.
Acuérdate que una persona que fue a su casa y atentó contra su esposo.
Un congresista que estaban jugando un partido de béisbol, creo que era.
También que lo atacaron, pero también vimos cómo arrastraron al senador Padilla de California, lo arrastraron las personas de ICE y hoy también arrastraron forzablemente a un candidato alcalde de Nueva York.
Así que estamos viendo que como el respeto que existía antes hacia los legisladores se está esfumando y esto es muy preocupante, sumamente preocupante.
Y lo que queremos ver es un tono más conciliatorio.
La Casa Blanca, de hecho, cuando se le preguntó al presidente si iba a llamar al gobernador, dijo que para qué, que eso sería una pérdida de tiempo.
Eso no lo hemos visto en gobernantes en este país antes.
Pasaba una tragedia y el primero que salía a buscar, a ver y a dar un tono de conciliación era el presidente.
Eso no lo estamos viendo con este presidente.
Él, al contrario, usa cualquier instancia para, como dicen, ponerle sal a la herida.
Para continuar usando.
Usando nombrecitos, insultando a la gente.
O sea, una retórica negativa, realmente negativa.
Por eso es que digo que viene y bajando de la Casa Blanca.
Simplemente para poner en contexto a nuestra audiencia.
Cuando ustedes hablan de Tim Walz, recordemos que además de ser el gobernador de Minnesota, donde asesinaron a la representante de la Cámara Estatal,
Tim Walz fue candidato a la vicepresidencia por el Partido Demócrata y era la fórmula vicepresidencial de Kamala Harris.
César, Daisy menciona el hecho de que Trump.
No quiso llamar a Tim Walz para ofrecerle sus condolencias por el atentado y también mencionó la detención de Brad Lander,
el candidato a la alcaldía en la ciudad de Nueva York, también demócrata y de la detención días antes de el senador estatal de California, Alex Padilla.
Ambos fueron o ambos son demócratas, perdón, y ambos fueron arrestados por autoridades federales.
Está entonces la Casa Blanca y el gobierno persiguiendo a los demócratas.
A ver, primero que todo, déjenme responder algo.
Daisy está lanzando acusaciones y no está simplemente dejando que las investigaciones transcurran.
Le ha puesto el dinero que quiera que cuando salga el tema de este señor Bolter en Minnesota no tiene nada que ver con colores políticos.
Ahí tiene que haber algo mucho más.
La forma de la ejecución, como cometió los crímenes, apuntan a ese a ese ángulo.
Pero lo que pasa es que los demócratas están desesperados por popularidad.
Y cualquier cosa que pase en el.
País se la van a colgar al presidente o pequeño republicano.
Y es irónico porque hablan de la división, pero los comentarios que hacen precisamente son los que más dividen cuando apuntan a que la violencia viene de los republicanos.
Cuando en este momento he venido resaltando yo aquí que eso no tiene nada que ver con tintes políticos, que es un desadaptado social.
Pero bueno, en fin, ese es el ese es el modo superándi de todos los de muchos de los demócratas como Daisy, que ese es el argumento de ella.
En el caso del señor Padilla, el senador Padilla.
Él quería la foto política y la obtuvo.
Está en una rueda de prensa.
Dice él que se presentó y luego hizo la pregunta.
No empezó a hacer preguntas y después se identificó cuando lo están sacando de esa rueda de prensa.
Vino a generar caos y desorden a una rueda de prensa donde no está invitado.
Obviamente lo que quería era la fotografía.
Y este señor que está corriendo la alcaldía de New York, el contralor de New York, pues también una carrera política que viene muerta y necesitaba la fotografía política para tratar de subir puntos en la alcaldía.
De Nueva York.
Donde está el alcalde mayor, el alcalde Adams, que por cierto, amiguísimo de los demócratas, hasta que les dijo la crisis, la crisis migratoria aquí en New York nos está llevando al caos.
En ese momento se volvió un enemigo político completo de los demócratas.
Esa es la realidad.
Solo muente, buscan la política, la fotografía política.
Lo mencioné en otro programa.
Aquí los cubanos de Miami tienen un dicho fantástico para ese tipo de gente como a la espadilla, como este señor de New York.
Y son unas postalitas.
Lo único que hacen es ir, hacer ruido, que les tomen la foto.
Están buscando la fotografía y el oportunismo político.
Eso es todo lo que están haciendo.
ICE está ejecutando las leyes que están allí y están cogiendo a la gente que ellos consideran que hay que sacar del país.
Que hay que ser sensible con el tema migratorio, por supuesto.
Que hay que ser sensible y estratégico en quién debería salir.
Los criminales, la gente que está trabajando y que merece una oportunidad, hay que encontrarles el camino legal.
Pero que los demócratas del partido y los líderes del partido están aprovechando esto para la fotografía política.
Lo están aprovechando.
Eso hizo Padilla.
Eso hizo el señor de Nueva York el día de hoy.
Pero sabe que no puede esperar uno menos de un partido que dentro de sus propias bases de votantes tiene una popularidad por el suelo.
Ahorita mismo están acéfalos.
No tienen un líder claro para las elecciones del 2028 y están desesperados.
El único que de pronto ha levantado la mano.
Bueno, es Gavin Newsom, pero a ese no le cree ni la mamá porque es un mentiroso.
Él miente constantemente.
Esa es la realidad política del Partido Demócrata el día de hoy.
Y les invito a revisar las encuestas.
Los mismos votantes demócratas no creen dentro del Partido Demócrata.
Esa es la realidad.
Y entonces se encuentra en esta situación para generar reacciones mediáticas que hoy nos tienen en este debate.
Usted dice que es simplemente para la fotografía e impulsar una carrera política.
Que está bastante desinflada ante el poder predominante de los republicanos.
Daisy, ¿qué responde usted?
Lo que yo respondo es que vamos a ver en los próximos meses, según se van y empiezan a calentar las campañas políticas,
que este presidente prometió que iba a bajar los precios de las cosas, de las comidas.
No lo ha hecho.
Que iba a bajar el precio de la gasolina.
No lo ha hecho.
Que iba a controlar la inflación.
No lo ha hecho.
Que iba a bajar.
Que iba a aumentar.
Que iba a aumentar los empleos.
No lo ha hecho.
Que iba a bajar el costo de la vida.
No lo ha hecho.
Que no iba a entrar en guerras.
Y ya vemos la situación que tenemos hoy en día en el Medio Oriente.
La bolsa de valores está por el suelo.
La agricultura y la construcción están siendo azotadas por las reglas migratorias.
Y esto va a afectar el precio de todo.
Tenemos los casos de violencia.
Nominando personas en el gabinete sin calificaciones.
Cuyo propósito es desmantelar las mismas agencias donde han sido nominados.
También tenemos la reducción de servicios a las personas.
También tenemos la situación de que estamos a punto de tener consecuencias serias
con el presupuesto que está presentando,
que va a reducir severamente el Medicaid y muchos de los servicios sociales de este país.
¿Qué pasa?
Cuando el pueblo americano empiece a ver todas estas cosas y ya lo están sintiendo.
Y ya lo están sintiendo con estas redadas migratorias.
Y dicen, ojo, que porque son criminales.
No.
Estadísticamente hay menos criminalidad en las poblaciones inmigrantes que en las poblaciones regulares.
Ah, que están cogiendo algo vino.
¿Y por qué siempre estas redadas son en sitios de trabajo donde esta gente está trabajando?
En los campos, en las factorías.
En las granjas.
Ahí esto lo van a juzgar porque están trabajando.
No, estas poblaciones vienen aquí a trabajar.
Son buenas, son dedicadas, vienen a mejorar la calidad de vida de sus familias
y contribuyen billones de dólares en taxes a la economía de los Estados Unidos
y no reciben nada a cambio porque las personas indocumentadas
no tienen derecho a accesar los servicios del gobierno.
Así que cuando la población...
La población en general y sobre todo aquí en el sur de la Florida,
donde tenemos una población altamente inmigrante,
que votaron por este señor porque les había prometido que iba a liberar a Cuba,
iba a liberar a Venezuela y que solamente iba a deportar a los criminales
y resulta que no, que ahora están, como dice el dicho,
y llega y todo el que llega es que le están sacando.
Sin mirar cómo lo están haciendo, lo están haciendo de una manera poco humana
y no es un hecho.
En general, o sea, no se están enfocando en los criminales, sino en todo el mundo.
Así que cuando las poblaciones vean esto en los próximos meses de la campaña
y de hecho ya hemos visto algunas elecciones especiales
donde increíblemente los candidatos demócratas han hecho muy bien en la votación.
Así que eso es lo que vamos a ver cuando llegue el momento de tomar la decisión
de quién va a ser el próximo líder de esta nación.
Y si con este listado que usted denumera varias,
varios de esos argumentos fueron utilizados por los manifestantes
en las protestas conocidas como no kings.
Ellos, muchos de ellos afirman que Estados Unidos está rumbo a un fascismo
liderado por un autócrata como Donald Trump.
César, qué responde usted al respecto?
Una narrativa vacía y por ejemplo,
Daisy, me parece que la última vez que abrió el reporte de finanzas
fue en noviembre del año pasado cuando estaba Joe Biden o tal vez no mal superado.
O no pone gasolina, a lo mejor tiene chofer.
Yo la realidad es que si usted va a la gasolinera hoy,
la gasolina regular aquí anda en dos dólares con 49, dos dólares con 70,
dependiendo del lugar donde vaya a nivel nacional.
El promedio anda en tres dólares y cachito, tres dólares, once más o menos, tres dólares, 17.
El promedio de gasolina el año pasado por estas fechas andaba por tres dólares con 66.
El promedio nacional en los huevos que estuvieron carísimos,
el comienzo de año hoy están bajos de nuevo.
Yo no entiendo cuál es el reporte financiero que está haciendo francamente Daisy
y le voy a poner en contexto de lo que acaba de mencionar Daisy del Big Beautiful Bill.
Ese proyecto de ley incluye varias cosas.
Dentro de eso incluye la extensión y permanencia de los recortes de los impuestos
que benefició a más del 70 por ciento de los estadounidenses.
Los demócratas siguen con la narrativa.
Te van a beneficiar a los millonarios, super millonarios del país.
Los contradice.
La misma CBP los contradice.
El más del 70 por ciento.
Y la realidad es, le voy a poner esto en contexto y también lo puede buscar.
Si esa ley no se extiende y se hace permanente este año en estados como la Florida,
más de tres mil dólares por familia promedio se van a aumentar los impuestos el próximo año.
Esa es una realidad.
Ese es un hecho.
Los demócratas andan con el cuento de que le van a quitar el Medicaid.
El presidente no va a quitar el Medicaid ni el Medicare.
Lo que ha dicho es que hay que revisar dónde la gente está.
Está colgado de un sistema que se supone que es para ayudar temporalmente, como es el Medicaid.
El Medicare no lo van a tocar.
El Medicaid.
Si usted es una persona joven que tiene el Medicaid y que puede trabajar, por qué no trabaja?
Eso es lo que están diciendo los republicanos.
Cualquier ayuda social debe de ser un trampolín y no un modo de vivir.
Esa es la realidad para poder empezar a reducir esa deuda que tenemos en este país de más de 36 mil millones de dólares,
que eventualmente será un problema.
Es un problema de seguridad nacional.
Esa es la realidad.
Y de hecho, el presupuesto aumenta la vida.
Les pido un momento a los dos precisamente para ya acercarnos a la conclusión de nuestro programa.
César, no me respondió mi pregunta muy concretamente para usted.
Donald Trump es un fascista y un rey, como denunciaron los manifestantes.
Los manifestantes pueden denunciar lo que sea, pero la misma pregunta es incluso insultante.
Es un presidente electo por más de 70 millones de norteamericanos.
Y está cumpliendo lo que dijo en la agenda que por lo que votaron.
Y eso es lo que está haciendo.
Y en cuatro años habrán otras elecciones y vendrá otro presidente.
Y Daisy, quiero preguntarle.
Por el contrario, las manifestaciones no evidencian que el presidente respeta la democracia y que además, como recordó César, es el presidente electo de Estados Unidos.
Por qué entonces los manifestantes lo tildan de fascista?
Porque han impulsado y ha presentado muchas acciones que son violaciones a la Constitución.
De este país que no respeta los derechos humanos y que están implementando políticas que son en detrimento a la nación.
Y por eso es que las personas están saliendo a protestar y a dar su voz, su voz a conocer de que no están de acuerdo con la dirección con que está yendo este país.
Y César, cómo explicar que un presidente demócrata ponga a los militares en las calles para reprimir a los manifestantes como ocurrió en Los Ángeles?
Sí.
No para reprimir a los manifestantes.
Para salvaguardar precisamente el bien público que es el bien de todos, que todos pagamos.
Que pagan los californianos para proteger precisamente que la gente que de verdad pacíficamente quiera marchar,
lo pueda hacer sin tener que lidiar con estos desadaptados sociales quemando patrullas, atacando a la policía.
Y cuando el gobierno estatal y el gobierno local no pueden responder a eso, el capítulo 10 le permite al presidente de Estados Unidos,
presidente de los Estados Unidos, invocar y tomar inmediatamente,
llamar a la Guardia Nacional.
Mandó a 4 mil efectivos.
El tema de los 700 marines también estaban asistiendo para traer el orden.
¿Surgió efecto?
Por supuesto que sí.
Tanto lo mencionaba al comienzo, Karen Bass, no le tocó otra más
que llamar al toque de queda y finalmente ya las cosas parece que se están
calmando en California.
Pero si no hubiera sido por eso, estos dos títeres políticos
que no sirven para nada, como es Karen Bass y este señor Gavin Newsom,
que es muy bueno para la fotografía, pues claramente tenían hecho un caos.
California, un estado tan espectacular y una ciudad tan linda como es Los Ángeles.
Usted dice entonces que Donald Trump salvaguardó Los Ángeles de los manifestantes
y los desadaptados desplegando a la Guardia Nacional y a los marines
y que era una medida necesaria ante la falta de decisión de el gobernador
del Estado y de la alcaldesa de la ciudad de ahí.
Y para finalizar, ¿cuál es su conclusión?
Al respecto.
La situación, mandar la Guardia Nacional,
él se muestra como el que está más a cargo
y lo que hizo fue inflamar lo que estaba pasando,
que hubiera terminado de cualquier manera.
Pero una vez que tú envuelves la Guardia Nacional,
que típicamente es llamada por el gobernador,
no por los federales,
y lo hizo aún en contra de los deseos del gobernador.
Y en un gobierno que siempre,
que siempre ha dicho que los estados deben tener sus derechos,
hizo todo lo contrario, le quitó los derechos al Estado
de tomar sus propias decisiones.
Daisy Baez y César Grajales, gracias por exponer sus argumentos
aquí en el debate de France 24.
Este programa fue producido por nuestra jefe de edición, Laura Garzón,
y nuestra jefe de invitados, Nathalie Quiroga.
Ustedes vean más en france24.com."""

OUTPUT_FILE = "caca_esp.json"
