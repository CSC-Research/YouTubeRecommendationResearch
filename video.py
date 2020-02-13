class Video:
    def __init__(self,id,title,descr):
        self.id = id
        self.title = title
        self.descr = descr
        self.recs = fill_recs(id)
        #self.comments = fill_comments(id)

    def fill_recs(id):
        recs = []
        json = '' #API call
        infile = open('output.json','r')
        json_obj = json.load(infile)
        print(json_obj['items'][0])
        for part in json_obj['items']:
            recs.append(part['id']['videoId'])
