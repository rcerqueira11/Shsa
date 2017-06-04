$("#partes").width();
$("#B").width()
$("#R").width()
$("#M").width()
$("#observacion").width()
console.log("partes:",$("#partes").width());
console.log("B:",$("#B").width());
console.log("R:",$("#R").width());
console.log("M:",$("#M").width());
console.log("observacion:",$("#observacion").width());

console.log("partes2:",$("#partes2").width());
console.log("B2:",$("#B2").width());
console.log("R2:",$("#R2").width());
console.log("M2:",$("#M2").width());
console.log("observacion2:",$("#observacion2").width());

console.log("partes3:",$("#partes3").width());
console.log("B3:",$("#B3").width());
console.log("R3:",$("#R3").width());
console.log("M3:",$("#M3").width());
console.log("observacion3:",$("#observacion3").width());


partes: 113
B: 10
R: 10
M: 12
observacion: 120
partes2: 137
B2: 10
R2: 10
M2: 12
observacion2: 120
partes3: 138
B3: 10
R3: 10
M3: 12
observacion3: 120


partes:  9.090909090909092%
B: 0.9090909090909091%
R: 0.9090909090909091%
M: 0.9090909090909091%
observacion: 10.909090909090908%
partes2: 13%
B2: 0.9090909090909091
R2: 0.9090909090909091
M2: 0.9090909090909091
observacion2: 10.909090909090908%
partes3:  13.181818181818182%
B3: 0.9090909090909091
R3: 0.9090909090909091
M3: 0.9090909090909091
observacion3: 10.909090909090908%



113
10
10
12
120



{# Condiciones Generales del vehiculo #}
	<div class="row">
		<div class="col-xs-12">
			<table class="table table-bordered" style="margin-bottom:0;margin-top:0px;">
				<thead>
					<tr>
	                	<td colspan="15" style="width:100%; background-color: white;"><center> CONDICIONES GENERALES DEL VEHI&Iacute;CULO </center></td>
	            	</tr>
					<th style="width:9%"><center>PARTES</center></th>
					<th style="width:3%"><center>B</center></th>
					<th style="width:3%"><center>R</center></th>
					<th style="width:3%"><center>M</center></th>
					<th style="width:15%"><center>OBSERVACI&Oacute;NES</center></th>
					<th style="width:9%"><center>PARTES</center></th>
					<th style="width:3%"><center>B</center></th>
					<th style="width:3%"><center>R</center></th>
					<th style="width:3%"><center>M</center></th>
					<th style="width:15%"><center>OBSERVACI&Oacute;NES</center></th>
					<th style="width:9%"><center>PARTES</center></th>
					<th style="width:3%"><center>B</center></th>
					<th style="width:3%"><center>R</center></th>
					<th style="width:3%"><center>M</center></th>
					<th style="width:15%"><center>OBSERVACI&Oacute;NES</center></th>
					
				</thead>
			</table>
					{% for condicion in condiciones  %}
						{% if forloop.first %}
						<table class="table table-bordered keeptogether" style="margin-bottom:0;margin-top:0px;">
							<thead >
								<th style="width:9%"><center>PARTES</center></th>
								<th style="width:3%"><center>B</center></th>
								<th style="width:3%"><center>R</center></th>
								<th style="width:3%"><center>M</center></th>
								<th style="width:15%"><center>OBSERVACI&Oacute;NES</center></th>
								<th style="width:9%"><center>PARTES</center></th>
								<th style="width:3%"><center>B</center></th>
								<th style="width:3%"><center>R</center></th>
								<th style="width:3%"><center>M</center></th>
								<th style="width:15%"><center>OBSERVACI&Oacute;NES</center></th>
								<th style="width:9%"><center>PARTES</center></th>
								<th style="width:3%"><center>B</center></th>
								<th style="width:3%"><center>R</center></th>
								<th style="width:3%"><center>M</center></th>
								<th style="width:15%"><center>OBSERVACI&Oacute;NES</center></th>
							
							</thead>
							<tr >
						{% endif %}
						{% if forloop.counter|primera_col %}
							<td >{{condicion.parte}}</td>
							<td >{% if condicion.fk_estado_vehiculo.codigo == 'B' %}X{% endif %}</td>
							<td >{% if condicion.fk_estado_vehiculo.codigo == 'R' %}X{% endif %}</td>
							<td >{% if condicion.fk_estado_vehiculo.codigo == 'M' %}X{% endif %}</td>
							<td >{{condicion.observacion}}</td>
						{% endif %}
						{% if forloop.counter|segunda_col %}
							<td >{{condicion.parte}}</td>
							<td >{% if condicion.fk_estado_vehiculo.codigo == 'B' %}X{% endif %}</td>
							<td >{% if condicion.fk_estado_vehiculo.codigo == 'R' %}X{% endif %}</td>
							<td >{% if condicion.fk_estado_vehiculo.codigo == 'M' %}X{% endif %}</td>
							<td >{{condicion.observacion}}</td>
						{% endif %}
						{% if forloop.counter|tercera_col %}
							<td >{{condicion.parte}}</td>
							<td >{% if condicion.fk_estado_vehiculo.codigo == 'B' %}X{% endif %}</td>
							<td >{% if condicion.fk_estado_vehiculo.codigo == 'R' %}X{% endif %}</td>
							<td >{% if condicion.fk_estado_vehiculo.codigo == 'M' %}X{% endif %}</td>
							<td >{{condicion.observacion}}</td>
						{% endif %}
						{% if forloop.counter|divisibleby:3 %}
							</tr>
						</table>
						<table class="table table-bordered keeptogether" style="margin-bottom:0;margin-top:0px;">
							<thead >
								<th style="width:9%"><center>PARTES</center></th>
								<th style="width:3%"><center>B</center></th>
								<th style="width:3%"><center>R</center></th>
								<th style="width:3%"><center>M</center></th>
								<th style="width:15%"><center>OBSERVACI&Oacute;NES</center></th>
								<th style="width:9%"><center>PARTES</center></th>
								<th style="width:3%"><center>B</center></th>
								<th style="width:3%"><center>R</center></th>
								<th style="width:3%"><center>M</center></th>
								<th style="width:15%"><center>OBSERVACI&Oacute;NES</center></th>
								<th style="width:9%"><center>PARTES</center></th>
								<th style="width:3%"><center>B</center></th>
								<th style="width:3%"><center>R</center></th>
								<th style="width:3%"><center>M</center></th>
								<th style="width:15%"><center>OBSERVACI&Oacute;NES</center></th>
							
							</thead>
							<tr >
						{% endif %}
						{% if forloop.last %}
							{% if not forloop.counter|divisibleby:3 %}
								<td ></td>
								<td ></td>
								<td ></td>
								<td ></td>
								<td ></td>
							{% endif %}
							</tr>
						</table>
						{% endif %}
					{% endfor %}
		</div>
	</div>