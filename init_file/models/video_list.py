from googleapiclient.discovery import build
# from config import DEVELOPER_KEY
DEVELOPER_KEY = 'AIzaSyA37YNwWV6juiyPFaLjIFUCh6pCISCDGYY'

# API権限の取得
api_service_name = 'youtube'
api_version = 'v3'
DEVELOPER_KEY = DEVELOPER_KEY

# インスタンスの作成
youtube = build(api_service_name,api_version,developerKey= DEVELOPER_KEY)

# ビデオのIDを返す
def video_ids():
  playlist_id = 'PLSFrP_aW8LfyEIahQGnpdvDtPUKKWxi-H'
  playlist_ids = []
  playlist = youtube.playlistItems().list(
    playlistId=playlist_id,
    part='snippet',
    fields="nextPageToken,items/snippet/resourceId/videoId",
    maxResults=50
  )

  while playlist:
    results = playlist.execute()
    items = results.get('items')
    for ids in items:
      playlist_ids.append(ids.get('snippet').get('resourceId').get('videoId'))
    playlist = youtube.playlistItems().list_next(playlist,results)
  
  return list(set(playlist_ids))

# 50個づつリストを区切ってイミュレート
def chunk(lst,n):
  for i in range(0,len(lst),n):
    yield lst[i:i+n]

# ビデオのタイトルとIDをタプルにしたリストを返す
def video_titles(playlist_ids_):
  video_list = list(chunk(playlist_ids_,50))
  list_video = []
  for vide in video_list:
    video = ",".join(vide)
    r = youtube.videos().list(
      part='snippet',
      id=video,
      fields='items/snippet/title'
    )
    res = r.execute()
    for points in res.get('items'):
      _ = points.get('snippet').get('title')
      list_video.append(_)
  video_tuple = list(map(tuple,zip(playlist_ids_,list_video)))

  return video_tuple