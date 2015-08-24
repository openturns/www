<HTML>

    <HEAD>
        <META http-equiv="Content-Type" content="text/HTML; charset=UTF-8" />
        <TITLE>OpenTURNS | The official OpenTURNS Website</TITLE>
        <LINK rel="stylesheet" href="home.css" type="text/css" media="screen" />
        <META name="generator" content="Vim 7.2.79" />
    </HEAD>

    <BODY>
<?php
// get dynamic home contents from a wiki page
//$homepage = file_get_contents('http://trac.openturns.org/wiki/HomeSpecific');
$newsurl = 'http://trac.openturns.org/wiki/MoreNews';
$homepage = file_get_contents($newsurl);
?>
        <div id="page">
            <div id="menu">
                <div class="menu-inside">
                    <div id=div-logo>   
                        <a href="http://trac.openturns.org/wiki/AboutLogo"><img id="img-logo" src="logo-openturns.png" alt="About OpenTURNS logo" title="About OpenTURNS logo" /></a>
                    </div>
                    <div class="menu-td">
                        <div id="menu-head">Documentation</div>
                        <a href="http://trac.openturns.org/wiki/QuickStart">Quick Start Guide</a><br>
                        <a href="http://trac.openturns.org/wiki/FAQ" alt="Frequently Asked Questions">FAQ</a><br>
                        <a href="http://trac.openturns.org/wiki/Examples">Examples</a><br>
                        <a href="http://trac.openturns.org/wiki/Documentation">Documentations</a><br>
                        <a href="http://trac.openturns.org/wiki/Training">Training</a><br>
                    </div>
                    <div class="menu-td">
                        <div id="menu-head">Installation</div>
                        <a href="http://trac.openturns.org/wiki/HowToLinuxInstall">Linux</a><br>
                        <a href="http://trac.openturns.org/wiki/HowToWindowsInstall">Windows</a><br>
                        <a href="http://trac.openturns.org/wiki/HowToCondaInstall">Conda</a><br>
                        <a href="http://trac.openturns.org/wiki/HowToInstallDevelopmentVersion">Developers</a>
                    </div>
                    <div class="menu-td">
			<div id="menu-head">Community</div>
                        <a href="http://trac.openturns.org/wiki/Modules">Modules</a><br>
                        <a href="http://trac.openturns.org/wiki/HowToContribute">How to contribute</a><br>
                        <a href="http://openturns.org/mailman/listinfo">Mailing list</a><br>
                        <a href="http://trac.openturns.org/newticket">Report a problem</a>
                    </div>
                    <div class="menu-td">
                        <div id="menu-head">Project</div>
                        <a href="http://trac.openturns.org/wiki/Partnership">PartnerShip</a><br>
                        <a href="http://trac.openturns.org/wiki/LegalInformation">Legal info</a>
                    </div>
                </div>
            </div> <!-- menu -->
            <div id="content">	
                <div id="first-row">
                    <div id="title">
                        <h4 class="title">
                            OpenTURNS
                            <br>
			</h4>
                        <font size="4">  
			OpenTURNS is a scientific library<br>
                        usable as a Python module dedicated <br>
			to the treatment of uncertainties.<br>
                        </font>
                        <br>

<?php
// set ot link
//<font color="#33852d">OpenTURNS</font>
                        /*
                        preg_match_all("/@@@src(.*)@@@src/s", $homepage, $downloadsrc, PREG_PATTERN_ORDER);
                        echo $downloadsrc[1][0];
                        preg_match_all("/@@@exe(.*)@@@exe/s", $homepage, $downloadexe, PREG_PATTERN_ORDER);
                        echo $downloadexe[1][0];
                         */
?>
                        <a style="border:none" href="http://sourceforge.net/projects/openturns/files" target="_blank"><img style="width: 120px; height: 34px;" src="download.png" alt="Download OpenTURNS" title="Download Open TURNS on SourceForge" /></a>
                    </div>
                    <div id="news-frame">
                        <div class="news">
                            <h2 class="newstitle">News</h2>
<?php
// show news title from the fresh news wiki page of the trac
//echo $newspage;
//preg_match_all("/%%%(.*)%%%/s", $homepage, $newscontent, PREG_PATTERN_ORDER);
$newsTitleShowed = 6;
$beginTitlePositions = array(0);
$endTitlePositions = array(0); // indice 0 store end positions of line 0
$nextPos = 0;
$titles = array();
$contents = array();
for ($i = 0; $i < $newsTitleShowed; $i++) {
  // search for a title line looks like: date - content -
  $match = preg_match("|([0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9])( -[^-]*)-|s", 
    $homepage, $newscontent, PREG_OFFSET_CAPTURE, $nextPos);
  if($match == 0)
    break;

  // get pos of the title line
  $beginTitlePositions[$i] = $newscontent[1][1];
  $endTitlePositions[$i] = $newscontent[2][1] + strlen($newscontent[2][0]) + strlen('- <br />');
  #echo 'b'.$beginTitlePositions[$i].' e'.$endTitlePositions[$i].'   <br>';

  $titles[$i] = '                            <p><b>'.$newscontent[1][0].'</b>'.$newscontent[2][0].'</p>';

  // to guess the contents, we need the next begin title pos
  if ($i > 0) {
    $contents[$i - 1] = str_replace ('</li></ul><ul><li>', '', substr($homepage, $endTitlePositions[$i - 1], ($beginTitlePositions[$i] - $endTitlePositions[$i - 1])));
  }
  #echo $contents[$i - 1];

  $nextPos = $beginTitlePositions[$i] + 1;
}
if ($i > 0) {
    $contents[$i - 1] = str_replace ('</li></ul><ul><li>', '', substr($homepage, $endTitlePositions[$i - 1], ($beginTitlePositions[$i] - $endTitlePositions[$i - 1])));
  //$contents[$i - 1] = substr($homepage, $endTitlePositions[$i - 1], ($beginTitlePositions[$i] - $endTitlePositions[$i - 1]));
}

for ($i = 0; $i < $newsTitleShowed; $i++) {
  echo $titles[$i];
}

?>

                            <a href="http://trac.openturns.org/wiki/MoreNews">more news...</a>
                        </div>
                    </div>
                </div>
                <div id="div-overview">
                    <img id="img-overview" src="OpenTURNSOverview.gif" alt="Typical workflow of uncertainty propagation: script, data modelling, propagation algorithm, sensitivity analysis">
                </div>
                <div id="last-news-description">
<?php
// show news content from the fresh news wiki page of the trac
$newsContentShowed = 2; // must be <= to the previous $newsTitleShowed
for ($i = 0; $i < $newsContentShowed; $i++) {
  echo $titles[$i];
  echo $contents[$i];
}
?>
<!--
                    <b>05-05-2011</b> - The <b>fourth OpenTURNS Users Day</b> is coming soon! <br>
                    The program can be found <a style="border:none" href="http://trac.openturns.org/wiki/UsersDay4">here</a>.<br>
                    It will be held the 7th of June, at EDF R&D, Clamart, see  <a style="border:none" href="http://research.edf.com/innovation-and-research-in-the-group/a-strategic-advantage-44206.html" target="_blank">here</a> to locate it.<br>
                    You have to subscribe to participate. Please send an email to anne[DOT]dutfoy[AT]edf[DOT]fr BEFORE THE 27th OF MAY 2011. 
-->
                </div>
            </div>  <!-- content -->
        </div> <!-- page -->
    </BODY>
</HTML>

