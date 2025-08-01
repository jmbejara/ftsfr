import os
import re
import tomli
import toml
from pathlib import Path
import bibtexparser
from openai import OpenAI
from typing import Dict, List, Tuple
import markdown
from decouple import config

OPENAI_API_KEY = config("OPENAI_API_KEY")


def parse_bibliography(bib_file: Path) -> Dict[str, Dict]:
    """Parse bibliography.bib and return a dictionary of entries."""
    with open(bib_file, "r", encoding="utf-8") as f:
        bib_database = bibtexparser.load(f)

    entries = {}
    for entry in bib_database.entries:
        key = entry.get("ID", "")
        if key:
            entries[key] = {
                "author": entry.get("author", ""),
                "title": entry.get("title", ""),
                "year": entry.get("year", ""),
                "journal": entry.get("journal", entry.get("booktitle", "")),
                "volume": entry.get("volume", ""),
                "number": entry.get("number", ""),
                "pages": entry.get("pages", ""),
                "publisher": entry.get("publisher", ""),
                "doi": entry.get("doi", ""),
                "url": entry.get("url", ""),
                "ENTRYTYPE": entry.get("ENTRYTYPE", ""),
                "booktitle": entry.get("booktitle", ""),
                "month": entry.get("month", ""),
            }
    return entries


def format_chicago_citation(bib_key: str, bib_entry: Dict) -> str:
    """Format a bibliography entry as a Chicago style citation."""
    # Clean up title - remove curly braces
    title = bib_entry.get("title", "").strip()
    title = re.sub(r"[{}]", "", title)

    # Format authors
    authors = bib_entry.get("author", "")
    if authors:
        # Split authors and format them
        author_list = authors.split(" and ")
        formatted_authors = []

        for author in author_list:
            author = author.strip()
            # Handle "Last, First" format
            if "," in author:
                parts = author.split(",")
                last = parts[0].strip()
                first = parts[1].strip() if len(parts) > 1 else ""
                formatted_authors.append(f"{last}, {first}")
            else:
                # Handle "First Last" format
                parts = author.split()
                if len(parts) > 1:
                    last = parts[-1]
                    first = " ".join(parts[:-1])
                    formatted_authors.append(f"{last}, {first}")
                else:
                    formatted_authors.append(author)

        # Format author string based on number of authors
        if len(formatted_authors) == 1:
            author_str = formatted_authors[0]
        elif len(formatted_authors) == 2:
            author_str = f"{formatted_authors[0]} and {formatted_authors[1]}"
        else:
            author_str = f"{formatted_authors[0]} et al."
    else:
        author_str = "Unknown Author"

    year = bib_entry.get("year", "n.d.")
    entry_type = bib_entry.get("ENTRYTYPE", "").lower()

    # Format based on entry type
    if entry_type == "article":
        journal = bib_entry.get("journal", "")
        volume = bib_entry.get("volume", "")
        number = bib_entry.get("number", "")
        pages = bib_entry.get("pages", "")

        citation = f'{author_str}. {year}. "{title}."'
        if journal:
            citation += f" {journal}"
        if volume:
            citation += f" {volume}"
            if number:
                citation += f"({number})"
        if pages:
            citation += f": {pages}"
        citation += "."

    elif entry_type == "book":
        publisher = bib_entry.get("publisher", "")
        citation = f"{author_str}. {year}. {title}."
        if publisher:
            citation += f" {publisher}."

    elif entry_type in ["incollection", "inproceedings"]:
        booktitle = bib_entry.get("booktitle", "")
        publisher = bib_entry.get("publisher", "")
        pages = bib_entry.get("pages", "")

        citation = f'{author_str}. {year}. "{title}."'
        if booktitle:
            citation += f" In {booktitle}"
        if pages:
            citation += f", {pages}"
        citation += "."
        if publisher:
            citation += f" {publisher}."

    elif entry_type == "unpublished":
        citation = f'{author_str}. {year}. "{title}." Unpublished manuscript.'

    else:
        # Default format
        citation = f'{author_str}. {year}. "{title}."'

    return citation


def load_existing_summaries(toml_file: Path) -> Dict:
    """Load existing summaries from TOML file."""
    if not toml_file.exists():
        return {}

    with open(toml_file, "rb") as f:
        return tomli.load(f)


