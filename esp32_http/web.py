import gc
gc.collect()

from microdot import Microdot, Response, redirect
import os
#from esp32.pdc import PdcSingleton as PDC

app = Microdot()
Response.default_content_type = 'text/html'

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../www'))


status_message = None


def send_file(filename, message=None):
    path = os.path.join(STATIC_DIR, filename)
    try:
        with open(path, 'rb') as f:
            content = f.read().decode('utf-8')
    except OSError:
        return Response('404 Not Found', status_code=404)
    
    if filename.endswith('.htm') or filename.endswith('.html'):
        content_type = 'text/html'
    elif filename.endswith('.css'):
        content_type = 'text/css'
    elif filename.endswith('.js'):
        content_type = 'application/javascript'
    else:
        content_type = 'application/octet-stream'
    
    if message:
        content = content.replace('<body>', '<body><div class="status-message">{}</div>'.format(message), 1)
    return Response(body=content.encode('utf-8'), headers={'Content-Type': content_type})

@app.route('/')
def index(request):
    global status_message
    msg = status_message
    status_message = None
    return send_file('page.htm', message=msg)

@app.route('/css/style.css')
def style_css(request):
    return send_file('style.css')

@app.route('/static/jquery.js')
def jquery_js(request):
    return send_file('jquery-3.5.1.min.js')

@app.route('/bpm/<bpm>')
def set_bpm_route(request, bpm):
    from esp32.pdc import PdcSingleton as PDC
    global status_message
    bpm = int(bpm)
    sl_ms = int(1000 / (bpm / 60))
    pdc = PDC()
    pdc.sleep_ms = sl_ms
    status_message = 'BPM wurde auf {} umgestellt.'.format(bpm)
    return redirect('/')

@app.route('/pat/<pat>')
def set_pat(request, pat):
    from esp32.pdc import PdcSingleton as PDC
    global status_message
    pdc = PDC()
    suc = pdc.board.set_pattern(pat)
    status_message = 'Pattern wurde auf {} umgestellt.'.format(pat)
    return redirect('/')

@app.route('/track/<track>')
def set_track_route(request, track):
    from esp32.pdc import PdcSingleton as PDC
    global status_message
    pdc = PDC()
    suc = pdc.board.track.set_track(int(track))
    status_message = 'Track wurde auf {} umgestellt.'.format(track)
    return redirect('/')

@app.route('/stop/')
def stop_route(request):
    global status_message
    status_message = 'Server wurde gestoppt.'
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
