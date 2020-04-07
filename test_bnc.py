from bnc import bnc

def test_download():
    content_url="/client/es_ES/search/asset/58090/0"
    sesion=bnc()
    mp3=sesion.downloadAudio(content_url)

    assert len(mp3)==23045106