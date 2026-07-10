
seccion = []
counter =1
with open("text.txt","r",encoding="utf-8") as text:
    for linea in text:
        seccion.append(linea.strip())
        if len(seccion) == 2400:
            with open(f"text_part{counter}.txt","w",encoding="utf-8") as parte:
                parte.write("\n".join(seccion))
            seccion = []
            counter += 1
        elif len(seccion) < 2400 and counter == 8:
            with open(f"text_part{counter}.txt","w",encoding="utf-8") as parte:
                parte.write("\n".join(seccion))
            seccion = []
            counter += 1