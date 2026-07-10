from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ──────────────────────────────────────────────
# COLOUR PALETTE (shared)
# ──────────────────────────────────────────────
PALETTES = {
    "api":   {"primary": colors.HexColor("#1A3C5E"),
              "accent":  colors.HexColor("#2E86C1"),
              "light":   colors.HexColor("#D6EAF8"),
              "mid":     colors.HexColor("#85C1E9"),
              "dark":    colors.HexColor("#0D2137")},
    "pbi":   {"primary": colors.HexColor("#742774"),
              "accent":  colors.HexColor("#F2C811"),
              "light":   colors.HexColor("#FDF5E6"),
              "mid":     colors.HexColor("#F5CBA7"),
              "dark":    colors.HexColor("#4A154B")},
    "ai":    {"primary": colors.HexColor("#1B4332"),
              "accent":  colors.HexColor("#40916C"),
              "light":   colors.HexColor("#D8F3DC"),
              "mid":     colors.HexColor("#74C69D"),
              "dark":    colors.HexColor("#081C15")},
}


def make_styles(pal):
    base = getSampleStyleSheet()

    def ps(name, parent="Normal", **kw):
        return ParagraphStyle(name, parent=base[parent], **kw)

    return {
        "title": ps("DocTitle",
                    fontSize=26, leading=32, textColor=colors.white,
                    alignment=TA_CENTER, spaceAfter=6, fontName="Helvetica-Bold"),
        "subtitle": ps("DocSub",
                       fontSize=13, leading=18, textColor=pal["mid"],
                       alignment=TA_CENTER, spaceAfter=4, fontName="Helvetica"),
        "meta": ps("DocMeta",
                   fontSize=9, leading=12, textColor=pal["light"],
                   alignment=TA_CENTER, fontName="Helvetica"),
        "h1": ps("H1", fontSize=14, leading=18, textColor=colors.white,
                 fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=4),
        "h2": ps("H2", fontSize=11, leading=15, textColor=pal["primary"],
                 fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=3),
        "h3": ps("H3", fontSize=10, leading=14, textColor=pal["accent"],
                 fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=2),
        "body": ps("Body", fontSize=9, leading=14, textColor=colors.HexColor("#2C2C2C"),
                   alignment=TA_JUSTIFY, spaceAfter=3, fontName="Helvetica"),
        "bullet": ps("Bullet", fontSize=9, leading=13, textColor=colors.HexColor("#2C2C2C"),
                     leftIndent=14, spaceAfter=2, fontName="Helvetica",
                     bulletIndent=4, bulletFontName="Helvetica"),
        "ref": ps("Ref", fontSize=8, leading=12, textColor=colors.HexColor("#555555"),
                  leftIndent=18, spaceAfter=1, fontName="Helvetica",
                  bulletIndent=8),
        "refhead": ps("RefHead", fontSize=9, leading=13,
                      textColor=pal["primary"], fontName="Helvetica-Bold",
                      spaceBefore=6, spaceAfter=2, leftIndent=0),
    }


def cover_block(story, pal, sty, title, subtitle, edition, description):
    """Full-width coloured cover using a Table."""
    cover_data = [[Paragraph(title,    sty["title"]),
                   Paragraph(subtitle, sty["subtitle"]),
                   Paragraph(edition,  sty["meta"]),
                   Paragraph(description, sty["meta"])]]
    cover_rows = [[Paragraph(title,       sty["title"])],
                  [Paragraph(subtitle,    sty["subtitle"])],
                  [Paragraph(edition,     sty["meta"])],
                  [Spacer(1, 6)],
                  [Paragraph(description, sty["meta"])]]
    t = Table([[row[0]] for row in cover_rows], colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), pal["primary"]),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [pal["primary"]]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.4*cm))


def section_header(story, pal, sty, number, title):
    """Coloured banner for a main section."""
    t = Table([[Paragraph(f"{number}. {title}", sty["h1"])]], colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), pal["accent"]),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [pal["accent"]]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*cm))


def subsection(story, sty, title):
    story.append(Paragraph(title, sty["h2"]))
    story.append(HRFlowable(width="100%", thickness=0.5,
                            color=colors.HexColor("#BBBBBB"), spaceAfter=2))


def point(story, sty, text):
    story.append(Paragraph(f"• {text}", sty["bullet"]))


def refs_block(story, sty, refs):
    story.append(Paragraph("📚 Bibliografía del tema:", sty["refhead"]))
    for r in refs:
        story.append(Paragraph(f"▸ {r}", sty["ref"]))
    story.append(Spacer(1, 0.3*cm))


