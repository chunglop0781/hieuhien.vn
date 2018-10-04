#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib , urllib2 , re , zlib , ast , os , uuid , json
from xbmcswift2 import Plugin , xbmc , xbmcgui , xbmcaddon
oo000 = Plugin ( )
ii = "plugin://plugin.video.hieuhien.vn.moviebox"
oOOo = 32
if 59 - 59: Oo0Ooo . OO0OO0O0O0 * iiiIIii1IIi . iII111iiiii11 % I1IiiI
@ oo000 . route ( '/' )
def IIi1IiiiI1Ii ( ) :
 I11i11Ii ( "None" , "None" )
 oO00oOo = xbmc . translatePath ( xbmcaddon . Addon ( ) . getAddonInfo ( 'path' ) ) . decode ( "utf-8" )
 oO00oOo = xbmc . translatePath ( os . path . join ( oO00oOo , "temp.jpg" ) )

 IiIi11iIIi1Ii = ""
 Oo0O = ( "Busy" , "Bận" , "Band" , "Beschäftigt" , "Bezig" , "忙" , "忙碌" )
 # while True :
  # IiI = urllib . quote ( xbmc . getInfoLabel ( "System.KernelVersion" ) . strip ( ) )
  # if not any ( b in IiI for b in Oo0O ) : break
 # while True :
  # ooOo = urllib . quote ( xbmc . getInfoLabel ( "System.FriendlyName" ) . strip ( ) )
  # if not any ( b in ooOo for b in Oo0O ) : break
 # try :
  # IiIi11iIIi1Ii = open ( '/sys/class/net/eth0/address' ) . read ( ) . strip ( )
 # except :
 # while True :
 #  IiIi11iIIi1Ii = xbmc . getInfoLabel ( "Network.MacAddress" ) . strip ( )
 #  if re . match ( "[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$" , IiIi11iIIi1Ii . lower ( ) ) : break
 #Oo = urllib2 . urlopen ( "http://www.viettv24.com/main/checkActivation.php?MacID=%s&app_id=%s&sys=%s&dev=%s" % ( "6C:0B:84:06:89:71" , "8" , IiI , ooOo ) ) . read ( )
 if (True):
	  o0O = [
	 { 'label' : 'Phim mới' , 'path' : '%s/latest/%s' % ( ii , urllib . quote_plus ( 'http://ictvnow.nl/vod/Api/GetListFilm' ) ) } ,
	 { 'label' : 'Phóng Sự & Tài Liệu' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://ictvnow.nl/vod/Api/GetListFilmByCate' ) , '33' ) , 'thumbnail' : 'http://ictvnow.nl/vod/images/category/13333734-Phim-Tai-Lieu.jpg' } ,
	 { 'label' : 'Ca Nhạc' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://ictvnow.nl/vod/Api/GetListFilmByCate' ) , '34' ) , 'thumbnail' : 'http://ictvnow.nl/vod/images/category/99844308-Ca-nhac.jpg' } ,
	 { 'label' : 'Hài Kịch' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://ictvnow.nl/vod/Api/GetListFilmByCate' ) , '35' ) , 'thumbnail' : 'http://ictvnow.nl/vod/images/category/519820-Hai-Kich.jpg' } ,
	 { 'label' : 'Phim Lẻ' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://ictvnow.nl/vod/Api/GetListFilmByCate' ) , '36' ) , 'thumbnail' : 'http://ictvnow.nl/vod/images/category/6855131-MOD.jpg' } ,
	 { 'label' : 'Phim Bộ' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://ictvnow.nl/vod/Api/GetListFilmByCate' ) , '37' ) , 'thumbnail' : 'http://ictvnow.nl/vod/images/category/46252803-Phim-Bo.jpg' } ,
	 { 'label' : 'Truyền Hình' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://ictvnow.nl/vod/Api/GetListFilmByCate' ) , '38' ) , 'thumbnail' : 'http://ictvnow.nl/vod/images/category/14266234-Live-TV.jpg' } ,
	 { 'label' : 'Nghe Truyện Đọc' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://ictvnow.nl/vod/Api/GetListFilmByCate' ) , '40' ) , 'thumbnail' : 'http://ictvnow.nl/vod/images/category/3488938-Sach-Noi.jpg' } ,
	 { 'label' : 'Dạy Nấu Ăn' , 'path' : '%s/genres/%s/%s' % ( ii , urllib . quote_plus ( 'http://ictvnow.nl/vod/Api/GetListFilmByCate' ) , '41' ) , 'thumbnail' : 'http://ictvnow.nl/vod/images/category/14376243-Am-Nhac.jpg' }
	 ]
	  return oo000 . finish ( o0O )
 else :
  IiiIII111iI = xbmcgui . Dialog ( )
  IiiIII111iI . ok ( "Chú ý" , Oo )
  if 34 - 34: iii1I1I / O00oOoOoO0o0O . O0oo0OO0 + Oo0ooO0oo0oO . I1i1iI1i - II
  if 100 - 100: i11Ii11I1Ii1i . ooO - OOoO / ooo0Oo0 * i1 - OOooo0000ooo
@ oo000 . route ( '/latest/<murl>' )
def OOo000 ( murl ) :
 I11i11Ii ( "Browse" , '/latest/%s' % murl )
 o0O = O0 ( murl , '' )
 if xbmc . getSkinDir ( ) == 'skin.xeebo' and oo000 . get_setting ( 'thumbview' , bool ) :
  return oo000 . finish ( o0O , view_mode = 52 )
 else :
  return oo000 . finish ( o0O )
  if 34 - 34: O0o00 % o0ooo / OOO0O / iiiIIii1IIi * iII111iiiii11 * OOO0O
@ oo000 . route ( '/genres/<murl>/<mid>' )
def i1iIIII ( murl , mid ) :
 I11i11Ii ( "Browse" , '/genres/%s/%s' % ( murl , mid ) )
 o0O = O0 ( murl , mid )
 if xbmc . getSkinDir ( ) == 'skin.xeebo' and oo000 . get_setting ( 'thumbview' , bool ) :
  return oo000 . finish ( o0O , view_mode = 52 )
 else :
  return oo000 . finish ( o0O )
  if 26 - 26: o0ooo . ooo0Oo0 - OOoO % OO0OO0O0O0 + OOoO
@ oo000 . route ( '/mirrors/<murl>/<mid>' )
def i1iiIIiiI111 ( murl , mid ) :
 I11i11Ii ( "Browse" , '/mirrors/%s/%s' % ( murl , mid ) )
 o0O = [ ]
 for oooOOOOO in i1iiIII111ii ( murl , mid ) :
  i1iIIi1 = { }
  i1iIIi1 [ "label" ] = oooOOOOO [ "name" ] . strip ( )
  ii11iIi1I = str ( uuid . uuid1 ( ) )
  iI111I11I1I1 = oo000 . get_storage ( ii11iIi1I )
  iI111I11I1I1 [ "list" ] = oooOOOOO [ "eps" ]
  i1iIIi1 [ "path" ] = '%s/eps/%s' % ( ii , urllib . quote_plus ( ii11iIi1I ) )
  o0O . append ( i1iIIi1 )
 return oo000 . finish ( o0O )
 if 55 - 55: I1i1iI1i % I1IiiI / i1 - ooO - OO0OO0O0O0 / iii1I1I
@ oo000 . route ( '/eps/<eps_list>' )
def iii11iII ( eps_list ) :
 I11i11Ii ( "Browse" , '/eps' )
 o0O = [ ]
 for i1I111I in oo000 . get_storage ( eps_list ) [ "list" ] :
  i1iIIi1 = { }
  i1iIIi1 [ "label" ] = i1I111I [ "name" ] . strip ( )
  i1iIIi1 [ "is_playable" ] = True
  i1iIIi1 [ "path" ] = '%s/play/%s' % ( ii , urllib . quote_plus ( i1I111I [ "url" ] ) )
  o0O . append ( i1iIIi1 )
 return oo000 . finish ( o0O )
 if 1 - 1: O0o00 % Oo0ooO0oo0oO * ooo0Oo0
@ oo000 . route ( '/play/<mid>' )
def OoOo ( mid ) :
 I11i11Ii ( "Play" , '/play/%s' % ( mid ) )
 IiIiIi = xbmcgui . DialogProgress ( )
 IiIiIi . create ( 'Hieuhien.vn' , '. Please wait...' )
 oo000 . set_resolved_url ( IIiI ( mid ) )
 IiIiIi . close ( )
 del IiIiIi
 if 22 - 22: O0oo0OO0 % i1
def IIiI ( mid ) :
 Oo = oo ( "http://ictvnow.nl/vod/Api/GetLinkByEpiId" , mid )
 OO0O00 = json . loads ( Oo ) [ "link" ] [ 0 ] [ "url" ]
 ii1 = OO0O00
 if "youtube" in OO0O00 :
  o0oO0o00oo = re . compile ( '(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)' ) . findall ( OO0O00 )
  II1i1Ii11Ii11 = o0oO0o00oo [ 0 ] [ len ( o0oO0o00oo [ 0 ] ) - 1 ] . replace ( 'v/' , '' )
  return 'plugin://plugin.video.youtube/play/?video_id=%s' % II1i1Ii11Ii11
 if "picasa" in OO0O00 :
  iII11i = re . compile ( 'authkey=(.+?)#' ) . findall ( OO0O00 )
  O0O00o0OOO0 = re . compile ( 'https://picasaweb.google.com/(\d+)/' ) . findall ( OO0O00 )
  Ii1iIIIi1ii = re . compile ( '#(\d+)' ) . findall ( OO0O00 )
  o0oo0o0O00OO = 480
  if oo000 . get_setting ( 'HQ' , bool ) :
   o0oo0o0O00OO = 720
  if ( O0O00o0OOO0 and Ii1iIIIi1ii ) :
   o0oO = "https://picasaweb.google.com/data/feed/api/user/%s/photoid/%s?alt=json%s" % ( O0O00o0OOO0 [ 0 ] , Ii1iIIIi1ii [ 0 ] , "" if not iII11i else "&authkey=" + iII11i [ 0 ] )
   Oo = urllib2 . urlopen ( o0oO ) . read ( )
   I1i1iii = json . loads ( Oo ) [ "feed" ] [ "media$group" ] [ "media$content" ]
   for i1iiI11I in I1i1iii :
    if ( i1iiI11I [ "type" ] == "video/mpeg4" ) and ( int ( i1iiI11I [ "height" ] ) <= o0oo0o0O00OO ) :
     ii1 = i1iiI11I [ "url" ]
  else :
   Oo = urllib2 . urlopen ( OO0O00 ) . read ( )
   o0oO = re . compile ( '(https://picasaweb.google.com/data/feed/tiny/user/\d+/photoid/\d+\?alt=jsonm&gupi=.+?)"' ) . findall ( Oo ) [ 0 ]
   Oo = urllib2 . urlopen ( o0oO ) . read ( )
   I1i1iii = json . loads ( Oo ) [ "feed" ] [ "media" ] [ "content" ]
   for i1iiI11I in I1i1iii :
    if ( i1iiI11I [ "type" ] == "video/mpeg4" ) and ( int ( i1iiI11I [ "height" ] ) <= o0oo0o0O00OO ) :
     ii1 = i1iiI11I [ "url" ]
 return ii1
 if 29 - 29: iII111iiiii11
def O0 ( url , mid ) :
 Oo = oo ( url , mid )
 o0O = [ ]
 for iI in json . loads ( Oo ) [ "film" ] :
  i1iIIi1 = { }
  i1iIIi1 [ "label" ] = iI [ "title_en" ]
  i1iIIi1 [ "thumbnail" ] = iI [ "cover_image" ] if ( "://" in iI [ "cover_image" ] ) else "http://ictvnow.nl" + urllib . quote ( iI [ "cover_image" ] . encode ( "utf8" ) )
  i1iIIi1 [ "path" ] = '%s/%s/%s/%s' % ( ii , "mirrors" , urllib . quote_plus ( 'http://ictvnow.nl/vod/Api/GetEpiByFilmId' ) , iI [ "ID" ] . strip ( ) )
  o0O . append ( i1iIIi1 )
 return o0O
 if 28 - 28: OOoO - O0o00 . O0o00 + I1i1iI1i - iII111iiiii11 + OO0OO0O0O0
def i1iiIII111ii ( murl , mid ) :
 Oo = oo ( murl , mid )
 oOoOooOo0o0 = [ ]
 for OOOO in json . loads ( Oo ) [ "server" ] :
  OOO00 = [ ]
  for iiiiiIIii in OOOO [ "data" ] :
   i1I111I = { }
   i1I111I [ "url" ] = iiiiiIIii [ "ID" ]
   i1I111I [ "name" ] = iiiiiIIii [ "name" ]
   OOO00 . append ( i1I111I )
  oooOOOOO = { }
  oooOOOOO [ "name" ] = "%s - %s (%s tập)" % ( OOOO [ "alias" ] . encode ( "utf8" ) , OOOO [ "name" ] . encode ( "utf8" ) , OOOO [ "episode" ] )
  oooOOOOO [ "eps" ] = OOO00
  oOoOooOo0o0 . append ( oooOOOOO )
 return oOoOooOo0o0
 if 71 - 71: OOoO + i1 * OOoO - Oo0ooO0oo0oO * II
@ oo000 . cached ( TTL = 60 )
def oo ( url , mid ) :
 Oooo0Ooo000 = urllib2 . Request ( url )
 Oooo0Ooo000 . add_header ( 'Accept-Encoding' , 'gzip, deflate, sdch' )
 ooii11I = ""
 if mid != "" :
  if "GetListFilmByCate" in url :
   Ooo0OO0oOO = urllib . urlencode ( { 'cateid' : mid } )
  else :
   Ooo0OO0oOO = urllib . urlencode ( { 'id' : mid } )
  ii11i1 = urllib2 . urlopen ( Oooo0Ooo000 , data = Ooo0OO0oOO )
  ooii11I = ii11i1 . read ( )
  ii11i1 . close ( )
  if "gzip" in ii11i1 . info ( ) . getheader ( 'Content-Encoding' ) :
   ooii11I = zlib . decompress ( ooii11I , 16 + zlib . MAX_WBITS )
  return ooii11I
 else :
  ii11i1 = urllib2 . urlopen ( Oooo0Ooo000 )
  ooii11I = ii11i1 . read ( )
  ii11i1 . close ( )
  if "gzip" in ii11i1 . info ( ) . getheader ( 'Content-Encoding' ) :
   ooii11I = zlib . decompress ( ooii11I , 16 + zlib . MAX_WBITS )
  return ooii11I
  if 29 - 29: i11Ii11I1Ii1i % O00oOoOoO0o0O + OOO0O / II + OOoO * II
i1I1iI = xbmc . translatePath ( xbmcaddon . Addon ( 'plugin.video.hieuhien.vn.moviebox' ) . getAddonInfo ( 'profile' ) )
if 93 - 93: iiiIIii1IIi % ooO * I1IiiI
if os . path . exists ( i1I1iI ) == False :
 os . mkdir ( i1I1iI )
Ii11Ii1I = os . path . join ( i1I1iI , 'visitor' )
if 72 - 72: OOooo0000ooo / I1IiiI * O0oo0OO0 - o0ooo
if os . path . exists ( Ii11Ii1I ) == False :
 from random import randint
 Oo0O0O0ooO0O = open ( Ii11Ii1I , "w" )
 Oo0O0O0ooO0O . write ( str ( randint ( 0 , 0x7fffffff ) ) )
 Oo0O0O0ooO0O . close ( )
 if 15 - 15: i11Ii11I1Ii1i + I1i1iI1i - iII111iiiii11 / OOoO
def oo000OO00Oo ( utm_url ) :
 O0OOO0OOoO0O = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
 import urllib2
 try :
  Oooo0Ooo000 = urllib2 . Request ( utm_url , None ,
 { 'User-Agent' : O0OOO0OOoO0O }
 )
  ii11i1 = urllib2 . urlopen ( Oooo0Ooo000 ) . read ( )
 except :
  print ( "GA fail: %s" % utm_url )
 return ii11i1
 if 70 - 70: O0o00 * O0oo0OO0 * ooo0Oo0 / i1
def I11i11Ii ( group , name ) :
 try :
  try :
   from hashlib import md5
  except :
   from md5 import md5
  from random import randint
  import time
  from urllib import unquote , quote
  from os import environ
  from hashlib import sha1
  oO = "1.0"
  OOoO0O00o0 = open ( Ii11Ii1I ) . read ( )
  iII = "MovieBox"
  o0 = "UA-52209804-2"
  ooOooo000oOO = "www.viettv24.com"
  Oo0oOOo = "http://www.google-analytics.com/__utm.gif"
  if name == "None" :
   Oo0OoO00oOO0o = Oo0oOOo + "?" + "utmwv=" + oO + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( iII ) + "&utmac=" + o0 + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , OOoO0O00o0 , "1" , "1" , "2" ] )
   if 80 - 80: ooO + OOoO - OOoO % OOooo0000ooo
   if 63 - 63: O00oOoOoO0o0O - i11Ii11I1Ii1i + OO0OO0O0O0 % ooo0Oo0 / iiiIIii1IIi / II
   if 98 - 98: OOooo0000ooo * OOooo0000ooo / OOooo0000ooo + ooo0Oo0
   if 34 - 34: OOO0O
   if 15 - 15: ooo0Oo0 * OOO0O * O0oo0OO0 % Oo0Ooo % I1i1iI1i - OOoO
  else :
   if group == "None" :
    Oo0OoO00oOO0o = Oo0oOOo + "?" + "utmwv=" + oO + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( iII + "/" + name ) + "&utmac=" + o0 + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , OOoO0O00o0 , "1" , "1" , "2" ] )
    if 68 - 68: o0ooo % I1IiiI . O0o00 . i11Ii11I1Ii1i
    if 92 - 92: OOooo0000ooo . o0ooo
    if 31 - 31: o0ooo . I1i1iI1i / OO0OO0O0O0
    if 89 - 89: I1i1iI1i
    if 68 - 68: Oo0ooO0oo0oO * iII111iiiii11 % OO0OO0O0O0 + Oo0ooO0oo0oO + OOO0O
   else :
    Oo0OoO00oOO0o = Oo0oOOo + "?" + "utmwv=" + oO + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( iII + "/" + group + "/" + name ) + "&utmac=" + o0 + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , OOoO0O00o0 , "1" , "1" , "2" ] )
    if 4 - 4: OOO0O + OO0OO0O0O0 * OOoO
    if 55 - 55: O0oo0OO0 + iiiIIii1IIi / I1i1iI1i * ooO - Oo0Ooo - i1
    if 25 - 25: i11Ii11I1Ii1i
    if 7 - 7: I1IiiI / O00oOoOoO0o0O * o0ooo . O0o00 . iiiIIii1IIi
    if 13 - 13: OOoO / Oo0Ooo
    if 2 - 2: O00oOoOoO0o0O / OO0OO0O0O0 / II % I1i1iI1i % i1
  print "============================ POSTING ANALYTICS ============================"
  oo000OO00Oo ( Oo0OoO00oOO0o )
  if 52 - 52: II
  if not group == "None" :
   o0OO0oOO0O0 = Oo0oOOo + "?" + "utmwv=" + oO + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmhn=" + quote ( ooOooo000oOO ) + "&utmt=" + "events" + "&utme=" + quote ( "5(" + iII + "*" + group + "*" + name + ")" ) + "&utmp=" + quote ( iII ) + "&utmac=" + o0 + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , "1" , OOoO0O00o0 , "1" , "2" ] )
   if 8 - 8: ooO
   if 7 - 7: II - O00oOoOoO0o0O
   if 100 - 100: ooO + ooo0Oo0 . OOoO * i1
   if 73 - 73: I1IiiI + O00oOoOoO0o0O
   if 46 - 46: Oo0ooO0oo0oO . O0oo0OO0 - iII111iiiii11
   if 93 - 93: OOooo0000ooo
   if 10 - 10: ooo0Oo0
   if 82 - 82: i11Ii11I1Ii1i - iiiIIii1IIi / OOoO + i1
   try :
    print "============================ POSTING TRACK EVENT ============================"
    oo000OO00Oo ( o0OO0oOO0O0 )
   except :
    print "============================  CANNOT POST TRACK EVENT ============================"
    if 87 - 87: ooO * i11Ii11I1Ii1i + OOoO / iiiIIii1IIi / OOooo0000ooo
 except :
  print "================  CANNOT POST TO ANALYTICS  ================"
  if 37 - 37: OOooo0000ooo - OOO0O * ooO % Oo0Ooo - o0ooo
if __name__ == '__main__' :
 oo000 . run ( )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
