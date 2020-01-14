<?php
	echo $_GET['flag'];
	file_put_contents('flag', $_GET['flag']);
