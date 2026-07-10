import fitz  # PyMuPDF
from deep_translator import GoogleTranslator  # <--- Librería de traducción gratuita

def extract_adobe_highlights(pdf_path):
    doc = fitz.open(pdf_path)
    highlighted_texts = []

    for page_num, page in enumerate(doc, start=1):
        words = page.get_text("words")
        annots = page.annots(types=(fitz.PDF_ANNOT_HIGHLIGHT,))
        
        for annot in annots:
            annot_rect = annot.rect
            annot_words = []
            
            for w in words:
                word_rect = fitz.Rect(w[0], w[1], w[2], w[3])
                intersection = word_rect & annot_rect
                if intersection.is_valid and (intersection.get_area() > word_rect.get_area() * 0.5):
                    annot_words.append((w[4], w[6]))  # (texto_palabra, número_de_línea)
            
            if annot_words:
                lines = {}
                for word, line_no in annot_words:
                    if line_no not in lines:
                        lines[line_no] = []
                    lines[line_no].append(word)
                
                full_text = "\n".join([" ".join(lines[l]) for l in sorted(lines.keys())])
                
                highlighted_texts.append({
                    "page": page_num,
                    "text": full_text
                })
                
    return highlighted_texts

# 1. Extracción original
results = extract_adobe_highlights("C:\\Users\\luanb\\Downloads\\Excel_2019_BIBLE (2).pdf")

# 2. Agrupación por páginas
pages = sorted(list(set([section['page'] for section in results])))

formatted = []
for page in pages:
    text = ''
    for section in results:
        if section['page'] == page:
            # Reemplazamos saltos de línea para unificar la idea en una sola línea
            text += f"{section['text'].replace('\n', ' ')} "
    
    # Limpiamos espacios dobles para mejorar la traducción
    text = " ".join(text.split())
    
    formatted.append({
        'page': page,
        'text': text
    })

# 3. TRADUCCIÓN E ESCRITURA EN ARCHIVO
# Configuramos el traductor de Inglés ('en') a Español ('es')
translator = GoogleTranslator(source='en', target='es')

with open('.\\textTr.txt', 'w', encoding='utf-8') as f:
    for section in formatted:
        print(f"Traduciendo los resaltados de la página {section['page']}...")
        
        original_text = section['text']
        translated_text = ""
        
        # Traducimos solo si hay texto extraído en esa página
        if original_text.strip():
            try:
                # Traduce el bloque completo para que las ideas fragmentadas ganen coherencia
                translated_text = translator.translate(original_text)
            except Exception as e:
                translated_text = f"[Error en traducción: {e}]"
        
        # Escribimos el formato final en el TXT con ambos idiomas
        f.write(f"=== Pagina {section['page']} ===\n")
        #f.write(f"ORIGINAL:\n{original_text}\n\n")
        f.write(f"\n{translated_text}\n")
        f.write("-" * 50 + "\n\n")

print("¡Proceso completado! Revisa tu archivo text.txt")
