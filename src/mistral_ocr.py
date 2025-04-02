from decouple import config
from mistralai import Mistral


def ocr_url_pdf_to_markdown(url, client):
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": url},
        include_image_base64=True,
    )

    full_doc = "\n\n".join(
        [
            f"### Page {i + 1}\n{ocr_response.pages[i].markdown}"
            for i in range(len(ocr_response.pages))
        ]
    )
    return full_doc


if __name__ == "__main__":
    api_key = config("MISTRAL_API_KEY")
    client = Mistral(api_key=api_key)

    # Main paper: Monash Time Series Forecasting Archive
    url = "https://openreview.net/pdf?id=wEc1mgAjU-"
    full_doc = ocr_url_pdf_to_markdown(url, client)
    with open(
        "./notes/monash_time_series_forecasting.md",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(full_doc)

    # Supplementary material: Monash Time Series Forecasting Archive
    url = "https://openreview.net/attachment?id=wEc1mgAjU-&name=supplementary_material"
    full_doc = ocr_url_pdf_to_markdown(url, client)
    with open(
        "./notes/monash_time_series_forecasting_appendix.md",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(full_doc)
