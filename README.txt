Consideraciones para poder ejecutar la API correctamente:

1. En el archivo .env se debera proporcionar las siguientes claves: Client_Secret. y Client_ID sin estas la api no funcionara

2. Para la obtencion del token de spotify el usuario debera estar registrado previamente en la base de datos, esto puede 
hacerse mediante un post en el endpoint de /users

3. Para el endpoint /spotify/artist/{id} se debera de proporcionar el id del artista correspondiente en la peticion como ejemplo
 Pitbull=0TnOYISbd1XYRBk9myaseg, este ID se puede pasar como un Path Param a traves de PostMan por ejemplo.
