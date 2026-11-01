<?php
$pass = $_GET["pass"];
$sql = "SELECT card FROM users WHERE password = '".$pass."'";
$id = addslashes($_GET['id']);
$query = 'SELECT title FROM books WHERE id = ' . $id;
$redirect_url = $_GET['url'];
header("Location: " . $redirect_url);
