

from playwright.sync_api import sync_playwright


#Extraction from Playwright (iOS)

def collect_fingerprint(page):
    fingerprint = {}

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

    # Screen info (fixed!)
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

    # Canvas fingerprint (your existing or improved version)
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

    # WebGL (add this for high entropy)
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

    return fingerprint


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        fp = collect_fingerprint(page)
        print("WebGL fingerprint:", fp.get('webgl', 'Not collected'))
        browser.close()
