-- Pandoc Lua filter for custom XML output

-- A flag to track if we have processed the first paragraph.
local first_paragraph_processed = false

-- This function is called for each paragraph (Para) element.
function Para(p)
  -- Check if this is the first paragraph.
  if not first_paragraph_processed then
    -- If it is, mark that we've processed it.
    first_paragraph_processed = true
    -- Wrap the paragraph's content in the <first-paragraph> tag.
    -- pandoc.Pandoc() processes the inline content (like text, emphasis, etc.)
    -- and 'xml' is the target format.
    return pandoc.RawBlock('xml', '<first-paragraph>' .. pandoc.write(pandoc.Pandoc(p.content), 'xml') .. '</first-paragraph>')
  else
    -- For all other paragraphs, wrap them in the <body-paragraph> tag.
    return pandoc.RawBlock('xml', '<body-paragraph>' .. pandoc.write(pandoc.Pandoc(p.content), 'xml') .. '</body-paragraph>')
  end
end

-- This function is called for each Header element.
function Header(h)
  -- Check if the header is a level 1 header (# H1).
  if h.level == 1 then
    -- Wrap the header's content in the <chapter-number> tag.
    return pandoc.RawBlock('xml', '<chapter-number>' .. pandoc.write(pandoc.Pandoc(h.content), 'xml') .. '</chapter-number>')
  end
  -- Return nil for other header levels to let Pandoc handle them with default behavior.
  return nil
end
