#!/usr/bin/python
# coding=utf-8
import urllib,requests,re,json,HTMLParser,os,uuid
from xbmcswift2 import Plugin, xbmc, xbmcgui, xbmcaddon
import hashlib

plugin         = Plugin()
h              = HTMLParser.HTMLParser()
pluginrootpath = "plugin://plugin.video.sctv.hieuhien.vn"
#
addon = xbmcaddon.Addon(id='plugin.video.sctv.hieuhien.vn')
profile = addon.getAddonInfo('profile')
home = addon.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ))
dataPatch = xbmc.translatePath(os.path.join(home, 'resources')) 

# Fake Device Params
device_model    = 'Xiaomi+Redmi+Note+3'
fake_device_id  = '825434'
manufacturer_id = '28B5FFFAA038CC150D9FAC9A12E26C18'
tok             = 'VjNqT05kcTVUMDVrUnpWVU1YQnJVbXBXVUZaclNsTlZSbEYzVUZFOVBRPT0='
######################################

query_string = {
	'tok' : tok,
	'cli' : '1',
	'lang': 'vi'
}

headers = {
	'Content-Type'   : 'application/x-www-form-urlencoded; charset =UTF-8',
	'Accept-Encoding': 'gzip'
}

def GetValidID(mobile, passw):
	login_uri = 'https://aaa-stage.sctv.vn/apiott/member_login'
	payloads = {
		'device_model'    : device_model,
		'password'        : passw,
		'device_id'       : fake_device_id,
		'manufacturer_id' : manufacturer_id,
		'type_id'         : '2',
		'mobile'          : mobile,
		'member_id'       : '0'
	}
	js = requests.post(login_uri,params=query_string,data=payloads,headers=headers).json()

	if js['result'] == '1':
		return js['data'][0]['DEVICE_ID'].encode('utf8'), js['data'][0]['MEMBER_ID'].encode('utf8')
	else:
		return None, None

def GetChannelPlayURL(channel_id, valid_user_id, valid_device_id):
	link_play = None

	if valid_user_id:
		channel_play    = 'https://api-stage.sctv.vn/apiott/channel_play'
		payloads = {
			'image_type'     : 'app_192_276',
			'product_id'     : '3',
			'channel_id'     : channel_id,
			'cate_id'        : '-1',
			'device_id'      : valid_device_id,
			'manufacturer_id': manufacturer_id,
			'member_id'      : valid_user_id
		}
		res = requests.post(channel_play,params=query_string,data=payloads,headers=headers)
		try :
			link_play = res.json()['data'][0]['RESULT_URL']
		except:
			pass
	if channel_id in ["2","106"]: #check id có thuộc nhóm đài bị mất tiếng?
		res = requests.get(link_play).text
		# trích xuất link play kế cuối
		res = re.compile("chunklist_.+?m3u8").findall(res)[-2]
		# ghép vào thành link _play hoàn chỉnh
		link_play = "/".join(link_play.split("/")[:-1] + [res])
	return link_play

