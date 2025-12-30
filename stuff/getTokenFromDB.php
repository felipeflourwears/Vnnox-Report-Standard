<?php

header("Content-Type: application/json");

function getTokenFromDB() {
    // Datos de conexión a la base de datos
    $host = "82.180.172.63";
    $user = "u958030263_popbeex24";
    $password = "HJ^hkdVuh7C.t.n";
    $database = "u958030263_bd_vnoxx";

    // Conectar a la base de datos
    $conn = new mysqli($host, $user, $password, $database);

    // Verificar la conexión
    if ($conn->connect_error) {
        http_response_code(500);
        echo json_encode(["error" => "Conexión fallida: " . $conn->connect_error]);
        exit;
    }

    // Consulta SQL para obtener el token
    $sql = "SELECT token FROM token WHERE id = 1";
    $result = $conn->query($sql);

    // Verificar si hay resultados
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $token = $row["token"];
        echo json_encode(["token" => $token]);
    } else {
        http_response_code(404);
        echo json_encode(["error" => "Token no encontrado"]);
    }

    // Cerrar conexión
    $conn->close();
}

// Llamar a la función para obtener el token
getTokenFromDB();

?>