# ══════════════════════════════════════════════
# PDF 1 — APIs y Desarrollo Web con Python
# ══════════════════════════════════════════════
def build_pdf1(path):
    pal = PALETTES["api"]
    doc = SimpleDocTemplate(path, pagesize=A4,
                            topMargin=1.8*cm, bottomMargin=1.8*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    sty = make_styles(pal)
    story = []

    # ── COVER ──
    cover_block(story, pal, sty,
                "PROGRAMA ACADÉMICO",
                "APIs con Python: HTTP, Autenticación, Serialización y Webhooks",
                "Edición 2024 · Nivel Intermedio-Avanzado",
                "Guía de estudio estructurada con bibliografía exacta por tema y subtema")
    story.append(Spacer(1, 0.5*cm))

    # Intro
    story.append(Paragraph(
        "Este programa proporciona una hoja de ruta completa para dominar el diseño, consumo y "
        "seguridad de APIs RESTful con Python. Cada tema incluye los puntos conceptuales "
        "específicos y las referencias bibliográficas precisas que el docente o estudiante "
        "debe consultar.",
        sty["body"]))
    story.append(Spacer(1, 0.4*cm))

    # ── TEMA 1 ──
    section_header(story, pal, sty, "TEMA 1", "VERBOS HTTP: GET, POST, PUT Y DELETE")

    subsection(story, sty, "1.1 Fundamentos del Protocolo HTTP")
    for p in [
        "Historia y evolución de HTTP/1.0 a HTTP/3.",
        "Estructura de una solicitud HTTP: request line, headers y body.",
        "Estructura de una respuesta HTTP: status line, headers y body.",
        "Códigos de estado HTTP: 1xx, 2xx, 3xx, 4xx, 5xx y sus significados.",
        "Diferencia entre HTTP y HTTPS; TLS/SSL en el contexto de APIs.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Fielding, R. T. (1999). Hypertext Transfer Protocol — HTTP/1.1. RFC 2616. IETF. https://www.rfc-editor.org/rfc/rfc2616",
        "Fielding, R. T., & Reschke, J. (2014). Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content. RFC 7231. IETF.",
        "Gourley, D., Totty, B., Sayer, M., Aggarwal, A., & Reddy, S. (2002). HTTP: The Definitive Guide. O'Reilly Media. ISBN: 978-1-56592-509-0",
        "Mozilla Developer Network (2024). HTTP. MDN Web Docs. https://developer.mozilla.org/es/docs/Web/HTTP",
    ])

    subsection(story, sty, "1.2 Verbo GET")
    for p in [
        "Semántica: recuperación de recursos sin modificar el estado del servidor.",
        "Idempotencia y seguridad del método GET según RFC 7231.",
        "Parámetros de consulta (query strings) y codificación URL.",
        "Paginación con GET: limit, offset, cursor-based pagination.",
        "Caché HTTP con GET: headers Cache-Control y ETag.",
        "Implementación en Python con Flask, FastAPI y requests.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Richardson, L., & Amundsen, M. (2013). RESTful Web APIs. O'Reilly Media. ISBN: 978-1-449-35806-8",
        "Masse, M. (2011). REST API Design Rulebook. O'Reilly Media. ISBN: 978-1-449-31050-9",
        "Grinberg, M. (2018). Flask Web Development. 2nd ed. O'Reilly Media. ISBN: 978-1-491-99173-2",
        "Abarca Romero, W. (2022). FastAPI: Desarrollo moderno de APIs. Independently published.",
    ])

    subsection(story, sty, "1.3 Verbo POST")
    for p in [
        "Semántica: creación de recursos y envío de datos al servidor.",
        "POST no es idempotente: implicaciones y manejo de duplicados.",
        "Cuerpo de la solicitud: JSON, form-data, multipart/form-data.",
        "Headers relevantes: Content-Type, Content-Length.",
        "Validación de datos en el servidor (Pydantic, Marshmallow).",
        "Respuestas apropiadas: 201 Created con header Location.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Richardson, L., & Amundsen, M. (2013). RESTful Web APIs. O'Reilly Media. ISBN: 978-1-449-35806-8",
        "Tiangolo, S. (2023). FastAPI Documentation. https://fastapi.tiangolo.com",
        "Lutz, M. (2019). Learning Python. 5th ed. O'Reilly Media. ISBN: 978-1-449-35573-9",
    ])

    subsection(story, sty, "1.4 Verbo PUT")
    for p in [
        "Semántica: reemplazo completo de un recurso existente.",
        "Idempotencia de PUT: múltiples llamadas producen el mismo resultado.",
        "PUT vs PATCH: cuándo usar cada uno (RFC 5789 para PATCH).",
        "Manejo de conflictos: código 409 Conflict.",
        "Uso correcto de URIs al actualizar recursos.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Dury, R. (2010). HTTP PATCH Method. RFC 5789. IETF. https://www.rfc-editor.org/rfc/rfc5789",
        "Masse, M. (2011). REST API Design Rulebook. O'Reilly Media. ISBN: 978-1-449-31050-9",
        "Richardson, L., Amundsen, M., & Ruby, S. (2013). RESTful Web Services Cookbook. O'Reilly Media. ISBN: 978-0-596-80168-7",
    ])

    subsection(story, sty, "1.5 Verbo DELETE")
    for p in [
        "Semántica: eliminación de un recurso identificado por la URI.",
        "Idempotencia del método DELETE.",
        "Soft delete vs hard delete: estrategias de diseño.",
        "Respuestas apropiadas: 200 OK, 204 No Content, 404 Not Found.",
        "Protección contra borrados accidentales: confirmación y permisos.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Fielding, R. T., & Reschke, J. (2014). RFC 7231. IETF.",
        "Richardson, L., & Amundsen, M. (2013). RESTful Web APIs. O'Reilly Media.",
        "Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly Media. ISBN: 978-1-449-37332-0",
    ])

    story.append(PageBreak())

    # ── TEMA 2 ──
    section_header(story, pal, sty, "TEMA 2", "AUTENTICACIÓN: JWT Y OAUTH2")

    subsection(story, sty, "2.1 Conceptos Generales de Autenticación y Autorización")
    for p in [
        "Diferencia entre autenticación (¿quién eres?) y autorización (¿qué puedes hacer?).",
        "Sesiones vs tokens: ventajas y desventajas en APIs.",
        "Mecanismos básicos: HTTP Basic Auth, API Keys.",
        "HTTPS como requisito mínimo para cualquier esquema de autenticación.",
        "OWASP Top 10 para APIs: broken authentication y exposición de datos.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Madden, N. (2020). API Security in Action. Manning Publications. ISBN: 978-1-617-29598-3",
        "OWASP Foundation (2023). OWASP API Security Top 10. https://owasp.org/API-Security/",
        "Schwartz, B., & Yaworski, P. (2021). Real-World Bug Hunting. No Starch Press. ISBN: 978-1-593-27896-5",
    ])

    subsection(story, sty, "2.2 JSON Web Tokens (JWT)")
    for p in [
        "Estructura de un JWT: Header.Payload.Signature (RFC 7519).",
        "Algoritmos de firma: HS256, RS256, ES256 — diferencias y cuándo usar cada uno.",
        "Claims estándar: iss, sub, aud, exp, nbf, iat, jti.",
        "Claims personalizados y buenas prácticas de diseño del payload.",
        "Flujo completo: generación, transmisión y verificación del token.",
        "Almacenamiento seguro en el cliente: localStorage vs HttpOnly cookies.",
        "Revocación de tokens y manejo de tokens expirados.",
        "Implementación en Python con la biblioteca PyJWT.",
        "Vulnerabilidades comunes: algoritmo 'none', weak secrets, token hijacking.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Jones, M., Bradley, J., & Sakimura, N. (2015). JSON Web Token (JWT). RFC 7519. IETF. https://www.rfc-editor.org/rfc/rfc7519",
        "Jones, M., & Hildebrand, J. (2015). JSON Web Encryption (JWE). RFC 7516. IETF.",
        "Parecki, A. (2020). OAuth 2.0 Simplified. Okta. https://www.oauth.com",
        "Madden, N. (2020). API Security in Action. Manning Publications. ISBN: 978-1-617-29598-3",
        "PyJWT Team (2023). PyJWT Documentation. https://pyjwt.readthedocs.io",
    ])

    subsection(story, sty, "2.3 OAuth 2.0")
    for p in [
        "Roles de OAuth 2.0: Resource Owner, Client, Authorization Server, Resource Server.",
        "Flujos (grants): Authorization Code, Implicit (obsoleto), Client Credentials, Resource Owner Password.",
        "Authorization Code Flow con PKCE para aplicaciones móviles y SPA.",
        "Tokens de acceso (access token) y tokens de refresco (refresh token).",
        "Scopes: definición y uso para control de acceso granular.",
        "Implementación con Authlib y python-oauth2 en Python.",
        "OpenID Connect (OIDC): capa de identidad sobre OAuth 2.0.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Hardt, D. (2012). The OAuth 2.0 Authorization Framework. RFC 6749. IETF. https://www.rfc-editor.org/rfc/rfc6749",
        "Sakimura, N., et al. (2014). OpenID Connect Core 1.0. OpenID Foundation. https://openid.net/specs/openid-connect-core-1_0.html",
        "Parecki, A. (2020). OAuth 2.0 Simplified. Okta. https://www.oauth.com",
        "Madden, N. (2020). API Security in Action. Manning Publications. ISBN: 978-1-617-29598-3",
        "Authlib Team (2023). Authlib Documentation. https://docs.authlib.org",
    ])

    story.append(PageBreak())

    # ── TEMA 3 ──
    section_header(story, pal, sty, "TEMA 3", "SERIALIZACIÓN: JSON, XML Y PROTOCOL BUFFERS")

    subsection(story, sty, "3.1 Principios de Serialización")
    for p in [
        "Definición: conversión de estructuras de datos en memoria a un formato transferible.",
        "Serialización vs marshalling: diferencias conceptuales.",
        "Criterios de elección: legibilidad, tamaño, velocidad, interoperabilidad.",
        "Tipos de datos y sus representaciones en distintos formatos.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Kleppmann, M. (2017). Designing Data-Intensive Applications. Cap. 4: Encoding and Evolution. O'Reilly Media. ISBN: 978-1-449-37332-0",
        "Richardson, L., & Amundsen, M. (2013). RESTful Web APIs. O'Reilly Media. ISBN: 978-1-449-35806-8",
    ])

    subsection(story, sty, "3.2 JSON (JavaScript Object Notation)")
    for p in [
        "Especificación RFC 8259 y ECMA-404: tipos de datos válidos.",
        "Módulo json de Python: json.dumps(), json.loads(), json.dump(), json.load().",
        "Manejo de tipos no serializables: datetime, Decimal, UUID — encoders personalizados.",
        "Validación de esquemas JSON con jsonschema y Pydantic.",
        "JSON Lines (JSONL) para flujos de datos.",
        "Rendimiento: ujson, orjson como alternativas más rápidas.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Bray, T. (Ed.). (2017). The JavaScript Object Notation (JSON) Data Interchange Format. RFC 8259. IETF. https://www.rfc-editor.org/rfc/rfc8259",
        "Python Software Foundation (2024). json — JSON encoder and decoder. Python Docs. https://docs.python.org/3/library/json.html",
        "Percival, H., & Gregory, B. (2020). Architecture Patterns with Python. O'Reilly Media. ISBN: 978-1-492-05279-9",
        "Pydantic Team (2024). Pydantic v2 Documentation. https://docs.pydantic.dev",
    ])

    subsection(story, sty, "3.3 XML (Extensible Markup Language)")
    for p in [
        "Estructura XML: elementos, atributos, namespaces, DTD y XML Schema (XSD).",
        "Parsers en Python: xml.etree.ElementTree, lxml, minidom.",
        "SAX vs DOM: diferencias de rendimiento y uso de memoria.",
        "XPath y XQuery para navegación en documentos XML.",
        "Conversión entre XML y diccionarios Python con xmltodict.",
        "Casos de uso actuales: SOAP, RSS, configuraciones empresariales.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Bray, T., et al. (2008). Extensible Markup Language (XML) 1.0. 5th ed. W3C. https://www.w3.org/TR/xml/",
        "Python Software Foundation (2024). xml.etree.ElementTree. Python Docs. https://docs.python.org/3/library/xml.etree.elementtree.html",
        "Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly Media. ISBN: 978-1-449-37332-0",
    ])

    subsection(story, sty, "3.4 Protocol Buffers (Protobuf)")
    for p in [
        "Origen: desarrollado por Google para comunicación interna eficiente.",
        "Definición de esquemas con archivos .proto (proto3).",
        "Tipos de datos: scalar, message, enum, repeated fields, maps.",
        "Compilación del esquema con protoc y generación de código Python.",
        "Serialización y deserialización binaria: ventajas en tamaño y velocidad.",
        "gRPC: framework RPC de alto rendimiento basado en Protobuf.",
        "Comparación de rendimiento: JSON vs XML vs Protobuf.",
        "Well-known types y Any para extensibilidad.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Google LLC (2024). Protocol Buffers Documentation. https://protobuf.dev",
        "Google LLC (2024). gRPC Documentation. https://grpc.io/docs/languages/python/",
        "Kleppmann, M. (2017). Designing Data-Intensive Applications. Cap. 4. O'Reilly Media. ISBN: 978-1-449-37332-0",
        "Indrasiri, K., & Kuruppu, D. (2021). gRPC: Up and Running. O'Reilly Media. ISBN: 978-1-492-05833-3",
    ])

    story.append(PageBreak())

    # ── TEMA 4 ──
    section_header(story, pal, sty, "TEMA 4", "WEBHOOKS: NOTIFICACIONES EN TIEMPO REAL")

    subsection(story, sty, "4.1 Concepto y Arquitectura de Webhooks")
    for p in [
        "Definición: callbacks HTTP inversos disparados por eventos en un servicio externo.",
        "Webhooks vs polling: comparativa de eficiencia y latencia.",
        "Webhooks vs WebSockets vs SSE: cuándo usar cada paradigma.",
        "Arquitectura event-driven: productor de eventos, consumidor, payload.",
        "Casos de uso reales: Stripe (pagos), GitHub (CI/CD), Slack, Twilio.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Percival, H., & Gregory, B. (2020). Architecture Patterns with Python. O'Reilly Media. ISBN: 978-1-492-05279-9",
        "Richardson, C. (2018). Microservices Patterns. Manning Publications. ISBN: 978-1-617-29433-7",
        "Webhook.site (2024). What is a Webhook? https://webhook.site/docs",
    ])

    subsection(story, sty, "4.2 Implementación de un Endpoint Receptor")
    for p in [
        "Configuración de un endpoint HTTP POST para recibir payloads.",
        "Implementación con Flask: manejo de request.get_json() y cabeceras.",
        "Implementación con FastAPI: body parsing con Pydantic models.",
        "Respuesta inmediata con 200 OK para evitar reintentos del emisor.",
        "Procesamiento asíncrono con Celery o asyncio para tareas largas.",
        "Registro (logging) estructurado de todos los webhooks recibidos.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Grinberg, M. (2018). Flask Web Development. 2nd ed. O'Reilly Media. ISBN: 978-1-491-99173-2",
        "Tiangolo, S. (2023). FastAPI Documentation. https://fastapi.tiangolo.com",
        "Percival, H., & Gregory, B. (2020). Architecture Patterns with Python. O'Reilly Media. ISBN: 978-1-492-05279-9",
    ])

    subsection(story, sty, "4.3 Seguridad y Verificación de Firmas")
    for p in [
        "Verificación de origen: validación de firma HMAC-SHA256 (firma de Stripe, GitHub).",
        "Implementación Python con hmac.compare_digest para evitar timing attacks.",
        "Uso de cabeceras secretas compartidas (X-Hub-Signature, Stripe-Signature).",
        "Lista de IPs permitidas (IP whitelisting) como capa adicional.",
        "HTTPS obligatorio para todos los endpoints de webhook.",
        "Manejo de reintentos y idempotencia con IDs de evento únicos.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Madden, N. (2020). API Security in Action. Manning Publications. ISBN: 978-1-617-29598-3",
        "Stripe Inc. (2024). Webhook Signatures. Stripe Documentation. https://stripe.com/docs/webhooks/signatures",
        "GitHub Inc. (2024). Securing your webhooks. GitHub Docs. https://docs.github.com/en/webhooks/using-webhooks/securing-your-webhooks",
        "Python Software Foundation (2024). hmac — Keyed-Hashing for Message Authentication. Python Docs.",
    ])

    subsection(story, sty, "4.4 Pruebas y Depuración de Webhooks en Desarrollo")
    for p in [
        "Uso de ngrok para exponer servidores locales al internet.",
        "Stripe CLI para simular eventos de webhook en desarrollo.",
        "Postman: envío manual de payloads para pruebas.",
        "Estrategias de reintentos: exponential backoff en el servidor emisor.",
        "Almacenamiento de eventos en base de datos para auditoría.",
        "Monitoreo con Sentry y logging centralizado.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Percival, H., & Gregory, B. (2020). Architecture Patterns with Python. O'Reilly Media. ISBN: 978-1-492-05279-9",
        "ngrok Inc. (2024). ngrok Documentation. https://ngrok.com/docs",
        "Stripe Inc. (2024). Test webhooks with the Stripe CLI. https://stripe.com/docs/stripe-cli/webhooks",
    ])

    # Final bibliography
    story.append(PageBreak())
    section_header(story, pal, sty, "REF", "BIBLIOGRAFÍA GENERAL CONSOLIDADA")
    story.append(Spacer(1, 0.3*cm))
    general_refs = [
        "Fielding, R. T., & Reschke, J. (2014). Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content. RFC 7231. IETF.",
        "Richardson, L., & Amundsen, M. (2013). RESTful Web APIs. O'Reilly Media. ISBN: 978-1-449-35806-8",
        "Masse, M. (2011). REST API Design Rulebook. O'Reilly Media. ISBN: 978-1-449-31050-9",
        "Jones, M., Bradley, J., & Sakimura, N. (2015). JSON Web Token (JWT). RFC 7519. IETF.",
        "Hardt, D. (2012). The OAuth 2.0 Authorization Framework. RFC 6749. IETF.",
        "Madden, N. (2020). API Security in Action. Manning Publications. ISBN: 978-1-617-29598-3",
        "Parecki, A. (2020). OAuth 2.0 Simplified. Okta. https://www.oauth.com",
        "Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly Media. ISBN: 978-1-449-37332-0",
        "Grinberg, M. (2018). Flask Web Development. 2nd ed. O'Reilly Media. ISBN: 978-1-491-99173-2",
        "Tiangolo, S. (2023). FastAPI Documentation. https://fastapi.tiangolo.com",
        "Percival, H., & Gregory, B. (2020). Architecture Patterns with Python. O'Reilly Media. ISBN: 978-1-492-05279-9",
        "Google LLC (2024). Protocol Buffers Documentation. https://protobuf.dev",
        "Indrasiri, K., & Kuruppu, D. (2021). gRPC: Up and Running. O'Reilly Media. ISBN: 978-1-492-05833-3",
        "OWASP Foundation (2023). OWASP API Security Top 10. https://owasp.org/API-Security/",
        "Richardson, C. (2018). Microservices Patterns. Manning Publications. ISBN: 978-1-617-29433-7",
    ]
    for r in general_refs:
        story.append(Paragraph(f"▸ {r}", sty["ref"]))
        story.append(Spacer(1, 0.1*cm))

    doc.build(story)
    print(f"PDF 1 generado: {path}")


