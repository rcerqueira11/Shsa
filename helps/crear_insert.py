

cadena = '"IN<option value="/Carens">Carens</option>|<option value="/Niro">Niro</option>|<option value="/Optima">Optima</option>|<option value="/Picanto">Picanto</option>|<option value="/Rio">Rio</option>|<option value="/Sorento">Sorento</option>|<option value="/Soul">Soul</option>|<option value="/Soul-EV">Soul EV</option>|<option value="/Sportage">Sportage</option>|<option value="/Venga">Venga</option>|<option value="/ceed">ceed</option>|<option value="/ceed-Sportswagon-">ceed Sportswagon</option>|<option value="/proceed-">pro_ceed</option>|<option value="/proceed-GT">pro_ceed GT</option>'
id = '26'

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

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

# find_between( s, '<option value="/' ,'</option>' )
# find_between( s, '<option value="' ,'</option>' )

# asd = "INSERT INTO rcs_modelovehiculo(nombre, codigo, fk_marca_vehiculo_id) VALUES ( '" + nombre+ "', '"+codigo+"', "+id+");"


options = cadena.split('|')
results = []
for option in options:
	separacion = find_between( option, '<option value="/' ,'</option>' )
	valores = separacion.split('">')
	nombre = valores[1].capitalize()
	if hasNumbers(valores[1]):
		nombre = valores[1].upper()	
	else:
		nombre = valores[1].capitalize()
	# nombre = valores[1].capitalize()
	codigo = valores[0].upper().replace('-','')
	results.append("INSERT INTO rcs_modelovehiculo(nombre, codigo, fk_marca_vehiculo_id) VALUES ( '" + nombre+ "', '"+codigo+"', "+id+");")

print results

# '<option value="/4C-">4C</option>|<option value="/Giulia">Giulia</option>|<option value="/Giulietta">Giulietta</option>|<option value="/MiTo-">MiTo</option>|<option value="/Stelvio">Stelvio</option>'

# '<option value="/4C-">4C</option>|<option value="/Giulia">Giulia</option>|<option value="/Giulietta">Giulietta</option>|<option value="/MiTo-">MiTo</option>|<option value="/Stelvio">Stelvio</option>'
