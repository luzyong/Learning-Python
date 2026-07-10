import fitz  # PyMuPDF

def extract_adobe_highlights(pdf_path):
    doc = fitz.open(pdf_path)
    highlighted_texts = []

    for page_num, page in enumerate(doc, start=1):
        # 1. Obtener todas las palabras de la página con sus coordenadas exactas
        # Cada palabra es una tupla: (x0, y0, x1, y1, "texto", block_no, line_no, word_no)
        words = page.get_text("words")
        
        # 2. Buscar las anotaciones de resaltado
        annots = page.annots(types=(fitz.PDF_ANNOT_HIGHLIGHT,))
        
        for annot in annots:
            annot_rect = annot.rect
            annot_words = []
            
            for w in words:
                # Creamos un rectángulo FitZ para la palabra individual
                word_rect = fitz.Rect(w[0], w[1], w[2], w[3])
                
                # Verificamos qué tanto se cruza la palabra con el resaltado.
                # Al usar la intersección evitamos capturar líneas vecinas.
                intersection = word_rect & annot_rect
                
                # Si el área que se cruza es mayor que el 50% de la palabra, es parte del resaltado
                if intersection.is_valid and (intersection.get_area() > word_rect.get_area() * 0.5):
                    annot_words.append((w[4], w[6]))  # (texto_palabra, número_de_línea)
            
            if annot_words:
                # Agrupamos las palabras respetando los saltos de línea originales
                lines = {}
                for word, line_no in annot_words:
                    if line_no not in lines:
                        lines[line_no] = []
                    lines[line_no].append(word)
                
                # Unimos las palabras de cada línea con espacios, y luego las líneas con saltos
                full_text = "\n".join([" ".join(lines[l]) for l in sorted(lines.keys())])
                
                highlighted_texts.append({
                    "page": page_num,
                    "text": full_text
                })
                
    return highlighted_texts

# Usage:
results = extract_adobe_highlights("C:\\Users\\luanb\\Downloads\\Excel_2019_BIBLE (2).pdf")
#print(results)

pages = []

for section in results:
    pages.append(section['page'])
    
pages = list(set(pages))
#print(pages)
formatted = []
for page in pages:
    text = ''
    for section in results:
        if section['page'] == page:
            text+=f'{section['text'].replace('\n',"")} '
    formatted.append({
        'page':page,
        'text':text
    })

#print(formatted)

with open('.\\text.txt','w', encoding='utf-8') as f:
    #f.write(f'{formatted}')
    for section in formatted:
        f.write(f"Page {section['page']}\n{section['text']}\n\n")
        