def extract_author_year(bib_entry: Dict) -> Tuple[str, str]:
    """Extract author names and year from bibliography entry."""
    author = bib_entry.get("author", "")
    year = bib_entry.get("year", "")

    # Extract first author's last name
    if author:
        # Handle different author formats
        authors = author.split(" and ")
        first_author = authors[0].strip()
        # Extract last name (handle both "Last, First" and "First Last" formats)
        if "," in first_author:
            last_name = first_author.split(",")[0].strip()
        else:
            parts = first_author.split()
            last_name = parts[-1] if parts else ""
        return last_name, year
    return "", year


def find_matching_md_file(
    bib_key: str, bib_entry: Dict, references_dir: Path, client: OpenAI
) -> Path:
    """Find matching markdown file in references directory."""
    author, year = extract_author_year(bib_entry)

    # Get all .md files
    md_files = list(references_dir.glob("*.md"))

    # First try exact matches
    for md_file in md_files:
        filename = md_file.stem.lower()
        if bib_key.lower() in filename:
            return md_file

    # Try author-year matching
    if author and year:
        candidates = []
        for md_file in md_files:
            filename = md_file.stem
            if author.lower() in filename.lower() and year in filename:
                candidates.append(md_file)

        if len(candidates) == 1:
            return candidates[0]
        elif len(candidates) > 1:
            # Use OpenAI to help with fuzzy matching
            title = bib_entry.get("title", "")
            prompt = f"""
            I need to match a bibliography entry to a markdown file.
            
            Bibliography entry:
            - Key: {bib_key}
            - Author: {author}
            - Year: {year}
            - Title: {title}
            
            Candidate files:
            {chr(10).join(f"- {f.name}" for f in candidates)}
            
            Which file most likely corresponds to this bibliography entry? 
            Return only the filename, nothing else.
            """

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0,
            )

            suggested_filename = response.choices[0].message.content.strip()
            for candidate in candidates:
                if candidate.name == suggested_filename:
                    return candidate

    return None


