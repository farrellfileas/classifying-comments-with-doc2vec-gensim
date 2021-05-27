"""
This is the script I used to scrape the comments into the CSV.

IMPORTANT NOTE FROM FARRELL:
This python script is from https://www.geeksforgeeks.org/how-to-extract-youtube-comments-using-youtube-api-python/
with slight edits to suit the needs of this project.
I DO NOT TAKE THE CREDIT FOR THIS PORTION OF THE CODE
"""
from googleapiclient.discovery import build

api_key = 'YOUR_API_KEY_HERE'


def video_comments(video_id, channel, f):
    # empty list for storing reply
    replies = []

    # creating youtube resource object
    youtube = build('youtube', 'v3',
                    developerKey=api_key)

    # retrieve youtube video results
    video_response = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id,
        maxResults=100
    ).execute()

    # iterate video response
    while video_response:

        # extracting required info
        # from each result object
        for item in video_response['items']:

            # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']

            # counting number of reply of comment
            replycount = item['snippet']['totalReplyCount']

            # if reply is there
            if replycount > 0:

                # iterate through all reply
                for reply in item['replies']['comments']:
                    # Extract reply
                    reply = reply['snippet']['textDisplay']

                    # Store reply is list
                    replies.append(reply)
            # print comment with list of reply
            f.write('\"'+comment.replace('\"', '\'') + '\", ' + channel + '\n')

            # empty reply list
            replies = []
        video_response = None

        # Again repeat
        # if 'nextPageToken' in video_response:
        #     video_response = youtube.commentThreads().list(
        #         part='snippet,replies',
        #         videoId=video_id
        #     ).execute()
        # else:
        #     break

f = open('youtube_comments.csv', 'w+', encoding='utf-8')
f.write('comment, channel\n')

# Enter video id
fox_ids = ["eVMEjZy65GU",
           'FHr8KCSnE7w',
           'V_7Z058MC7M',
           'cEZ6XhtbmrQ',
           'L4gh1TCxqp4',
           'T0on0May3JM',
           '9l03g_z0gNo',
           'Z_foudD52pQ',
           'SdsrhDkl_p8',
           'TQOnTj3CyaM']
cnn_ids = ['ovLKZFNm-8M',
           'imaYlHjhzEY',
           'mCraxvYUdjI',
           'tMrImA2DPy8',
           'PO8VS4NFbVU',
           'VqQ73XolxUs',
           'U5z1GhjJY_A',
           'OpzxQMgVDTY',
           'DJOB2DiNNsY',
           'jhC-RgbR6gc']

# Call function
for videoId in fox_ids:
    video_comments(videoId, 'FOX', f)

for videoId in cnn_ids:
    video_comments(videoId, 'CNN', f)
