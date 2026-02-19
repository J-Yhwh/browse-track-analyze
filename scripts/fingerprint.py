
## Fingerprinting detection - details the extenr of digital 'fingerprints' acrodd common cookies
## P.S -Playwright can run JS to collect fingerprint data 


def collect_fingerprint(page):

  fp = page.evaluate("""
    () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        ctx.textBaseline = "top";
        ctx.font = "14px 'TimesNewRoman'";
        ctx.fillStyle = "#f60";
        ctx.fillRect(125,1,62,20);
        ctx.fillStyle = "#069";
        ctx.fillText("Hello, world!",2,15);
        ctx.fillStyle = "rgba(102, 204, 0, 0.7)";
        ctx.fillText("Hello, world!",4,17);
        const canvasHash = canvas.toDataURL();

        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        const webglVendor = gl ? gl.getParameter(gl.UNMASKED_VENDOR_WEBGL) : null;
        const webglRenderer = gl ? gl.getParameter(gl.UNMASKED_RENDERER_WEBGL) : null;

        const fonts = [];
        const testString = "abcdefghijklmnopqrstuvwxyz0123456789";
        const baseWidth = measureTextWidth(testString, "monospace");
        const fontList = ["Arial", "Courier New", "Georgia", "Helvetica", "Times New Roman", "Verdana", /* add more */];
        for (const font of fontList) {
            const w = measureTextWidth(testString, font);
            if (w !== baseWidth) fonts.push(font);
        }

        return {
            canvasHash,
            webglVendor,
            webglRenderer,
            fontsDetected: fonts.length,
            screen: `${screen.width}x${screen.height}`,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            hardwareConcurrency: navigator.hardwareConcurrency,
        };
    }

    function measureTextWidth(text, font) {
        const span = document.createElement('span');
        span.style.font = font;
        span.style.visibility = 'hidden';
        span.innerText = text;
        document.body.appendChild(span);
        const width = span.offsetWidth;
        document.body.removeChild(span);
        return width;
    }
    """)

    # Simple uniqueness score (entropy approximation)
    attributes = len(fp)
    score = min(100, attributes * 10)  # Rough: more attributes = higher uniqueness
    return {"fingerprint": fp, "uniqueness_score": score}
