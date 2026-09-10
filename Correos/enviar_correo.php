<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
use Dotenv\Dotenv;

// Cargar el autoloader de Composer
require 'vendor/autoload.php';

// --- CARGAR VARIABLES DE ENTORNO ---
$dotenv = Dotenv::createImmutable(__DIR__);
$dotenv->load();

// --- CONFIGURACIÓN DE DATOS DEL CONDUCTOR Y RECEPTOR ---
$nombreConductor = "Liann";
$correoDestinatario = "lmelanny0604@gmail.com"; // Cambiar por el correo de prueba
$urlDesuscripcion = "https://www.nurvans.com/legal/desuscripcion";

// Leer plantilla HTML
$htmlContent = file_get_contents('plantilla_bienvenida.html');

// --- REEMPLAZAR VARIABLES DINÁMICAS EN EL HTML ---
$htmlContent = str_replace('{{nombre_conductor}}', $nombreConductor, $htmlContent);
$htmlContent = str_replace('{{unsubscribe_url}}', $urlDesuscripcion, $htmlContent);

// --- INSTANCIA DE PHPMailer ---
$mail = new PHPMailer(true);

try {
    // Configuraciones del servidor SMTP desde .env
    $mail->SMTPDebug  = 0;
    $mail->isSMTP();
    $mail->Host       = $_ENV['SMTP_HOST'];
    $mail->SMTPAuth   = true;
    $mail->Username   = $_ENV['SMTP_USERNAME'];
    $mail->Password   = $_ENV['SMTP_PASSWORD'];
    $mail->SMTPSecure = $_ENV['SMTP_ENCRYPTION'] === 'tls' 
                        ? PHPMailer::ENCRYPTION_STARTTLS 
                        : PHPMailer::ENCRYPTION_SMTPS;
    $mail->Port       = (int)$_ENV['SMTP_PORT'];
    $mail->CharSet    = 'UTF-8';

    // Remitente y Destinatario desde .env
    $mail->setFrom($_ENV['MAIL_FROM_ADDRESS'], $_ENV['MAIL_FROM_NAME']);
    $mail->addAddress($correoDestinatario, $nombreConductor);
    $mail->addReplyTo($_ENV['MAIL_REPLY_TO'], 'Atención al Cliente Nurvans');

    // Contenido del Correo
    $mail->isHTML(true);
    $mail->Subject = '¡Bienvenido a Nurvans! Tu solicitud fue aprobada';
    $mail->Body    = $htmlContent;
    $mail->AltBody = "Hola {$nombreConductor}, tu solicitud ha sido aprobada exitosamente. Descarga la app y empieza a generar ingresos hoy mismo.";

    // Enviar correo
    $mail->send();
    echo 'El correo ha sido enviado exitosamente.';

} catch (Exception $e) {
    echo "Error al enviar el correo: {$mail->ErrorInfo}";
}