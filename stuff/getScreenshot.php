<?php

// Recibir datos de la notificación POST-JSON
$postData = json_decode(file_get_contents("php://input"), true);

// Verificar si hay datos
if (!empty($postData)) {
    // Recuperar datos de la notificación
    $idPlayer = $postData['playerId'];
    $playerTime = $postData['playerTime']; 
    $screenShotUrl = $postData['screenShotUrl'];

    // Descargar la imagen y guardarla en el servidor
    $imageContents = file_get_contents($screenShotUrl);

    // Asegurarse de que la carpeta scrennplayers exista
    if (!file_exists('screenPlayers')) {
        mkdir('screenPlayers', 0777, true);
    }

    // Guardar la imagen en la carpeta scrennplayers con un nombre específico
    $imageName = 'screenPlayers/' . $idPlayer . '.jpg';
    file_put_contents($imageName, $imageContents);

} else {
    echo "Error: No se recibieron datos en la notificación.";
}
?>
