#!/usr/bin/python
# coding=utf-8
import requests,re,time
from xbmcswift2 import Plugin, xbmc, xbmcgui, xbmcaddon
import hashlib

plugin         = Plugin()
pluginrootpath = "plugin://plugin.video.hieuhien.vn.sctv"

headers = {
	"X-Requested-With" : "XMLHttpRequest",
	"User-Agent"       : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
	"Content-Type"     : "application/x-www-form-urlencoded; charset=UTF-8",
	"Accept-Encoding"  : "gzip, deflate"
}

@plugin.route('/')
def Home():
	items = [
		{'label': 'BTV 5 HD', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/119', 'thumbnail': 'https://static-stage.sctv.vn/channel/119/ssport3.png', 'is_playable': True},
		{'label': 'SCTV 15', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/20', 'thumbnail': 'https://static-stage.sctv.vn/channel/20/ssport2.png', 'is_playable': True},
		{'label': 'SCTV HD Thể Thao', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/22', 'thumbnail': 'https://static-stage.sctv.vn/channel/22/SCTVThethaoHD-1.png', 'is_playable': True},
		{'label': 'ANTV', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/31', 'thumbnail': 'https://static-stage.sctv.vn/channel/31/antv.png', 'is_playable': True},
		{'label': 'Ariang', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/157', 'thumbnail': 'https://static-stage.sctv.vn/channel/157/arirang(korea).png', 'is_playable': True},
		{'label': 'Channel News Asia', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/163', 'thumbnail': 'https://static-stage.sctv.vn/channel/163/channelnewasia.png', 'is_playable': True},
		{'label': 'Channel V', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/158', 'thumbnail': 'https://static-stage.sctv.vn/channel/158/channelV.png', 'is_playable': True},
		{'label': 'DW', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/159', 'thumbnail': 'https://static-stage.sctv.vn/channel/159/DW(deutschewelle).png', 'is_playable': True},
		{'label': 'HTV2', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/63', 'thumbnail': 'https://static-stage.sctv.vn/channel/63/htv21.png', 'is_playable': True},
		{'label': 'HTV7 HD', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/38', 'thumbnail': 'https://static-stage.sctv.vn/channel/38/htv7-hd.png', 'is_playable': True},
		{'label': 'HTV9 HD', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/40', 'thumbnail': 'https://static-stage.sctv.vn/channel/40/htv9-hd.png', 'is_playable': True},
		{'label': 'National Geographic', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/160', 'thumbnail': 'https://static-stage.sctv.vn/channel/160/NationalGeographic.png', 'is_playable': True},
		{'label': 'NHK World', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/161', 'thumbnail': 'https://static-stage.sctv.vn/channel/161/nhkworld(korea).png', 'is_playable': True},
		{'label': 'Quốc Hội Việt Nam', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/123', 'thumbnail': 'https://static-stage.sctv.vn/channel/123/QuocHoi.png', 'is_playable': True},
		{'label': 'Quốc Phòng Việt Nam', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/140', 'thumbnail': 'https://static-stage.sctv.vn/channel/140/QPVN.png', 'is_playable': True},
		{'label': 'SCTV 01', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/7', 'thumbnail': 'https://static-stage.sctv.vn/channel/7/s1.png', 'is_playable': True},
		{'label': 'SCTV 02 HD - Yan TV', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/2', 'thumbnail': 'https://static-stage.sctv.vn/channel/2/s2HD.png', 'is_playable': True},
		{'label': 'SCTV 04', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/9', 'thumbnail': 'https://static-stage.sctv.vn/channel/9/s4.png', 'is_playable': True},
		{'label': 'SCTV 04 HD - Giải trí tổng hợp', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/109', 'thumbnail': 'https://static-stage.sctv.vn/channel/109/Giatritonghop.png', 'is_playable': True},
		{'label': 'SCTV 06 HD', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/16', 'thumbnail': 'https://static-stage.sctv.vn/channel/16/sctv6hd.png', 'is_playable': True},
		{'label': 'SCTV 07', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/13', 'thumbnail': 'https://static-stage.sctv.vn/channel/13/s7.png', 'is_playable': True},
		{'label': 'SCTV 09', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/8', 'thumbnail': 'https://static-stage.sctv.vn/channel/8/s9.png', 'is_playable': True},
		{'label': 'SCTV 09 HD - Phim Châu Á', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/129', 'thumbnail': 'https://static-stage.sctv.vn/channel/129/S-PhimChauAHD.png', 'is_playable': True},
		{'label': 'SCTV 11', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/106', 'thumbnail': 'https://static-stage.sctv.vn/channel/106/s11.png', 'is_playable': True},
		{'label': 'SCTV 11 HD - Văn hóa - Nghệ thuật', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/130', 'thumbnail': 'https://static-stage.sctv.vn/channel/130/s-Vanhoa-Nghethuat-HD.png', 'is_playable': True},
		{'label': 'SCTV 12', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/103', 'thumbnail': 'https://static-stage.sctv.vn/channel/103/S12.png', 'is_playable': True},
		{'label': 'SCTV 13', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/18', 'thumbnail': 'https://static-stage.sctv.vn/channel/18/s13.png', 'is_playable': True},
		{'label': 'SCTV 13 HD - Phụ nữ & Gia đình', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/114', 'thumbnail': 'https://static-stage.sctv.vn/channel/114/PhuNuVagd.png', 'is_playable': True},
		{'label': 'SCTV 14', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/19', 'thumbnail': 'https://static-stage.sctv.vn/channel/19/s14.png', 'is_playable': True},
		{'label': 'SCTV 16', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/21', 'thumbnail': 'https://static-stage.sctv.vn/channel/21/s16.png', 'is_playable': True},
		{'label': 'SCTV 18', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/164', 'thumbnail': 'https://static-stage.sctv.vn/channel/164/s18.png', 'is_playable': True},
		{'label': 'SCTV HD Du Lịch', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/17', 'thumbnail': 'https://static-stage.sctv.vn/channel/17/DuLich.png', 'is_playable': True},
		{'label': 'SCTV HD Hài', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/85', 'thumbnail': 'https://static-stage.sctv.vn/channel/85/Hai.png', 'is_playable': True},
		{'label': 'SCTV HD Phim nước ngoài đặc sắc', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/110', 'thumbnail': 'https://static-stage.sctv.vn/channel/110/PhimNuocNgoai.png', 'is_playable': True},
		{'label': 'SCTV HD Phim Tổng Hợp', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/108', 'thumbnail': 'https://static-stage.sctv.vn/channel/108/S-PhimTongHopHD.png', 'is_playable': True},
		{'label': 'SCTV HD Phim Việt', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/84', 'thumbnail': 'https://static-stage.sctv.vn/channel/84/PhimVietHD.png', 'is_playable': True},
		{'label': 'SCTV HD Sân Khấu', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/107', 'thumbnail': 'https://static-stage.sctv.vn/channel/107/SCTVHDSanKhau.png', 'is_playable': True},
		{'label': 'SCTV Phim Tổng Hợp', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/4', 'thumbnail': 'https://static-stage.sctv.vn/channel/4/PhimTongHopSD.png', 'is_playable': True},
		{'label': 'SCTV Phim Tổng Hợp', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/4', 'thumbnail': 'https://static-stage.sctv.vn/channel/4/PhimTongHopSD.png', 'is_playable': True},
		{'label': 'SEE HD (SCTV HD Thiếu nhi)', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/112', 'thumbnail': 'https://static-stage.sctv.vn/channel/112/ThieuNhi.png', 'is_playable': True},
		{'label': 'SEE TV - SCTV 3', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/10', 'thumbnail': 'https://static-stage.sctv.vn/channel/10/s3.png', 'is_playable': True},
		{'label': 'Sofa TV', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/135', 'thumbnail': 'https://static-stage.sctv.vn/channel/135/logosofatv.png', 'is_playable': True},
		{'label': 'STARMOVIES', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/26', 'thumbnail': 'https://static-stage.sctv.vn/channel/26/star-movie.png', 'is_playable': True},
		{'label': 'STARWORLD', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/28', 'thumbnail': 'https://static-stage.sctv.vn/channel/28/starworld.png', 'is_playable': True},
		{'label': 'TH An Giang', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/141', 'thumbnail': 'https://static-stage.sctv.vn/channel/141/ATVangiang.png', 'is_playable': True},
		{'label': 'TH Cần Thơ', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/118', 'thumbnail': 'https://static-stage.sctv.vn/channel/118/thtpct.PNG', 'is_playable': True},
		{'label': 'TH Đồng Tháp', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/147', 'thumbnail': 'https://static-stage.sctv.vn/channel/147/THDTdongthap.png', 'is_playable': True},
		{'label': 'TH Hậu Giang', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/148', 'thumbnail': 'https://static-stage.sctv.vn/channel/148/HGTVhaugiang.png', 'is_playable': True},
		{'label': 'TH Ninh Bình', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/150', 'thumbnail': 'https://static-stage.sctv.vn/channel/150/NTVninhbinh.png', 'is_playable': True},
		{'label': 'Th Ninh Thuận', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/151', 'thumbnail': 'https://static-stage.sctv.vn/channel/151/NTVninhthuan.png', 'is_playable': True},
		{'label': 'TH Vĩnh Long 1', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/62', 'thumbnail': 'https://static-stage.sctv.vn/channel/62/THVL1.png', 'is_playable': True},
		{'label': 'TH Vĩnh Long 2', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/124', 'thumbnail': 'https://static-stage.sctv.vn/channel/124/THVL2.png', 'is_playable': True},
		{'label': 'ToDay TV', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/5', 'thumbnail': 'https://static-stage.sctv.vn/channel/5/Today.png', 'is_playable': True},
		{'label': 'TTXVN', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/122', 'thumbnail': 'https://static-stage.sctv.vn/channel/122/TTXVn.png', 'is_playable': True},
		{'label': 'TV5 Monde', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/162', 'thumbnail': 'https://static-stage.sctv.vn/channel/162/tv5(monde).png', 'is_playable': True},
		{'label': 'VOV', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/121', 'thumbnail': 'https://static-stage.sctv.vn/channel/121/logo_phatthanh_vov.png', 'is_playable': True},
		{'label': 'VTC 10', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/153', 'thumbnail': 'https://static-stage.sctv.vn/channel/153/vtc10.png', 'is_playable': True},
		{'label': 'VTC 14', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/155', 'thumbnail': 'https://static-stage.sctv.vn/channel/155/vtc14.png', 'is_playable': True},
		{'label': 'VTC 9 Lets Việt', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/65', 'thumbnail': 'https://static-stage.sctv.vn/channel/65/vtc9_letsviet.png', 'is_playable': True},
		{'label': 'VTV1 HD', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/41', 'thumbnail': 'https://static-stage.sctv.vn/channel/41/vtv1-hd.png', 'is_playable': True},
		{'label': 'VTV3 HD', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/137', 'thumbnail': 'https://static-stage.sctv.vn/channel/137/vtv3hd.png', 'is_playable': True},
		{'label': 'VTV9', 'path': 'plugin://plugin.video.hieuhien.vn.sctv/play/36', 'thumbnail': 'https://static-stage.sctv.vn/channel/36/vtv9_sd.jpg', 'is_playable': True}
	]
	if plugin.get_setting('thumbview', bool):
		if xbmc.getSkinDir() in ('skin.confluence','skin.eminence'):
			return plugin.finish(items, view_mode = 500)
		elif xbmc.getSkinDir() == 'skin.xeebo':
			return plugin.finish(items, view_mode = 52)
		else:
			return plugin.finish(items)
	else:
		return plugin.finish(items)

def LogIn(phone, passw):
	try:
		headers = {
			"User-Agent"      : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
			"Accept-Encoding" : "gzip, deflate, sdch, br"
		}
		payloads = {
			"mobile"   : phone,
			"password" : passw
		}
		sess = requests.Session()
		sess.headers.update(headers)
		resp = sess.post("http://tv24.vn/client/login/process", data = payloads)
		user_name = re.compile('(?s)<span class="user-info">(.+?)</span>').findall(resp.text)[0].strip()
		return user_name, sess
	except:
		return None, None

def getTV24Link(cid, sess):	
	mes = 'Không lấy được kênh %s từ TV24.VN!' % cid
	try:
		resp = sess.get(
			"http://tv24.vn/kenh-truyen-hinh/%s/-" % cid
		)
		token = re.compile('value="(\d+-.+?)"').findall(resp.text)[0]
		payloads = {
			"channel_id": cid,
			"channel_token": token
		}
		resp = sess.post(
			"http://tv24.vn/client/channel/link",
			data = payloads
		)
		res_json = resp.json()
		mes = res_json["message"]
		enc_url = res_json["data"]["PLAY_URL"]
		time.sleep(3)
		return dec(token,enc_url)
	except:
		header  = "Get link thất bại!!!"
		message = mes
		xbmc.executebuiltin('Notification("%s", "%s", "%d", "%s")' % (header, message, 10000, ''))
		return ""

def dec(key, b64_encrypted_str):
	b64_encrypted_str = b64_encrypted_str.decode("base64")
	j    = 0
	x    = ""
	out  = ""
	s    = [i for i in range(0,256)]
	for i in range(0,256):
		j    = (j + s[i] + ord(key[i % len(key)])) % 256
		x    = s[i]
		s[i] = s[j]
		s[j] = x
	i=0;
	j=0;
	for k in range (0, len(b64_encrypted_str)):
		i    = (i + 1) % 256
		j    = (j + s[i]) % 256
		x    = s[i]
		s[i] = s[j]
		s[j] = x
		out += chr(ord(b64_encrypted_str[k])^s[(s[i] + s[j]) % 256])
	return out

@plugin.route('/play/<cid>', name="play_with_local_acc")
@plugin.route('/play/<cid>/<phone>/<passw>')
def play(cid,phone="",passw=""):
	if phone == "": phone = plugin.get_setting('usernamesctv')
	if passw == "":
		passw = plugin.get_setting('passwordsctv')
		# hash_object = hashlib.md5(passw)
		# passw = hash_object.hexdigest()
	user_name, sess  = LogIn(phone, passw)
	if user_name is not None:
		dialogWait = xbmcgui.DialogProgress()
		dialogWait.create('SCTV (tv24.vn)', 'Chào [COLOR orange]%s[/COLOR]. Đang mở kênh %s. Vui lòng đợi trong giây lát...' % (user_name.encode("utf8"), cid))
		plugin.set_resolved_url(get_playable_url(cid,sess))
		dialogWait.close()
		del dialogWait
	else:
		dialog = xbmcgui.Dialog()
		yes = dialog.yesno(
			'Đăng nhập không thành công!\n',
			'Chưa có tài khoản? Đăng ký tại [COLOR lime]tv24.vn/dang-ky[/COLOR].\n[COLOR yellow]Bạn muốn nhập tài khoản bây giờ không?[/COLOR]',
			yeslabel='OK, nhập ngay',
			nolabel='Chờ tí, Đăng ký đã!'
		)
		if yes:
			plugin.open_settings()
			play(cid)

def get_playable_url(cid,sess):
	return getTV24Link(cid, sess)

if __name__ == '__main__':
	plugin.run()