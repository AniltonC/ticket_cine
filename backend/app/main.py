from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Ticket Cine API",
    description="A movie theater seat reservation website.",
    version="1.0.0"
)


@app.get("/", response_class=HTMLResponse)
async def root():
    html_reponse = """
    <html>
        <body>
            <h2 title="I'm a header">Ticket Cine</h2>
            <p title="I'm a tooltip">A movie theater seat reservation website.</p>
        </body>
    </html>
"""
    return html_reponse