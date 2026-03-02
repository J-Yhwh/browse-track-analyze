


import json
from pathlib import Path
from playwright.sync_api import sync_playwright

def collect_fingerprint(page):
    fingerprint = {}
    try:
        # Basic navigator info
        fingerprint.update(page.evaluate("""
            () => ({
                userAgent: navigator.userAgent,
                language: navigator.language || navigator.userLanguage,
                languages: navigator.languages,
                platform: navigator.platform,
                hardwareConcurrency: navigator.hardwareConcurrency,
                deviceMemory: navigator.deviceMemory,
                maxTouchPoints: navigator.maxTouchPoints
            })
        """))

        # Timezone
        fingerprint['timezone'] = page.evaluate("() => Intl.DateTimeFormat().resolvedOptions().timeZone")

        # Screen info
        fingerprint['screen'] = page.evaluate("""
            () => ({
                width: screen.width,
                height: screen.height,
                availWidth: screen.availWidth,
                availHeight: screen.availHeight,
                colorDepth: screen.colorDepth,
                pixelDepth: screen.pixelDepth,
                orientation: screen.orientation ? screen.orientation.type : null
            })
        """)

        # Canvas fingerprint
        fingerprint['canvas'] = page.evaluate("""
            () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                ctx.textBaseline = 'top';
                ctx.font = '14px Arial';
                ctx.fillStyle = '#f60';
                ctx.fillRect(125, 1, 62, 20);
                ctx.fillStyle = '#069';
                ctx.fillText('Hello, world!', 2, 15);
                ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
                ctx.fillText('Hello, world!', 4, 17);
                return canvas.toDataURL();
            }
        """)

        # WebGL fingerprint (high entropy)
        fingerprint['webgl'] = page.evaluate("""
            () => {
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                if (!gl) return { error: 'WebGL not supported' };
                const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                return {
                    vendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : null,
                    renderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : null,
                    version: gl.getParameter(gl.VERSION)
                };
            }
        """)

    except Exception as e:
        fingerprint['error'] = str(e)

    return fingerprint

if __name__ == "__main__":
    with sync_playwright() as p:
        # Use chromium for now (ANGLE/SwiftShader for WebGL)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        page.goto("https://example.com", wait_until="networkidle")

        fp = collect_fingerprint(page)

        print("Collected fingerprint:", fp)

        # Save to data/ folder
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True, parents=True)

        output_file = output_dir / "webgl_fingerprint.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fp, f, indent=4, ensure_ascii=False)

        print(f"Fingerprint saved to: {output_file}")

        browser.close()


# After saving JSON (prints out the OS fingerprint canva suniqie to each computer / machine)
canvas_data_url = fp.get('canvas')
if canvas_data_url and canvas_data_url.startswith('data:image/png;base64,'):
    import base64
    base64_string = canvas_data_url.split(',')[1]
    canvas_bytes = base64.b64decode(base64_string)
    canvas_file = output_dir / "canvas_fingerprint.png"
    with open(canvas_file, 'wb') as f:
        f.write(canvas_bytes)
    print(f"Canvas image saved to: {canvas_file}")
