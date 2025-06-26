import base64
import re
from pathlib import Path

def embed_local_images_in_markdown(markdown_text, base_path="."):
    """
    Substitui os paths de imagens locais no markdown por imagens embutidas em base64.

    Args:
        markdown_text (str): Conteúdo do arquivo markdown.
        base_path (str): Pasta base onde estão as imagens.

    Returns:
        str: Markdown com imagens embutidas.
    """
    # Regex para encontrar ![alt](path)
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    def replace_image(match):
        alt_text = match.group(1)
        img_path = Path(base_path) / match.group(2)

        if not img_path.exists():
            return f"❌ Imagem não encontrada: {img_path}"

        mime = "image/png" if img_path.suffix.lower() == ".png" else "image/jpeg"

        with open(img_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()

        return f'<img src="data:{mime};base64,{encoded}" alt="{alt_text}" width="760px"/>'

    # Substituir todas as ocorrências no markdown
    return re.sub(pattern, replace_image, markdown_text)
