# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re


class BaidutiebaPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient('192.168.75.2',27017)
        self.db = self.conn['yuliao']

    def process_item(self, item, spider):


        comments = item['comments']['data']['comment_list']
        users = item['comments']['data']['user_list']
        pattern = re.compile('<a.*?>')

        if comments != []:
            for key, value in item['stairs'].items():
                comment_id = str(value['comment_id'])

                if comment_id in list(comments.keys()):
                    # print(comment_id)
                    value['more_comment'] = dict()

                    more_comment_list = comments[comment_id]['comment_info']
                    for commentkey, commentvalue in enumerate(more_comment_list):
                        single_comment = dict()
                        single_comment['from_user_id'] = commentvalue['user_id']
                        single_comment['from_user_name'] = commentvalue['username']
                        commentvalue['content'].replace('：', ':')

                        try:
                            if commentvalue['content'].strip().startswith('回复'):

                                single_comment['to_user_name'] = commentvalue['content'].strip().split(':')[0][
                                                                 2:].strip()
                                single_comment['to_user_name'] = re.sub(pattern, '', single_comment['to_user_name'])
                                single_comment['to_user_name'] = re.sub('</a>', '', single_comment['to_user_name'])
                                single_comment['to_user_id'] = ''
                                for userkey, uservalue in users.items():
                                    if uservalue['user_name'] == single_comment['to_user_name']:
                                        single_comment['to_user_id'] = uservalue['user_id']
                                        break
                                # print (commentvalue['content'])

                                single_comment['conent'] = "".join(commentvalue['content'].strip().split(':')[1:])

                            else:
                                single_comment['to_user_id'] = value['stair_user_id']
                                single_comment['to_user_name'] = value['stair_user_name']
                                single_comment['content'] = commentvalue['content'].strip()

                            value['more_comment'][str(commentkey)] = single_comment
                        except Exception as e:
                            print(e.args)
                            print(commentvalue['content'])
                            continue
        if self.db.tieba.find({'url': item['url']}).count() > 0:
            self.db.tieba.update({'url': item['url']}, {"$set": {'stairs': item['stairs']}})
            return item
        else:
            del item['comments']
            self.db.tieba.insert(dict(item))
            return item






