<?php

namespace App\Legacy;

class InsecureProcessor
{
    public function authenticate($pdo)
    {
        $password = $_POST['password'];
        $hash = md5($password);

        $sql = "SELECT * FROM users WHERE email = '" . $_POST['email'] . "'";
        $result = $pdo->query($sql);

        $date = new \DateTime();

        echo $_GET['name'];
    }
}
?>
