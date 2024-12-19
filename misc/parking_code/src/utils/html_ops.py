
def write_page( name, title, rrate, body ):
    
    meta = ''
    if rrate is not None:
        meta = '<meta http-equiv="refresh" content="%d" />' % rrate

    html = """\
           <html>
               <head>
                   %s
                   <title>%s</title>
               </head>
               %s
           </html>""" % ( meta, title, body)

    fido = open(name,'w')
    fido.write(html)
    fido.close()
    
    return

