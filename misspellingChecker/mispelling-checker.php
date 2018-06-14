<?php
/*
Plugin Name: 0Misspelling Checker
Plugin URI: http://localhost/
Description: This is a plugin to check misspelling on the site. 
Author: Juhwan Yoo
Version: 1.0
Author URI: http://localhost/
*/
global $jal_db_version;
$jal_db_version = '1.1';
register_activation_hook (__FILE__, 'jal_misspelling_install');
function jal_misspelling_install() {
	global $wpdb;
	$table_name = $wpdb->prefix . 'misspelling';
	$charset_collate = $wpdb->get_charset_collate();
	$sql = "CREATE TABLE $table_name (
		id mediumint(9) NOT NULL AUTO_INCREMENT,
		time datetime DEFAULT '0000-00-00 00:00:00' NOT NULL,
		knox_id tinytext NOT NULL,
		email tinytext NOT NULL,
		full_name tinytext NOT NULL,
		employee_number tinytext NOT NULL,
		user_information tinytext NOT NULL,
		department_name tinytext NOT NULL,
		target_url varchar(55) DEFAULT '' NOT NULL,
		error_number mediumint(9) NOT NULL,
		result_url tinytext NOT NULL,
		PRIMARY KEY  (id)
	) $charset_collate;";
	require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
	dbDelta( $sql );
	add_option( 'jal_db_version', $jal_db_version );
	$installed_ver = get_option( "jal_db_version" );
	if ( $installed_ver != $jal_db_version ) {
		$table_name = $wpdb->prefix . 'liveshoutbox';
		$sql = "CREATE TABLE $table_name (
			id mediumint(9) NOT NULL AUTO_INCREMENT,
			time datetime DEFAULT '0000-00-00 00:00:00' NOT NULL,
			knox_id tinytext NOT NULL,
			email tinytext NOT NULL,
			full_name tinytext NOT NULL,
			employee_number tinytext NOT NULL,
			user_information tinytext NOT NULL,
			department_name tinytext NOT NULL,
			target_url varchar(55) DEFAULT '' NOT NULL,
			error_number mediumint(9) NOT NULL,
			result_url tinytext NOT NULL,
			PRIMARY KEY  (id)
		);";
		require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
		dbDelta( $sql );
		update_option( "jal_db_version", $jal_db_version );
	}
}
register_activation_hook(__FILE__, 'wp_contact_activation');
function wp_contact_activation() {
}
register_deactivation_hook(__FILE__, 'wp_contact_deactivation');
function wp_contact_deactivation() {
}
/*
add_action('wp_enqueue_scripts', 'fwds_scripts');
function fwds_scripts() {
	wp_register_script('input', plugins_url('js/index.js', __FILE__));
	wp_enqueue_script('input');
}
*/
add_action('wp_enqueue_scripts', 'fwds_misspelling_styles');
function fwds_misspelling_styles() {
	wp_register_style('style', plugins_url('css/style.css', __FILE__));
	wp_enqueue_style('style');
}
add_action('admin_enqueue_scripts', 'load_wp_media_files');
function load_wp_media_files() {
	wp_enqueue_media();
}
add_shortcode('my_misspelling', 'wp_misspelling_checker');
function wp_misspelling_checker() {
	if ( is_user_logged_in() ) {
		$current_time = current_time('mysql');
		$current_user = wp_get_current_user();
		$str = $current_user->mo_ldap_local_custom_attribute_distinguishedname;
		$strTok = explode(',', $str);
		$count = count($strTok);
		$searchName = 'OU=';
		$distinguish_name = '';
		for($i = 0;$i < $count;$i++){
			if (strpos($strTok[$i], $searchName) !== false){ 
				array_push($strTok, str_replace($searchName, '', $strTok[$i]));
			}
			unset($strTok[$i]);
		}
		$strTok = array_reverse(array_values($strTok));
		for($i = 3;$i < count($strTok);$i++){
			if ($i !== 3) $distinguish_name .= ' > ';
			$distinguish_name .= $strTok[$i];
		}
		$html = '
<form action="#v_form" method="post" id="v_form">
<h3>Required data</h3>
<table bgcolor="grey" cellpadding="1">
<tr bgcolor="white">
<td align="center" width="20%"><label for="target_url">target URL</label></td>
<td><input type="text" name="target_url" id="target_url" placeholder="Please input the target URL you want to check misspellings." /></td></tr>
</table>
<h3>Client information</h3>
<table bgcolor="grey" cellpadding="1">
<tr bgcolor="white">
<td align="center" width="20%"><label for="time">time</label></td>
<td><input type="text" name="time" id="time" value="'.$current_time.'" /></td></tr>
<tr bgcolor="white">
<td align="center"><label for="knox_id">Knox ID</label></td>
<td><input type="text" name="knox_id" id="knox_id" value="'.$current_user->user_login.'" /></td></tr>
<tr bgcolor="white">
<td align="center"><label for="email">email</label></td>
<td><input type="email" name="email" id="email" value="'.$current_user->user_email.'" /></td></tr>
<tr bgcolor="white">
<td align="center"><label for="full_name">full name</label></td>
<td><input type="text" name="full_name" id="full_name" value="'.$current_user->display_name.'" /></td></tr>
<tr bgcolor="white">
<td align="center"><label for="employee_number">employee number</label></td>
<td><input type="text" name="employee_number" id="employee_number" value="'.$current_user->mo_ldap_local_custom_attribute_employeenumber.'" /></td></tr>
<tr bgcolor="white">
<td align="center"><label for="department_name">department name</label></td>
<td><input type="text" name="department_name" id="department_name" value="'.$distinguish_name.'" /></td></tr>
<tr bgcolor="white">
<td align="center"><label for="user_information">user information</label></td>
<td><input type="text" width="100%" name="user_information" id="user_information" value="'.$current_user->mo_ldap_local_custom_attribute_displayname.'" /></td></tr>
</table>
<div align="center" id="loading2" style="display:none;">Misspelling checking is in progress.<img src="/images/Preloader_7.gif" alt="" /></div>
<input type="submit" id="submit" name="submit_form" onClick="this.style.visibility=\'hidden\'" value="submit" /><br>
</form>
<script type="text/javascript">
(function (d) {
    d.getElementById("v_form").onsubmit = function () {
    d.getElementById("submit").style.display = "none";
    d.getElementById("loading2").style.display = "block";
  };
}(document));
</script>
';
		ob_start();
		echo $html;
		$html = ob_get_clean();
		// does the inserting, in case the form is filled and submitted
		if ( isset( $_POST["submit_form"] ) && $_POST["target_url"] != "" ) {
			$table_name = $wpdb->prefix . 'misspelling';
			$time = strip_tags($_POST["time"], "");
			$knox_id = strip_tags($_POST["knox_id"], "");
			$email = strip_tags($_POST["email"], "");
			$full_name = strip_tags($_POST["full_name"], "");
			$employee_number = strip_tags($_POST["employee_number"], "");
			$department_name = strip_tags($_POST["department_name"], "");
			$user_information = strip_tags($_POST["user_information"], "");
			$target_url = strip_tags($_POST["target_url"], "");
    			$html = '
<br>
<br><h3>Submitted data</h3>
<table width="100%" bgcolor="grey" cellpadding="1">
<tr bgcolor="white">
<td align="center" width="20%">target URL</td>
<td>'.$target_url.'</td></tr>
<tr bgcolor="white">
<td align="center" width="20%">time</td>
<td>'.$time.'</td></tr>
<tr bgcolor="white">
<td align="center" width="20%">Knox ID</td>
<td>'.$knox_id.'</td></tr>
<tr bgcolor="white">
<td align="center" width="20%">email</td>
<td>'.$email.'</td></tr>
<tr bgcolor="white">
<td align="center" width="20%">full name</td>
<td>'.$full_name.'</td></tr>
<tr bgcolor="white">
<td align="center" width="20%">employee number</td>
<td>'.$employee_number.'</td></tr>
<tr bgcolor="white">
<td align="center" width="20%">department name</td>
<td>'.$department_name.'</td></tr>
<tr bgcolor="white">
<td align="center" width="20%">user information</td>
<td>'.$user_information.'</td></tr>
</table>
';
			$count = 0;
			$pluginpath = plugin_dir_path(__FILE__);
			$filename = str_replace(' ', '_', str_replace(':', '-', $time)).'_'.str_replace('/', '_', str_replace('://', '_', $target_url));
			$filepath = home_url()."/result/".$filename;
			$logpath = $filepath.".log";
			$filepath = $filepath.".csv";
			$html .= '<h6>Your request was successfully submitted and completed. Thanks!!</h6>';
			// $html .= '<meta http-equiv="refresh" content="3; url='.get_permalink().'">';
			$command = '/usr/bin/sudo '.$pluginpath.'includes/start.sh "'.$pluginpath.'includes/misspelling.py" "" "'.$filename.'.csv" "'.$filename.'.log" "'.$target_url.'"';
			$descriptorspec = array(
				0 => array("pipe", "r"),
				1 => array("pipe", "w"),
				2 => array("file", "./result/error-output.log", "a"),
			);
			$process = proc_open($command, $descriptorspec, $pipes);
			echo '<h3>Result</h3>';
			if (is_resource($process)) {
				fwrite($pipes[0]);
				while(!feof($pipes[1])) {
					$message = fgets($pipes[1], 1024);
					if (strpos($message, 'Not found') !== False) {
						echo nl2br($message);
						$count += 1;
					}
				}
				fclose($pipes[1]);
				$return_value = proc_close($process);
				$message = "[END] Command returned $return_value";
				//$message .= "<br>+ Please check "."<a href=\"".$filepath."\" target=\"_blank_\">the result file</a>"." for details.";
				$message .= "<br>+ Please check the "."<a href=\"".$filepath."\" target=\"_blank_\">result file</a>"." and "."<a href=\"".$logpath."\" target=\"_blank_\">log file</a>"." for details.";
				if ($count == 0) {
					$message .= "<br>+ There is no error ";
				}
				else if ($count == 1) {
					$message .= "<br>+ There is $count error ";
				}
				else {
					$message .= "<br>+ There are $count errors ";
				}
				$message .= "@ <a href=\"".$target_url."\" target=\"_blank_\">".$target_url."</a>";
				echo nl2br($message);
			}
			else {
				$filepath = "";
			}
			global $wpdb;
			$table_name = $wpdb->prefix . 'misspelling';
			$wpdb->insert( 
				$table_name, 
				array( 
					'time' => $time,
					'knox_id' => $knox_id,
					'email' => $email,
					'full_name' => $full_name,
					'employee_number' => $employee_number,
					'department_name' => $department_name,
					'user_information' => $user_information,
					'target_url' => $target_url,
					'error_number' => $count,
					'result_url' => $filepath,
				)
			);
		}
		// if the form is submitted but the name is empty
		if ( isset( $_POST["submit_form"] ) && $_POST["target_url"] == "" ) {
			$html .= "<p>You need to fill the required fields.</p>";
		}
		// outputs everything
		echo $html;	
	}
	else {
		$login = '<meta http-equiv="refresh" content="0; url='.wp_login_url( get_permalink() ).'">';
		echo $login;
	}
}
?>
