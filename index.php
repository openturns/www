

<HTML>

  <HEAD>
    <META http-equiv="Content-Type" content="text/HTML; charset=UTF-8" />

    <TITLE>OpenTURNS</TITLE>

    <LINK rel="stylesheet" href="index.css" type="text/css" media="screen" />
    <LINK rel="shortcut icon" href="/favicon.ico" type="image/x-icon" /> 
    <LINK rel="icon" href="/favicon.ico" type="image/x-icon" />
    <META name="generator" content="Vim 7.2.79" />


<SCRIPT language="JavaScript">
<!--
// automatically resize iframe on load or reload
function resizeSubFrame()
{
  // height of the banner
  var bannerHeight = 42;

  //find the height of the internal page
  var subHeight = document.body.scrollHeight; 

  //change the height of the iframe
  document.getElementById('subFrame').height = subHeight - bannerHeight;
}
//-->
</SCRIPT>

<?php
if (isset($_GET['subwindow']))
  $subwindow = $_GET['subwindow'];
else
  $subwindow = 'home';
?>

  </HEAD>

<!-- show banner -->
  <BODY>
    <DIV id="page">
      <DIV id="header">
        <H1><A href="/">OpenTURNS</A></H1>
        <P class="description">The official OpenTURNS website</P>
        <UL class="sitemenu">
          <LI><A <?php if ($subwindow == 'home') echo 'class="active"'; ?> href="/?subwindow=home" title="Go to the OpenTURNS homepage.">Home</A></LI>
          <LI><A <?php if ($subwindow == 'doc') echo 'class="active"'; ?> href="/?subwindow=doc" title="Get OpenTURNS documentation.">Doc</A></LI>
          <LI><A <?php if ($subwindow == 'share') echo 'class="active"'; ?> href="/?subwindow=share" title="Go to the share place.">Share</A></LI>
          <LI><A <?php if ($subwindow == 'code') echo 'class="active"'; ?> href="https://github.com/openturns" target="_blank" title="Browse OpenTURNS source code.">Code</A></LI>
          <LI><A <?php if ($subwindow == 'download') echo 'class="active"'; ?> href="http://sourceforge.net/projects/openturns/files" target="_blank" title="Download OpenTURNS.">Download</A></LI>
        </UL>
      </DIV>

    </DIV>
    <HR/>

<!-- show sub window -->
<?php
//$suburl = '/home.php';
switch ($subwindow) {
case 'wiki': 
  $suburl = 'http://trac.openturns.org/wiki';
  break;
case 'share': 
  $suburl = 'http://trac.openturns.org/blog';
  break;
case 'doc':
  $suburl = 'http://trac.openturns.org/wiki/Documentation';
  break;
case 'code':
  $suburl = 'https://github.com/openturns';
  break;
case 'download':
  $suburl = 'http://sourceforge.net/projects/openturns/files';
  break;
default:
  $suburl = '/home.php';
  //$suburl = 'http://trac.openturns.org/wiki';
}
echo '<IFRAME onload="resizeSubFrame();" id="subFrame" src="' . $suburl . '" frameborder="0" width="100%" height="85%" marginwidth="1" marginheight="1">Frame not supported. Frame that should has been displayed : <A href="' . $suburl . '">' . $suburl . '</A>.</IFRAME>';

?>
  </BODY>
</HTML>

