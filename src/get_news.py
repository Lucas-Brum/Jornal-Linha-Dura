import requests
from bs4 import BeautifulSoup
import re, json

try:
    from readability import Document
    HAS_READABILITY = True
except Exception:
    HAS_READABILITY = False


class NewsAPI:
    @staticmethod
    def get_top_stories(api_token, the_news_api_top_stories, locale="br", language="pt", limit=1):
        params = {
            "locale": locale,
            "language": language,
            "limit": limit,
            "api_token": api_token
        }
        resp = requests.get(the_news_api_top_stories, params=params, timeout=20)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def get_url(json_resp, index=0):
        return json_resp["data"][index]["url"]

    @staticmethod
    def get_title(json_resp, index=0):
        return json_resp["data"][index]["title"]  # estava pegando 'url'

    @staticmethod
    def get_html_news(url):
        headers = {"User-Agent": "Mozilla/5.0"}  # ajuda a evitar bloqueios simples
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        return resp.text

    @staticmethod
    def extract_text(html: str) -> str:
        """Recebe o HTML e retorna só o texto principal da matéria."""
        def _limpa(txt: str) -> str:
            txt = re.sub(r"[ \t]+", " ", txt)
            txt = re.sub(r"\n{3,}", "\n\n", txt)
            return txt.strip()

        # 1) Readability (se existir)
        if HAS_READABILITY:
            try:
                doc = Document(html)
                soup = BeautifulSoup(doc.summary(), "html.parser")
                blocos = []
                for tag in soup.find_all(["p", "li", "h2", "h3"]):
                    t = tag.get_text(" ", strip=True)
                    if t:
                        blocos.append(t)
                texto = _limpa("\n\n".join(blocos))
                if len(texto) >= 300:
                    return texto
            except Exception:
                pass

        # 2) JSON-LD (NewsArticle/Article → articleBody/text)
        try:
            soup_full = BeautifulSoup(html, "html.parser")
            for s in soup_full.find_all("script", {"type": "application/ld+json"}):
                raw = (s.string or s.get_text() or "").strip()
                if not raw:
                    continue
                try:
                    data = json.loads(raw)
                except Exception:
                    continue
                fila = data if isinstance(data, list) else [data]
                i = 0
                while i < len(fila):
                    item = fila[i]; i += 1
                    if not isinstance(item, dict):
                        continue
                    if "@graph" in item and isinstance(item["@graph"], list):
                        fila.extend(item["@graph"])
                    tipo = str(item.get("@type", "")).lower()
                    if tipo in {"newsarticle", "article", "blogposting"}:
                        corpo = item.get("articleBody") or item.get("text") or ""
                        corpo = _limpa(corpo)
                        if len(corpo) > 100:
                            return corpo
        except Exception:
            pass

        # 3) Fallback: maior bloco de <p> dentro de <article>/<main>/<div>
        try:
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "noscript", "form", "svg", "iframe", "header", "footer", "nav", "aside"]):
                tag.decompose()

            candidatos = []
            if soup.find("article"):
                candidatos.append(soup.find("article"))
            candidatos += soup.find_all(["main", "section", "div"], limit=60)

            melhor, melhor_len = "", 0
            for c in candidatos:
                if not c:
                    continue
                ps = c.find_all("p")
                if not ps:
                    continue
                txt = "\n\n".join(p.get_text(" ", strip=True) for p in ps)
                txt = _limpa(txt)
                if len(txt) > melhor_len:
                    melhor, melhor_len = txt, len(txt)

            if melhor:
                return melhor
        except Exception:
            pass

        # 4) Último recurso: todos os <p> da página
        try:
            soup = BeautifulSoup(html, "html.parser")
            texto = "\n\n".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))
            return _limpa(texto)
        except Exception:
            return ""

    @staticmethod
    def get_article_text(url: str) -> str:
        """Atalho: baixa o HTML e já retorna o texto da matéria."""
        html = NewsAPI.get_html_news(url)
        return NewsAPI.extract_text(html)
