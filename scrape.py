import requests
import json
import os

def get_replies(video_id, cid):
    reply_cursor = 0
    reply_max_count = 50
    replies = {}
    while True:
        reply_url = 'https://www.tiktok.com/api/comment/list/reply/?aid=1988&comment_id={}&count={}&cursor={}&item_id={}'.format(cid, reply_max_count, reply_cursor, video_id)
        reply_request = requests.get(reply_url)

        for reply in reply_request.json()['comments']:
            comment_data = build_comment(reply)
            replies[comment_data['cid']] = comment_data

        if reply_request.json()['has_more'] == 0:
            break
        reply_cursor += reply_max_count

    # fix ordering
    to_clean = []
    for reply in replies:
        if replies[reply]['reply_to_reply_id'] != '0':
            try:
                replies[replies[reply]['reply_to_reply_id']]['replies'].append(replies[reply])
                to_clean.append(reply)
            except KeyError:
                print('comment deleted ig')

    for reply in to_clean:
        del replies[reply]

    return list(replies.values())

def build_comment(comment):
    return {
        'text': comment['text'],
        'unique_id': comment['user']['unique_id'] if 'unique_id' in comment['user'] else '',
        'nickname': comment['user']['nickname'] if 'nickname' in comment['user'] else '',
        'cid': comment['cid'],
        'reply_comment_total': comment['reply_comment_total'] if 'reply_comment_total' in comment else 0,
        'reply_id': comment['reply_id'],
        'reply_to_reply_id': comment['reply_to_reply_id'],
        'digg_count': comment['digg_count'],
        'replies': []
    }

def get_comments(video_id):
    cursor = 0
    directory = './scrapetok/comments/'
    count = 0
    max_count = 50
    comments = []
    while True:
        comments_url = 'https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={}&count={}&cursor={}'.format(video_id, max_count, cursor)
        r = requests.get(comments_url)

        for comment in r.json()['comments']:
            count += 1
            comment_data = build_comment(comment)

            if comment_data['reply_comment_total'] > 0:
                comment_data['replies'] = get_replies(video_id, comment_data['cid'])

            comments.append(comment_data)
        
        if r.json()['has_more'] == 0:
            break     
        cursor += max_count
    
    return comments

def scrape_collection(collection_id, directory):
    cursor = 0
    count = 0
    max_count = 30
    while True:
        collection_url = 'https://www.tiktok.com/api/collection/item_list?aid=1988&collectionId={}&count={}&cursor={}&sourceType=113'.format(collection_id, max_count, cursor)
        r = requests.get(collection_url)

        for item in r.json()['itemList']:
            video_metadata = {
                'author_username': item['author']['uniqueId'],
                'author_id': item['author']['id'],
                'description': item['desc'] if 'desc' in item else '',
                'music_title': item['music']['title'] if 'title' in item['music'] else '',
                'music_author': item['music']['authorName'] if 'authorName' in item['music'] else '',
                'item_id': item['id'],
                'comments': get_comments(item['id']) if 'comments' in item['id'] else []
            }

            #print('collecting {}'.format(video_metadata['item_id']))

            with open(os.path.join(directory, '{}_metadata.json'.format(video_metadata['item_id'])), 'w') as fd:
                json.dump(video_metadata, fd)
                #print('metadata downloaded')

            if 'music' in item and 'playUrl' in item['music']: 
                audio_url = item['music']['playUrl']
                audio_request = requests.get(audio_url)
                #print('downloading audio')
                with open(os.path.join(directory, '{}_audio.mp3'.format(video_metadata['item_id'])), 'wb') as fd:
                    for chunk in audio_request.iter_content(chunk_size=1024):
                        fd.write(chunk)


            if 'imagePost' in item:
                # is image
                i = 0
                for image in item['imagePost']['images']:
                    image_url = image['imageURL']['urlList'][0]
                    image_request = requests.get(image_url)
                    #print('downloading image {}'.format(i))
                    with open(os.path.join(directory, '{}_{}.jpeg'.format(video_metadata['item_id'], i)), 'wb') as fd:
                        for chunk in image_request.iter_content(chunk_size=1024):
                            fd.write(chunk)
                    i += 1
            else:
                # is video
                video_url = item['video']['playAddr']
                video_request = requests.get(video_url)
                with open(os.path.join(directory, '{}.mp4'.format(video_metadata['item_id'])), 'wb') as fd:
                    #print('downloading video')
                    for chunk in video_request.iter_content(chunk_size=1024):
                        fd.write(chunk)

            count += 1
            print(count)
        if r.json()['hasMore'] == False:
            break
        cursor += max_count

    print('{} done!'.format(count))

scrape_collection('7111887189571160875', './scrapetok/funnies/')
#scrape_collection('7111887189571160875', './scrapetok/funnies/')
