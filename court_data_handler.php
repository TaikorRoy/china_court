<?php
$servername = "localhost";
$username = "root";
$password = "";

$json = file_get_contents('php://input');
$data = json_decode($json, true);
$request_validation = array_key_exists("postId", $data)&&array_key_exists("postUrl", $data);

if ($request_validation)
{
	$con = mysql_connect($servername, $username, $password);
	mysql_query("SET character_set_results = 'utf8', character_set_client = 'utf8', character_set_connection = 'utf8', character_set_database = 'utf8', character_set_server = 'utf8'", $con);
	if (!$con)
	  {
		  die('Could not connect: ' . mysql_error());
		  echo 'Could not connect DB';
	  }
	else
	  {
		mysql_select_db("court", $con);
		$sql = "INSERT INTO billloss (postId, postUrl, postYmd, postCorp, postCourt, postContent, billsId, billsAmount, billsCorp, billsGain, billsPay, billsYmdStart, billsYmdEnd, postSection, pubDate, uploadDate) VALUES ('$data[postId]', '$data[postUrl]', '$data[postYmd]', '$data[postCorp]', '$data[postCourt]', '$data[postContent]', '$data[billsId]', '$data[billsAmount]', '$data[billsCorp]', '$data[billsGain]', '$data[billsPay]', '$data[billsYmdStart]', '$data[billsYmdEnd]', '$data[postSection]', '$data[pubDate]', '$data[uploadDate]')";
		mysql_query($sql);
		mysql_close($con);
		echo "Php Update DB Success !";
	  }
}
else
{
    echo "Invalid Request";
}
?>