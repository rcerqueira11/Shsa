
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

find_between( s, '<option value="/' ,'</option>' )
# find_between( s, '<option value="' ,'</option>' )

asd = "INSERT INTO rcs_modelovehiculo(nombre, codigo, fk_marca_vehiculo_id) VALUES ( '" + nombre+ "', '"+codigo+"', "+id+");"

cadena = ""

options = cadena.split('|')

for option in options:



'<option value="/4C-">4C</option>|<option value="/Giulia">Giulia</option>|<option value="/Giulietta">Giulietta</option>|<option value="/MiTo-">MiTo</option>|<option value="/Stelvio">Stelvio</option>'

'<option value="-1">Selecciona</option>|<option value="/4C-">4C</option>|<option value="/Giulia">Giulia</option>|<option value="/Giulietta">Giulietta</option>|<option value="/MiTo-">MiTo</option>|<option value="/Stelvio">Stelvio</option>'
