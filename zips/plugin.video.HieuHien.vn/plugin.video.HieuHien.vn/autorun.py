# -*- coding: utf-8 -*-

import xbmc, xbmcaddon

addon = xbmcaddon.Addon(id='plugin.video.HieuHien.vn')

Autorun = addon.getSetting('en_dis')

if Autorun == 'true':				
    xbmc.executebuiltin("RunAddon(plugin.video.HieuHien.vn)")