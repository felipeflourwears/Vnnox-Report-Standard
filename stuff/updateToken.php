<?php

function getToken() {
    // URL del endpoint para enviar la solicitud POST
    $url = "https://openapi-us.vnnox.com/v1/oauth/token";

    // Token de autorización para la solicitud POST
    $token = 'h7vr53';
    $username = 'popatelier';
    $passw = 'Beex2025%popa';

    // Datos del cuerpo de la solicitud
    $data = array(
        'username' => $username,
        'password' => $passw
    );

    // Convertir los datos a JSON
    $jsonData = json_encode($data);

    // Encabezados de la solicitud
    $headers = array(
        'username: popatelier',
        'token: ' . $token,
        'Content-Type: application/json'
    );

    // Inicializar cURL
    $ch = curl_init();

    // Configurar opciones de cURL
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData); // Enviar los datos JSON
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);  // Añadir los encabezados

    // Desactivar la verificación SSL (solo para depuración)
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

    // Ejecutar la solicitud
    $response = curl_exec($ch);

    // Verificar si ocurrió un error con cURL
    if(curl_errno($ch)) {
        echo 'Error de cURL: ' . curl_error($ch) . "\n";
    }

    // Obtener el código de estado HTTP
    $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    // Cerrar la sesión de cURL
    curl_close($ch);

    // Variable para almacenar el token o el mensaje de error
    $result = null;

    // Comprobar el resultado de la solicitud
    if ($statusCode == 200) {
        echo "¡Solicitud exitosa!\n";
        // Decodificar el JSON de la respuesta
        $responseData = json_decode($response, true);
        // Extraer el token de la respuesta JSON
        $result = $responseData['data']['token'] ?? null;
    } else {
        echo "Error en la solicitud: " . $statusCode . "\n";
        echo $response . "\n"; // Imprime el contenido de la respuesta en caso de error
    }

    
    return $result; // Devuelve el token o null en caso de error
}

function updateTokenInDB($newToken) {
    // Datos de conexión a la base de datos
    $host = "82.180.172.63";
    $user = "u958030263_popbeex24";
    $password = "HJ^hkdVuh7C.t.n";
    $database = "u958030263_bd_vnoxx";

    // Conectar a la base de datos
    $conn = new mysqli($host, $user, $password, $database);

    // Verificar la conexión
    if ($conn->connect_error) {
        die("Conexión fallida: " . $conn->connect_error);
    }

    // Preparar la consulta SQL para actualizar el token
    $sql = "UPDATE token SET token = ? WHERE id = 1";

    // Preparar la consulta
    $stmt = $conn->prepare($sql);
    if (!$stmt) {
        die("Error en la preparación de la consulta: " . $conn->error);
    }

    // Enlazar el nuevo token al statement
    $stmt->bind_param("s", $newToken);

    // Ejecutar la consulta
    if ($stmt->execute()) {
        echo "Token actualizado correctamente.";
    } else {
        echo "Error al actualizar el token: " . $stmt->error;
    }

    // Cerrar la conexión
    $stmt->close();
    $conn->close();
}

// Obtener el nuevo token de la API
$newToken = getToken();

// Si se obtuvo un token válido, actualizar la base de datos
if ($newToken) {
    updateTokenInDB($newToken);
} else {
    echo "No se pudo obtener el token.";
}
?>