# ══════════════════════════════════════════════
# PDF 2 — Power BI
# ══════════════════════════════════════════════
def build_pdf2(path):
    pal = PALETTES["pbi"]
    doc = SimpleDocTemplate(path, pagesize=A4,
                            topMargin=1.8*cm, bottomMargin=1.8*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    sty = make_styles(pal)
    story = []

    cover_block(story, pal, sty,
                "PROGRAMA ACADÉMICO",
                "Microsoft Power BI: Del Dato al Dashboard",
                "Edición 2024 · Niveles Básico, Intermedio y Avanzado",
                "Plan de estudios completo con bibliografía exacta por tema y subtema")
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "Programa diseñado para dominar Power BI Desktop, Power Query (M), DAX, "
        "el servicio en la nube y la integración empresarial. Cada sección incluye "
        "puntos concretos y las fuentes bibliográficas precisas para el docente y el alumno.",
        sty["body"]))
    story.append(Spacer(1, 0.4*cm))

    # ── TEMA 1 ──
    section_header(story, pal, sty, "TEMA 1", "INTRODUCCIÓN A POWER BI Y SU ECOSISTEMA")

    subsection(story, sty, "1.1 ¿Qué es Power BI?")
    for p in [
        "Definición de Business Intelligence y su importancia estratégica.",
        "Componentes del ecosistema: Power BI Desktop, Power BI Service, Power BI Mobile.",
        "Power BI Report Server: diferencias con el servicio en la nube.",
        "Power BI Embedded: integración en aplicaciones propias.",
        "Licenciamiento: Free, Pro, Premium Per User (PPU), Premium Capacity.",
        "Roadmap y ciclo de actualizaciones mensuales de Microsoft.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Ferrari, A., & Russo, M. (2020). Analyzing Data with Power BI and Power Pivot for Excel. Microsoft Press. ISBN: 978-1-509-30-4",
        "Aspin, A. (2022). Pro Power BI Desktop. 4th ed. Apress. ISBN: 978-1-484-27814-2",
        "Microsoft Corporation (2024). Power BI Documentation. https://learn.microsoft.com/es-es/power-bi/",
        "Alexander, M., & Kusleika, R. (2022). Excel 2019 Power Programming with VBA. Wiley. ISBN: 978-1-119-51432-7",
    ])

    subsection(story, sty, "1.2 Instalación y Entorno de Trabajo")
    for p in [
        "Descarga e instalación de Power BI Desktop (requisitos del sistema).",
        "Configuración regional y de idioma.",
        "Interfaz de usuario: paneles de Informe, Datos y Modelo.",
        "Cinta de opciones: vistas y accesos directos clave.",
        "Configuración de opciones globales y del archivo actual.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Aspin, A. (2022). Pro Power BI Desktop. 4th ed. Apress. ISBN: 978-1-484-27814-2",
        "Clark, A., & Sherpa, B. (2020). Microsoft Power BI Quick Start Guide. 2nd ed. Packt Publishing. ISBN: 978-1-800-20184-5",
    ])

    story.append(PageBreak())
    # ── TEMA 2 ──
    section_header(story, pal, sty, "TEMA 2", "CONEXIÓN Y TRANSFORMACIÓN DE DATOS CON POWER QUERY")

    subsection(story, sty, "2.1 Conectores de Datos")
    for p in [
        "Conectores de archivo: Excel, CSV, JSON, XML, PDF.",
        "Conectores de base de datos: SQL Server, MySQL, PostgreSQL, Oracle.",
        "Conectores de servicios en la nube: Azure, SharePoint, Google Analytics, Salesforce.",
        "Conectores web: importación desde URL y APIs REST.",
        "Actualización de datos: DirectQuery vs Import vs Dual.",
        "Parámetros de conexión y almacenamiento de credenciales.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Webb, C., & Lachev, T. (2014). Power Query for Power BI and Excel. Apress. ISBN: 978-1-430-26619-9",
        "Microsoft Corporation (2024). Conectores en Power Query. https://learn.microsoft.com/es-es/power-query/connectors/",
        "Ferrari, A., & Russo, M. (2020). Analyzing Data with Power BI and Power Pivot for Excel. Microsoft Press.",
    ])

    subsection(story, sty, "2.2 Transformación de Datos con Power Query (M)")
    for p in [
        "Interfaz del Editor de Power Query: paneles Consultas, Configuración y Vista previa.",
        "Pasos aplicados: naturaleza declarativa y reproducibilidad.",
        "Operaciones esenciales: filtrar, ordenar, agrupar, dinamizar y anular dinamización.",
        "Tipos de datos: detección, cambio y errores comunes.",
        "Combinar consultas: Merge (JOIN) y Append (UNION).",
        "Columnas personalizadas con fórmulas M.",
        "Lenguaje M: sintaxis básica, funciones Text.*, Date.*, List.*, Table.*.",
        "Gestión de valores nulos y errores en transformaciones.",
        "Parámetros y funciones reutilizables en M.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Webb, C., & Lachev, T. (2014). Power Query for Power BI and Excel. Apress. ISBN: 978-1-430-26619-9",
        "Giles, K. (2019). Power Query Cookbook. Packt Publishing. ISBN: 978-1-800-20800-4",
        "Microsoft Corporation (2024). Referencia del lenguaje de fórmulas de Power Query M. https://learn.microsoft.com/es-es/powerquery-m/",
    ])

    story.append(PageBreak())
    # ── TEMA 3 ──
    section_header(story, pal, sty, "TEMA 3", "MODELADO DE DATOS")

    subsection(story, sty, "3.1 Fundamentos del Modelo de Datos")
    for p in [
        "Vista de Modelo: gestión de tablas y relaciones.",
        "Tipos de relaciones: uno a uno, uno a muchos, muchos a muchos.",
        "Dirección del filtro cruzado: unidireccional vs bidireccional.",
        "Cardinalidad y su impacto en el rendimiento.",
        "Tablas de hechos vs tablas de dimensiones.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Ferrari, A., & Russo, M. (2020). Analyzing Data with Power BI and Power Pivot for Excel. Microsoft Press. ISBN: 978-1-509-30-4",
        "Kimball, R., & Ross, M. (2013). The Data Warehouse Toolkit. 3rd ed. Wiley. ISBN: 978-1-118-53080-1",
    ])

    subsection(story, sty, "3.2 Esquemas de Modelado")
    for p in [
        "Esquema estrella (Star Schema): tabla de hechos central y dimensiones.",
        "Esquema copo de nieve (Snowflake Schema): ventajas y desventajas.",
        "Modelos planos vs modelos relacionales en Power BI.",
        "Tabla de fechas: importancia y creación con DAX o Power Query.",
        "Roles de seguridad a nivel de fila (RLS): definición de filtros por rol.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Kimball, R., & Ross, M. (2013). The Data Warehouse Toolkit. 3rd ed. Wiley. ISBN: 978-1-118-53080-1",
        "Ferrari, A., & Russo, M. (2015). Microsoft Excel 2013: Building Data Models with PowerPivot. Microsoft Press. ISBN: 978-0-735-66696-7",
        "Aspin, A. (2022). Pro Power BI Desktop. 4th ed. Apress. ISBN: 978-1-484-27814-2",
    ])

    story.append(PageBreak())
    # ── TEMA 4 ──
    section_header(story, pal, sty, "TEMA 4", "DAX: DATA ANALYSIS EXPRESSIONS")

    subsection(story, sty, "4.1 Fundamentos de DAX")
    for p in [
        "¿Qué es DAX? Diferencias con fórmulas de Excel.",
        "Columnas calculadas vs Medidas vs Tablas calculadas.",
        "Contexto de fila vs contexto de filtro: el concepto más importante de DAX.",
        "Funciones básicas: SUM, COUNT, AVERAGE, MIN, MAX, IF, SWITCH.",
        "Funciones de texto: CONCATENATE, LEFT, RIGHT, MID, FORMAT.",
        "Funciones de fecha: TODAY, NOW, YEAR, MONTH, DAY, DATEDIFF.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Russo, M., & Ferrari, A. (2019). The Definitive Guide to DAX. 2nd ed. Microsoft Press. ISBN: 978-1-509-30765-5",
        "Ferrari, A., & Russo, M. (2020). Analyzing Data with Power BI and Power Pivot for Excel. Microsoft Press.",
        "Microsoft Corporation (2024). Referencia de funciones DAX. https://learn.microsoft.com/es-es/dax/dax-function-reference",
    ])

    subsection(story, sty, "4.2 DAX Intermedio y Avanzado")
    for p in [
        "Funciones de inteligencia de tiempo: TOTALYTD, SAMEPERIODLASTYEAR, DATEADD, DATESBETWEEN.",
        "CALCULATE: la función más poderosa de DAX — modificación del contexto de filtro.",
        "FILTER, ALL, ALLEXCEPT, REMOVEFILTERS: manipulación del contexto.",
        "Variables DAX (VAR ... RETURN): legibilidad y rendimiento.",
        "Funciones de tabla: SUMMARIZE, ADDCOLUMNS, CROSSJOIN, GENERATE.",
        "Iteradores: SUMX, AVERAGEX, RANKX, MAXX, MINX.",
        "Medidas de porcentaje, variación y acumulados.",
        "Optimización de fórmulas DAX con DAX Studio.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Russo, M., & Ferrari, A. (2019). The Definitive Guide to DAX. 2nd ed. Microsoft Press. ISBN: 978-1-509-30765-5",
        "Collie, R., & Singh, A. (2016). Power Pivot and Power BI: The Excel User's Guide to DAX. Holy Macro! Books. ISBN: 978-1-615-47049-2",
        "DAX Studio Team (2024). DAX Studio Documentation. https://daxstudio.org",
    ])

    story.append(PageBreak())
    # ── TEMA 5 ──
    section_header(story, pal, sty, "TEMA 5", "VISUALIZACIONES Y DISEÑO DE REPORTES")

    subsection(story, sty, "5.1 Tipos de Visualizaciones")
    for p in [
        "Gráficos básicos: barras, columnas, líneas, áreas, circulares.",
        "Gráficos de dispersión (scatter) y de burbujas.",
        "Mapas: mapas de burbujas, mapas coropléticos y mapas de forma.",
        "Tablas y matrices: formato condicional, totales y subtotales.",
        "Tarjetas (cards) y medidores (gauges) para KPIs.",
        "Gráficos de cascada (waterfall) y embudos (funnel).",
        "Treemap y gráficos de anillos.",
        "Visualizaciones de IA: narrativa inteligente, preguntas y respuestas, árbol de descomposición.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Few, S. (2012). Show Me the Numbers: Designing Tables and Graphs to Enlighten. 2nd ed. Analytics Press. ISBN: 978-0-970-60199-7",
        "Knaflic, C. N. (2015). Storytelling with Data: A Data Visualization Guide for Business Professionals. Wiley. ISBN: 978-1-119-00225-3",
        "Aspin, A. (2022). Pro Power BI Desktop. 4th ed. Apress. ISBN: 978-1-484-27814-2",
    ])

    subsection(story, sty, "5.2 Diseño de Dashboards Efectivos")
    for p in [
        "Principios de diseño visual: jerarquía, contraste, alineación, proximidad.",
        "Selección del gráfico correcto según el tipo de mensaje.",
        "Uso del color: paletas accesibles, semáforos, branding corporativo.",
        "Interactividad: segmentadores, filtros cruzados, drill-through, marcadores.",
        "Tooltips personalizados: tooltips de página.",
        "Diseño responsive: vistas de teléfono y tablet.",
        "Guías de estilo corporativo y plantillas (.pbit).",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Knaflic, C. N. (2015). Storytelling with Data. Wiley. ISBN: 978-1-119-00225-3",
        "Ware, C. (2012). Information Visualization: Perception for Design. 3rd ed. Morgan Kaufmann. ISBN: 978-0-123-81464-7",
        "Clark, A., & Sherpa, B. (2020). Microsoft Power BI Quick Start Guide. 2nd ed. Packt Publishing. ISBN: 978-1-800-20184-5",
    ])

    subsection(story, sty, "5.3 Visualizaciones Personalizadas")
    for p in [
        "AppSource: exploración e instalación de visuales de terceros.",
        "Visuales certificados por Microsoft vs no certificados.",
        "Introducción al desarrollo de visuales con Power BI Visuals SDK (TypeScript/D3.js).",
        "Visuals populares: Gantt, Timeline, Bullet Chart, Hierarchy Slicer.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Microsoft Corporation (2024). Develop a Power BI visual. https://learn.microsoft.com/en-us/power-bi/developer/visuals/",
        "Aspin, A. (2022). Pro Power BI Desktop. 4th ed. Apress.",
    ])

    story.append(PageBreak())
    # ── TEMA 6 ──
    section_header(story, pal, sty, "TEMA 6", "POWER BI SERVICE Y COLABORACIÓN EN LA NUBE")

    subsection(story, sty, "6.1 Publicación y Administración")
    for p in [
        "Publicación de informes desde Desktop al Service.",
        "Áreas de trabajo (Workspaces): clásicos vs modernos.",
        "Conjuntos de datos compartidos y reutilización entre informes.",
        "Actualización programada de datos: gateways de datos.",
        "Power BI Gateway (personal y empresarial): configuración y solución de problemas.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Microsoft Corporation (2024). Power BI Service Documentation. https://learn.microsoft.com/es-es/power-bi/fundamentals/",
        "Ferrari, A., & Russo, M. (2020). Analyzing Data with Power BI and Power Pivot for Excel. Microsoft Press.",
        "Aspin, A. (2022). Pro Power BI Desktop. 4th ed. Apress. ISBN: 978-1-484-27814-2",
    ])

    subsection(story, sty, "6.2 Seguridad, Distribución e Integración")
    for p in [
        "Row-Level Security (RLS) dinámica con USERNAME() y USERPRINCIPALNAME().",
        "Aplicaciones de Power BI: empaquetado y distribución a usuarios finales.",
        "Inserción de informes en Teams, SharePoint y aplicaciones web (embed).",
        "Power BI REST API: automatización con Python y Power Automate.",
        "Alertas de datos y suscripciones a informes.",
        "Linaje de datos y análisis de impacto.",
        "Power BI Premium: conjuntos de datos grandes, paginación avanzada, XMLA.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Microsoft Corporation (2024). Power BI REST API. https://learn.microsoft.com/es-es/rest/api/power-bi/",
        "Clark, A., & Sherpa, B. (2020). Microsoft Power BI Quick Start Guide. 2nd ed. Packt Publishing.",
        "Russo, M., & Ferrari, A. (2019). The Definitive Guide to DAX. 2nd ed. Microsoft Press.",
    ])

    # Bibliografía general
    story.append(PageBreak())
    section_header(story, pal, sty, "REF", "BIBLIOGRAFÍA GENERAL CONSOLIDADA")
    story.append(Spacer(1, 0.3*cm))
    for r in [
        "Ferrari, A., & Russo, M. (2020). Analyzing Data with Power BI and Power Pivot for Excel. Microsoft Press. ISBN: 978-1-509-30-4",
        "Russo, M., & Ferrari, A. (2019). The Definitive Guide to DAX. 2nd ed. Microsoft Press. ISBN: 978-1-509-30765-5",
        "Aspin, A. (2022). Pro Power BI Desktop. 4th ed. Apress. ISBN: 978-1-484-27814-2",
        "Webb, C., & Lachev, T. (2014). Power Query for Power BI and Excel. Apress. ISBN: 978-1-430-26619-9",
        "Giles, K. (2019). Power Query Cookbook. Packt Publishing. ISBN: 978-1-800-20800-4",
        "Clark, A., & Sherpa, B. (2020). Microsoft Power BI Quick Start Guide. 2nd ed. Packt Publishing. ISBN: 978-1-800-20184-5",
        "Collie, R., & Singh, A. (2016). Power Pivot and Power BI: The Excel User's Guide to DAX. Holy Macro! Books. ISBN: 978-1-615-47049-2",
        "Kimball, R., & Ross, M. (2013). The Data Warehouse Toolkit. 3rd ed. Wiley. ISBN: 978-1-118-53080-1",
        "Knaflic, C. N. (2015). Storytelling with Data. Wiley. ISBN: 978-1-119-00225-3",
        "Few, S. (2012). Show Me the Numbers. 2nd ed. Analytics Press. ISBN: 978-0-970-60199-7",
        "Ware, C. (2012). Information Visualization: Perception for Design. 3rd ed. Morgan Kaufmann. ISBN: 978-0-123-81464-7",
        "Microsoft Corporation (2024). Power BI Documentation. https://learn.microsoft.com/es-es/power-bi/",
        "Microsoft Corporation (2024). Referencia de funciones DAX. https://learn.microsoft.com/es-es/dax/",
        "Microsoft Corporation (2024). Referencia del lenguaje M. https://learn.microsoft.com/es-es/powerquery-m/",
    ]:
        story.append(Paragraph(f"▸ {r}", sty["ref"]))
        story.append(Spacer(1, 0.1*cm))

    doc.build(story)
    print(f"PDF 2 generado: {path}")


