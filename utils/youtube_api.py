from googleapiclient.discovery import build

def suggest_courses(query):
    api_key = 'AIzaSyDqFCokq96up6ijDMpm-L4la9-xSiIlNYo'
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        q=f'{query} course',
        part='snippet',
        type='playlist',  # Fetching playlists instead of videos
        maxResults=3
    )
    response = request.execute()
    
    # Returning playlist titles and URLs
    return [(item['snippet']['title'], f"https://www.youtube.com/playlist?list={item['id']['playlistId']}") for item in response['items']]
