from iview_class import *

ART = 'art-default.jpg'
ICON = 'icon-default.jpg'

def Start():

  HTTP.CacheTime = CACHE_1HOUR

@handler('/video/aubciview', 'ABC iView', art=ART, thumb=ICON)
def MainMenu():

  oc = ObjectContainer(title2 = 'ABC iView')
  cats = iView_Config.List_Categories()

  for key in cats:

    oc.add(DirectoryObject(
      key = Callback(GetSeriesByCategory, category=key),
      title = cats[key]
    ))

  oc.objects.sort(key = lambda obj: obj.title)

  return oc

@route('/video/aubciview/series/{category}')
def GetSeriesByCategory(category):

  cat = iView_Category(category)

  oc = ObjectContainer(title2 = cat.title)

  series = cat.series_list

  for item in series:

    oc.add(DirectoryObject(
      key = Callback(GetEpisodesBySeries, series=item[0]),
      title = item[1]
    ))

  oc.objects.sort(key = lambda obj: obj.title)

  return oc

@route('/video/aubciview/episode/play')
def Play_iView(iView_Title, iView_Summary, iView_Path, iView_Thumb, iView_Duration, video_url, include_container=False):

  vco = VideoClipObject(
      key = Callback(Play_iView, iView_Title=iView_Title, iView_Summary=iView_Summary, iView_Path=iView_Path, iView_Thumb=iView_Thumb, iView_Duration=iView_Duration, video_url=video_url, include_container=True),
      rating_key = iView_Path,
      title = iView_Title,
      summary = iView_Summary,
      thumb = iView_Thumb,
      duration = int(iView_Duration),
      items = [
        MediaObject(
          parts = [
            PartObject(
              key = RTMPVideoURL(url = video_url, clip = iView_Config.CLIP_PATH() + iView_Path, swf_url = iView_Config.SWF_URL)
            )
          ]
        )
      ]
    )

  if include_container:
    return ObjectContainer(objects=[vco])
  else:
    return vco

@route('/video/aubciview/episode/{series}')
def GetEpisodesBySeries(series):

  show = iView_Series(series)

  oc = ObjectContainer(title2 = show.title, no_cache = True)

  episodes = show.episodes
  rtmp_url = iView_Config.RTMP_URL()

  for item in episodes:
    oc.add(Play_iView(item[1], item[2], item[3], item[4], item[5], rtmp_url))

  oc.objects.sort(key = lambda obj: obj.title)

  return oc
