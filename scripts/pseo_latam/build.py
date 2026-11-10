#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de páginas de SEO programático (LATAM, en español) para Kiss My Site.
Uso: python3 scripts/pseo_latam/build.py

Mismo patrón que scripts/pseo/build.py (EEUU, inglés), pero:
- Contenido en español, localizado por país (ver COUNTRY_PHRASES).
- Datos reales (title/meta/H1/keyword/enlazado) vienen de
  scripts/pseo_latam/data/latam_data.json, extraído del Excel
  "KissMySite_LATAM_Metadatos_SEO_Versión_Final.xlsx" del especialista.
- Las FAQs no vinieron en el Excel esta vez — las escribo acá, mismo
  criterio que las de EEUU.
- Páginas en /es/agencia-{servicio}-{lugar} (en vez de /en/agency-...).
"""
import html as htmlmod
import json
import os
import subprocess

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "public", "es")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "public", "assets")
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "latam_data.json")

with open(DATA_PATH, encoding="utf-8") as f:
    DATA = json.load(f)

# Alcance final acordado con el especialista: 5 países + sus 2 ciudades
# principales cada uno (15 ubicaciones x 3 servicios = 45 páginas). Ya no 82
# ciudades — el alcance se redujo a este conjunto, que es el que viene
# completo (estructura + FAQs) en el Excel.
ALL_COUNTRIES = ["Perú", "Paraguay", "Panamá", "Colombia", "México"]

# ---------------------------------------------------------------------------
# Variación local por país — pedido explícito del especialista: el término
# de "tienda" cambia según el país, y el idioma debe sonar natural en cada
# mercado, no una traducción mecánica.
# ---------------------------------------------------------------------------
COUNTRY_PHRASES = {
    "Perú":      dict(tienda="tienda virtual"),
    "Paraguay":  dict(tienda="tienda online"),
    "Panamá":    dict(tienda="tienda online"),
    "Colombia":  dict(tienda="tienda virtual"),
    "México":    dict(tienda="tienda en línea"),
}

SERVICE_LABELS = {"SEO": "SEO", "CRO": "CRO", "Ecommerce": "Ecommerce"}

# ---------------------------------------------------------------------------
# Contenido compartido entre todas las páginas (igual en todos los países)
# ---------------------------------------------------------------------------
TESTIMONIALS = [
    dict(
        quote="Cuando empezamos con la idea de lanzar nuestra tienda online Hawaianas.com.ar, estábamos "
              "bastante desorientados. Ahí aparecieron Cande y Mati de KissMy.Site, y no solo hicieron que el "
              "proyecto fuera posible, sino que nos acompañaron en cada etapa, ayudándonos a ordenar ideas y "
              "aportando su experiencia con una generosidad enorme. Más allá de la calidad profesional, lo que "
              "más destacamos es la calidez humana con la que trabajaron — los recomendamos con total "
              "confianza.",
        author="Amira Maslub", role="Gerenta de E-commerce", company="Hawaianas",
    ),
    dict(
        quote="Estamos muy conformes con el servicio de Kiss My Site y el acompañamiento en nuestra estrategia "
              "de SEO. Destacamos la predisposición, profesionalismo y compromiso del equipo, su capacidad "
              "para entender las necesidades de nuestro negocio y adaptar las propuestas a nuestros objetivos. "
              "El seguimiento es constante y la comunicación muy clara, con una mirada estratégica que va más "
              "allá del SEO y aporta una visión integral del posicionamiento y la experiencia del sitio. "
              "Recomendamos a Kiss My Site como una agencia profesional, comprometida y cercana, que realmente "
              "se involucra con el proyecto.",
        author="Micaela Verta", role="Analista Sr. de VTEX", company="ShopGallery",
    ),
]

METHOD_TOOLS = "Google Search Console, GA4, Semrush, Screaming Frog, Hotjar y GTM"

DIFFERENTIATORS_TABLE = [
    ("Reporta métricas de vanidad", "Reporta ingresos y pipeline atribuidos"),
    ("Una estrategia genérica para cada cliente", "Un roadmap armado con tus propios datos y competidores"),
    ("Un account manager que rota", "El mismo consultor senior de la auditoría a la ejecución"),
    ("Te ata a un contrato de 12 meses", "Sin permanencia mínima: te quedás porque funciona"),
    ("Manda un PDF una vez por trimestre", "Sesiones de trabajo quincenales y un dashboard compartido en vivo"),
]

# ---------------------------------------------------------------------------
# Plantillas por servicio — mismo copy para todos los países/ciudades, con
# {lugar} (ciudad o país) y {tienda} como únicas variables.
# ---------------------------------------------------------------------------
SERVICE_TEMPLATES = {
    "SEO": dict(
        service_type_schema="Optimización en motores de búsqueda",
        hero_lede="Si el posicionamiento orgánico no está trabajando activamente para vos, estás dejando "
                  "tráfico calificado y ventas sobre la mesa todos los días en uno de los mercados más "
                  "competitivos de la región. Auditamos tu sitio, armamos un plan técnico, de contenidos y de "
                  "autoridad basado en la intención real de búsqueda, y lo medimos hasta los ingresos, no solo "
                  "hasta los rankings.",
        hero_bullets=[
            "Auditoría técnica completa, priorizada por impacto en ingresos, no un checklist de 200 ítems",
            "Contenido construido alrededor de la intención de búsqueda en {lugar}, no de volumen de keywords "
            "genérico",
            "Tu propio dashboard en vivo: el mismo que usamos nosotros, todos los días",
            "Sin contratos de permanencia. Si no estamos moviendo la aguja, lo vas a saber.",
        ],
        proof_stats=[
            ("8+", "Años gestionando programas de SEO"),
            ("40+", "Clientes activos en distintas industrias"),
            ("+180%", "Crecimiento promedio de tráfico orgánico, 12 meses"),
            ("4.2x", "Retorno de inversión promedio"),
        ],
        pain_h2="Si ya buscaste una agencia SEO en {lugar}, probablemente ya viviste esto",
        pain_items=[
            ("Reportes llenos de rankings y cero ingresos.", "Subiste keywords al top 3 y los ingresos se "
             "mantuvieron igual. Te vendieron rankings, no demanda."),
            ("Un plan de contenidos que nadie pidió leer.", "Cero volumen de búsqueda, cero intención de "
             "compra: tráfico en el papel, no en tu cuenta bancaria."),
            ("Deuda técnica que nadie toca.", "Google gasta presupuesto de rastreo en URLs que no deberían "
             "existir, mientras tus páginas más importantes no se indexan."),
            ("100% dependiente de medios pagos.", "El día que pausás la inversión publicitaria, el tráfico se "
             "cae a cero."),
            ("Nadie te puede decir cuánto genera lo orgánico realmente.", "Ni la agencia anterior, ni tu "
             "configuración de analítica, y sin ese número, cualquier conversación de presupuesto es una "
             "suposición."),
        ],
        services_h2="SEO integral: técnico, contenido y autoridad",
        services_lede="No vendemos \"paquetes de contenido\" aislados. Trabajamos las palancas que realmente "
                      "mueven el posicionamiento orgánico, priorizadas por impacto en tu negocio.",
        services_cards=[
            ("🔧", "SEO técnico", "Rastreo completo, Core Web Vitals, arquitectura de URLs, datos "
             "estructurados y renderizado JS, priorizado por esfuerzo vs. impacto."),
            ("🔍", "Investigación de keywords", "Mapeamos todo tu mercado por intención de búsqueda real y lo "
             "cruzamos con tu catálogo o servicios, resolviendo canibalización y vacíos."),
            ("✍️", "Producción de contenido", "Páginas de categoría, comparativas y guías de compra escritas "
             "para ganar una decisión: cada página construida alrededor de una keyword y una métrica."),
            ("🔗", "Digital PR", "Enlaces editoriales de medios reales y relevantes. Sin granjas de enlaces, "
             "sin riesgo de penalización."),
            ("📍", "SEO local", "Perfil de Google Business, landing pages locales y citaciones, para que "
             "aparezcas en búsquedas \"cerca de mí\" y a nivel ciudad en {lugar}."),
            ("🧩", "SEO programático", "Landing pages estructuradas y basadas en datos, a escala, hechas "
             "bien, con contenido realmente diferencial, no páginas duplicadas finas."),
        ],
        method_h2="De la auditoría a los ingresos, en cuatro etapas",
        method_steps=[
            ("Diagnóstico", "Semana 1-2", "Analizamos tu sitio, tus competidores directos en {lugar} y tu "
             "tráfico e ingresos actuales. Te llevás un documento accionable de cualquier manera."),
            ("Roadmap", "Semana 3", "Auditoría técnica completa, investigación de keywords por intención y "
             "mapeo de arquitectura. Definimos KPIs y armamos el dashboard compartido."),
            ("Ejecución", "Mes 2-6", "Sprints mensuales: arreglos técnicos junto a tu equipo de desarrollo, "
             "publicación de contenido y construcción de autoridad. Reunión quincenal, reporte mensual."),
            ("Medición e iteración", "Continuo", "Redoblamos lo que funciona, cortamos lo que no, y abrimos "
             "nuevos clusters. Acá es donde lo orgánico empieza a bajar el costo de adquisición."),
        ],
        industries=[
            ("💻", "Tecnología y SaaS"), ("🎬", "Entretenimiento y medios"), ("🏨", "Turismo y hotelería"),
            ("🏠", "Inmobiliario"), ("🏥", "Salud"), ("👗", "Retail y moda"),
            ("🌱", "Agro y alimentos"), ("💼", "Servicios profesionales"),
        ],
        approach_h2="Nuestro enfoque, en la práctica",
        approach_lede="Todavía no tenemos un caso publicado en {lugar}: así es un primer proyecto real, "
                      "basado en cómo trabajamos.",
        approach_steps=[
            ("Arrancamos con la auditoría gratuita.", "Un rastreo completo más una revisión de tus principales "
             "competidores en {lugar}. Te llevás los tres problemas más costosos que encontramos, por escrito, "
             "nos contrates o no."),
            ("Armamos un roadmap atado a ingresos.", "No un checklist: un plan priorizado que dice qué "
             "arreglo mueve qué número, y por cuánto, aproximadamente."),
            ("Reportamos lo que le importa al negocio.", "Tráfico orgánico y rankings son insumos. El reporte "
             "que importa mide leads e ingresos atribuidos a lo orgánico."),
        ],
        mid_cta=[
            ("¿Cansado de pagar por rankings que no convierten?",
             "Averigüemos dónde se está perdiendo tráfico orgánico, sin costo y sin compromiso."),
            ("¿Querés ver cómo se vería esto para tu industria?",
             "Pedí una auditoría gratuita enfocada en tu sitio y tus competidores en {lugar}."),
            ("¿Listo para una agencia que reporta ingresos, no métricas de vanidad?",
             "Pedí tu auditoría de SEO gratis y mirá el primer roadmap antes de comprometerte a nada."),
        ],
        final_h2="Conseguí tu auditoría de SEO gratis para {lugar}",
        final_body="Contanos sobre tu proyecto y en 48 horas hábiles te entregamos un análisis real de tu "
                   "situación orgánica, sin costo y sin compromiso.",
    ),
    "CRO": dict(
        service_type_schema="Optimización de tasa de conversión",
        hero_lede="Ya tenés el tráfico. En un mercado tan caro para publicitar como {lugar}, duplicar la "
                  "inversión en ads es la forma más costosa de crecer. Hacemos que el tráfico que ya tenés te "
                  "deje más dinero: auditorías de conversión, experimentación y optimización de funnel, "
                  "respaldadas por método y evidencia.",
        hero_bullets=[
            "Auditoría de conversión basada en datos cuantitativos y cualitativos",
            "Programa de testing A/B: hipótesis, medición y aprendizaje",
            "Cada cambio validado con significancia estadística, no con opinión",
            "Trabajamos con lo que ya tenés: no hace falta un rediseño completo",
        ],
        proof_stats=[
            ("8+", "Años gestionando programas de CRO"),
            ("40+", "Clientes activos en distintas industrias"),
            ("+95%", "Suba promedio en tasa de conversión, 12 meses"),
            ("1 de 3", "Fugas encontradas en una primera auditoría típica"),
        ],
        pain_h2="Si ya te quemaste con una agencia de CRO en {lugar}, esto te va a sonar conocido",
        pain_items=[
            ("Un rediseño completo, vendido como \"optimización\".", "Meses de trabajo, ningún test A/B, "
             "ninguna forma de saber qué movió realmente el número."),
            ("Tests que se cortan apenas \"van ganando\".", "Declarados ganadores antes de llegar a "
             "significancia estadística, y la mejora desaparece en producción."),
            ("Reportes de tasa de conversión, nunca de ingresos.", "Una tasa puede subir mientras el ingreso "
             "por sesión baja. Nadie lo revisó."),
            ("Cambios de \"mejores prácticas\" genéricas.", "Copiados de un blog, no de tus grabaciones de "
             "sesión ni de tus datos de funnel reales."),
            ("Ninguna idea de qué testear después.", "Un solo test y después silencio, sin backlog ni "
             "marco de priorización."),
        ],
        services_h2="CRO integral: investigación, testing y evidencia",
        services_lede="No corremos tests por correr tests. Cada hipótesis sale de datos reales sobre tu "
                      "tráfico en {lugar} y cómo se comporta de verdad.",
        services_cards=[
            ("🔬", "Auditoría de conversión", "Revisión cuantitativa de analítica más mapas de calor y "
             "grabaciones de sesión para encontrar dónde y por qué se cae la gente."),
            ("🧪", "Testing A/B y multivariado", "Hipótesis estructuradas, cálculo correcto de tamaño de "
             "muestra y resultados validados estadísticamente: nunca una moneda al aire."),
            ("🛒", "Optimización de checkout y formularios", "Revisión campo por campo de tus pasos de mayor "
             "fricción, donde los cambios chicos mueven más ingresos."),
            ("📊", "Revisión de analítica y tracking", "GA4 y GTM auditados para que cada test se mida contra "
             "números en los que realmente podés confiar."),
            ("🧭", "Investigación UX", "Entrevistas a usuarios y testing de usabilidad cuando los datos dicen "
             "\"algo está mal\" pero no \"por qué\"."),
            ("📈", "Personalización", "Experiencias segmentadas para tu tráfico de mayor valor, una vez "
             "ganados los tests fundacionales."),
        ],
        method_h2="De la auditoría a la mejora comprobada, en cuatro etapas",
        method_steps=[
            ("Diagnóstico", "Semana 1-2", "Revisamos tu funnel, tu configuración de analítica y tus "
             "principales competidores en {lugar}. Te llevás las tres fugas más costosas por escrito, nos "
             "contrates o no."),
            ("Backlog de hipótesis", "Semana 3", "Priorizamos un roadmap de testing por impacto y esfuerzo "
             "esperado, y armamos el dashboard de reporte compartido."),
            ("Ejecución", "Mes 2-6", "Ciclos mensuales de testing: diseño, construcción, corrida hasta "
             "significancia, análisis. Reunión quincenal, reporte mensual."),
            ("Medición e iteración", "Continuo", "Los ganadores se implementan de forma permanente, los "
             "perdedores quedan documentados como aprendizaje. El backlog nunca se seca."),
        ],
        industries=[
            ("💻", "SaaS y tecnología"), ("🛍️", "Ecommerce y retail"), ("🏨", "Turismo y hotelería"),
            ("🏥", "Salud"), ("🏠", "Inmobiliario"), ("💰", "Servicios financieros"),
            ("🎓", "Educación"), ("💼", "Servicios profesionales"),
        ],
        approach_h2="Nuestro enfoque, en la práctica",
        approach_lede="Todavía no tenemos un caso publicado en {lugar}: así es un primer proyecto real, "
                      "basado en cómo trabajamos.",
        approach_steps=[
            ("Arrancamos con la auditoría gratuita.", "Una revisión completa de funnel y analítica, más un "
             "vistazo a tus principales competidores en {lugar}. Te llevás las tres fugas más costosas por "
             "escrito, nos contrates o no."),
            ("Armamos un backlog de hipótesis, no un test aislado.", "Priorizado por impacto esperado en "
             "ingresos, para que el roadmap sobreviva más allá del primer resultado."),
            ("Reportamos ingresos, no solo tasa de conversión.", "Cada test mide ingreso por sesión y costo "
             "por lead, validado con significancia estadística antes de declarar un ganador."),
        ],
        mid_cta=[
            ("Tu tráfico ya está ahí: lo estás perdiendo en la puerta.",
             "Pedí una auditoría de conversión gratuita y encontrá las tres fugas más costosas de tu funnel."),
            ("¿Querés ver cómo sería un roadmap de testing para tu sitio?",
             "Pedí una auditoría gratuita y te mostramos dónde están las ganancias más rápidas."),
            ("¿Listo para un crecimiento que puedas comprobar?",
             "Pedí tu auditoría de CRO gratis y mirá las primeras hipótesis de testing antes de comprometerte "
             "a nada."),
        ],
        final_h2="Conseguí tu auditoría de CRO gratis para {lugar}",
        final_body="Contanos sobre tu proyecto y en 48 horas hábiles te entregamos las fugas más costosas de "
                   "tu funnel actual, sin costo y sin compromiso.",
    ),
    "Ecommerce": dict(
        service_type_schema="Desarrollo de Ecommerce",
        hero_lede="La diferencia entre una {tienda} en {lugar} que escala y una que se estanca es la base. Te "
                  "acompañamos en cada paso (plataforma, catálogo, pagos y CRO) para que tu tienda esté "
                  "construida sobre bases sólidas y estratégicas desde el día uno.",
        hero_bullets=[
            "Selección y desarrollo de plataforma: Shopify, Shopify Plus, BigCommerce, WooCommerce o VTEX",
            "SEO de catálogo y categorías, construido para cómo la gente busca realmente",
            "CRO de checkout para cerrar la brecha entre visitas y pedidos",
            "Migraciones que no pierden tu posicionamiento ni tus ingresos actuales",
        ],
        proof_stats=[
            ("8+", "Años construyendo tiendas de ecommerce"),
            ("40+", "Clientes activos en distintas industrias"),
            ("+120%", "Crecimiento promedio de ingresos, 12 meses"),
            ("0", "Posiciones perdidas en una migración bien planificada"),
        ],
        pain_h2="Si estás evaluando una agencia de ecommerce en {lugar}, probablemente ya te topaste con esto",
        pain_items=[
            ("Una tienda que se ve bien y convierte mal.", "Nadie testeó el checkout con usuarios reales antes "
             "del lanzamiento: la fricción se esconde en los detalles."),
            ("Una migración que hundió tu posicionamiento.", "Sin plan de redirecciones, sin metadatos "
             "migrados, y tres meses de tráfico orgánico perdido."),
            ("Una plataforma elegida por los motivos equivocados.", "Elegida porque estaba de moda, no porque "
             "se ajuste al tamaño de tu catálogo o a tu plan de crecimiento."),
            ("Integraciones que no se hablan entre sí.", "Inventario, envíos y tu ERP viven en tres lugares "
             "distintos, y alguien lo concilia a mano."),
            ("SEO tratado como un detalle menor.", "Páginas de categoría y producto construidas para el "
             "diseño, no para las búsquedas que realmente generan tráfico en {lugar}."),
        ],
        services_h2="Ecommerce integral: construcción, optimización y crecimiento",
        services_lede="No lanzamos una tienda y desaparecemos. Cada proyecto se diseña pensando en lo que "
                      "realmente hace crecer los ingresos después del lanzamiento.",
        services_cards=[
            ("🛠️", "Desarrollo y migraciones", "Shopify, Shopify Plus, BigCommerce, WooCommerce y VTEX, con un "
             "plan completo de redirecciones y metadatos en cada migración."),
            ("🗂️", "SEO de catálogo y categorías", "Navegación facetada, paginación y estructura de categorías "
             "construidas alrededor de la intención de búsqueda real, no solo del diseño."),
            ("💳", "CRO de checkout", "Revisión campo por campo de tu paso de mayor abandono, testeado y "
             "validado, no supuesto."),
            ("🔌", "Integraciones", "Pasarelas de pago, impuestos, transportistas y herramientas de ERP o 3PL, "
             "para que el checkout sea rápido y confiable."),
            ("📈", "Analítica y atribución", "Tracking de ecommerce en GA4 bien configurado, para que cada "
             "peso de ingreso se atribuya al canal que lo generó."),
            ("✉️", "Marketing de ciclo de vida", "Flujos de carrito abandonado, post-compra y recuperación de "
             "clientes que convierten una compra en ingresos recurrentes."),
        ],
        method_h2="De la auditoría al lanzamiento, en cuatro etapas",
        method_steps=[
            ("Diagnóstico", "Semana 1-2", "Revisamos tu tienda actual (o definimos el alcance de una nueva), "
             "tus competidores en {lugar}, y tu catálogo y tráfico. Te llevás un documento accionable de "
             "cualquier manera."),
            ("Roadmap", "Semana 3", "Decisión de plataforma, arquitectura de información y un backlog "
             "priorizado de arreglos o tareas de desarrollo, con el dashboard compartido armado."),
            ("Ejecución", "Mes 2-6", "Sprints de desarrollo o arreglos, SEO de catálogo y categorías, CRO de "
             "checkout. Reunión quincenal, reporte mensual."),
            ("Medición e iteración", "Continuo", "Monitoreamos tasa de conversión, ticket promedio y tráfico "
             "orgánico semana a semana después del lanzamiento, y seguimos testeando el checkout."),
        ],
        industries=[
            ("👗", "Moda e indumentaria"), ("💄", "Belleza y cuidado personal"), ("🏠", "Hogar y muebles"),
            ("🍔", "Alimentos y bebidas"), ("💪", "Salud y bienestar"), ("🎁", "Especialidad y regalos"),
            ("📱", "Electrónica"), ("🐾", "Productos para mascotas"),
        ],
        approach_h2="Nuestro enfoque, en la práctica",
        approach_lede="Todavía no tenemos un caso publicado en {lugar}: así es un primer proyecto real, "
                      "basado en cómo trabajamos.",
        approach_steps=[
            ("Arrancamos con la auditoría gratuita.", "Una revisión completa de tu tienda, o una sesión de "
             "alcance para una nueva, más un vistazo a tus principales competidores en {lugar}."),
            ("Planificamos la migración antes de tocar nada.", "Cada URL mapeada, cada redirección "
             "planificada, metadatos y datos estructurados preservados, con indexación y tráfico monitoreados a "
             "diario después del lanzamiento."),
            ("Reportamos ingresos, no solo tráfico.", "Tasa de conversión, ticket promedio y tráfico orgánico "
             "medidos semana a semana, para que sepas que la tienda realmente está funcionando, no solo "
             "online."),
        ],
        mid_cta=[
            ("No dejes que una plataforma inestable frene tu crecimiento.",
             "Pedí una auditoría gratuita de tu tienda y descubrí qué te está costando ventas antes de que te "
             "cueste más."),
            ("¿Querés ver cómo se vería esto para tu catálogo?",
             "Pedí una auditoría gratuita enfocada en tu plataforma, tus productos y tu tráfico en {lugar}."),
            ("¿Listo para una tienda construida para escalar, no solo para lanzar?",
             "Pedí tu auditoría de ecommerce gratis y mirá el primer roadmap antes de comprometerte a nada."),
        ],
        final_h2="Conseguí tu auditoría de ecommerce gratis para {lugar}",
        final_body="Contanos sobre tu tienda y en 48 horas hábiles te entregamos los arreglos de mayor "
                   "impacto, sin costo y sin compromiso.",
    ),
}

def _fmt(value, **ctx):
    if isinstance(value, str):
        return value.format(**ctx)
    if isinstance(value, list):
        return [_fmt(v, **ctx) for v in value]
    if isinstance(value, tuple):
        return tuple(_fmt(v, **ctx) for v in value)
    return value

def build_page_data(url):
    info = DATA["estructura"][url]
    enlaces = DATA["enlaces"].get(url, [])
    faqs = DATA["faqs"][url]

    servicio = info["servicio"]
    pais = info["pais"]
    ciudad = info["ciudad"]
    nivel = info["nivel"]
    lugar = ciudad if ciudad else pais
    slug = url.split("/es/")[1]

    tmpl = SERVICE_TEMPLATES[servicio]
    phrases = COUNTRY_PHRASES[pais]
    d = {k: _fmt(v, lugar=lugar, tienda=phrases["tienda"]) for k, v in tmpl.items()}

    related = []
    for link in enlaces:
        dest_slug = link["destino"].split("/es/")[1]
        dest_info = DATA["estructura"].get(link["destino"], {})
        dest_servicio = dest_info.get("servicio", servicio)
        dest_lugar = dest_info.get("ciudad") or dest_info.get("pais", "")
        related.append((dest_slug, f"Agencia {dest_servicio} {dest_lugar}"))

    d.update(
        slug=slug,
        servicio=servicio,
        service_label=SERVICE_LABELS[servicio],
        pais=pais,
        ciudad=ciudad,
        lugar=lugar,
        nivel=nivel,
        eyebrow=f"Agencia de {SERVICE_LABELS[servicio]} · {lugar}",
        title=info["title"],
        meta_desc=info["meta"],
        h1=info["h1"],
        faqs=[tuple(qa) for qa in faqs],
        related=related,
        schema_area_served=(
            {"@type": "Country", "name": pais} if nivel == "País"
            else {"@type": "City", "name": ciudad, "containedInPlace": {"@type": "Country", "name": pais}}
        ),
    )
    return d

# ---------------------------------------------------------------------------
# Render (idéntico en estructura al de EEUU — mismas clases CSS, mismo JS)
# ---------------------------------------------------------------------------
def esc(s):
    return htmlmod.escape(s, quote=True)

def render_bullets(items):
    return "\n".join(f'<li>{esc(b)}</li>' for b in items)

def render_proof_stats(stats):
    return "\n".join(
        f'<div class="stat-box"><span class="stat-value">{esc(v)}</span>'
        f'<span class="stat-label">{esc(l)}</span></div>'
        for v, l in stats
    )

def render_pain_items(items):
    out = []
    for lead, body in items:
        out.append(f'''<div class="pain-row">
  <div class="pain-x"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M6 6l12 12M18 6L6 18"/></svg></div>
  <p><b>{esc(lead)}</b>{esc(body)}</p>
</div>''')
    return "\n".join(out)

def render_service_cards(cards):
    out = []
    for icon, title, desc in cards:
        out.append(f'''<div class="svc2-card glass glow-card">
  <div style="font-size:1.6rem;margin-bottom:10px;">{icon}</div>
  <h3>{esc(title)}</h3>
  <p>{esc(desc)}</p>
</div>''')
    return "\n".join(out)

def render_steps(steps):
    out = []
    for i, (title, timing, desc) in enumerate(steps, 1):
        out.append(f'''<div class="step-row">
  <div class="step-num">{i:02d}</div>
  <div>
    <h4>{esc(title)} <span style="color:var(--muted);font-weight:400;font-size:0.85rem;">— {esc(timing)}</span></h4>
    <p>{esc(desc)}</p>
  </div>
</div>''')
    return "\n".join(out)

def render_industries(industries):
    out = []
    for icon, name in industries:
        out.append(f'''<div class="industry-card glass glow-card">
  <span class="industry-icon">{icon}</span>
  <span>{esc(name)}</span>
</div>''')
    return "\n".join(out)

def render_approach(steps):
    out = []
    for i, (title, body) in enumerate(steps, 1):
        out.append(f'''<div class="approach-card glass glow-card">
  <span class="approach-num">{i:02d}</span>
  <h4>{esc(title)}</h4>
  <p>{esc(body)}</p>
</div>''')
    return "\n".join(out)

def render_testimonials():
    out = []
    for t in TESTIMONIALS:
        out.append(f'''<div class="testi-card glass glow-card">
  <div class="testi-quote">&quot;</div>
  <blockquote>{esc(t["quote"])}</blockquote>
  <div class="testi-who">{esc(t["author"])}, {esc(t["role"])} — {esc(t["company"])}</div>
</div>''')
    return "\n".join(out)

def render_diff_table():
    cards = "\n".join(f'''<div class="why-card glass glow-card">
  <div class="why-old">
    <div class="why-old-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M6 6l12 12M18 6L6 18"/></svg></div>
    <p>{esc(a)}</p>
  </div>
  <div class="why-new">
    <div class="why-new-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M4 12l5 5L20 6"/></svg></div>
    <p>{esc(b)}</p>
  </div>
</div>''' for a, b in DIFFERENTIATORS_TABLE)
    return f'<div class="why-compare">{cards}</div>'

def render_faqs(faqs):
    out = []
    for q, a in faqs:
        out.append(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>')
    return "\n".join(out)

def render_related(related):
    out = []
    for slug, label in related:
        out.append(f'<a class="related-link" href="/es/{slug}">{esc(label)} <span>&rarr;</span></a>')
    return "\n".join(out)

def render_faq_schema(faqs):
    items = ",\n".join(f'''    {{
      "@type": "Question",
      "name": {json_str(q)},
      "acceptedAnswer": {{ "@type": "Answer", "text": {json_str(a)} }}
    }}''' for q, a in faqs)
    return f'''{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{items}
  ]
}}'''

def json_str(s):
    return json.dumps(s, ensure_ascii=False)

def render_mid_cta(headline, body, hue):
    return f'''<section class="section section-slim" data-hue="{hue}">
  <div class="mid-cta glass glow-card">
    <div class="mid-cta-copy">
      <h3>{esc(headline)}</h3>
      <p>{esc(body)}</p>
    </div>
    <a class="pill pill-glow" href="#pseo-contact">Quiero mi auditoría gratis &rarr;</a>
  </div>
</section>'''

def render_page(d):
    canonical = f"https://kissmy.site/es/{d['slug']}"
    schema_service = f'''{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "{canonical}#business",
  "name": "Kiss My Site — Agencia de {esc(d['service_label'])} en {esc(d['lugar'])}",
  "url": "{canonical}",
  "description": {json_str(d['meta_desc'])},
  "serviceType": "{esc(d['service_type_schema'])}",
  "areaServed": {json.dumps(d['schema_area_served'], ensure_ascii=False)},
  "address": {{ "@type": "PostalAddress", "addressCountry": "{esc(d['pais'])}" }}
}}'''
    schema_breadcrumb = f'''{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://kissmy.site/es" }},
    {{ "@type": "ListItem", "position": 2, "name": "Agencia {d['service_label']} {esc(d['pais'])}", "item": "https://kissmy.site/es/agencia-{d['slug'].split('-')[1]}-{d['pais'].lower().replace('é','e').replace('á','a')}" }},
    {{ "@type": "ListItem", "position": 3, "name": "{esc(d['h1'])}", "item": "{canonical}" }}
  ]
}}'''
    schema_faq = render_faq_schema(d['faqs'])

    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<script src="/atribucion.js" defer></script>
<title>{esc(d['title'])}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(d['meta_desc'])}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/images/favicon.png">
<link rel="stylesheet" href="/assets/kms-shared.min.css">
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-M7NT6F3');</script>
<!-- End Google Tag Manager -->
<script type="application/ld+json">{schema_service}</script>
<script type="application/ld+json">{schema_breadcrumb}</script>
<script type="application/ld+json">{schema_faq}</script>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-M7NT6F3"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

<canvas id="galaxy"></canvas>

<div class="page">

<svg width="0" height="0" style="position:absolute;">
  <defs>
    <filter id="navGlassFilter">
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.012" numOctaves="2" seed="7" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" xChannelSelector="R" yChannelSelector="G" scale="18" />
    </filter>
  </defs>
</svg>

<nav id="siteNav">
  <a class="logo" href="/"><img src="/images/logo-lips.png" alt="Kiss My Site" style="height:28px;width:auto;">kiss my site</a>
  <ul class="navlinks">
    <li><a href="/#pillars">Qué hacemos</a></li>
    <li><a href="/#packs">Packs</a></li>
    <li><a href="/#services">Servicios</a></li>
    <li><a href="/#clients">Clientes</a></li>
  </ul>
  <div class="nav-right">
    <a class="nav-cta" href="#pseo-contact">Hablemos</a>
    <button class="navburger" id="navBurger" aria-label="Abrir menú" aria-expanded="false"><span class="bar"></span></button>
  </div>
</nav>

<div class="mobile-menu" id="mobileMenu">
  <button class="mobile-menu-close" id="mobileMenuClose" aria-label="Cerrar menú">&times;</button>
  <ul>
    <li><a href="/" data-close>Inicio</a></li>
    <li><a href="/#pillars" data-close>Qué hacemos</a></li>
    <li><a href="/#packs" data-close>Packs</a></li>
    <li><a href="/#services" data-close>Servicios</a></li>
    <li><a href="/#clients" data-close>Clientes</a></li>
  </ul>
  <a class="mm-cta" href="#pseo-contact" data-close>Hablemos &rarr;</a>
</div>

<div class="whatsapp-float" id="whatsappFloat-wrap">
  <a class="whatsapp-float" id="whatsappFloat" href="#" target="_blank" rel="noopener" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" fill="#fff"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.48 1.32 5.02L2 22l5.25-1.38a9.9 9.9 0 004.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2zm5.86 14.02c-.24.68-1.4 1.32-1.93 1.4-.5.08-1.11.11-1.79-.11-.41-.13-.94-.31-1.63-.6-2.86-1.24-4.73-4.13-4.87-4.32-.14-.19-1.17-1.55-1.17-2.96 0-1.41.74-2.1 1-2.39.26-.29.57-.36.76-.36.19 0 .38 0 .55.01.18.01.41-.07.64.49.24.58.81 2 .88 2.14.07.14.12.31.02.5-.09.19-.14.31-.28.48-.14.17-.29.37-.42.5-.14.14-.28.29-.12.57.16.28.71 1.17 1.52 1.9 1.05.94 1.93 1.23 2.21 1.37.28.14.44.12.6-.07.16-.19.68-.79.86-1.06.18-.27.37-.22.62-.13.26.09 1.62.77 1.9.91.28.14.46.21.53.33.07.12.07.68-.17 1.36z"/></svg>
  </a>
</div>

<!-- Bloque 1: Hero -->
<section class="section service-hero" data-hue="263">
  <div class="svc2-hero">
    <div class="svc2-hero-copy">
      <div class="eyebrow">&middot; {esc(d['eyebrow'])}</div>
      <h1 class="sf-heading">{esc(d['h1'])}</h1>
      <p class="lede">{esc(d['hero_lede'])}</p>
      <ul class="svc2-bullets">
{render_bullets(d['hero_bullets'])}
      </ul>
      <div class="svc2-cta-row">
        <a class="pill pill-glow" href="#pseo-contact">Pedí tu auditoría gratis &rarr;</a>
        <a class="pill pill-ghost" href="#pseo-method">Ver nuestro método</a>
      </div>
      <div class="svc2-fineprint">Auditoría gratuita, sin compromiso. Respuesta en 48 horas hábiles.</div>
    </div>
    <div class="svc2-card glass glow-card">
      <h3>Auditoría de {esc(d['service_label'])} Gratis</h3>
      <p>Revisamos tu sitio real y te entregamos los tres problemas más costosos, con una estimación de lo que te están costando.</p>
      <a class="pill pill-glow" href="#pseo-contact">Quiero mi auditoría &rarr;</a>
    </div>
  </div>
</section>

<!-- Bloque 2: Franja de prueba social -->
<section class="section" data-hue="270" style="padding-top:0;">
  <div class="proof-strip">
{render_proof_stats(d['proof_stats'])}
  </div>
</section>

<!-- Bloque 3: Diagnóstico del problema -->
<section class="section" data-hue="276">
  <div class="eyebrow">&middot; El problema</div>
  <h2 class="sf-heading">{esc(d['pain_h2'])}</h2>
  <div class="pain-list">
{render_pain_items(d['pain_items'])}
  </div>
</section>

{render_mid_cta(d['mid_cta'][0][0], d['mid_cta'][0][1], 272)}

<!-- Bloque 4: Servicio y entregables -->
<section class="section" data-hue="263" id="pseo-what">
  <div class="eyebrow">&middot; Qué incluye</div>
  <h2 class="sf-heading">{esc(d['services_h2'])}</h2>
  <p class="section-lede">{esc(d['services_lede'])}</p>
  <div class="svc2-card-grid">
{render_service_cards(d['services_cards'])}
  </div>
</section>

<!-- Bloque 5: Metodología -->
<section class="section" data-hue="258" id="pseo-method">
  <div class="eyebrow">&middot; Cómo trabajamos</div>
  <h2 class="sf-heading">{esc(d['method_h2'])}</h2>
  <div class="pain-list">
{render_steps(d['method_steps'])}
  </div>
  <p style="color:var(--muted);font-size:0.9rem;margin-top:24px;">Herramientas que usamos día a día: {METHOD_TOOLS}.</p>
</section>

<!-- Bloque 6: Industrias -->
<section class="section" data-hue="283">
  <div class="eyebrow">&middot; Industrias</div>
  <h2 class="sf-heading">Industrias con las que trabajamos en {esc(d['lugar'])}</h2>
  <div class="industries-grid">
{render_industries(d['industries'])}
  </div>
</section>

{render_mid_cta(d['mid_cta'][1][0], d['mid_cta'][1][1], 260)}

<!-- Bloque 8: Nuestro enfoque -->
<section class="section" data-hue="268">
  <div class="eyebrow">&middot; Nuestro enfoque</div>
  <h2 class="sf-heading">{esc(d['approach_h2'])}</h2>
  <div class="approach-block">
    <p class="section-lede">{esc(d['approach_lede'])}</p>
    <div class="approach-grid">
{render_approach(d['approach_steps'])}
    </div>
  </div>
</section>

<!-- Bloque 9: Testimonios -->
<section class="section" data-hue="276">
  <div class="eyebrow">&middot; Lo que dicen nuestros clientes</div>
  <h2 class="sf-heading">Lo que dicen nuestros clientes</h2>
  <div class="testi-grid testi-grid--two">
{render_testimonials()}
  </div>
</section>

<!-- Bloque 10: Diferenciadores -->
<section class="section" data-hue="263">
  <div class="eyebrow">&middot; Por qué Kiss My Site</div>
  <h2 class="sf-heading">Por qué las empresas de {esc(d['lugar'])} nos eligen en vez de una agencia típica</h2>
  {render_diff_table()}
</section>

{render_mid_cta(d['mid_cta'][2][0], d['mid_cta'][2][1], 285)}

<!-- Bloque 11: FAQs -->
<section class="section" data-hue="287">
  <div class="eyebrow">&middot; Preguntas frecuentes</div>
  <h2 class="sf-heading">Preguntas sobre {esc(d['service_label'])} en {esc(d['lugar'])}, respondidas</h2>
  <div class="faq-list">
{render_faqs(d['faqs'])}
  </div>
  <nav class="related-services" aria-label="Páginas relacionadas">
    <span class="related-label">Páginas relacionadas</span>
    <div class="related-chips">
{render_related(d['related'])}
    </div>
  </nav>
</section>

<!-- Bloque 13: CTA final y formulario -->
<section class="section" id="pseo-contact" data-hue="270">
  <div class="final-grid">
    <div class="final-copy">
      <div class="eyebrow">&middot; Empezá ahora</div>
      <h2 class="sf-heading" style="text-align:left;margin:0 0 20px;max-width:none;">{esc(d['final_h2'])}</h2>
      <p style="color:var(--muted);font-size:0.98rem;margin:0 0 24px;max-width:52ch;">{esc(d['final_body'])}</p>
    </div>
    <div class="svc2-form-card glass glow-card">
      <h3>Pedí tu auditoría gratis</h3>
      <p>Todos los campos marcados con * son obligatorios.</p>
      <form class="contact-form svc2-form" id="svc2form-{d['slug']}">
        <div><label for="f-name">Nombre completo *</label><input id="f-name" name="name" required></div>
        <div><label for="f-email">Email corporativo *</label><input id="f-email" name="email" type="email" required></div>
        <div><label for="f-company">Empresa *</label><input id="f-company" name="company" required></div>
        <div><label for="f-phone">Teléfono / WhatsApp</label><input id="f-phone" name="phone" type="tel"></div>
        <div class="full"><label for="f-message">¿Cuál es tu principal desafío hoy?</label><textarea id="f-message" name="message"></textarea></div>
        <!-- Atribución: los completa atribucion.js. Dejarlos vacíos. -->
        <input type="hidden" name="utm_term"         data-attr="utm_term">
        <input type="hidden" name="utm_campaign"     data-attr="utm_campaign">
        <input type="hidden" name="utm_source"       data-attr="utm_source">
        <input type="hidden" name="utm_medium"       data-attr="utm_medium">
        <input type="hidden" name="utm_content"      data-attr="utm_content">
        <input type="hidden" name="gclid"            data-attr="gclid">
        <input type="hidden" name="gbraid"           data-attr="gbraid">
        <input type="hidden" name="wbraid"           data-attr="wbraid">
        <input type="hidden" name="fbclid"           data-attr="fbclid">
        <input type="hidden" name="landing_inicial"  data-attr="landing_inicial">
        <input type="hidden" name="referrer_inicial" data-attr="referrer_inicial">
        <input type="hidden" name="primera_visita"   data-attr="primera_visita">
        <label class="hp-field" aria-hidden="true"><input type="text" name="_hp" tabindex="-1" autocomplete="off"></label>
        <input type="checkbox" name="botcheck" class="hp-field" tabindex="-1" aria-hidden="true">
        <div class="full"><button class="pill pill-glow" type="submit">Pedir mi auditoría gratis &rarr;</button></div>
      </form>
      <div class="svc2-success" id="svc2success-{d['slug']}">
        <h3>¡Gracias, pedido enviado! 🎉</h3>
        <p>Te vamos a contactar dentro de las 48 horas hábiles al email que nos diste.</p>
      </div>
    </div>
  </div>
</section>

</div>

<script src="/assets/kms-shared.min.js" defer></script>
</body>
</html>
'''

def minify_shared_assets():
    pairs = [("kms-shared.css", "kms-shared.min.css"), ("kms-shared.js", "kms-shared.min.js")]
    for src, out in pairs:
        src_path = os.path.join(ASSETS_DIR, src)
        out_path = os.path.join(ASSETS_DIR, out)
        subprocess.run(
            ["npx", "esbuild", src_path, "--minify", f"--outfile={out_path}"],
            check=True, cwd=os.path.join(os.path.dirname(__file__), "..", ".."),
        )
        print(f"minified {src} -> {out} ({os.path.getsize(out_path)} bytes)")

def urls_for_countries(countries):
    out = [url for url, info in DATA["estructura"].items() if info["pais"] in countries]
    return sorted(out)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    minify_shared_assets()
    urls = urls_for_countries(ALL_COUNTRIES)
    print(f"Generating {len(urls)} pages for countries: {ALL_COUNTRIES}")
    for url in urls:
        d = build_page_data(url)
        html_out = render_page(d)
        path = os.path.join(OUT_DIR, f"{d['slug']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_out)
        print(f"wrote {path} ({len(html_out.encode())} bytes)")

if __name__ == "__main__":
    main()