@plugin.route('/')
def Home():
	items = [
		{'label': 'ANTV', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/31', 'thumbnail': 'https://static-stage.sctv.vn/channel/31/antv.png', 'is_playable': True},
		{'label': 'Ariang', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/157', 'thumbnail': 'https://static-stage.sctv.vn/channel/157/arirang(korea).png', 'is_playable': True},
		{'label': 'BTV3 HD', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/120', 'thumbnail': 'https://static-stage.sctv.vn/channel/120/btv3HD.png', 'is_playable': True},
		{'label': 'BTV5 HD', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/119', 'thumbnail': 'https://static-stage.sctv.vn/channel/119/btv5hd.png', 'is_playable': True},
		{'label': 'Channel News Asia', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/163', 'thumbnail': 'https://static-stage.sctv.vn/channel/163/channelnewasia.png', 'is_playable': True},
		{'label': 'Channel V', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/158', 'thumbnail': 'https://static-stage.sctv.vn/channel/158/channelV.png', 'is_playable': True},
		{'label': 'DW', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/159', 'thumbnail': 'https://static-stage.sctv.vn/channel/159/DW(deutschewelle).png', 'is_playable': True},
		{'label': 'HTV2', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/63', 'thumbnail': 'https://static-stage.sctv.vn/channel/63/htv21.png', 'is_playable': True},
		{'label': 'HTV7 HD', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/38', 'thumbnail': 'https://static-stage.sctv.vn/channel/38/htv7-hd.png', 'is_playable': True},
		{'label': 'HTV9 HD', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/40', 'thumbnail': 'https://static-stage.sctv.vn/channel/40/htv9-hd.png', 'is_playable': True},
		{'label': 'National Geographic', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/160', 'thumbnail': 'https://static-stage.sctv.vn/channel/160/NationalGeographic.png', 'is_playable': True},
		{'label': 'NHK World', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/161', 'thumbnail': 'https://static-stage.sctv.vn/channel/161/nhkworld(korea).png', 'is_playable': True},
		{'label': 'Quốc Hội Việt Nam', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/123', 'thumbnail': 'https://static-stage.sctv.vn/channel/123/QuocHoi.png', 'is_playable': True},
		{'label': 'Quốc Phòng Việt Nam', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/140', 'thumbnail': 'https://static-stage.sctv.vn/channel/140/QPVN.png', 'is_playable': True},
		{'label': 'SCTV 1', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/7', 'thumbnail': 'https://static-stage.sctv.vn/channel/7/s1.png', 'is_playable': True},
		{'label': 'SCTV 2 HD - Yan TV', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/2', 'thumbnail': 'https://static-stage.sctv.vn/channel/2/s2HD.png', 'is_playable': True},
		{'label': 'SCTV 3 - SEE TV', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/10', 'thumbnail': 'https://static-stage.sctv.vn/channel/10/s3.png', 'is_playable': True},
		{'label': 'SCTV 4', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/9', 'thumbnail': 'https://static-stage.sctv.vn/channel/9/s4.png', 'is_playable': True},
		{'label': 'SCTV 6 HD', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/16', 'thumbnail': 'https://static-stage.sctv.vn/channel/16/sctv6hd.png', 'is_playable': True},
		{'label': 'SCTV 7', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/13', 'thumbnail': 'https://static-stage.sctv.vn/channel/13/s7.png', 'is_playable': True},
		{'label': 'SCTV 9', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/8', 'thumbnail': 'https://static-stage.sctv.vn/channel/8/s9.png', 'is_playable': True},
		{'label': 'SCTV 11 HD', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/106', 'thumbnail': 'https://static-stage.sctv.vn/channel/106/s11.png', 'is_playable': True},
		{'label': 'SCTV 12', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/103', 'thumbnail': 'https://static-stage.sctv.vn/channel/103/S12.png', 'is_playable': True},
		{'label': 'SCTV 13', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/18', 'thumbnail': 'https://static-stage.sctv.vn/channel/18/s13.png', 'is_playable': True},
		{'label': 'SCTV 14', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/19', 'thumbnail': 'https://static-stage.sctv.vn/channel/19/s14.png', 'is_playable': True},
		{'label': 'SCTV 15', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/20', 'thumbnail': 'https://static-stage.sctv.vn/channel/20/s15.png', 'is_playable': True},
		{'label': 'SCTV 16', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/21', 'thumbnail': 'https://static-stage.sctv.vn/channel/21/s16.png', 'is_playable': True},
		{'label': 'SCTV HD Du Lịch', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/17', 'thumbnail': 'https://static-stage.sctv.vn/channel/17/DuLich.png', 'is_playable': True},
		{'label': 'SCTV HD Giải trí tổng hợp', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/109', 'thumbnail': 'https://static-stage.sctv.vn/channel/109/Giatritonghop.png', 'is_playable': True},
		{'label': 'SCTV HD Hài', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/85', 'thumbnail': 'https://static-stage.sctv.vn/channel/85/Hai.png', 'is_playable': True},
		{'label': 'SCTV HD Phim Châu Á', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/129', 'thumbnail': 'https://static-stage.sctv.vn/channel/129/S-PhimChauAHD.png', 'is_playable': True},
		{'label': 'SCTV HD Phim nước ngoài đặc sắc', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/110', 'thumbnail': 'https://static-stage.sctv.vn/channel/110/PhimNuocNgoai.png', 'is_playable': True},
		{'label': 'SCTV HD Phim Tổng Hợp', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/108', 'thumbnail': 'https://static-stage.sctv.vn/channel/108/S-PhimTongHopHD.png', 'is_playable': True},
		{'label': 'SCTV HD Phim Việt', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/84', 'thumbnail': 'https://static-stage.sctv.vn/channel/84/PhimVietHD.png', 'is_playable': True},
		{'label': 'SCTV HD Phụ nữ & Gia đình', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/114', 'thumbnail': 'https://static-stage.sctv.vn/channel/114/PhuNuVagd.png', 'is_playable': True},
		{'label': 'SCTV HD Sân Khấu', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/107', 'thumbnail': 'https://static-stage.sctv.vn/channel/107/SCTVHDSanKhau.png', 'is_playable': True},
		{'label': 'SCTV HD Thể Thao', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/22', 'thumbnail': 'https://static-stage.sctv.vn/channel/22/SCTVThethaoHD-1.png', 'is_playable': True},
		{'label': 'SCTV HD Văn hóa - Nghệ thuật', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/130', 'thumbnail': 'https://static-stage.sctv.vn/channel/130/s-Vanhoa-Nghethuat-HD.png', 'is_playable': True},
		{'label': 'SCTV Phim Tổng Hợp', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/4', 'thumbnail': 'https://static-stage.sctv.vn/channel/4/PhimTongHopSD.png', 'is_playable': True},
		{'label': 'SEE HD (SCTV HD Thiếu nhi)', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/112', 'thumbnail': 'https://static-stage.sctv.vn/channel/112/ThieuNhi.png', 'is_playable': True},
		{'label': 'Sofa TV', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/135', 'thumbnail': 'https://static-stage.sctv.vn/channel/135/logosofatv.png', 'is_playable': True},
		{'label': 'STARMOVIES', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/26', 'thumbnail': 'https://static-stage.sctv.vn/channel/26/star-movie.png', 'is_playable': True},
		{'label': 'STARWORLD', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/28', 'thumbnail': 'https://static-stage.sctv.vn/channel/28/starworld.png', 'is_playable': True},
		{'label': 'TH Bến Tre', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/143', 'thumbnail': 'https://static-stage.sctv.vn/channel/143/THBTbentre.png', 'is_playable': True},
		{'label': 'TH Cần Thơ', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/118', 'thumbnail': 'https://static-stage.sctv.vn/channel/118/thtpct.PNG', 'is_playable': True},
		{'label': 'TH Đồng Tháp', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/147', 'thumbnail': 'https://static-stage.sctv.vn/channel/147/THDTdongthap.png', 'is_playable': True},
		{'label': 'TH Hậu Giang', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/148', 'thumbnail': 'https://static-stage.sctv.vn/channel/148/HGTVhaugiang.png', 'is_playable': True},
		{'label': 'TH Kiên Giang', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/149', 'thumbnail': 'https://static-stage.sctv.vn/channel/149/KGkiengiang.png', 'is_playable': True},
		{'label': 'TH Ninh Bình', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/150', 'thumbnail': 'https://static-stage.sctv.vn/channel/150/NTVninhbinh.png', 'is_playable': True},
		{'label': 'Th Ninh Thuận', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/151', 'thumbnail': 'https://static-stage.sctv.vn/channel/151/NTVninhthuan.png', 'is_playable': True},
		{'label': 'TH Vĩnh Long 1', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/62', 'thumbnail': 'https://static-stage.sctv.vn/channel/62/THVL1.png', 'is_playable': True},
		{'label': 'TH Vĩnh Long 2', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/124', 'thumbnail': 'https://static-stage.sctv.vn/channel/124/THVL2.png', 'is_playable': True},
		{'label': 'ToDay TV', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/5', 'thumbnail': 'https://static-stage.sctv.vn/channel/5/Today.png', 'is_playable': True},
		{'label': 'TV5 Monde', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/162', 'thumbnail': 'https://static-stage.sctv.vn/channel/162/tv5(monde).png', 'is_playable': True},
		{'label': 'VOV', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/121', 'thumbnail': 'https://static-stage.sctv.vn/channel/121/logo_phatthanh_vov.png', 'is_playable': True},
		{'label': 'VTC 10', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/153', 'thumbnail': 'https://static-stage.sctv.vn/channel/153/vtc10.png', 'is_playable': True},
		{'label': 'VTC 11', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/154', 'thumbnail': 'https://static-stage.sctv.vn/channel/154/vtc11.png', 'is_playable': True},
		{'label': 'VTC 14', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/155', 'thumbnail': 'https://static-stage.sctv.vn/channel/155/vtc14.png', 'is_playable': True},
		{'label': 'VTC 9 Lets Việt', 'path': 'plugin://plugin.video.sctv.hieuhien.vn/play/65', 'thumbnail': 'https://static-stage.sctv.vn/channel/65/vtc9_letsviet.png', 'is_playable': True},
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

@plugin.route('/play/<cid>', name="play_with_local_acc")
@plugin.route('/play/<cid>/<phone>/<passw>')
def play(cid,phone="",passw=""):
	if phone == "": phone = plugin.get_setting('usernamesctv')
	if passw == "":
		passw = plugin.get_setting('passwordsctv')
		hash_object = hashlib.md5(passw)
		passw = hash_object.hexdigest()
	valid_device_id, valid_user_id  = GetValidID(phone, passw)
	if valid_user_id:
		dialogWait = xbmcgui.DialogProgress()
		dialogWait.create('SCTV', 'Đang mở kênh...')
		plugin.set_resolved_url(get_playable_url(cid,valid_user_id,valid_device_id))
		dialogWait.close()
		del dialogWait
	else:
		dialog = xbmcgui.Dialog()
		yes = dialog.yesno(
			'Số Phone hoặc Password không đúng!',
			'Chưa có tài khoản SCTV, tải app và đăng ký. Bạn có nhập tài khoản bây giờ không?',
			yeslabel='OK, nhập ngay',
			nolabel='Nhập sau!'
		)
		if yes:
			plugin.open_settings()
			# print "SCTV Phone %s saved!" % plugin.get_setting('usernamesctv')
			play(cid)

def get_playable_url(cid,valid_user_id,valid_device_id):
	return GetChannelPlayURL(cid, valid_user_id, valid_device_id)

if __name__ == '__main__':
	plugin.run()