# ══════════════════════════════════════════════
# PDF 3 — IA, ML, Deep Learning, LLMs, Transformers
# ══════════════════════════════════════════════
def build_pdf3(path):
    pal = PALETTES["ai"]
    doc = SimpleDocTemplate(path, pagesize=A4,
                            topMargin=1.8*cm, bottomMargin=1.8*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    sty = make_styles(pal)
    story = []

    cover_block(story, pal, sty,
                "PROGRAMA ACADÉMICO",
                "Inteligencia Artificial: ML, Deep Learning, LLMs y Modelos Transformer",
                "Edición 2024 · Nivel Fundacional a Avanzado",
                "Plan de estudios con puntos específicos, bibliografía exacta y papers seminales")
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "Este programa cubre el espectro completo de la IA moderna: desde los fundamentos "
        "matemáticos del Machine Learning hasta los grandes modelos de lenguaje (LLMs) "
        "y su despliegue en producción. Cada tema incluye los conceptos concretos a abordar "
        "y las fuentes primarias y secundarias más relevantes.",
        sty["body"]))
    story.append(Spacer(1, 0.4*cm))

    # ── TEMA 1 ──
    section_header(story, pal, sty, "TEMA 1", "FUNDAMENTOS MATEMÁTICOS PARA IA/ML")

    subsection(story, sty, "1.1 Álgebra Lineal")
    for p in [
        "Vectores, matrices y tensores: operaciones fundamentales.",
        "Producto punto, multiplicación de matrices y su significado geométrico.",
        "Eigenvalores y eigenvectores: aplicaciones en PCA.",
        "Descomposición SVD (Singular Value Decomposition).",
        "Normas de vectores y matrices: L1, L2, Frobenius.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. Cap. 2: Linear Algebra. MIT Press. ISBN: 978-0-262-03561-3. Disponible en: https://www.deeplearningbook.org",
        "Strang, G. (2016). Introduction to Linear Algebra. 5th ed. Wellesley-Cambridge Press. ISBN: 978-0-980-23272-4",
        "3Blue1Brown (2016). Essence of Linear Algebra [Serie de videos]. YouTube. https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab",
    ])

    subsection(story, sty, "1.2 Cálculo y Optimización")
    for p in [
        "Derivadas parciales y gradientes: intuición geométrica.",
        "Regla de la cadena (chain rule): base del backpropagation.",
        "Descenso del gradiente (GD): batch, mini-batch y estocástico (SGD).",
        "Algoritmos de optimización avanzados: Momentum, RMSprop, Adam, AdaGrad.",
        "Funciones de pérdida: MSE, MAE, Cross-Entropy, Binary Cross-Entropy.",
        "Hyperparámetros: tasa de aprendizaje, schedulers (step decay, cosine annealing).",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. Cap. 4: Numerical Computation & Cap. 8: Optimization. MIT Press.",
        "Kingma, D. P., & Ba, J. (2015). Adam: A Method for Stochastic Optimization. ICLR 2015. arXiv:1412.6980",
        "Ruder, S. (2016). An overview of gradient descent optimization algorithms. arXiv:1609.04747",
    ])

    subsection(story, sty, "1.3 Estadística y Probabilidad")
    for p in [
        "Distribuciones de probabilidad: gaussiana, Bernoulli, categórica.",
        "Teorema de Bayes y su aplicación en clasificadores.",
        "Estimación de máxima verosimilitud (MLE) y MAP.",
        "Bias-variance tradeoff: overfitting y underfitting.",
        "Métricas de evaluación: accuracy, precision, recall, F1, AUC-ROC, MAE, RMSE.",
        "Validación cruzada (k-fold cross-validation).",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. Cap. 3: Probability and Information Theory. MIT Press.",
        "Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer. ISBN: 978-0-387-31073-2",
        "James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An Introduction to Statistical Learning. 2nd ed. Springer. ISBN: 978-1-071-61418-1. Disponible en: https://www.statlearning.com",
    ])

    story.append(PageBreak())

    # ── TEMA 2 ──
    section_header(story, pal, sty, "TEMA 2", "MACHINE LEARNING CLÁSICO")

    subsection(story, sty, "2.1 Aprendizaje Supervisado")
    for p in [
        "Regresión lineal y logística: fundamentos y regularización (L1/Lasso, L2/Ridge).",
        "Árboles de decisión: criterios de división (Gini, Entropía), poda.",
        "Random Forest: bagging, importancia de características.",
        "Gradient Boosting: XGBoost, LightGBM, CatBoost.",
        "Support Vector Machines (SVM): kernel trick, márgenes.",
        "K-Nearest Neighbors (KNN): distancias y curse of dimensionality.",
        "Naive Bayes: suposición de independencia condicional.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow. 3rd ed. O'Reilly Media. ISBN: 978-1-098-12597-4",
        "Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer. ISBN: 978-0-387-31073-2",
        "James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An Introduction to Statistical Learning. 2nd ed. Springer.",
        "Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. KDD 2016. arXiv:1603.02754",
    ])

    subsection(story, sty, "2.2 Aprendizaje No Supervisado")
    for p in [
        "Clustering: K-Means, K-Medoids, DBSCAN, Gaussian Mixture Models.",
        "Reducción de dimensionalidad: PCA, t-SNE, UMAP.",
        "Detección de anomalías: Isolation Forest, Local Outlier Factor.",
        "Modelos de temas (topic modeling): LDA (Latent Dirichlet Allocation).",
        "Aprendizaje por refuerzo: Q-Learning, política y valor, MDP.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow. 3rd ed. O'Reilly Media.",
        "Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction. 2nd ed. MIT Press. ISBN: 978-0-262-03924-6. Disponible en: http://incompleteideas.net/book/the-book.html",
        "McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv:1802.03426",
    ])

    subsection(story, sty, "2.3 Pipelines y Herramientas")
    for p in [
        "Scikit-learn: Pipeline, ColumnTransformer, GridSearchCV, RandomizedSearchCV.",
        "Feature engineering: encoding categórico, escalado, imputación.",
        "Selección de características: filtros, wrappers, métodos embedded.",
        "Manejo de datos desbalanceados: SMOTE, class weights.",
        "Serialización de modelos: pickle, joblib, ONNX.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow. 3rd ed. O'Reilly Media.",
        "Scikit-learn Developers (2024). Scikit-learn Documentation. https://scikit-learn.org/stable/",
        "Zheng, A., & Casari, A. (2018). Feature Engineering for Machine Learning. O'Reilly Media. ISBN: 978-1-491-95324-0",
    ])

    story.append(PageBreak())

    # ── TEMA 3 ──
    section_header(story, pal, sty, "TEMA 3", "REDES NEURONALES Y DEEP LEARNING")

    subsection(story, sty, "3.1 El Perceptrón y Redes Feed-Forward")
    for p in [
        "El perceptrón de Rosenblatt: historia y limitaciones.",
        "Perceptrón multicapa (MLP): capas ocultas y funciones de activación.",
        "Funciones de activación: Sigmoid, Tanh, ReLU, Leaky ReLU, ELU, GELU, Swish.",
        "Backpropagation: derivación matemática paso a paso.",
        "Inicialización de pesos: Xavier/Glorot, He initialization.",
        "Regularización: Dropout, Batch Normalization, Layer Normalization, Weight Decay.",
        "Early stopping y técnicas de control de overfitting.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press. ISBN: 978-0-262-03561-3",
        "Nielsen, M. A. (2015). Neural Networks and Deep Learning. Determination Press. http://neuralnetworksanddeeplearning.com",
        "Chollet, F. (2021). Deep Learning with Python. 2nd ed. Manning Publications. ISBN: 978-1-617-29686-7",
        "LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436-444. https://doi.org/10.1038/nature14539",
    ])

    subsection(story, sty, "3.2 Redes Neuronales Convolucionales (CNN)")
    for p in [
        "Operación de convolución: filtros, stride, padding, feature maps.",
        "Pooling: max pooling, average pooling, global average pooling.",
        "Arquitecturas clásicas: LeNet-5, AlexNet, VGG, GoogLeNet/Inception, ResNet.",
        "Conexiones residuales (skip connections) y su importancia.",
        "Transfer learning y fine-tuning con modelos preentrenados.",
        "Aplicaciones: clasificación de imágenes, detección de objetos (YOLO, Faster R-CNN), segmentación.",
        "Implementación con TensorFlow/Keras y PyTorch.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. Cap. 9: Convolutional Networks. MIT Press.",
        "He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. CVPR 2016. arXiv:1512.03385",
        "Chollet, F. (2021). Deep Learning with Python. 2nd ed. Manning Publications. ISBN: 978-1-617-29686-7",
        "Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow. 3rd ed. O'Reilly Media.",
    ])

    subsection(story, sty, "3.3 Redes Neuronales Recurrentes (RNN, LSTM, GRU)")
    for p in [
        "El problema de las secuencias: dependencias temporales.",
        "RNN básica: backpropagation through time (BPTT) y vanishing gradient.",
        "LSTM (Long Short-Term Memory): celdas de estado, puertas (input, forget, output).",
        "GRU (Gated Recurrent Unit): simplificación del LSTM.",
        "Encoder-Decoder para secuencias de longitud variable.",
        "Mecanismo de atención clásico (Bahdanau, 2015) como precursor del Transformer.",
        "Aplicaciones: PLN, series temporales, generación de texto.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Hochreiter, S., & Schmidhuber, J. (1997). Long Short-Term Memory. Neural Computation, 9(8), 1735-1780.",
        "Cho, K., et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder. EMNLP 2014. arXiv:1406.1078",
        "Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR 2015. arXiv:1409.0473",
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. Cap. 10: Sequence Modeling. MIT Press.",
    ])

    story.append(PageBreak())

    # ── TEMA 4 ──
    section_header(story, pal, sty, "TEMA 4", "ARQUITECTURA TRANSFORMER")

    subsection(story, sty, "4.1 Self-Attention y Multi-Head Attention")
    for p in [
        "Intuición del mecanismo de atención: alinear y traducir.",
        "Self-attention (scaled dot-product attention): Q, K, V — queries, keys y values.",
        "Cálculo de atención: Attention(Q,K,V) = softmax(QK^T / sqrt(d_k))V.",
        "Multi-head attention: paralelismo y captura de distintos patrones.",
        "Complejidad cuadrática de la atención y sus implicaciones.",
        "Atención causal (enmascarada) en modelos autoregresivos.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). Attention is All You Need. NeurIPS 2017. arXiv:1706.03762",
        "Alammar, J. (2018). The Illustrated Transformer. [Blog post]. https://jalammar.github.io/illustrated-transformer/",
        "Rush, A. M. (2018). The Annotated Transformer. [Blog post]. https://nlp.seas.harvard.edu/2018/04/03/attention.html",
    ])

    subsection(story, sty, "4.2 Arquitectura Completa del Transformer")
    for p in [
        "Encoder: N capas de multi-head attention + FFN + Layer Norm + residual connections.",
        "Decoder: enmascarado + cross-attention sobre la salida del encoder.",
        "Embeddings posicionales: sinusoidales (paper original) vs aprendidos.",
        "Feed-forward sublayer: proyección expand-and-contract (4x).",
        "Hiperparámetros: d_model, d_ff, n_heads, n_layers, dropout.",
        "Variantes de normalización: Pre-LN vs Post-LN.",
        "Encoder-only (BERT), Decoder-only (GPT), Encoder-Decoder (T5, BART).",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Vaswani, A., et al. (2017). Attention is All You Need. NeurIPS 2017. arXiv:1706.03762",
        "Tunstall, L., von Werra, L., & Wolf, T. (2022). Natural Language Processing with Transformers. O'Reilly Media. ISBN: 978-1-098-10313-2",
        "Phuong, M., & Hutter, M. (2022). Formal Algorithms for Transformers. arXiv:2207.09238",
    ])

    subsection(story, sty, "4.3 Modelos Transformer Fundamentales")
    for p in [
        "BERT (2018): preentrenamiento bidireccional, MLM y NSP, fine-tuning.",
        "GPT / GPT-2 / GPT-3: escalado de parámetros y emergencia de capacidades.",
        "T5 (2019): enfoque text-to-text unificado.",
        "RoBERTa: mejoras de entrenamiento sobre BERT.",
        "DistilBERT: destilación del conocimiento para modelos ligeros.",
        "Vision Transformer (ViT): aplicación del Transformer a imágenes.",
        "Comparativa de tamaños: parámetros, FLOPS y rendimiento en benchmarks.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. NAACL 2019. arXiv:1810.04805",
        "Radford, A., et al. (2019). Language Models are Unsupervised Multitask Learners (GPT-2). OpenAI Blog.",
        "Raffel, C., et al. (2020). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (T5). JMLR, 21(140). arXiv:1910.10683",
        "Dosovitskiy, A., et al. (2021). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (ViT). ICLR 2021. arXiv:2010.11929",
        "Tunstall, L., von Werra, L., & Wolf, T. (2022). NLP with Transformers. O'Reilly Media. ISBN: 978-1-098-10313-2",
    ])

    story.append(PageBreak())

    # ── TEMA 5 ──
    section_header(story, pal, sty, "TEMA 5", "GRANDES MODELOS DE LENGUAJE (LLMs)")

    subsection(story, sty, "5.1 Fundamentos de los LLMs")
    for p in [
        "Definición y escala: ¿qué hace a un modelo 'grande'?",
        "Ley de escala (Scaling Laws): Chinchilla, relación parámetros-datos-FLOPS.",
        "Preentrenamiento: autoregressive language modeling (next-token prediction).",
        "Tokenización: BPE (Byte-Pair Encoding), WordPiece, SentencePiece.",
        "Vocabulario, secuencias de contexto y longitud de ventana.",
        "Capacidades emergentes: in-context learning, chain-of-thought, pocos disparos.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Brown, T., et al. (2020). Language Models are Few-Shot Learners (GPT-3). NeurIPS 2020. arXiv:2005.14165",
        "Hoffmann, J., et al. (2022). Training Compute-Optimal Large Language Models (Chinchilla). NeurIPS 2022. arXiv:2203.15556",
        "Wei, J., et al. (2022). Emergent Abilities of Large Language Models. TMLR. arXiv:2206.07682",
        "Kaddour, J., et al. (2023). Challenges and Applications of Large Language Models. arXiv:2307.10169",
    ])

    subsection(story, sty, "5.2 Alineación y Fine-tuning")
    for p in [
        "Instruction tuning: FLAN, InstructGPT — seguir instrucciones en lenguaje natural.",
        "RLHF (Reinforcement Learning from Human Feedback): recompensa y PPO.",
        "DPO (Direct Preference Optimization): alternativa más simple al RLHF.",
        "Parameter-Efficient Fine-Tuning (PEFT): LoRA, QLoRA, Prefix Tuning, Adapter layers.",
        "Hallucinations: causas, detección y técnicas de mitigación.",
        "Constitutional AI (CAI) y RLAIF: alternativas de alineación.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Ouyang, L., et al. (2022). Training language models to follow instructions with human feedback (InstructGPT). NeurIPS 2022. arXiv:2203.02155",
        "Rafailov, R., et al. (2023). Direct Preference Optimization: Your Language Model is Secretly a Reward Model (DPO). NeurIPS 2023. arXiv:2305.18290",
        "Hu, E. J., et al. (2022). LoRA: Low-Rank Adaptation of Large Language Models. ICLR 2022. arXiv:2106.09685",
        "Dettmers, T., et al. (2023). QLoRA: Efficient Finetuning of Quantized LLMs. NeurIPS 2023. arXiv:2305.14314",
    ])

    subsection(story, sty, "5.3 LLMs Abiertos y Ecosistema")
    for p in [
        "LLaMA / LLaMA 2 / LLaMA 3: arquitectura y licenciamiento.",
        "Mistral, Mixtral (MoE): Mixture of Experts para eficiencia.",
        "Gemma (Google), Phi (Microsoft): modelos pequeños de alto rendimiento.",
        "Quantización: GGUF, GGML, AWQ, GPTQ — inferencia en hardware limitado.",
        "Ollama, llama.cpp, Hugging Face Transformers: herramientas de despliegue local.",
        "Benchmarks: MMLU, HellaSwag, ARC, TruthfulQA, HumanEval.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Touvron, H., et al. (2023). Llama 2: Open Foundation and Fine-Tuned Chat Models. arXiv:2307.09288",
        "Jiang, A. Q., et al. (2024). Mixtral of Experts. arXiv:2401.04088",
        "Wolf, T., et al. (2020). Transformers: State-of-the-Art Natural Language Processing. EMNLP 2020. arXiv:1910.03771",
        "Hugging Face (2024). Open LLM Leaderboard. https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard",
    ])

    story.append(PageBreak())

    # ── TEMA 6 ──
    section_header(story, pal, sty, "TEMA 6", "TÉCNICAS AVANZADAS Y APLICACIONES")

    subsection(story, sty, "6.1 Prompt Engineering")
    for p in [
        "Zero-shot, one-shot y few-shot prompting.",
        "Chain-of-Thought (CoT) prompting: razonamiento paso a paso.",
        "Tree-of-Thought (ToT) y Self-Consistency.",
        "ReAct: razonamiento + acción en LLMs.",
        "Role prompting, formato de salida estructurada.",
        "Inyección de prompts y seguridad (prompt injection, jailbreak).",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS 2022. arXiv:2201.11903",
        "Yao, S., et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. arXiv:2305.10601",
        "White, J., et al. (2023). A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT. arXiv:2302.11382",
        "DAIR.AI (2024). Prompt Engineering Guide. https://www.promptingguide.ai",
    ])

    subsection(story, sty, "6.2 Retrieval-Augmented Generation (RAG)")
    for p in [
        "Motivación: actualizar el conocimiento de un LLM sin reentrenarlo.",
        "Pipeline RAG: chunking, embeddings, vector store, retrieval, generación.",
        "Modelos de embeddings: OpenAI text-embedding-ada-002, Sentence Transformers.",
        "Bases de datos vectoriales: Chroma, Pinecone, Weaviate, FAISS, Milvus.",
        "RAG avanzado: HyDE, reranking, multi-query retrieval, parent-child chunks.",
        "Evaluación de RAG: RAGAS framework, fidelidad y relevancia.",
        "Implementación con LangChain y LlamaIndex.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020. arXiv:2005.11401",
        "Gao, Y., et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv:2312.10997",
        "LangChain (2024). LangChain Documentation. https://python.langchain.com",
        "Liu, J. (2024). LlamaIndex Documentation. https://docs.llamaindex.ai",
    ])

    subsection(story, sty, "6.3 Agentes y Sistemas Multi-Agente")
    for p in [
        "LLM Agents: razonamiento, herramientas y memoria.",
        "Frameworks de herramientas: function calling (OpenAI), tool use (Anthropic).",
        "Memoria de agentes: a corto plazo (ventana de contexto) y a largo plazo (vectores).",
        "LangGraph: flujos de agente con estado.",
        "AutoGen, CrewAI: sistemas de múltiples agentes cooperativos.",
        "Evaluación de agentes: métricas de éxito de tareas, fidelidad, eficiencia.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Yao, S., et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR 2023. arXiv:2210.03629",
        "Wang, L., et al. (2024). A Survey on Large Language Model based Autonomous Agents. Frontiers of Computer Science. arXiv:2308.11432",
        "LangChain (2024). LangGraph Documentation. https://langchain-ai.github.io/langgraph/",
    ])

    story.append(PageBreak())

    # ── TEMA 7 ──
    section_header(story, pal, sty, "TEMA 7", "MLOps Y DESPLIEGUE EN PRODUCCIÓN")

    subsection(story, sty, "7.1 Ciclo de Vida del Modelo ML")
    for p in [
        "MLOps: principios, madurez y comparativa con DevOps.",
        "Gestión de experimentos: MLflow, Weights & Biases (W&B).",
        "Versionado de datos y modelos: DVC (Data Version Control).",
        "Feature stores: Feast, Tecton.",
        "CI/CD para ML: pipelines de entrenamiento automatizado.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Burkov, A. (2020). Machine Learning Engineering. True Positive Inc. Disponible en: http://mlebook.com",
        "Huyen, C. (2022). Designing Machine Learning Systems. O'Reilly Media. ISBN: 978-1-098-10796-3",
        "Sculley, D., et al. (2015). Hidden Technical Debt in Machine Learning Systems. NeurIPS 2015.",
    ])

    subsection(story, sty, "7.2 Despliegue y Monitoreo de Modelos LLM")
    for p in [
        "Serving LLMs: vLLM, TGI (Text Generation Inference), TensorRT-LLM.",
        "Quantización para producción: INT8, INT4 con bitsandbytes.",
        "API de OpenAI, Anthropic Claude, Google Gemini: integración y mejores prácticas.",
        "LLMOps: monitoreo de deriva (drift), evaluación continua, A/B testing.",
        "Costos y optimización: caché de KV, batching, prompt compression.",
        "Seguridad en LLMs: guardrails, output filtering, Llama Guard.",
    ]:
        point(story, sty, p)
    refs_block(story, sty, [
        "Huyen, C. (2022). Designing Machine Learning Systems. O'Reilly Media. ISBN: 978-1-098-10796-3",
        "Izsak, P., et al. (2021). How to Train BERT with an Academic Budget. arXiv:2104.07705",
        "vLLM Team (2024). vLLM Documentation. https://docs.vllm.ai",
        "Anthropic (2024). Claude API Documentation. https://docs.anthropic.com",
        "OpenAI (2024). OpenAI API Documentation. https://platform.openai.com/docs",
    ])

    # Bibliografía consolidada
    story.append(PageBreak())
    section_header(story, pal, sty, "REF", "BIBLIOGRAFÍA GENERAL CONSOLIDADA")
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("LIBROS FUNDAMENTALES", sty["h2"]))
    for r in [
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press. ISBN: 978-0-262-03561-3. https://www.deeplearningbook.org",
        "Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer. ISBN: 978-0-387-31073-2",
        "James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). An Introduction to Statistical Learning. 2nd ed. Springer. ISBN: 978-1-071-61418-1",
        "Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow. 3rd ed. O'Reilly Media. ISBN: 978-1-098-12597-4",
        "Chollet, F. (2021). Deep Learning with Python. 2nd ed. Manning Publications. ISBN: 978-1-617-29686-7",
        "Tunstall, L., von Werra, L., & Wolf, T. (2022). Natural Language Processing with Transformers. O'Reilly Media. ISBN: 978-1-098-10313-2",
        "Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction. 2nd ed. MIT Press. ISBN: 978-0-262-03924-6",
        "Huyen, C. (2022). Designing Machine Learning Systems. O'Reilly Media. ISBN: 978-1-098-10796-3",
        "Burkov, A. (2020). Machine Learning Engineering. True Positive Inc. http://mlebook.com",
        "Nielsen, M. A. (2015). Neural Networks and Deep Learning. Determination Press. http://neuralnetworksanddeeplearning.com",
    ]:
        story.append(Paragraph(f"▸ {r}", sty["ref"]))
        story.append(Spacer(1, 0.1*cm))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("PAPERS SEMINALES", sty["h2"]))
    for r in [
        "Vaswani, A., et al. (2017). Attention is All You Need. NeurIPS 2017. arXiv:1706.03762",
        "Devlin, J., et al. (2019). BERT: Pre-training of Deep Bidirectional Transformers. NAACL 2019. arXiv:1810.04805",
        "Brown, T., et al. (2020). Language Models are Few-Shot Learners (GPT-3). NeurIPS 2020. arXiv:2005.14165",
        "He, K., et al. (2016). Deep Residual Learning for Image Recognition. CVPR 2016. arXiv:1512.03385",
        "LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep Learning. Nature, 521, 436-444.",
        "Hochreiter, S., & Schmidhuber, J. (1997). Long Short-Term Memory. Neural Computation, 9(8), 1735-1780.",
        "Raffel, C., et al. (2020). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer. JMLR. arXiv:1910.10683",
        "Ouyang, L., et al. (2022). Training Language Models to Follow Instructions (InstructGPT). NeurIPS 2022. arXiv:2203.02155",
        "Hu, E. J., et al. (2022). LoRA: Low-Rank Adaptation of Large Language Models. ICLR 2022. arXiv:2106.09685",
        "Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020. arXiv:2005.11401",
        "Hoffmann, J., et al. (2022). Training Compute-Optimal LLMs (Chinchilla). NeurIPS 2022. arXiv:2203.15556",
        "Touvron, H., et al. (2023). LLaMA 2. arXiv:2307.09288",
    ]:
        story.append(Paragraph(f"▸ {r}", sty["ref"]))
        story.append(Spacer(1, 0.1*cm))

    doc.build(story)
    print(f"PDF 3 generado: {path}")


if __name__ == "__main__":
    import os
    os.makedirs("./outputs", exist_ok=True)
    build_pdf1("./outputs/01_APIs_Python_HTTP_JWT_Webhooks.pdf")
    build_pdf2("./outputs/02_PowerBI_Plan_Academico.pdf")
    build_pdf3("./outputs/03_IA_ML_DeepLearning_LLMs_Transformers.pdf")
    print("✅ Los 3 PDFs han sido generados exitosamente.")