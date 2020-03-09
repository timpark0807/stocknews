from secrets import client_id, client_secret, password, user_agent, redirect_uri, username, token
import praw
import json
import requests


class StockNews:

    def __init__(self):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  password=password,
                                  user_agent=user_agent,
                                  redirect_uri=redirect_uri,
                                  username=username)


    def main(self):
        comments_raw = self._get_comments_raw()
        comments_dict = self._get_comments_dict(comments_raw)
        self._add_articles(comments_dict)
        self._process_comments(comments_dict)
        return True

    def _process_comments(self, comments_dict):
        for comment_object, comment_dict in comments_dict.items():
            news_table = comment_dict['news_table']
            if not comment_object.saved:
                comment_object.reply(news_table)
                comment_object.save()

    def _add_articles(self, comments_dict):
        for comment_object, comment_dict in comments_dict.items():
            ticker = comment_dict['ticker']
            last = comment_dict['last']
            comment_dict['news_table'] = self._get_news_table(ticker, last)

    def _get_news_table(self, ticker, last):
        temp = []
        news = self._get_news_articles(ticker, last)
        for article in news:
            temp.append(self._get_markdown_table_row(article))
        output = self._get_table(temp)
        return output

    def _get_markdown_table_row(self, article):
        return f"{article['headline']}|[{article['source']}]({article['url']})"

    def _get_table(self, news):
        table = ["**Headline**|**Link** \n-|-"]
        table.extend(news)
        return ' \n'.join(table)

    def _get_comments_dict(self, comments):
        comments_dict = {}
        for comment in comments:
            comments_dict[comment] = {}
            comment_string = str(comment.body)
            comments_dict[comment]['ticker'] = self._get_ticker(comment_string)
            comments_dict[comment]['last'] = self._get_last(comment_string)
        return comments_dict

    def _get_ticker(self, comment_string):
        return comment_string.split()[1][1:]

    def _get_last(self, comment_string):
        check = comment_string.split()
        if len(check) == 3:
            return check[-1]
        return 5

    def _get_comments_raw(self):
        subreddit = self.reddit.subreddit('investing')
        retval = []
        for comment in subreddit.comments(limit=50):
            if '!stocknews' in comment.body:
                retval.append(comment)
        return retval

    def _get_news_articles(self, ticker, last=5):
        url = f'https://cloud.iexapis.com/stable/stock/{ticker}/news?last={last}&token={token}'
        response = requests.get(url)
        json_data = json.loads(response.text)
        return json_data


if __name__ == '__main__':
    sn = StockNews()
    sn.main()