from pathlib import Path
import argparse
import os
import re
import time

from pypdf import PdfReader
from google import genai
from google.genai import types
from pydantic import BaseModel

# run and apply with | python datasheet_convention.py --apply

# UPDATE!! - path to docs/datasheets directory that you want to enforce the convention
DATASHEET_DIR = Path("../../power/docs/datasheets")
MODEL = "gemini-flash-lite-latest"

# set your own key, i am NOT paying for allat
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

REQUEST_DELAY = 5


class Component(BaseModel):
    type: str
    part_number: str


def extract_text(pdf):
    reader = PdfReader(pdf)

    text = ""
    for page in reader.pages[:2]:
        text += (page.extract_text() or "") + "\n"

    return text


def identify_component(text):
    prompt = f"""
You are identifying an electronic component from its datasheet.

Extract:
- type: a concise generic component category, such as LDO, FET, MCU, ADC,
  adc, mcu, sensor, any ic, diode, op-amp, connector, regulator, etc.
- part_number: the exact manufacturer part number.

Use the actual component described by the datasheet.
Do not use manufacturer names, package names, document numbers,
Do NOT guess. Label unconfident for manual review.
revision numbers, or generic words as the part number.

Keep the type concise.
Use common engineering abbreviations where appropriate.
Examples:
- CAN transceiver -> CANT
- buck converter -> BUCK
- boost converter -> BOOST
- inductor -> IND
- capacitor -> CAP
- microcontroller -> MCU
- operational amplifier -> OPAMP
- analog-to-digital converter -> ADC
- digital-to-analog converter -> DAC
- digital isolator -> ISO
- connector -> CONN

Do not use a hardcoded category list. Determine the appropriate
concise type from the datasheet.

Return ONLY valid JSON:

{{
  "type": "TYPE",
  "part_number": "PARTNUM"
}}

DATASHEET TEXT:
{text}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Component,
        ),
    )

    return Component.model_validate_json(response.text)


def clean(value):
    value = value.upper().strip()
    value = re.sub(r"[^A-Z0-9._-]+", "-", value)
    return value.strip("-")


def already_conventional(pdf):

    pattern = r"^[A-Z0-9._-]+-[A-Z0-9._-]+\.pdf$"

    return re.match(pattern, pdf.name, re.IGNORECASE) is not None


def process_pdf(pdf, apply=False):
    if already_conventional(pdf):
        print(f"[OK]       {pdf.name}")
        return

    text = extract_text(pdf)

    if not text.strip():
        print(f"[SKIP]     {pdf.name}: no text extracted")
        return

    try:
        result = identify_component(text)

        component_type = clean(result.type)
        part_number = clean(result.part_number)

    except Exception as e:
        print(f"[ERROR]    {pdf.name}: {e}")
        return

    if not component_type or not part_number:
        print(f"[SKIP]     {pdf.name}: incomplete Gemini result")
        return

    new_name = f"{component_type}-{part_number}.pdf"
    new_path = pdf.with_name(new_name)

    if pdf.name.lower() == new_name.lower():
        print(f"[OK]       {pdf.name}")
        return

    if new_path.exists():
        print(f"[CONFLICT] {pdf.name} -> {new_name}")
        return

    if apply:
        pdf.rename(new_path)
        print(f"[RENAMED]  {pdf.name} -> {new_name}")
    else:
        print(f"[DRY RUN]  {pdf.name} -> {new_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Automatically rename datasheets using Gemini."
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rename files. Without this flag, runs in dry-run mode."
    )

    args = parser.parse_args()

    datasheet_dir = DATASHEET_DIR.expanduser().resolve()

    if not datasheet_dir.exists():
        print(f"Directory does not exist: {datasheet_dir}")
        return

    if not datasheet_dir.is_dir():
        print(f"Path is not a directory: {datasheet_dir}")
        return

    pdfs = sorted(datasheet_dir.glob("*.pdf"))

    if not pdfs:
        print(f"No PDFs found in {datasheet_dir}")
        return

    print(
        f"{'APPLYING CHANGES' if args.apply else 'DRY RUN'}"
        f" | {len(pdfs)} PDF(s)\n"
    )

    for i, pdf in enumerate(pdfs):
        process_pdf(pdf, apply=args.apply)

        if (
            i < len(pdfs) - 1
            and not already_conventional(pdf)
        ):
            time.sleep(REQUEST_DELAY)


if __name__ == "__main__":
    main()