def generate_paper_summary(md_file: Path, client: OpenAI) -> Dict[str, str]:
    """Generate paper summary using OpenAI API."""
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = f"""
    Please analyze the following academic paper and provide:
    
    1. A 3-4 sentence description of the paper's main contribution and findings
    2. A markdown list of key empirical facts (3-5 bullet points)
    3. A markdown list of key lessons learned (3-5 bullet points)
    4. A markdown list of key data sources used (if applicable, otherwise write "- Not applicable")
    5. A markdown list of key data cleaning steps (if applicable, otherwise write "- Not applicable")
    
    Format your response as JSON with keys: description, empirical_facts, lessons_learned, data_sources, cleaning_steps
    
    Paper content:
    {content[:15000]}  # Limit content to avoid token limits
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    import json

    return json.loads(response.choices[0].message.content)


def save_summaries_to_toml(summaries: Dict, toml_file: Path):
    """Save summaries to TOML file in alphabetical order."""
    # Sort by key
    sorted_summaries = dict(sorted(summaries.items()))

    with open(toml_file, "w", encoding="utf-8") as f:
        toml.dump(sorted_summaries, f)


def generate_markdown_from_toml(summaries: Dict, bib_entries: Dict) -> str:
    """Generate markdown document from summaries."""
    md_content = "# Paper Summaries\n\n"

    for key in sorted(summaries.keys()):
        summary = summaries[key]
        md_content += f"## {key}\n\n"

        # Add Chicago citation if bibliography entry exists
        if key in bib_entries:
            citation = format_chicago_citation(key, bib_entries[key])
            md_content += f"**Citation:** {citation}\n\n"

        md_content += f"**Description:**\n{summary['description']}\n\n"

        # Format lists properly with blank line before list
        empirical_facts = summary["empirical_facts"]
        if isinstance(empirical_facts, list):
            md_content += f"**Key Empirical Facts:**\n\n"
            for fact in empirical_facts:
                md_content += f"- {fact}\n"
            md_content += "\n"
        else:
            md_content += f"**Key Empirical Facts:**\n{empirical_facts}\n\n"

        lessons_learned = summary["lessons_learned"]
        if isinstance(lessons_learned, list):
            md_content += f"**Key Lessons Learned:**\n\n"
            for lesson in lessons_learned:
                md_content += f"- {lesson}\n"
            md_content += "\n"
        else:
            md_content += f"**Key Lessons Learned:**\n{lessons_learned}\n\n"

        data_sources = summary["data_sources"]
        if isinstance(data_sources, list):
            md_content += f"**Data Sources:**\n\n"
            for source in data_sources:
                md_content += f"- {source}\n"
            md_content += "\n"
        else:
            md_content += f"**Data Sources:**\n{data_sources}\n\n"

        cleaning_steps = summary["cleaning_steps"]
        if isinstance(cleaning_steps, list):
            md_content += f"**Data Cleaning Steps:**\n\n"
            for step in cleaning_steps:
                md_content += f"- {step}\n"
            md_content += "\n"
        else:
            md_content += f"**Data Cleaning Steps:**\n{cleaning_steps}\n\n"

        md_content += "---\n\n"

    return md_content


def convert_markdown_to_html(md_content: str, output_file: Path):
    """Convert markdown to HTML."""
    html_content = markdown.markdown(md_content, extensions=["extra", "codehilite"])

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Paper Summaries</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }}
            h1 {{
                color: #333;
                border-bottom: 2px solid #333;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #555;
                margin-top: 30px;
            }}
            strong {{
                color: #444;
            }}
            ul {{
                margin: 10px 0;
            }}
            hr {{
                margin: 40px 0;
                border: none;
                border-top: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)


def main():
    # Setup paths
    reports_dir = Path("reports")
    references_dir = Path("_references")
    output_dir = Path("_output/paper_summaries")

    bib_file = reports_dir / "bibliography.bib"
    toml_file = reports_dir / "paper_summaries.toml"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize OpenAI client
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Parse bibliography
    print("Parsing bibliography...")
    bib_entries = parse_bibliography(bib_file)
    print(f"Found {len(bib_entries)} bibliography entries")

    # Load existing summaries
    print("\nLoading existing summaries...")
    existing_summaries = load_existing_summaries(toml_file)
    print(f"Found {len(existing_summaries)} existing summaries")

    # Find new entries to process
    new_entries = {k: v for k, v in bib_entries.items() if k not in existing_summaries}
    print(f"\nFound {len(new_entries)} new entries to process")

    # Process new entries
    unmatched_entries = []

    for i, (bib_key, bib_entry) in enumerate(new_entries.items(), 1):
        print(f"\nProcessing {i}/{len(new_entries)}: {bib_key}")

        # Find matching MD file
        md_file = find_matching_md_file(bib_key, bib_entry, references_dir, client)

        if md_file:
            print(f"  Found matching file: {md_file.name}")
            try:
                # Generate summary
                print("  Generating summary...")
                summary = generate_paper_summary(md_file, client)
                existing_summaries[bib_key] = summary
                print("  ✓ Summary generated successfully")
            except Exception as e:
                print(f"  ✗ Error generating summary: {e}")
                unmatched_entries.append((bib_key, bib_entry, f"Error: {e}"))
        else:
            print(f"  ✗ No matching file found")
            author, year = extract_author_year(bib_entry)
            unmatched_entries.append(
                (bib_key, bib_entry, f"Could not find file for {author} ({year})")
            )

    # Save updated summaries
    if new_entries:
        print("\nSaving updated summaries to TOML...")
        save_summaries_to_toml(existing_summaries, toml_file)

    # Generate markdown and HTML
    print("\nGenerating markdown and HTML outputs...")
    md_content = generate_markdown_from_toml(existing_summaries, bib_entries)

    md_output = output_dir / "paper_summaries.md"
    html_output = output_dir / "paper_summaries.html"

    with open(md_output, "w", encoding="utf-8") as f:
        f.write(md_content)

    convert_markdown_to_html(md_content, html_output)
    print(f"  ✓ Generated {md_output}")
    print(f"  ✓ Generated {html_output}")

    # Report unmatched entries
    if unmatched_entries:
        print("\n" + "=" * 60)
        print(f"UNMATCHED ENTRIES ({len(unmatched_entries)} total):")
        print("=" * 60)
        for bib_key, bib_entry, reason in unmatched_entries:
            print(f"\n{bib_key}:")
            print(f"  Title: {bib_entry.get('title', 'N/A')}")
            print(f"  Author: {bib_entry.get('author', 'N/A')}")
            print(f"  Year: {bib_entry.get('year', 'N/A')}")
            print(f"  Reason: {reason}")

    print("\nDone!")


if __name__ == "__main__":
    main()
