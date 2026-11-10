import serve_eleven_review_v003 as base
base.OUT=base.ROOT/'声音/声线返修试听-v004'
base.CHOICE=base.OUT/'作者选择.json'
base.ENDPOINT='/api/voice-choice-v004'
if __name__=='__main__':base.ThreadingHTTPServer(('127.0.0.1',8977),base.Handler).serve_forever()
