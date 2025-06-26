#!/usr/bin/env python3
# flake8: noqa

import panflute as pf
import re
import datetime

ARABIC_CHAR_REGEX = re.compile(r'[\u0600-\u06FF]')


def prepare(doc):
    """Processes metadata for the title and the date."""
    # --- DATE FORMATTING ---
    if 'created' in doc.metadata:
        created_meta = doc.get_metadata('created')
        if isinstance(created_meta, str):
            date_str = created_meta
        else:
            date_str = pf.stringify(created_meta)
        
        try:
            # Use non-zero-padded day for macOS/Linux compatibility (%-d)
            parsed_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = parsed_date.strftime('%B %-d, %Y')
            doc.metadata['created'] = pf.MetaString(formatted_date)
        except ValueError:
            pass

    # --- TITLE FORMATTING ---
    if 'title' in doc.metadata:
        title_meta = doc.get_metadata('title')
        if isinstance(title_meta, str):
            title_md = title_meta
        else:
            title_md = pf.stringify(title_meta)

        parts = re.split(r'([\u0600-\u06FF\s]+)', title_md) # Slightly improved regex to capture spaces
        new_title_parts = []
        for part in parts:
            if part:
                if ARABIC_CHAR_REGEX.search(part):
                    # MODIFIED: Changed \textarabic to \foreignlanguage for babel/lualatex compatibility
                    new_title_parts.append(pf.RawInline(f'\\foreignlanguage{{arabic}}{{{part}}}', format='latex'))
                else:
                    new_title_parts.append(pf.Str(part))
        doc.metadata['title'] = pf.MetaList(*new_title_parts)


def action(elem, doc):
    """Main filter action that processes the document body."""
    if not isinstance(elem, (pf.Para, pf.Plain)):
        return

    # Block-level tagging for paragraphs that are predominantly Arabic
    if isinstance(elem, pf.Para):
        if hasattr(elem.parent, 'attributes') and 'lang' in elem.parent.attributes:
            return
        text = pf.stringify(elem)
        if len(text) > 0:
            arabic_len = len(ARABIC_CHAR_REGEX.findall(text))
            if (arabic_len / len(text)) > 0.5:
                return pf.Div(elem, attributes={'lang': 'ar'})

    # Two-pass process for inline content in mixed-language paragraphs
    pass1_content = []
    for child in elem.content:
        if isinstance(child, pf.Str) and ARABIC_CHAR_REGEX.search(child.text):
            pass1_content.append(pf.Span(child, attributes={'lang': 'ar'}))
        else:
            pass1_content.append(child)

    final_content = []
    for i, child in enumerate(pass1_content):
        final_content.append(child)
        if isinstance(child, pf.Span) and child.attributes.get('lang') == 'ar':
            if i + 1 < len(pass1_content):
                next_elem = pass1_content[i+1]
                if isinstance(next_elem, pf.Str) and next_elem.text.startswith(':'):
                    final_content.append(pf.RawInline(r'\textLR{}', format='latex'))

    elem.content = pf.ListContainer(*final_content)
    return elem


def main(doc=None):
    return pf.run_filter(action, prepare=prepare, doc=doc)

if __name__ == '__main__':
    main()