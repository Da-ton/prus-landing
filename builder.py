import re

# Read the first commit's HTML
with open('index_first.html', 'r', encoding='utf-8') as f:
    first_html = f.read()

# Read the current HTML (which has the new blocks)
with open('index.html', 'r', encoding='utf-8') as f:
    current_html = f.read()

def extract_section(html, section_id):
    # Regex to find a block by ID, e.g. id="target-audience"
    # We look for <section class="..." id="..."> and capture until </section>
    # Note: we might need a more robust extraction if nested <section> exists, but they don't.
    pattern = r'(<section[^>]*id="' + section_id + r'"[^>]*>.*?</section>)'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        return match.group(1)
    return ""

target_audience_html = extract_section(current_html, 'target-audience')
white_import_html = extract_section(current_html, 'legal')
why_me_html = extract_section(current_html, 'why-me')
faq_html = extract_section(current_html, 'faq')

# Clean up the extracted blocks so they fit the boxed layout
# They currently might have <div class="mx-auto max-w-[1200px]..."> inside them.
# In the boxed layout, the <section> itself is inside the 1200px container.
# So we should remove their inner 1200px container wrappers, or just leave them if they don't hurt, 
# but they will have double padding.
def clean_block(html):
    # If the block has <div class="mx-auto max-w-[1200px]... "> we can just strip that div or replace it
    # Actually, simplest is to just change "w-full mx-auto max-w-[1200px] px-6..." to just "" or keep it simple.
    # To be safe, replacing class="mx-auto max-w-[1200px] px-6 md:px-10 lg:px-20" with nothing
    html = html.replace('mx-auto max-w-[1200px] px-6 md:px-10 lg:px-20', 'w-full')
    html = html.replace('mx-auto max-w-[1200px]', 'w-full')
    return html

target_audience_html = clean_block(target_audience_html)
white_import_html = clean_block(white_import_html)
why_me_html = clean_block(why_me_html)
faq_html = clean_block(faq_html)

# Now, where to inject them into index_first.html?
# In index_first.html, the structure is:
# <!-- Hero Section --> ...
# <!-- Consolidated Expertise Section --> ...
# <!-- Core Categories --> ...
# <!-- Factory Gallery Section --> ...
# <!-- Process Section --> ...
# <!-- Pricing --> ...
# <!-- Contact --> ...

# Order requested earlier:
# Hero
# -> TARGET AUDIENCE ("With Whom I Work")
# Expertise
# Core Categories
# Factory Gallery
# Process
# -> WHITE IMPORT
# Pricing
# -> WHY ME
# -> FAQ
# Contact

# Inject Target Audience before Expertise
first_html = first_html.replace('<!-- Consolidated Expertise Section -->', 
                                '<!-- Target Audience -->\n' + target_audience_html + '\n\n<!-- Consolidated Expertise Section -->')

# Inject White Import before Pricing
first_html = first_html.replace('<!-- Pricing -->', 
                                '<!-- White Import -->\n' + white_import_html + '\n\n<!-- Pricing -->')

# Inject Why Me and FAQ before Contact
first_html = first_html.replace('<!-- Contact -->', 
                                '<!-- Why Me -->\n' + why_me_html + '\n\n<!-- FAQ -->\n' + faq_html + '\n\n<!-- Contact -->')

# Add the FAQ script right before </body></html>
script = """
    <script>
        // FAQ Accordion
        document.querySelectorAll('.faq-trigger').forEach(trigger => {
            trigger.addEventListener('click', () => {
                const content = trigger.nextElementSibling;
                const icon = trigger.querySelector('.faq-icon');
                
                // Close others
                document.querySelectorAll('.faq-content').forEach(otherContent => {
                    if (otherContent !== content) {
                        otherContent.style.maxHeight = null;
                        otherContent.previousElementSibling.querySelector('.faq-icon').style.transform = 'rotate(0deg)';
                    }
                });

                // Toggle current
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                    icon.style.transform = 'rotate(0deg)';
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                    icon.style.transform = 'rotate(180deg)';
                }
            });
        });
    </script>
</body>"""
first_html = first_html.replace('</body>', script)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(first_html)

print("Builder finished.")
