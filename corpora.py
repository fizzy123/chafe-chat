import json, bz2
from gensim import corpora

dictionary = corpora.Dictionary()
file = '/Users/nobr/Documents/2017/RC_2017-03.bz2'
for line in bz2.BZ2File(file, "r"):
    post = json.loads(line)
    if int(post['score']) < 0:
        dictionary.add_documents([post['body'].split()])
dictionary.save('/tmp/reddit_comments.dict')

once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(once_ids)
dictionary.compactify()

class MyCorpus(object):
    def __iter__(self):
        for line in bz2.BZ2File(file, "r"):
            # assume there's one document per line, tokens separated by whitespace
            post = json.loads(line)
            if int(post['score']) < 0:
                yield dictionary.doc2bow(post['body'].split())

corpora = MyCorpus()
corpora.MmCorpus.serialize('/tmp/corpus.mm', corpus)
