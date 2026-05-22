
seccion = []
counter =1
with open("chat.txt","r",encoding="utf-8") as chat:
    for linea in chat:
        seccion.append(linea.strip())
        if len(seccion) == 2400:
            with open(f"chat_part{counter}.txt","w",encoding="utf-8") as parte:
                parte.write("\n".join(seccion))
            seccion = []
            counter += 1
        elif len(seccion) < 2400 and counter == 8:
            with open(f"chat_part{counter}.txt","w",encoding="utf-8") as parte:
                parte.write("\n".join(seccion))
            seccion = []
            counter += 1