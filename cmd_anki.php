<?php
// var_dump($_SERVER["argv"]);


$p = array();
if (isset($_SERVER["argv"][1])) {
    foreach ($_SERVER["argv"] as $key => $value) {
        $l = explode('=', $value);
        if (count($l) == 2) {
            $paramName = trim(strtolower($l[0]), ' ()[]');
            if (strlen($paramName) > 0) {
                $p[$paramName] = trim($l[1]);
            }
        }
    }
}
if (isset($p['file']) && file_exists($p['file'])) {
    echo '[cmd_php.php]' . $p['file'];
    echo "\n" . '===============================================================================' . "\n";


    $result = '';
    $t = file_get_contents($p['file']);
    $tList = explode("\n", $t);
    foreach ($tList as $k => $v) {
        // echo "\n" . '[' . $k . ']' . strlen($result);
        $v = trim($v, '; \t\n\r\0\x0B');
        $sList = explode(';', $v);
        if (is_array($sList) && count($sList) === 2) {
            $s1 = preg_replace("/ {2,}/"," ", trim(htmlspecialchars($sList[0], ENT_QUOTES)));
            $s2 = preg_replace("/ {2,}/"," ", trim(htmlspecialchars($sList[1], ENT_QUOTES)));
            $result = $s1 . ';' . $s2 . "\n";
            echo $result;
        } elseif (is_array($sList) && count($sList) > 2) {
            //throw new Exception('count($sList) > 2 [' . $k .']', 1);
        } else {

        }
    }
/*    if (strlen( $result) > 0 ) {
        echo $result;
    } else {
        echo $t;
    }*/

    echo "\n" . '===============================================================================' . "\n";
/*    $fileName = dirname( $p['file'] ) .'/'. basename($p['file'], '.anki.txt') . '.txt';
    file_put_contents($fileName, $result);*/
}

